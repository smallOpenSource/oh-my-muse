---
name: ultra-init
description: "아이디어·러프 브리프·그린필드를 계획→구현→QA 통과까지 핸즈오프 1회 자율 실행하는 풀사이클 오케스트레이터. 사용자가 'ultra-init', '알아서 만들어줘', '핸즈오프 빌드'라고 요청하면 사용."
argument-hint: "[--short|--deliberate] [--gated] [--qa tests,build,lint,typecheck] [--critic=architect|critic|codex] [--plan-id <id>] <브리프 / 만들 것>"
---

# ultra-init: 자율 풀사이클 오케스트레이터

## Purpose

거친 브리프 하나를 받아 **계획 → 목표 등록 → 영속 실행 → QA**까지 멈추지 않고 끝내는 thin orchestrator다. 묶는 스킬들을 재구현하지 않고 의존 순서대로 **호출만** 한다. 항상 실제 스킬을 호출하므로 각 스킬이 진화해도 동작이 동기화된다. 서브 스킬의 내부를 이 파일에 복사하지 않는다.

번들 파이프라인(실행 순서):

```
ralplan --deliberate  →  ultragoal  →  ralph  →  ultraqa  →  complete
계획(합의)               목표 원장      영속 실행            QA 순환      완료/정리
```

순서 주의: 요청 텍스트에 적힌 순서와 달리 ultra-init은 의존 순서대로 돌린다. **ultragoal이 ralph 실행 전에 목표를 등록**하고, **ultrawork는 ralph 내부의 병렬 엔진**이라 별도 페이즈가 아니다. 의도적이며 실수가 아니다.

## Autonomy Contract

- 기본값 = 완전 자율. ultra-init 호출 자체가 이번 턴의 명시적 실행 승인이다. 페이즈 사이에서 승인 프롬프트를 띄우지 않는다.
- 유일한 정지 조건은 아래 Stop Conditions.
- 오버라이드: `--gated` = Phase 1(계획) 직후 사용자 승인 대기, 이후 자동 계속.

## Loop Authority Rules

루프/영속 엔진이 여러 개라 경쟁 루프를 막기 위해 **한 번에 하나의 루프 권위만 활성화**하고, 페이즈는 엄격히 순차 실행한다.

1. Phase 3에서는 ralph가 유일한 루프 권위다. 끝까지 돌게 둔다.
2. ultragoal은 `artifact_only` 모드로 — 내구 계획 + 원장 + 증거만. ralph 실행 중 경쟁하는 목표 루프를 만들지 않는다.
3. ultraqa는 ralph 완료 후 Phase 4에서만, 터미널 QA 서브게이트로. ralph와 동시 실행 금지.
4. ultrawork는 별도 페이즈가 아니다. ralph 내부 병렬 엔진으로 취급한다.

## Workflow

### Phase 0 — Preflight

- 인자에서 브리프를 resolve한다. 비어 있으면 한 번만 묻고 진행한다.
- 플래그 파싱: `--deliberate`(기본)/`--short`(가벼운 계획), `--gated`, `--qa <dims>`, `--critic=...`, `--plan-id <id>`.
- 서브 스킬 확인: 번들된 스킬(ralplan·ralph·ultraqa·ultragoal·cancel 등)은 `~/workspace/skills/<name>/`에 이식된 것만 호출한다. 미이식 스킬이 있으면 해당 페이즈를 degraded 모드로(계획은 `plan.md` 기록, 추적은 세션 스코프) 돌리고 보고에 명시한다.

### Phase 1 — PLAN: ralplan --deliberate

- 이식된 ralplan 스킬을 non-interactive 모드로 호출해 합의 승인된 계획을 만든다.
- 산출물: ADR + 순서 있는 user story + story별 테스트 가능한 acceptance criteria + 테스트 계획. `--deliberate` 모드면 **pre-mortem(실패 시나리오 3가지)** + 확장 테스트 계획도 포함.
- Autonomy: 합의 승인된 계획은 실행 승인으로 간주하고 계속. (`--gated` → 여기서 사용자 승인 대기 후 계속.)

### Phase 1.5 — 변경 전 실패 기록 (QA 게이트의 베이스라인)

- Phase 2 전에 각 QA 차원의 명령을 변경 없는 트리에서 한 번씩 돌려, 이미 실패하는 항목(테스트명·에러 라인)을 기록한다. Phase 4에서 "원래 실패"와 "이번 변경의 회귀"를 가르는 기준이 된다.
- `git stash`/`git reset` 금지. 트리에 변경이 있으면 `git worktree`로 HEAD의 깨끗한 복사본에서 돌린다. 의존성 미설치로 "command not found"만 나온 기록은 베이스라인이 아니다.
- 세션이 compaction될 수 있으면 이 기록을 이어쓰기 노트에 남긴다.

### Phase 2 — SEED GOALS: ultragoal

- 승인된 story를 내구 원장에 등록한다(병렬 세션 충돌 방지를 위해 plan-id로 네임스페이스 분리).
- `artifact_only`(내구 계획 + 원장 + 증거). 경쟁 루프 금지.
- 이점: 세션이 중간에 죽어도 원장으로 깨끗하게 resume 가능.

### Phase 3 — EXECUTE: ralph

- ralph에 **브리프 + 승인된 계획의 story와 acceptance criteria**를 입력으로 넘긴다. ralph의 PRD 정제 단계가 이미 나온 고품질 기준을 그대로 채택한다. `--critic` 스레딩.
- ralph가 story-by-story로 전부 `passes: true`가 될 때까지 반복 → reviewer 검증 → deslop → post-deslop 회귀 재검증. ralph가 이 페이즈의 루프 권위.
- "계속 진행" 신호가 와도 중단하지 않는다. 끝까지 돌게 둔다.

### Phase 4 — QA GATE: ultraqa

- ralph 완료 후 터미널 크로스차원 QA 게이트. 기본 순서 `typecheck → lint → build → tests`, 또는 `--qa` 목록.
- 각 차원은 최대 5회 순환: RUN QA → diagnose → fix → 반복. 같은 실패가 3회 반복되면 조기 종료.

### Phase 5 — COMPLETE

- 최종 체크포인트: quality-gate 증거와 함께 완료 기록. 게이트가 하나라도 clean이 아니면 complete 표시 금지 — blocker를 기록하고 Phase 3로 돌아간다.
- 전부 완료 확인 → ralph/ultraqa/mode 상태 정리(`cancel` 상당).
- 간결하고 증거 기반의 최종 요약: 계획 내용, 전달된 story, 수정된 파일, reviewer 판정, deslop 결과, 차원별 QA 결과, 원장 위치.

## Stop Conditions

자율 모드에서도 멈추고 보고한다:

- 사용자 입력이 필요한 하드 블로커(자격증명 누락, 외부 서비스 다운, 스코핑으로 해결 안 되는 진짜 모호한 요구사항).
- 사용자가 stop/cancel/abort → 상태 정리 후 중단.
- 같은 실패가 **3회** 반복 → 근본 문제 가능성으로 surface.
- ralplan이 합의에 도달 못 하면(최대 5회) → 최선의 계획을 제시하고 진행 여부를 묻는다.

그 외: 멈추지 않고, 페이즈 사이에서 허락을 묻지 않는다.

## Output Contract

- [ ] Phase 1: 합의 승인된 계획(ADR, 순서 있는 story, 테스트 가능한 acceptance criteria, 확장 테스트 계획)
- [ ] Phase 2: ultragoal 원장 등록(또는 degraded `plan.md`)
- [ ] Phase 3: 모든 story `passes: true`, reviewer 검증, deslop, post-deslop 회귀 green
- [ ] Phase 4: 대상 차원 전부 ultraqa green
- [ ] Phase 5: 최종 체크포인트(clean quality-gate 증거), 상태 정리, 증거 기반 최종 요약("should"/"looks good" 금지 — 실제 명령 출력 제시)

## Operating Rules

- Thin-orchestrator 규칙: 항상 실제 스킬/CLI를 호출한다. 내부를 복제하지 않는다.
- 오버라이드 요약: `--short`(가벼운 ralplan), `--gated`(계획 후 승인 대기), `--qa tests,build`(QA 차원 제한), `--critic=...`(ralph reviewer), `--plan-id <id>`(병렬 실행용 안정 원장 id).
- 한계: 원본의 `omc` CLI·`Skill("oh-my-claudecode:<name>")`·`Task(subagent_type=...)` 메커니즘은 Claude Code 전용이다. 이 환경에서는 `~/workspace/skills/`에 이식된 동명 스킬을 호출하고, 장기 실행·병렬 위임이 필요하면 `subagent.spawn` 또는 background exec + process 도구를 쓴다. `omc` CLI가 없으면 Phase 2는 degraded 모드(`plan.md` 기록)로 명시한다. 서브 스킬 미이식은 조용히 건너뛰지 않고 보고에 명시한다.
