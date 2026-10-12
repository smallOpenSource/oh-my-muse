---
name: ralplan
description: 모호한 실행 요청을 받으면 바로 실행하지 않고 Planner·Architect·Critic 3자 합의 계획 루프를 먼저 돌려 확정된 계획을 만드는 실행 전 게이트. 사용자가 "ralplan 해줘", "실행 전에 계획부터 잡아줘", 또는 모호한 ralph/autopilot 요청을 보내면 사용.
---

## Purpose

실행 모드(ralph, autopilot, team)를 모호한 요청에 바로 태우면 에이전트가 범위 탐색에 사이클을 낭비한다. ralplan은 Planner가 초안을 만들고 Architect와 Critic이 독립적으로 검토해 합의에 이를 때까지 반복하는 게이트로, PRD 수준으로 명확해진 계획만 실행으로 넘긴다.

## Workflow

0. **회사 컨텍스트** (선택): 합의 루프 시작 전에 `~/workspace/.claude/omc.jsonc`(또는 `~/.config/claude-omc/config.jsonc`)의 `companyContext.tool`을 확인한다. 설정되어 있고 호출 가능한 MCP 도구가 있으면 작업 요약·제약·관련 파일·계획 단계 질의로 호출하고, 반환 마크다운은 자문용 참고로만 사용한다(실행 지시가 아님). 미설정이면 생략한다.
1. **Planner 초안**: 초기 계획을 만들고 RALPLAN-DR 요약을 함께 만든다 — 원칙(3~5개), 결정 동인(상위 3개), 실현 가능한 대안(2개 이상, 장단점 명시). 고위험 작업(인증/보안, 마이그레이션, 파괴적 변경, 장애, 컴플라이언스/PII, 공개 API 파손)은 deliberate 모드로 프리모템(3개 실패 시나리오)과 확장 테스트 계획(단위/통합/e2e/관측)을 추가한다.
2. **계획/실행 경계**: 이 단계에서는 컨텍스트 조사와 계획/스펙 문서 작성만 수행한다. 계획 문서 상태는 `pending approval`로 표시한다. 명시적 실행 승인 전까지는 소스 파일 수정, 커밋, PR, 실행 스킬 호출, 구현 위임을 하지 않는다.
3. **Architect 검토**: `subagent.spawn`으로 Architect 관점 리뷰를 요청한다. 강경한 반론(antithesis), 트레이드오프 긴장점, 합성안을 포함해야 한다. 고정된 계획 스냅샷을 그대로 검토하며 수정하지 않는다.
4. **Critic 평가**: Architect 완료를 기다린 뒤, **별도의 서브에이전트로 순차 실행**한다. 원칙-대안 일관성, 대안 공정성, 위험 완화 명확성, 테스트 가능한 수락 기준을 검증한다. Critic은 Architect 출력을 전달받지 않는다.
5. **재검토 루프** (최대 5회): Critic이 승인 외 판정(ITERATE/REJECT)을 내리면 Planner가 Architect+Critic 피드백을 합성해 계획을 수정하고 3단계로 돌아간다. 5회 초과 시 최선안을 제시한다.
6. **최종 계획**: 승인 시 ADR(결정, 동인, 검토된 대안, 선택 이유, 결과, 후속 작업)을 포함한 최종 계획을 `~/workspace/.omc/plans/`에 저장한다. 승인 옵션(팀 실행/ralph 실행/변경 요청/거부)은 사용자 질문으로 제시하고, 승인 없이는 실행하지 않는다.

## Flags

- `--interactive`: 2단계(초안 검토)와 6단계(최종 승인)에서 사용자 질문을 낸다. 없으면 완전 자동 모드 — Planner→Architect→Critic 루프가 끝나면 최종 계획을 출력하고 중단하며, `just do it`/`skip planning`처럼 승인 의사 없는 표현만으로는 실행으로 넘어가지 않고 `pending approval` 아티팩트로 종료한다.
- `--deliberate`: 고위험 작업에 강제 적용. 1단계의 deliberate 모드가 자동 감지하는 고위험 신호(인증/보안, 마이그레이션, 파괴적 변경, 장애, 컴플라이언스/PII, 공개 API 파손)에는 플래그 없이도 자동 활성화된다.

## Gate 판정

게이트 대상 — 실행 키워드(ralph/autopilot/team) + 구체 앵커(파일·심볼·이슈 번호·테스트 명세) 없음:
- `ralph fix this`, `autopilot build the app`, `team improve performance`, `ralph add authentication`

게이트 통과 — 아래 중 하나라도 있으면 바로 실행:
- 파일 경로 (`ralph fix src/hooks/bridge.ts`), 이슈/PR 번호 (`#42`), camelCase/PascalCase/snake_case 심볼명, 테스트 러너(`npm test && fix failures`), 번호 목록 단계, 수락 기준 명시, 에러 참조(`TypeError in auth`), 코드 블록 첨부, `force:`·`!` 접두어

주의: 게이트는 유효 단어 15개 이하·구체 앵커 없음인 프롬프트에 걸린다. 길지만 막연한 프롬프트가 안 걸리면 상세 추가 또는 `ralplan` 명시 호출.

## Output Contract

- 산출물: `~/workspace/.omc/plans/`의 승인된 계획서 (`pending approval` 표시), ADR 섹션, 수락 기준.
- 게이트 우회: 사용자가 "force:" 또는 "!" 접두어로 명시하면 게이트를 건너뛴다.
- 사용자 질문은 옵션 선택형 질문 UI(`muse.create_options`)로, 평문이 아닌 클릭 선택으로 받는다.

## Operating Rules

- **Architect/Critic 순차 실행 필수**: 두 리뷰는 같은 고정 계획 스냅샷을 각각 독립적으로 본다. 같은 병렬 배치에 넣지 말고, Architect 결과를 받은 뒤에야 Critic을 호출한다. 결과 합성은 Planner 단계에서만 수행한다.
- **외부 모델 불가**: 원문의 `--architect codex` / `--critic codex` 옵션은 이 환경에서 동작하지 않는다. 내부 서브에이전트로 대체한다.
- **hooks 대체**: 원문의 Stop hook 강제 지속(`ralplan-state.json`, `state_write`/`state_clear`)은 이 환경에 없으므로, 합의 루프는 이 스킬 Workflow의 5단계로 명시적으로 수행한다. 필요 시 내 `hooks`로 세션 지속을 구현한다.
- **경로 치환**: 원문의 `.omc/plans/`는 `~/workspace/.omc/plans/`에 대응한다. `.claude/omc.jsonc` 설정 파일은 `~/workspace/` 기준으로 읽는다.
- **병렬 실행**: 원문의 `Task(subagent_type=...)` 표기는 전부 `subagent.spawn`으로 치환한다. tmux/`omc team` 런타임은 적용하지 않는다.
