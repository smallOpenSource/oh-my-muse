---
name: deep-interview
description: "소크라테스식 심층 인터뷰 — 모호한 아이디어를 차원별 모호도 점수로 측정하며 한 번에 한 질문씩 물어 스펙으로 결정화한다. 사용자가 'deep interview', '인터뷰해줘', '제대로 이해하고 질문 다 해줘', '가정하지 말고 물어봐'라고 요청하면 사용."
---

# deep-interview: 소크라테스식 심층 인터뷰

## Purpose

- 모호한 아이디어를 **가정 폭로형 질문**으로 파고들어, 모호도가 임계값 이하로 떨어질 때까지 진행한다.
- 차원: Goal Clarity(목표), Constraint Clarity(제약), Success Criteria Clarity(성공 기준), Context Clarity(맥락, brownfield만).
- 산출물: `.omc/specs/deep-interview-{slug}.md` 스펙. 인터뷰는 요구사항 수집만 하며, **명시적 실행 승인 전까지 파일 변경·실행 금지**.

## Workflow

### 0. 초기화

1. 인자 파싱: `[--quick|--standard|--deep] [--frontier] [아이디어]`.
2. 브라운필드 판정: 소스·패키지 파일·git 히스토리가 있고 아이디어가 기존 것의 수정/확장이면 brownfield, 아니면 greenfield.
3. 브라운필드: `subagent.spawn`으로 관련 코드베이스를 먼저 조사해 codebase_context로 저장. **코드가 알려주는 것을 사용자에게 묻지 않는다** — 질문할 때는 파일 경로·심볼·패턴을 인용한다.

### 1. Round 0 — 토폴로지 확정 (점수 산정 전 1회)

- 최상위 컴포넌트 1~6개를 열거하고 사용자에게 확인 질문 1회: "이 토폴로지가 맞습니까? 추가/삭제/병합/분할/연기할 것이 있습니까?"
- 확정 후 고정. 이후 라운드의 점수는 확정된 컴포넌트마다 독립적으로 산정, 연기된 컴포넌트는 모호도 계산에서 제외(목록은 유지).

### 2. 인터뷰 루프 (모호도 ≤ 임계값 또는 조기 종료까지)

- **기본: 한 번에 한 질문.** 예외는 `--frontier` — 설계 트리의 프론티어(전제조건이 해결된 질문들)를 한 라운드에 묶어 묻는다(한 번에 최대 4개).
- 질문 타겟: 컴포넌트×차원 중 점수가 가장 낮은 쌍. 왜 그 쌍이 병목인지 한 문장으로 밝히고 질문한다.
- 질문 스타일: 가정을 폭로하라 ("'작업을 관리한다'에서 사용자가 가장 먼저 하는 구체적 행동은?"). 범위 자체가 흐릿하면(핵심 명사가 불안정) 온톨로지형 질문 — "이것의 핵심 실체는 무엇입니까?"
- 답변 후 차원별 0.0~1.0 점수 산정, 모호도 계산:
  - greenfield: `1 − (goal×0.40 + constraints×0.30 + criteria×0.30)`
  - brownfield: `1 − (goal×0.35 + constraints×0.25 + criteria×0.25 + context×0.15)`
- 임계값 기본 **0.2** (설정이 있으면 그 값 사용).

### 3. 챌린지 모드 (라운드별 1회씩, 별도 에이전트 spawn이 아니라 프롬프트 주입으로 수행)

- 4라운드+: **Contrarian** — "반대가 사실이면?" 핵심 가정 도전.
- 6라운드+: **Simplifier** — "여전히 가치 있는 가장 단순한 버전은?"
- 8라운드+ (모호도 > 0.3일 때): **Ontologist** — "이것은 정말로 무엇입니까?" 핵심 실체 재확인.

### 4. 한계선

- 10라운드: 계속/진행 선택 경고. 20라운드: 하드캡, 현재 명료도로 진행.
- 3라운드 이후 조기 종료 가능 — 남은 모호도와 리스크를 경고와 함께 제시.
- 중단은 즉시, 상태 저장 후 재개.

### 5. 스펙 결정화 (모호도 ≤ 임계값 또는 조기 종료 시)

`.omc/specs/deep-interview-{slug}.md`에 작성:

```markdown
# Deep Interview Spec: {제목}
## Metadata (Interview ID, Rounds, Final Ambiguity, Type, Threshold)
## Clarity Breakdown (차원별 점수표)
## Topology (활성 컴포넌트 커버리지 / 연기 사유)
## Goal / Constraints / Non-Goals / Acceptance Criteria
## Assumptions Exposed & Resolved
## Interview Transcript
```

### 6. 실행 브리지 — 승인 게이트

- 스펙 완성 후 `pending approval`로 표시. 승인 전까지 **mutation 금지** (파일 수정·커밋·푸시·실행 위임).
- 실행은 deep-interview가 직접 하지 않는다. 사용자가 실행 경로(autopilot/team/ralph 등)를 선택하면 스펙을 전달.
- **3단계 정제 경로(권장, 선택)**: 인터뷰(명확성 게이트) → `plan` 스킬 합의(타당성 게이트: Planner 계획·Architect 검토·Critic 검증, 합의까지 반복) → 별도 승인(실행 경로 선택, 자동 핸드오프 없음). 단계를 건너뛰면 품질 보증이 약해진다 — 인터뷰 생략 시 잘못된 것 빌드, plan 합의 생략 시 허술한 계획, 승인 생략 시 실행 없음(정제된 계획만 산출).

## Output Contract

- 스펙 파일 경로 `.omc/specs/deep-interview-{slug}.md` + 최종 모호도 점수 + `pending approval` 상태.
- 일시 파일은 `.omc/state/`에만 (레포 루트 금지).

## Operating Rules

- 한계: 원본의 `omc.deepInterview.ambiguityThreshold` 설정(`~/.claude/settings.json`)·`state_write`·`AskUserQuestion` UI·`omc-plan`/`autopilot` 체인은 이 환경에 없음. 임계값은 설정이 없으면 0.2 기본, 질문은 채팅으로, 실행 브리지는 채팅 트리거(예: "team으로 실행해줘")로 대체한다.
- 브라운필드 확인 질문은 반드시 레포 증거(경로·심볼)를 인용. 증거 없이 묻지 않는다.
- 절대 새로 지어내지 말 것: 코드베이스에 없는 파일·심볼·동작을 인용하지 않는다. 탐색이 실패하면 greenfield로 진행하되 한계를 명시한다.
- 생략 항목: 온톨로지 안정도 수식·per-component 회전 타겟팅 상세·Autoresearch 모드·3단계 승인 파이프라인 상세(원문 길이 대비 핵심 워크플로만 유지).
