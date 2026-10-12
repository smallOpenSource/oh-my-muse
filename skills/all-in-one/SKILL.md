---
name: all-in-one
description: "(banker) 한 요청으로 합의 계획→검증 구현→독립 테스트 게이트를 연쇄(계획→구현→QA). 코딩 작업을 계획부터 통과까지 최대 rigor로 한 번에. 사용자가 'all-in-one 해줘'/'all in one'이라고 요청하면 사용(한 줄 수정은 직접 처리, 아이디어 확장은 제외)."
argument-hint: "[--short] [--checkpoint] [--critic=critic|architect] [--qa=tests|build|lint|typecheck] [--no-deslop] <task description>"
---

# all-in-one — Plan → Implement → QA, one command

[ALL-IN-ONE ACTIVATED — SEQUENTIAL 3-STAGE PIPELINE]

## Purpose
- 하나의 코딩 작업을 **합의 계획(Stage 1) → 검증 구현(Stage 2) → 독립 테스트 게이트(Stage 3)** 3단계로 순차 실행하는 오케스트레이터
- 구현·계획·테스트를 직접 하지 않음. 각 단계의 루프·재시도·검증은 위임받은 서브에이전트가 소유. 이 스킬은 단계 순서 호출·핸드오프·게이트·정직 보고만 담당
- 3단계 존재 이유(서로 다른 실패 모드 방어, 각 단계 리뷰어는 이전 단계 작성자와 독립 — anti-self-approval):
  1. **잘못/부실한 것 만들기** → Stage 1의 합의 + pre-mortem + 확장 테스트 계획이 코드 작성 전에 포착
  2. **부분/미검증 빌드를 "완료" 선언** → Stage 2의 스토리별 구현 + critic 검증이 포착
  3. **빌더 자체 검사로 못 잡은 통합/회귀 깨짐** → Stage 3의 독립 테스트 사이클이 포착

## When to use
- 계획 → 검증 구현 → 테스트 게이트를 한 번에, 최대 rigor로 처리하고 싶은 실질적 코딩 작업
- `계획 → 구현 → QA`를 손으로 돌리던 것을 하나의 요청으로 묶고 싶을 때
- 작업이 다소 미지정이어도 됨 — Stage 1 합의 계획이 스코핑을 흡수하므로 구체성 요구가 낮음

## When NOT to use
- **한 줄 수정·자잘한 변경** → 직접 수정하거나 단일 에이전트에 위임. 세 개의 무거운 루프는 과잉
- **순수 탐색/브레인스토밍** → 구현 전 단계 스킬(계획 스킬)로. 아무것도 구현하지 말 것
- **2-3줄 아이디어의 요구사항 확장** → 아이디어 확장 인터뷰가 먼저
- **프론트 스펙/레퍼런스 패리티 작업** → 전용 UI QA 스킬로

## Flags

| Flag | Effect | Default |
|---|---|---|
| `--short` | Stage 1이 pre-mortem + 확장 테스트 계획 없이 짧게(저위험 작업용) | off → 정식 합의 |
| `--checkpoint` | Stage 1(계획)과 Stage 2(구현) 사이에 사용자 승인 게이트 삽입 | off → 자동 진행 |
| `--critic=critic\|architect` | Stage 2 검증에 넘길 리뷰어 | `critic` |
| `--qa=tests\|build\|lint\|typecheck` | Stage 3의 QA 목표 | `tests` |
| `--no-deslop` | Stage 2에 전달(리뷰 후 정리 패스 생략) | off |

플래그가 아닌 나머지 전체가 `<task description>`.

## Workflow

### Stage 0 — 전제 확인
- Stage 1의 `ralplan` 스킬, Stage 2의 `ralph` 스킬이 workspace 스킬로 연결되어 있는지 확인(둘 다 이식됨). 없으면 해당 단계를 서브에이전트 에뮬레이션으로 대체
- 원본의 OMC(oh-my-claudecode) `ultraqa` 스킬은 이 환경에 이식되지 않음 → **Stage 3은 `subagent.spawn` 독립 QA 에이전트로 에뮬레이션**(아래 Stage 3 참조)

### Stage 1 — Plan: `ralplan` 스킬
- 이식된 `ralplan` 스킬을 호출: `--deliberate <task description>`(`--short`가 있으면 `--deliberate` 생략)
- ralplan이 Planner → Architect → Critic 합의 루프를 돌리고, Critic 승인 시 최종 계획을 저장하고 **멈춤**(이 "멈춤"은 계획 단계의 끝, 파이프라인의 끝이 아님)
- `ralplan` 호출이 전체 파이프라인 실행(이 턴의 standing opt-in)과 호환됨을 전제 — 계획 파일 경로를 캡처해 Stage 2로 전달
- **`--checkpoint`** 가 켜져 있으면: 진행 전에 사용자에게 계획 제시 + *승인·구현 / 수정 요청 / 중단* 선택. 승인 시에만 계속
- **합의 미달성**(합의 반복 상한 내 승인 없음): 자동 진행 금지. 최선의 계획을 제시하고 사용자에게 진행 방식을 물음. 미승인 계획 위에 빌드 금지

### Stage 2 전 — 변경 전 실패 기록(베이스라인)
- Stage 2 시작 전, `--qa` 목표의 명령을 **변경 전 트리**에서 1회 실행해 실패 항목(테스트명·에러 줄)을 이 대화에 기록한다. 이 기록이 Stage 3 게이트의 베이스라인이다 — 새 실패와 기존 실패를 구분하는 유일한 근거.
- `git stash`·`git reset`으로 변경 전 상태를 만들지 마라. 트리에 이미 변경이 있으면 HEAD의 깨끗한 복사본에서 측정한다(`git worktree add --detach <tmp> HEAD`, 실행 후 `git worktree remove <tmp>`). 새 worktree엔 의존성(node_modules·venv)이 없으니 먼저 링크/설치하고, 명령이 실제로 돌았는지 확인한다("command not found"로만 된 기록은 베이스라인이 아니다).
- 기록은 이 대화에만 산다. Stage 3 전에 세션이 compaction/종료될 수 있으면 `ready-compact` 노트에 함께 남긴다.

### Stage 2 — Implement: `ralph` 스킬
- 전제: 합의·승인된 계획 존재(자동 또는 `--checkpoint` 승인)
- 이식된 `ralph` 스킬을 호출: `--critic=<critic flag>`(`--no-deslop`이 있으면 함께 전달) + Stage 1 계획 파일 경로 + 태스크 개요
- ralph에게 계획 파일 경로를 태스크 정의로 넘기고 "이미 합의된 계획 — 재계획 말고 스토리별 구현 + 검증이 임무"라고 명시
- ralph는 자체 루프 수행: 스토리별 구현 → 수용 기준 검증 → critic 검증 → deslop(`--no-deslop`이 없으면) → 회귀 재실행 → 종료
- **Stage 3 시작 전에 Stage 2 ralph가 완전히 종료되어야 함**(구현과 QA의 작업 상태가 겹치면 안 됨)
- **근본적 블로커 보고 시**(3회 이상 반복되는 동일 이슈, 크레덴셜 누락, 불명확한 요구사항, 외부 의존성 다운): 중단하고 보고. 깨진/부분 빌드에 Stage 3을 돌리고 완료라 부르지 말 것

### Stage 3 — QA gate: 독립 테스트 (ultraqa 미이식 → 에뮬레이션)
- 전제: Stage 2 ralph 완전 종료(작업 상태 겹침 없음)
- `ultraqa` 스킬은 이 환경에 없음 → `subagent.spawn`으로 **새로운 독립** QA 에이전트 실행(빌드한 주체와 다른 에이전트). 목표 = `--qa` 플래그(기본 `--tests`)
- QA 사이클(최대 5회):
  1. **검증** — 새로운 독립 QA 에이전트가 `--qa` 목표를 실행해 PASS/FAIL + 명령·출력·실패 항목 보고. 실패가 기존 것인지의 판단은 눈대중이 아니라 **베이스라인 기록으로** — 베이스라인에 없는 실패는 새 실패다.
  2. **PASS** → 게이트 통과, 최종 보고로.
  3. **FAIL** → 진단 서브에이전트(읽기 전용)가 근본 원인을 진단하고, 수정 서브에이전트가 변경 범위 안에서 최소 수정. 다음 사이클은 **반드시 새로운** verifier로 검증한다(실패를 본 verifier 재사용 금지).
- **베이스라인 실패는 이 게이트에서 고치지 않는다** — 별도로 보고한다.
- 동일 실패(같은 테스트·같은 에러 서명) 3회 반복 시 조기 종료 — 사이클을 더 돌릴 문제가 아니라 사용자에게 보고할 근본 문제다.
- 결과는 정직하게 보고:
  - **목표 달성** → "ALL-IN-ONE COMPLETE" + 사이클 수
  - **최대 사이클 소진 / 동일 실패 3회** → "STOPPED" + QA 진단 내용. 게이트를 통과하지 못했으면 성공이라 주장 금지

## Orchestrator rules
- 단계는 엄격히 순서대로. 각 단계의 성공 게이트 통과 전 다음 단계 시작 금지. 건너뛰기·순서 변경·두 단계 루프 동시 실행 금지
- 단계 경계마다 진행 상황 한 줄 출력(`[all-in-one] Stage 1/3 — planning…` 등) — 사용자가 파이프라인 위치를 항상 알 수 있게
- 이 스킬만의 영속 루프나 상태 파일 추가 금지. 루프와 상태는 위임받은 서브에이전트가 소유
- 서브에이전트의 내부 "stop"/종료는 **그 단계**의 끝이지 파이프라인의 끝이 아님(Stage 1·2 종료 후에도 계속 진행)
- 중지 조건:
  - Stage 1 합의 실패 → 최선 계획 제시, 사용자에게 질의(빌드 금지)
  - Stage 2 근본적 블로커 → 중단·보고(QA 실행 금지)
  - Stage 3 사이클 소진/동일 실패 3회 → 진단 정직 보고(성공 주장 금지)
  - 사용자가 "중단"/"취소" → 실행 중인 서브에이전트·백그라운드 작업을 정리(`process.kill` 등)하고 중단

## Output Contract
- 파이프라인 종료(완료·중단) 시 간결하고 정직한 최종 보고:
  - **Plan**: 합의 도달 여부, 계획 파일 경로, 기각된 대안과 이유(1줄)
  - **Implementation**: 완료된 스토리/단계, 변경 파일, critic 판정
  - **QA**: QA 목표, N 사이클 후 PASS 또는 STOPPED + 진단, 베이스라인(변경 전) 실패는 별도 나열(게이트에서 고치지 않음)
  - **미달성/범위 제한/연기**: 있는 그대로 명시 — 통과하지 못한 게이트를 덮지 말 것

## Operating Rules
- **서브에이전트 위임**: Claude Code의 Task tool 자리는 이 환경의 `subagent.spawn`으로 대체. 각 단계는 독립 실행 단위로, 리뷰어(Critic·QA)는 작성자(Planner·Builder)와 다른 주체로(anti-self-approval 유지)
- **Stage 1·2는 이식된 `ralplan`/`ralph` 스킬을 정식 경로로 사용**(이미 workspace에 이식됨). 이 두 스킬이 없으면 해당 단계를 서브에이전트로 에뮬레이션
- **Stage 3의 `ultraqa`는 미이식** → `subagent.spawn` 독립 QA 에이전트 에뮬레이션이 가장 가까운 대안. 나중에 ultraqa 동등 스킬이 연결되면 그때부터 우선 사용
- `--critic`의 `codex` 옵션은 Codex 런타임 전용이라 제외(`critic`|`architect`만)
- 플래그 해석: `--short`(Stage 1 간소화), `--checkpoint`(Stage 1→2 사이 승인), `--critic`(Stage 2 리뷰어), `--qa`(Stage 3 목표), `--no-deslop`(Stage 2 정리 패스 생략)
