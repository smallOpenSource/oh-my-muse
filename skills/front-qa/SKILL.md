---
name: front-qa
description: "스펙(note 파일) 기반 프론트엔드 구현 + 레퍼런스 대비 엄격 parity QA 워크플로(계획→구현 루프→게이트). 사용자가 'front-qa 해줘', '스펙대로 프론트 구현해줘', '레퍼런스 parity QA해줘'라고 요청하면 사용."
---

# front-qa — 스펙 기반 프론트엔드 구현 + 엄격 QA

## Purpose
스펙 파일(기본 `docs/note.txt`)의 요구사항을 React 프론트엔드(`$FRONTEND_DIR`, 예: `apps/web`)에 구현하고,
**레퍼런스 구현(reference implementation — 예: 이전 Streamlit/타 빌드)과 엄격 비교 + 스펙 지시 정확 준수**를 검증한다. 모든 항목 해결까지 진행한다.

**원천**: banker 플러그인의 `/front-qa` 커맨드를 Muse 환경용 스킬로 이식. 원본의 OMC(`/ralplan`·`/ralph`)·Codex(OMX) 전용 호출은 아래 환경 매핑으로 대체한다.

### Muse 환경 매핑
| 원본 | 이 환경에서의 대체 |
|---|---|
| `/ralplan --deliberate` (Planner→Architect→Critic) | 계획 수립을 직접 수행(원칙/드라이버/옵션+기각 사유/pre-mortem/테스트 계획/ADR) 후 계획 파일로 저장 |
| `/ralph --critic=critic` 구현 루프 | `subagent.spawn`으로 executor 위임 + orchestrator fresh 재검증 + critic 판정까지 ITERATE |
| 병렬 explore/general-purpose 에이전트 (Task tool) | `subagent.spawn` 병렬 정찰 |
| AskUserQuestion | 사용자에게 직접 확인(옵션 제시는 사용 가능한 수단으로) |
| `/loop` 장기 루프 | exec 백그라운드 + process 도구로 장기 실행 관리. credit/token 비용은 사용자가 감수한다는 전제(원본 directive 유지) |
| `/oh-my-claudecode:cancel` | 루프 취소 수단으로 대체 |

## Workflow
(원칙: 계획 없는 즉시실행 금지)

### 1. 스펙 정독 + 코드베이스 정찰
- 대상 스펙 파일을 읽어 요구사항을 항목화.
- 코드베이스 정찰(`subagent.spawn` 병렬): 각 항목의 현재 React 상태 ↔ 레퍼런스 구현 갭을 `file:line` 증거로 매핑.

### 2. 계획 수립
Planner(정찰 종합)→Architect→Critic consensus(ITERATE 폐루프). Principles/Drivers/Options(기각 사유)/pre-mortem/확장 테스트계획(unit·integration·e2e 선택·observability)/ADR. 항목을 충돌-안전 순서의 스테이지로 분해(파일 경합 시 순차, 독립 시 병렬 가능). 계획을 대상 repo의 plans 디렉터리(예: `.omc/plans/`)에 저장.

### 3. 구현 루프 (스테이지별)
새 feature 브랜치(현 HEAD off)에서 스테이지별:
- executor 위임(`subagent.spawn`) 구현 + 테스트 작성/수정.
- 🔴 **orchestrator fresh 재검증**(executor 완료보고 신뢰 금지 — 과거 오보고 사례): typecheck + 관련/전체 vitest.
- critic APPROVE까지 ITERATE.
- 로컬 커밋 + `scripts/parity-gate.sh:TEST_FLOOR` 실측 상향(같은 커밋). dead-code 제거 시 floor 하향도 정당(문서화).
- 위험 스테이지(env·deps·build·CSS토큰·스키마)는 **전체 parity-gate** 실행.

### 4. 홀리스틱 리뷰
critic이 **스펙 N항목 逐条 충족 + 레퍼런스 parity + 교차충돌 0 + 불변 보존**을 검증(충족표).

### 5. 필수 deslop
`ai-slop-cleaner`를 변경 파일 범위에 적용. dead-code/중복/과추상/장황주석만(맥락 주석 보존). 무변경이면 무변경.

### 6. regression + 루프 종료
regression 실행 후 루프를 취소·종료한다.

### 루프/중단 (사용자 directive)
- **loop 지시 시**: 모든 문제 해결까지 진행. credit/llm/token 비용 비고려.
- **중단 조건**: 컨텍스트 85% 도달 OR 작업 완료 → 작업·loop 중단(체크포인트: prd.json·progress.txt·메모리).

### 🔴 불변 제약
- 보안모델: 비밀 서버사이드 주입·VITE_ 비밀 금지·`client.ts` onResponse 인터셉터 금지(openapi-fetch body 1회 소비)·`.env`는 gitignore 유지(dist 실토큰 0).
- FSD 단방향(app→pages→widgets→features→entities→shared)·feature↔feature import 0.
- No-mock/하드코딩 금지·env 기반. **백엔드 무수정**(프론트 전용; server/auth BFF는 프론트 코드라 가능).
- 비배포 로컬도구(배포·엔드포인트 RBAC 서버강제 = 비목표). push/머지 = **사용자 통제**(원격 origin은 사용자 설정).
- 답변·문서 한글(기술 토큰 영문).

## Output Contract
- 스펙 항목별 결과를 **표**(항목/상태/근거 `file:line`)로 간결히.
- 테스트 수 변화(기준 floor→최종)·각 스테이지 critic 판정·게이트 결과.
- 미충족/수용-범위한정/후속분리 항목 정직 명시.
- "완료"는 모든 항목 해결(또는 정직한 미충족 표기) + regression 통과 후에만.

## Operating Rules
1. 계획 없는 즉시실행 금지 — 스테이지 분해와 계획 파일 저장이 먼저다.
2. executor의 "완료" 보고를 신뢰하지 말고 orchestrator가 직접 재검증한다(typecheck + vitest 실측).
3. critic APPROVE 없는 스테이지는 다음으로 넘어가지 않는다.
4. 불변 제약(보안·FSD·백엔드 무수정·push 사용자 통제)은 어떤 스테이지에서도 깨지 않는다.
5. 이 환경의 한계: OMC/OMX 전용 스킬(`/ralplan`, `/ralph`, `$ralph`, `$web-clone` 등)은 이 환경에 없으므로 위 환경 매핑표의 대안을 쓴다. `scripts/parity-gate.sh`·`ai-slop-cleaner`는 대상 repo/환경에 있을 때만 적용하고, 없으면 동등한 게이트(빌드+테스트+정적 분석)로 대체하되 그 사실을 보고한다.
