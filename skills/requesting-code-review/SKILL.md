---
name: requesting-code-review
description: "태스크 완료·주요 기능 구현·머지 전, 작업이 요구사항을 만족하는지 검증할 때 사용"
---

# 코드 리뷰 요청

이슈가 연쇄되기 전에 잡으려고 코드 리뷰어 서브에이전트를 파견한다. 리뷰어는
정밀하게 만든 평가 컨텍스트를 받는다 — 내 세션 히스토리는 절대 아니다.

**핵심 원칙:** 일찍, 자주 리뷰한다.

**[환경 한계]** 이 서브에이전트 환경에서는 직접 서브에이전트를 파견할 수 없다.
리뷰가 필요하면 상위 에이전트에게 위임 요청한다 — 아래 템플릿을 채운 프롬프트를
보고서에 담아 전달한다. 위임이 불가하면 [code-reviewer.md](code-reviewer.md)를
읽고 같은 기준으로 직접 리뷰하되, 작성자 셀프 리뷰는 약하다는 한계를 밝힌다.

## 리뷰 요청 시점

**필수:**
- subagent-driven-development의 각 태스크 뒤
- 주요 기능 완료 뒤
- main 머지 전

**선택 (가치 있음):**
- 막혔을 때 (새 관점)
- 리팩터 전 (베이스라인 확인)
- 복잡한 버그 수정 뒤

## 요청 방법

**1. git SHA 확보:**
```bash
BASE_SHA=$(git rev-parse HEAD~1)  # 또는: git merge-base origin/main HEAD
HEAD_SHA=$(git rev-parse HEAD)
```

**2. 코드 리뷰어 파견:**

[code-reviewer.md](code-reviewer.md)의 템플릿을 채워 파견한다.

**플레이스홀더:**
- `{DESCRIPTION}` - 무엇을 만들었는지 간단 요약
- `{PLAN_OR_REQUIREMENTS}` - 무엇을 해야 하는지
- `{BASE_SHA}` - 시작 커밋
- `{HEAD_SHA}` - 끝 커밋

**3. 피드백 조치:**
- Critical 이슈는 즉시 수정
- Important 이슈는 진행 전 수정
- Minor 이슈는 나중에 참고
- 리뷰어가 틀렸으면 근거와 함께 반박

## 예시

```
[Task 2 완료: 검증 함수 추가]

You: 태스크 3 전에 코드 리뷰를 요청합니다.

BASE_SHA=$(git log --oneline | grep "Task 1" | head -1 | cut -d' ' -f1)
HEAD_SHA=$(git rev-parse HEAD)

[코드 리뷰어 파견]
  DESCRIPTION: 4개 이슈 타입의 verifyIndex()·repairIndex() 추가
  PLAN_OR_REQUIREMENTS: docs/superpowers/plans/deployment-plan.md의 Task 2
  BASE_SHA: a7981ec
  HEAD_SHA: 3df7661

[서브에이전트 반환]:
  강점: 깔끔한 아키텍처, 실제 테스트
  이슈:
    Important: 진행 표시 누락
    Minor: 보고 간격 매직 넘버 (100)
  평가: 진행 가능

You: [진행 표시 수정]
[Task 3 계속]
```

## 흔한 합리화

| 변명 | 현실 |
|------|------|
| "리뷰어를 파견하는 대신 diff를 내가 직접 리뷰하자" | 당신은 조정자다 — diff를 인라인으로 리뷰하면 작업을 계속 몰고 가는 데 필요한 컨텍스트를 태운다. 리뷰어 서브에이전트를 파견하라: diff와 평가는 그 컨텍스트에 살고, 당신에게는 발견만 돌아온다. |
| "리뷰어는 내 세션 히스토리 전체가 있어야 변경을 이해한다" | 정밀하게 만든 컨텍스트를 준다, 세션 히스토리는 아니다. 그래야 리뷰어가 내 사고 과정이 아니라 작업 산출물에 집중한다. |

## 경고 신호

**절대 금지:**
- "단순하다"며 리뷰 건너뛰기
- Critical 이슈 무시
- 고치지 않은 Important 이슈를 안고 진행
- 정당한 기술적 피드백과 말싸움

**리뷰어가 틀렸으면:**
- 기술적 근거로 반박
- 동작을 증명하는 코드/테스트 제시
- 확인 요청

템플릿: [code-reviewer.md](code-reviewer.md)
