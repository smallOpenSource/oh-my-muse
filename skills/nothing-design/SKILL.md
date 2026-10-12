---
name: nothing-design
description: "Nothing 브랜드 스타일(미니멀·도트매트릭스·모노크롬) UI 디자인 시스템 적용. 사용자가 'Nothing 스타일로 디자인해줘', 'Nothing design 적용해줘'라고 명시적으로 요청하면 사용. 일반 UI 작업에는 자동 트리거하지 않는다."
---

# Nothing-Inspired UI/UX Design System

## Purpose

Swiss 타이포그래피·인더스트리얼 디자인(Braun, Teenage Engineering)에 뿌리를 둔 시니어 프로덕트
디자이너의 툴킷. 모노크롬·타이포그래피 주도·정보 밀도 높되 clutter 없음. 다크/라이트 모드 동등 설계.

**디자인 작업 시작 전, 필요한 Google Fonts와 로드 방식을 반드시 선언**한다(`references/tokens.md` §1 참조).
폰트가 이미 있다고 추정하지 않는다.

**트리거 원칙**: 이 스킬은 사용자가 Nothing 스타일을 명시적으로 요청했을 때만 쓴다. 일반 UI 작업에
자동 적용하지 않는다.

## Workflow

1. **Declare fonts** — 로드할 Google Fonts를 사용자에게 알린다(`references/tokens.md` 참조)
2. **Ask mode** — dark or light? 어느 쪽도 기본값이 아니다.
3. **Sketch hierarchy** — 코드 작성 전 3-layer를 먼저 식별한다
4. **Compose** — craft rules 적용(Operating Rules)
5. **Check tokens** — 정확한 값은 `references/tokens.md`
6. **Build components** — 패턴은 `references/components.md`
7. **Adapt to platform** — 출력 규약은 `references/platform-mapping.md`

## Output Contract

산출물은 아래를 만족해야 한다:

- 3-layer hierarchy 명시 (Primary 1개 / Secondary / Tertiary) — squint 테스트 통과
- 폰트 예산 준수: 가족 ≤2, 사이즈 ≤3, 웨이트 ≤2
- 회색조 ≤4단계로 계층 표현 (`--text-display`→`--text-primary`→`--text-secondary`→`--text-disabled`)
- 토큰 값은 `references/tokens.md`에서, 컴포넌트 패턴은 `references/components.md`에서 가져옴
- 다크/라이트 중 사용자가 고른 모드로 설계 (둘 다 1급)
- 화면당 패턴을 깨는 지점 정확히 1곳

## Operating Rules

### Craft rules — 구성법

**1. Visual Hierarchy: Three-Layer Rule.** 화면은 정확히 3개 중요도 레이어.

| Layer | What | How |
|-------|------|-----|
| **Primary** | 사용자가 처음 보는 ONE thing. 숫자·헤드라인·상태 | Doto 또는 Space Grotesk display 사이즈. `--text-display`. 48–96px breathing room |
| **Secondary** | 보조 맥락. 라벨·설명·관련 데이터 | Space Grotesk body/subheading. `--text-primary`. primary에 8–16px로 타이트하게 그룹 |
| **Tertiary** | 메타데이터·내비·시스템 정보. 보이지만 경쟁 금지 | Space Mono caption/label. `--text-secondary` 또는 `--text-disabled`. ALL CAPS. 가장자리/하단으로 |

Squint 테스트: 화면을 찡그리고 봐도 무엇이 가장 중요한지 보여야 한다. 두 요소가 경쟁하면 하나는
줄이거나, 흐리게 하거나, 옮긴다. 흔한 실수: 전부 "secondary"로 만들기. 균일한 크기+균일한 간격 =
시각적 평탄함. primary는 터무니없이 크게, tertiary는 터무니없이 작게. 대비 자체가 계층이다.

**2. Font Discipline.** 화면당 최대: 폰트 패밀리 2개(Space Grotesk + Space Mono. Doto는 hero 순간만) /
폰트 사이즈 3개(큼·중간·작음 각 1) / 웨이트 2개(Regular + 하나 — 보통 Light 또는 Medium, Bold는 드묾).
새 사이즈를 추가하려거든 먼저 묻는다: 간격이나 색으로 구분할 수 있는가?

| Decision | Size | Weight | Color |
|----------|:---:|:---:|:---:|
| Heading vs. body | Yes | No | No |
| Label vs. value | No | No | Yes |
| Active vs. inactive nav | No | No | Yes |
| Hero number vs. unit | Yes | No | No |
| Section title vs. content | Yes | Optional | No |

경험칙: 새 font-size에 손이 가면 대개 간격 문제다. 사이즈 대신 거리를 더한다.

**3. Spacing as Meaning.** 간격이 관계 전달의 1차 도구다.
Tight(4–8px)="함께 속함" / Medium(16px)="같은 그룹의 다른 항목" / Wide(32–48px)="새 그룹 시작" /
Vast(64–96px)="새 컨텍스트". **구분선이 필요하면 간격이 잘못된 것이다.** 구분선은 간격 대비
부족의 증상. 구조적으로 동일한 항목이 빽빽한 데이터 리스트에서만 쓴다.

**4. Container Strategy (가벼운 순).** ① 간격만(proximity) ② 단일 구분선 ③ 은은한 border ④ 배경이
바뀌는 surface 카드. 아래로 갈수록 시각적 무게 증가. 가장 중요한 요소는 절대 박스에 넣지 않는다 —
배경 위에 띄운다.

**5. Color as Hierarchy.** 모노크롬에서 회색조 자체가 계층이다. 화면당 최대 4단계.
`--accent` 빨강(#D71921)은 계층의 일부가 아니다 — "여기, 지금 봐라"는 인터럽트다. 급한 게 없으면
화면에 빨강 없음. 데이터 상태 색(success/warning/accent)은 데이터 값을 인코딩할 때만 예외 —
**값 자체**에 색을 입히고 라벨·행 배경에는 입히지 않는다.

**6. Consistency vs. Variance.** 일관되게: 폰트 패밀리·라벨 처리(항상 Space Mono ALL CAPS)·간격
리듬·색 역할·컴포넌트 형태·정렬. **화면당 정확히 한 곳에서만** 패턴을 깬다(거대 숫자·사각형 속 원형
위젯·회색 속 빨강·Doto 헤드라인·전부 타이트한데 한 곳만 vast한 간격). 이 한 번의 break가 디자인이다.

**7. Compositional Balance.** 비대칭 > 대칭. 중앙 정렬은 제네릭하다. 큰 것 왼쪽+작은 것 오른쪽,
top-heavy, edge-anchored를 선호. 무거운 요소는 더 무거운 요소가 아니라 더 많은 빈 공간으로 균형.

**8. The Nothing Vibe.** 빈 공간의 자신감 / 작은 것의 정밀도(letter-spacing·정확한 회색값·4px 간격) /
데이터 자체가 미학(`36GB/s` in Space Mono 48px) / 기계적 정직함(토글=물리 스위치) / 화면당 하나의
놀라움(도트매트릭스 헤드라인·원형 위젯·빨간 점) / 타악기적이지 유체적이지 않음(click, not swoosh).

**9. 데이터 밀집 화면의 시각적 다양성.** 3개 이상 데이터 섹션이면 형태를 달리한다: hero number(무거움,
1회) / segmented progress bar / concentric rings / inline compact bar / number-only + status color /
sparkline / stat row(가벼움). 리드 섹션→가장 무겁게, FORM은 달리하되 VOICE는 동일하게.

### Anti-patterns — 절대 금지

- UI 크롬에 그라디언트 금지. 그림자·블러 금지. 플랫 + border 분리.
- 스켈레톤 로딩 금지. `[LOADING...]` 텍스트 또는 segmented spinner.
- 토스트 팝업 금지. 인라인 상태 텍스트: `[SAVED]`, `[ERROR: ...]`
- 슬픈 얼굴 일러스트·마스코트·장황한 empty state 금지. 테이블 zebra striping 금지.
- filled 아이콘·멀티컬러 아이콘·UI용 이모지 금지. parallax·scroll-jacking·과잉 애니메이션 금지.
- spring/bounce easing 금지. subtle ease-out만.
- 카드 border-radius > 16px 금지. 버튼은 pill(999px) 또는 technical(4–8px).
- 데이터 시각화: 색 도입 전에 **opacity**(100%/60%/30%) 또는 **pattern**(solid/striped/dotted)으로 구분.

### Reference files

- `references/tokens.md` — 폰트·타입 스케일·컬러 시스템(다크+라이트)·간격·그리드·모션·아이콘·도트매트릭스 모티프
- `references/components.md` — 카드·버튼·인풋·리스트·테이블·내비·태그·segmented control·progress bar·차트·위젯·오버레이·상태 패턴
- `references/platform-mapping.md` — HTML/CSS, SwiftUI, React/Tailwind, Paper 출력 규약
