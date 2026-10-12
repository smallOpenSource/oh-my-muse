---
name: self-improve
description: 자율 진화형 코드 개선 엔진 — 사용자가 "self-improve 실행해줘", "이 레포를 자동으로 개선해줘", "벤치마크 기준으로 코드를 진화시켜줘"라고 요청하면 사용. 연구→계획→실행→토너먼트 선발→기록 루프를 정지 조건까지 자율 반복한다.
---

# Self-Improvement Orchestrator

## Purpose

개선 루프의 전체 수명주기를 관리하는 루프 컨트롤러다: 설정, 연구, 계획, 실행, 토너먼트 선발, 이력 기록, 시각화, 정지 조건 평가. 전문 역할을 서브에이전트에 위임하고 입출력을 조율한다. 부속 파일(`si-*.md`, `scripts/`, `templates/`, `data_contracts.md`)은 이 스킬 디렉터리에 상대 경로로 보관된다.

## Workflow

### 자율 실행 정책

- **게이트 통과 후 루프가 시작되면 사용자에게 절대 멈춰서 묻지 않는다.** 반복 사이·반복 내 단계 사이에 확인을 요구하지 않는다. 요약하고 대기하지 않고 즉시 다음 단계를 실행한다.
- 에이전트 실패: 1회 재시도 후 해당 에이전트를 건너뛰고 계속. 반복 이력에 기록한다.
- 모든 계획이 거부되면 / 모든 실행자가 실패하면 / 벤치마크 오류 시: 기록하고 다음 반복으로 자동 진행한다.
- 루프를 멈추는 것은 아래 정지 조건뿐이다.
- 신뢰 경계: 루프는 설정 단계에서 사용자가 명시적으로 확인한 레포 경로와 벤치마크 명령만 실행한다. 패키지 설치·시스템 설정 변경을 하지 않으며, 벤치마크 명령이 접근하는 범위를 넘어 네트워크에 접근하지 않는다.
- **봉인 파일**: `scripts/validate.sh`이 벤치마크 코드가 루프에 의해 수정되지 않도록 강제한다.

### 상태 추적

상태 루트는 `scripts/resolve-paths.mjs`가 반환한 경로다. 기본값은 `~/workspace/self-improve/topics/default/`, 토픽 지정 시 `~/workspace/self-improve/topics/{topic_slug}/`다. 아래 `<self-improve-root>/`는 그 해석된 루트를 가리킨다.

```
<self-improve-root>/
├── config/   settings.json(아래 전체 키) / goal.md / harness.md(H001/H002/H003) / idea.md
├── state/    agent-settings.json(반복 수, 최고 점수, 상태, 카운터) / iteration_state.json(반복 내 진행도) /
│             research_briefs/ / iteration_history/ / merge_reports/ / plan_archive/
├── plans/    현재 라운드 계획
└── tracking/ raw_data.json / baseline.json / events.json / progress.png
```

`config/settings.json` 전체 키: `number_of_agents`, `benchmark_command`, `benchmark_format`, `benchmark_direction`, `max_iterations`, `plateau_threshold`, `plateau_window`, `target_value`, `primary_metric`, `sealed_files`, `regression_threshold`, `circuit_breaker_threshold`, `target_branch`, `current_repo_url`, `fork_url`, `upstream_url`, `topic_slug`.

### 역할 매핑

원본의 Claude Code Task tool·OMC 전용 에이전트(planner, architect, critic, executor, git-master)는 이 환경에 없으므로, 아래 역할을 `subagent.spawn`으로 생성한 서브에이전트에 프롬프트로 직접 부여해 수행한다. 연구 프롬프트는 이 디렉터리의 `si-researcher.md`, 벤치마크 빌더는 `si-benchmark-builder.md` 내용을 그대로 전달한다. 목표 인터뷰는 `si-goal-clarifier.md`를 읽고 이 컨텍스트에서 직접 실행한다(사용자 대화형).

| 단계 | 역할 | 수행 방식 |
|---|---|---|
| 연구 | 코드베이스 분석 + 가설 생성 | 서브에이전트 + `si-researcher.md` |
| 계획 | 가설 → 구조화 계획 | 서브에이전트 N개 병렬 (N = `number_of_agents`) |
| 아키텍처 검토 | 6점 체크리스트 | 서브에이전트(자문 전용) |
| 비평 검토 | 하네스 규칙 강제(H001/H002/H003) | 서브에이전트(승인/거부 판정) |
| 실행 | 계획 구현 + 벤치마크 | 서브에이전트 N개 병렬 |
| Git | 원자적 머지/태그 | 직접 git 명령 실행 |

### 설정 단계

1. 대상 레포 경로 확인. 미설정이면 사용자에게 묻는다.
2. `node {skill_dir}/scripts/resolve-paths.mjs --project-root {repo_path} [--topic "..."] [--slug "..."] --ensure-dirs`로 루트 해석.
3. 이 디렉터리의 `templates/`를 해석된 루트의 `config/`로 복사.
4. **신뢰 확인(필수, 생략 불가)**: `trust_confirmed`이 true가 아니면 `"Self-improve will run benchmark commands inside {repo_path}. ... Confirm? [yes/no]"`를 사용자에게 확인받고 `agent-settings.json`에 기록. 거부 시 중단.
5. 목표 미설정 → `si-goal-clarifier.md`의 4차원(Objective, Metric, Target, Scope) 소크라테스식 인터뷰를 직접 실행 → `config/goal.md`에 기록.
6. 벤치마크 미설정 → 서브에이전트에 `si-benchmark-builder.md`를 프롬프트로 전달. 레포 조사 → 벤치마크 생성/랩핑 → 3회 검증 → 베이스라인 기록. 이후 벤치마크 명령을 사용자에게 확인받는다. 거부 시 중단.
7. 하네스 미설정 → 기본 규칙(H001: 가설 정확히 1개, H002: approach_family 3연속 반복 금지, H003: 라운드 내 다양성) 확인 또는 커스터마이즈.
8. **게이트**: `si_setting_goal`, `si_setting_benchmark`, `si_setting_harness`, `trust_confirmed` 모두 true.
9. 개선 브랜치 생성(없으면): `git -C {repo_path} checkout -b improve/{goal_slug} {target_branch}` 후 원래 브랜치로 복귀. `{goal_slug}`은 목표에서 도출(소문자 언더스코어).
10. `state/agent-settings.json`에 `status: "running"`, `iteration: 0` 기록.

### 개선 루프 (게이트 통과 후 자율 실행)

**Step 0 — 오래된 worktree 정리(매 반복 필수, 멱등)**: `git -C {repo_path} worktree list`에서 현재 반복에 속하지 않는 `worktrees/round_*`를 `worktree remove --force`로 제거 후 `worktree prune`.

**Step 1 — 상태 갱신**: `agent-settings.json`의 iteration을 현재 반복으로 기록(TTL 성격).

**Step 2 — 중단 요청 확인**: `agent-settings.json`의 `status`가 `user_stopped`이면(또는 cancel 스킬로 상태가 지워졌으면) 현재 라운드 worktree 정리 → `iteration_state.json`에 `status: "interrupted"` 기록 → 정상 종료. `cancel`을 다시 호출하지 않는다.

**Step 3 — 사용자 아이디어 확인**: `config/idea.md`가 비어 있지 않으면 플래너에게 전달할 스냅샷을 뜨고 비운다.

**Step 4 — 연구**: 서브에이전트 1개에 `si-researcher.md` + (반복 번호, 레포 경로, goal.md, iteration_history/, research_briefs/, `data_contracts.md` 섹션 3 스키마)를 전달. 출력: `state/research_briefs/round_{n}.json`. 실패 시 이력만으로 진행.

**Step 5 — 계획**: 서브에이전트 N개를 병렬로 실행. 각 프롬프트에 연구 브리프, 이력, 하네스 규칙, 계획 문서 스키마(`data_contracts.md`), 그리고 "JSON 출력, 인터뷰 모드 생략, 가설 정확히 1개, approach_family 태그 포함" 오버라이드를 전달. 출력: `plans/round_{n}/plan_planner_{id}.json`.

**Step 6 — 검토(계획별 순차)**: (a) 아키텍처 검토 — 6점 체크리스트(테스트 가능성, 참신성, 범위, 대상 파일 존재·비봉인, 구현 명확성, 기대 결과 현실성), 자문 전용. (b) 비평 검토 — H001/H002/H003 + 스키마 검증 + 이력 인식. `critic_approved: false`인 계획은 실행 제외. 전부 거부되면 기록 후 Step 9로.

**Step 7 — 실행**: 승인된 계획마다 worktree 생성 후 서브에이전트 병렬 실행.

```bash
git -C {repo_path} worktree add worktrees/round_{n}_executor_{id} -b experiment/round_{n}_executor_{id} improve/{goal_slug}
```

프롬프트에 승인된 계획 JSON, worktree 경로, 벤치마크 명령, 봉인 파일 목록, `scripts/validate.sh` 경로, 벤치마크 결과 스키마를 전달. 지시: 계획 충실 구현 → validate.sh 실행 → 벤치마크 실행 → 벤치마크 결과 JSON 출력.

**Step 8 — 토너먼트 선발**(직접 수행): `status: "success"` 후보만 수집 → `benchmark_score`로 순위(방향 준수) → 순위 순으로 (a) 무회귀 검사(방향에 따라 `best_score` 이상/이하 유지) → (b) `improve/{goal_slug}`에 `--no-ff` 머지(메시지: `"Iteration {n}: {가설} (score: {before} → {after})"`) → (c) 머지 상태 재벤치마크 → 확인되면 승자 확정, 회귀면 `git reset --hard HEAD~1`로 되돌리고 다음 후보, 충돌이면 `merge --abort` 후 다음 후보. `auto_push: true`면 푸시(비차단). 탈락 브랜치는 태그 후 삭제. `state/merge_reports/round_{n}.json` 기록(스키마: `data_contracts.md` 섹션 9).

**Step 9 — 기록·시각화**: `state/iteration_history/round_{n}.json` 기록. `agent-settings.json` 업데이트: iterations+1, 개선이 `plateau_threshold` 이상이면 best_score 갱신·plateau 카운터 리셋, 미만이면 plateau+1, 승자 없으면 circuit_breaker+1. `tracking/raw_data.json`에 후보별 추가 → `python3 {skill_dir}/scripts/plot_progress.py --tracking-dir <self-improve-root>/tracking` 실행 → plans를 `state/plan_archive/round_{n}/`에 보관.

**Step 10 — 정리**: 라운드 worktree 제거 + `worktree prune`. `iteration_state.json`을 `completed`로.

**Step 11 — 정지 조건 평가**(하나라도 참이면 종료):

| 조건 | 검사 |
|---|---|
| 사용자 중단 | `status == "user_stopped"` |
| 목표 달성 | `best_score`가 `target_value` 도달(방향 준수) |
| 정체 | `plateau_consecutive_count >= plateau_window` |
| 최대 반복 | `iterations >= max_iterations` |
| 회로 차단기 | `circuit_breaker_count >= circuit_breaker_threshold` |

하나도 해당 없으면 즉시 Step 1로.

### 재개

호출 시 Step 0을 먼저 실행한 뒤 `agent-settings.json`을 읽는다: `user_stopped`이면 재개 여부 질문, `running`이면 크래시로 보고 자동 재개, `idle`이면 새로 시작. `iteration_state.json`이 `in_progress`면 `current_step`부터 재개한다.

### 완료

최종 상태 기록 → `target_reached`이고 `auto_pr: true`면 PR 생성(기본 false: 수동 `gh pr create --head improve/{goal_slug} --base {target_branch}` 안내) → plot_progress.py 최종 실행 → 요약 보고서 출력:

```
=== Self-Improvement Loop Complete ===
Status: {status}
Iterations: {iterations}
Best Score: {best_score} (baseline: {baseline})
Improvement: {delta} ({delta_pct}%)
```

→ `cancel` 스킬로 상태 정리.

### 오류 처리

| 상황 | 조치 |
|---|---|
| 에이전트 무출력 | 1회 재시도 후 기록·계속 |
| 연구 브리프 비어 있음 | 이력만으로 진행 |
| 전 계획 거부 | 실행 생략·기록·다음 반복 |
| 전 실행자 실패 | 토너먼트 생략·기록·다음 반복 |
| 머지 충돌 | 후보 탈락, 다음 후보 |
| 재벤치마크 회귀 | 머지 되돌리고 다음 후보 |
| 푸시 실패 | 경고 기록·계속 |
| worktree 이미 존재 | 제거 후 재생성 |
| 설정 파일 손상 | 보고 후 중단 |

### Approach Family Taxonomy

각 계획은 정확히 하나의 태그: `architecture`(모델/컴포넌트 구조), `training_config`(옵티마이저·LR·스케줄러·배치), `data`(로딩·증강·전처리), `infrastructure`(혼합 정밀도·분산·컴파일 커널), `optimization`(알고리즘·수치 최적화), `testing`(평가 방법론), `documentation`(문서만), `other`(설명 필수).

## Output Contract

- 설정 단계: 확인된 레포 경로·벤치마크 명령·목표·하네스를 사용자에게 보고하고 게이트 통과 여부를 명시한다.
- 각 반복: 승자 여부·점수 변화(`{before} → {after}`)·머지 결과를 이력에 기록한다.
- 완료 시: 위 완료 보고서 형식으로 상태·반복 수·최고 점수·개선율을 출력한다.
- 실패·건너뜀은 모두 iteration_history에 사유와 함께 기록한다.

## Operating Rules

- Claude Code 메커니즘 치환: Task tool → `subagent.spawn`; OMC 전용 에이전트(planner/architect/critic/executor/git-master) → 프롬프트에 역할을 명시한 서브에이전트; `state_write`/`state_list_active` 등 MCP 상태 도구 → `<self-improve-root>/state/*.json` 파일 직접 관리; tmux 오케스트레이션 → 서브에이전트 병렬 실행.
- AskUserQuestion 도구가 없으면 일반 질문 텍스트로 대체한다.
- 외부 모델(Codex/Gemini 등)을 벤치마크·실행에 사용하는 원본 옵션은 이 환경에서 불가 — 대체 없음, 요구받으면 불가함을 명시한다.
- hooks 연동(원본의 stop hook 등)은 이 환경에 없으므로 생략. 중단 요청은 `cancel` 스킬 또는 `agent-settings.json`의 `status: "user_stopped"`로 전달한다.
- 원본의 "Parallel session caveats"(멀티 레포 `.omc-workspace` 마커, OMC_SESSION_ID 등)는 Claude Code 전용이므로 생략. 병렬 실행이 필요하면 토픽 슬러그를 분리해 루트를 나눈다.
- 모든 git 작업은 대상 레포 안에서 수행한다. OMC 프로젝트 루트가 아니다.
- 신뢰 확인 없이 벤치마크 명령을 실행하지 않는다.
