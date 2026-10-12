---
name: ultragoal
description: 간단한 브리프를 순서가 있는 목표들의 집합으로 쪼개, 추가 전용 장부에 시작/체크포인트/차단/실패 이벤트를 기록하며 장기 이니셔티브를 여러 세션에 걸쳐 추적한다. 사용자가 "ultragoal 해줘", "이 큰 일을 장기로 추적해줘"라고 요청하면 사용.
---

## Purpose

긴 작업은 세션 재시작·워크트리 교체·리뷰 반복에도 살아남아야 한다. ultragoal은 브리프를 순서 있는 목표(story) 집합으로 쪼개고, 각 story의 시도 횟수와 증거를 추가 전용(append-only) 장부에 기록하며, 최종 완료를 ai-slop-cleaner + 검증 + 코드 리뷰 품질 게이트 뒤에 둔다.

## Workflow

1. **목표 생성**: 브리프에서 목표 집합을 만든다. `~/workspace/.omc/ultragoal/plans/` 아래에 planId별 디렉터리에 저장한다. 병렬 세션을 쓰면 planId를 세션마다 다르게 지정해 충돌을 피한다 (`--auto-plan-id`는 브리프 제목에서 `{epochMs}-{slug}` 파생). 이후 모든 단계에 같은 planId를 계속 쓴다.
2. **다음 story 시작**: 가장 이른 대기 중인 story를 활성화하고, 이 세션에서 수행할 story 지침(핸드오프)을 출력한다. 세션을 시작하는 에이전트는 이 지침을 읽고 story를 수행한다. story 이름(goal-id)을 지정하면 해당 story만 정확히 대상으로 한다 — 다른 story로 넘어가지(폴스루) 않으며, 순서가 아닌 대기 story도 시작할 수 있다. 다른 활성 story·알 수 없는 id·완료·리뷰 차단·(`--retry-failed` 없는) 실패 story는 상태 변경 없이 거부한다. 진행 중 명명 story는 시도 횟수 변경 없이 재개한다.
3. **체크포인트**: story 완료 시 `checkpoint --goal-id <id> --status complete --evidence "<테스트/파일/PR 증거>"`를 기록한다. 최종 story는 품질 게이트 증거(aiSlopCleaner, verification, codeReview 전부 깨끗)까지 포함해야 한다.
4. **차단 기록**: 최종 리뷰가 깨끗하지 않으면 완료 표시를 하지 말고 `record-review-blockers`로 새 차단 story를 추가해 작업을 이어간다.
5. **상태 조회**: 언제든 `status`로 장부를 확인한다. 차단 story는 리뷰 이슈 해결 + 게이트 재실행 후 다시 진행한다.

## Output Contract

- 산출물: `~/workspace/.omc/ultragoal/plans/<planId>/` 아래의 계획서와 장부(append-only), 세션별 story 핸드오프 텍스트.
- 장부 이벤트: start, checkpoint, blocker, failure만 기록하고, 기존 기록은 수정하지 않는다.
- 최종 완료 조건: 마지막 story의 품질 게이트 3종(ai-slop-cleaner, verification, code-review)이 전부 깨끗할 때만 완료.

## Operating Rules

- **Claude Code `/goal` 불가**: 원문은 Claude Code의 `/goal` 슬래시 명령과 연동되지만, 이 환경에는 `/goal` 메커니즘이 없다. `omc ultragoal` CLI와 `/goal` 연동, `--claude-goal-json` 스냅샷, PreToolUse `/goal` 가드는 적용되지 않는다. story 진행은 이 스킬 Workflow의 checkpoint/blocker 단계로 수행한다.
- **`omc` CLI 불가**: 원문의 `omc ultragoal` 셸 명령은 이 환경에서 제공되지 않는다. 장부·계획 파일(`~/workspace/.omc/ultragoal/`)을 직접 읽고 쓰는 방식으로 대체하고, 동일한 이벤트 의미(start/checkpoint/blocker/failure)를 유지한다.
- **경로 치환**: 원문의 `.omc/ultragoal`은 `~/workspace/.omc/ultragoal/`에 대응한다. MCP 회사 컨텍스트 호출은 해당 도구가 없으면 생략한다.
- **병렬 세션**: planId를 세션별로 분리해 장부 충돌을 피한다. 이는 원문의 `--plan-id`/`--auto-plan-id` 규칙과 동일하다.
