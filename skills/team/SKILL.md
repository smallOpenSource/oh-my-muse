---
name: team
description: 사용자가 "팀으로 작업해줘", "N명의 에이전트로 병렬 작업해줘", "에이전트 여러 개로 나눠서 작업해줘"라고 요청하면 발동. 공유 작업 리스트 위에서 N명의 조정된 서브에이전트를 단계별 파이프라인(plan→prd→exec→verify→fix)으로 병렬 실행하는 팀 오케스트레이션 스킬.
---

# Team

## Purpose

- 하나의 작업을 파일/모듈 스코프의 서브태스크로 분해하고, 여러 서브에이전트를 **병렬**로 실행해 조정하는 팀 오케스트레이션.
- 팀 실행은 단계별 파이프라인을 따른다: `team-plan → team-prd → team-exec → team-verify → team-fix` (루프).
- 각 스테이지에는 역할(role)에 맞는 전문 에이전트를 라우팅한다. 역할 프롬프트는 `~/workspace/skills/team/references/agents/<역할>.md`에 정의된다(analyst, architect, code-reviewer, code-simplifier, critic, debugger, designer, document-specialist, executor, explore, git-master, planner, qa-tester, scientist, security-reviewer, test-engineer, tracer, verifier, writer — 19종).
- 리드(orchestrator)는 이 스킬을 실행하는 주체이며, 워크플로·상태·핸드오프를 관리한다. 워커는 실행만 담당하고 리드 역할을 수행하지 않는다.

## Workflow

### 1. 입력 파싱

- **N** (에이전트 수, 1–20): 지정되지 않으면 작업 분해 결과에 따라 자동 결정.
- **task** (작업 설명): 분해 대상 고수준 작업.

### 2. team-plan — 분석과 분해

- `explore` 역할로 코드베이스를 탐색하고, `planner` 역할로 작업을 서브태스크로 분해한다.
- 서브태스크 규칙: 파일 또는 모듈 스코프로 분할해 충돌 방지, 독립적이거나 명확한 의존 순서, 간결한 `subject` + 상세한 `description`, 의존 관계 명시.
- 요구사항이 불명확하면 `analyst` 추가, 시스템 경계가 복잡하면 `architect` 추가.

**역할 프롬프트 경로 계약:** 모든 역할의 프롬프트는 `references/agents/<역할>.md` 파일에서 읽어 `subagent.spawn`의 `message`에 넣어 실행한다.

### 3. team-prd — 요구사항 명시 (필요 시)

- 스코프가 모호하거나 수용 기준(acceptance criteria)이 없을 때만 진입.
- `analyst` 역할로 요구사항을 추출하고, 필요 시 `critic`으로 스코프를 견제한다.
- 종료 조건: 수용 기준과 작업 경계가 명시적으로 정리됨.

### 4. 팀 상태 초기화

팀 상태는 `~/workspace/team/<slug>/state.json` 파일에 저장한다(`slug`는 작업 설명에서 파생된 소문자·숫자·하이픈 식 slug, 예: `fix-ts-errors`).

| 필드            | 설명                                                              |
| --------------- | ----------------------------------------------------------------- |
| `active`        | 팀 모드 활성 여부                                                  |
| `current_phase` | 현재 스테이지: `team-plan`, `team-prd`, `team-exec`, `team-verify`, `team-fix` (종료: `complete` / `failed` / `cancelled`) |
| `team_name`     | slug (상태·핸드오프·보고용)                                        |
| `agent_count`   | 워커 에이전트 수                                                   |
| `task`          | 원본 작업 설명                                                     |
| `fix_loop_count`| 현재 fix 반복 횟수                                                 |
| `max_fix_loops` | fix 최대 반복 횟수 (기본값: 3)                                     |
| `stage_history` | 스테이지 전이 이력 (쉼표 구분)                                     |

스테이지 전이마다 `current_phase`와 `stage_history`를 갱신한다. 시작 전 상태 파일이 있고 `active=true`이며 `current_phase`가 비종료 상태면, 새 팀을 만들지 말고 **resume**한다(기존 핸드오프와 작업 상태를 읽고 마지막 스테이지부터 재개). 종료 상태(terminal states)는 `complete`·`failed`·`cancelled` — 취소는 `cancel` 스킬의 표준 취소 흐름을 따르고(본 스킬에서 플래그·범위 규칙을 중복 정의하지 않음), 핸드오프 파일은 resume용으로 보존한다.

### 5. 스테이지 핸드오프

스테이지 전이 전, 리드는 다음 스테이지용 핸드오프 문서를 작성한다: `~/workspace/team/<slug>/handoffs/<stage>.md`.

```markdown
## Handoff: <current-stage> → <next-stage>

- **Decided**: [이 스테이지의 핵심 결정]
- **Rejected**: [검토 후 기각한 대안과 이유]
- **Risks**: [다음 스테이지가 주의할 리스크]
- **Files**: [생성·수정된 핵심 파일]
- **Remaining**: [다음 스테이지에 남긴 항목]
```

- 리드는 다음 스테이지의 워커를 spawn하기 전에 **이전 핸드오프를 반드시 먼저 읽고**, 그 내용을 워커 프롬프트에 포함시킨다.
- 핸드오프는 10–20줄 이내의 경량 문서로 작성한다.
- 핸드오프는 취소/종료 후에도 보존되며 세션 재개(resume)에 사용한다.

### 6. team-exec — 병렬 실행

- 모든 워커를 `subagent.spawn`으로 **한 번에 병렬** 실행한다(하나가 끝나길 기다리지 않는다).
- 워커 프롬프트 = 역할 프롬프트(`references/agents/<역할>.md`) + 워커 프리앰블 + 할당된 서브태스크.
- 워커당 소유자를 사전에 할당한다(원자적 클레임이 없으므로 리드가 소유자 배정).
- 워커 규칙: 서브에이전트 생성 금지, 절대경로 사용, 리더 오케스트레이션 금지, 할당된 태스크만 수행, 완료/실패 결과를 리드에게 보고.

**스테이지별 에이전트 라우팅:**

| Stage           | 필수 에이전트 | 선택 에이전트 |
| --------------- | ------------- | ------------- |
| **team-plan**   | `explore`, `planner` | `analyst`, `architect` |
| **team-prd**    | `analyst` | `critic` |
| **team-exec**   | `executor` | `debugger`(빌드 오류), `designer`(UI), `writer`(문서), `test-engineer`(테스트) |
| **team-verify** | `verifier` | `security-reviewer`(인증/암호화), `code-reviewer`(대규모 변경) |
| **team-fix**    | `executor` | `debugger` |

**라우팅 규칙:**

1. 스테이지별 에이전트는 리드가 선택한다. 사용자의 N 지정은 `team-exec` 워커 수에만 영향을 준다.
2. 비용 절감 모드에서는 상위 티어를 한 단계 낮춰도 되지만, `team-verify`는 최소 `executor`급 이상 품질을 유지한다.
3. 보안 민감 변경 또는 20개 이상 파일 변경 시 `team-verify`에 `security-reviewer` + `code-reviewer`를 포함한다.

### 7. team-verify — 검증

- `verifier`가 실행 결과와 수용 기준을 대조해 판정한다.
- **통과:** 남은 필수 수정이 없으면 파이프라인 종료로 이동.
- **실패:** 수정 태스크를 생성하고 `team-fix`로 이동.

### 8. team-fix — 수정 (루프)

- `executor`/`debugger`가 결함을 수정한 뒤 흐름은 `team-exec → team-verify`로 복귀한다.
- `fix_loop_count`가 `max_fix_loops`(기본 3)를 초과하면 종료 상태 `failed`로 전환한다(무한 루프 금지).

### 9. 종료

1. 모든 서브태스크가 완료/실패 상태인지 확인한다.
2. 워커 결과는 `subagent.spawn` 결과로 자동 전달되므로, 리드가 직접 결과를 수집·집계한다.
3. 사용자에게 최종 보고를 제시한다(Output Contract 참조).
4. `~/workspace/team/<slug>/state.json`의 `active`를 `false`로 갱신한다(핸드오프는 보존).

## Output Contract

리드는 사용자에게 다음을 보고해야 한다:

- **파이프라인 결과 요약**: 각 스테이지(plan→prd→exec→verify→fix)별 수행 여부와 결과.
- **서브태스크별 상태**: 완료/실패 목록과 한 줄 요약.
- **검증 판정**: `team-verify` 통과 여부, `code-reviewer`/`security-reviewer` 의견(실행 시).
- **fix 루프 횟수**: `fix_loop_count` / `max_fix_loops`.
- **생성·수정 파일 목록**.
- **잔여 이슈/차단 요소**: 미완료·실패 항목과 사유, 후속 조치 제안.
- **핸드오프 경로**: `~/workspace/team/<slug>/handoffs/`.

## Operating Rules

### 동작 불가 요소와 대안

1. **tmux 기반 팀 오케스트레이션 불가** — 원본의 `omc team` / `omc-teams` 멀티플렉서 워커 방식은 이 환경에서 동작하지 않는다. 대안: 모든 워커를 `subagent.spawn`으로 병렬 실행한다.
2. **외부 CLI 모델 연동 불가** — Codex/Gemini/Antigravity/Cursor 등 외부 모델 워커(`codex_worker`, `gemini_worker`, `antigravity_worker`)는 지원하지 않는다. 대안: 모든 역할은 Muse 기반 subagent로 실행하며, provider 라우팅 개념은 사용하지 않는다.
3. **Claude Code implicit agent team 메시징 서피스 없음** — 워커↔리드 간 자동 전달 대화 채널이 없다. 대안: `subagent.spawn` 결과는 부모 세션에 자동 전달되므로, 리드가 결과를 직접 수집하고 다음 스테이지/워커 프롬프트에 문맥을 넣어 분배한다. 원본의 `shutdown_request`/`shutdown_response` 프로토콜도 동일하게 결과 수집으로 대체한다.
4. **`state_write`/`state_read` MCP 없음** — 대안: 팀 상태는 `~/workspace/team/<slug>/state.json` 파일로 저장·조회한다.
5. **원본 hooks 없음** — 대안: 주기적 상태 점검 등 반복 작업이 필요하면 Muse의 `cron`/`hooks`를 별도로 구성한다.
6. **Team + Ralph 조합 미지원** — Ralph 지속 루프(재시도·아키텍트 검증)와의 연동은 이식되지 않았다. 대안: 실패 시 스킬을 수동으로 재실행하거나, 반복 재시행이 필요하면 `cron`으로 예약한다.
7. **동적 스케일링 미지원** — 실행 중 워커 증감(`scale_up`/`scale_down`) 기능은 없다. 대안: 필요 시 리드가 `subagent.spawn`으로 워커를 추가 실행한다.
8. **`.claude/omc.jsonc` 설정 파일 미지원** — 팀 설정 파일 스키마는 이식되지 않았다. N(1–20)과 작업 설명은 채팅 입력으로 전달한다.

### 주의사항 (원본 gotchas 유지)

- **원자적 태스크 클레임 없음** — 두 워커가 같은 태스크를 가져갈 수 있다. 리드가 워커 spawn 전에 소유자를 사전 할당하고, 워커는 할당된 태스크만 수행한다.
- **태스크 ID는 문자열** — 태스크 목록 도구의 ID는 문자열(예: `"1"`, `"2"`)로 취급한다.
- **워커는 서브에이전트를 생성하지 않는다** — 워커 프롬프트에 명시하고, 워커가 오케스트레이션 행동을 하면 리드가 중단시킨다.
- **워커 프롬프트에 시크릿을 넣지 않는다** — 프롬프트는 로그·상태·대화 기록에 남을 수 있다.
- **내부/라이프사이클 항목 필터링** — 서브에이전트 spawn 과정에서 생기는 내부 항목은 실제 태스크 집계에서 제외한다.
- **팀 이름은 slug 형식** — 소문자, 숫자, 하이픈만 사용한다.
