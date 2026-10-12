---
name: visual-verdict
description: "생성된 UI 스크린샷을 참조 이미지와 비교해 엄격한 JSON 판정(pass/revise/fail)을 반환하는 시각 QA 스킬. 사용자가 'visual-verdict 해줘', '스크린샷 비교해줘', '시각 검수해줘'라고 요청하고 참조 이미지와 생성 스크린샷이 준비됐을 때 사용."
---

# Visual Verdict

## Purpose

생성된 UI 스크린샷을 하나 이상의 참조 이미지와 비교하고, 다음 수정 반복을 주도할 수 있는 엄격한 JSON 판정을 반환한다.

## Workflow

1. 입력 수집: `reference_images[]`(참조 이미지 경로 1개 이상), `generated_screenshot`(현재 산출물 이미지), 선택 `category_hint`(예: `hackernews`, `sns-feed`, `dashboard`).
2. 비교: 레이아웃·간격·타이포그래피·색상·위계를 참조와 대조한다.
3. 아래 Output Contract 형태의 **JSON만** 반환한다.
4. `score < 90`이면 시각 작업을 완료로 보지 말고, 수정 후 이 스킬을 다시 돌린다(루프).

## Output Contract

```json
{
  "score": 0,
  "verdict": "revise",
  "category_match": false,
  "differences": ["Top nav spacing is tighter than reference"],
  "suggestions": ["Increase nav item horizontal padding by 4px"],
  "reasoning": "Core layout matches, but style details still diverge."
}
```

- `score`: 0~100 정수. 합격 기준은 **90+**
- `verdict`: `pass` | `revise` | `fail`
- `category_match`: 의도한 UI 카테고리/스타일과 일치하면 `true`
- `differences[]`: 구체적 시각 불일치 (레이아웃, 간격, 타이포, 색상, 위계)
- `suggestions[]`: 불일치에 대응하는 실행 가능한 다음 수정안
- `reasoning`: 1~2문장 요약

## Operating Rules

- JSON 외 텍스트 출력 금지. 판정은 이 JSON이 권위(authoritative) 판정이다.
- 차이 진단이 어려우면 픽셀 단위 diff(예: pixel diff/pixelmatch 오버레이)를 **보조 디버그 수단**으로 써 핫스팟을 찾고, 이를 `differences[]`·`suggestions[]`로 번역한다.
- 한계와 대안: 이 환경에는 라이브 브라우저가 없으므로 **브라우저에서 직접 스크린샷을 캡처할 수 없다.** 가장 가까운 대안은 사용자가 업로드한 스크린샷 파일(~/workspace/user/media_library/ 또는 제공된 경로)과 media_library 스킬의 이미지를 참조·비교 이미지로 사용하는 것이다. 캡처 자동화가 필요하면 부모 에이전트에 브라우저 위임을 요청한다.
