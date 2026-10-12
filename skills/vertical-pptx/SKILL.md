---
name: vertical-pptx
description: "A4 세로(210x297mm) 규격 PPTX 생성·점검·수리와 16:9 덱의 A4 세로 변환. 사용자가 'A4 세로 pptx 만들어줘', '세로형 슬라이드', '인쇄용 pptx', 'vertical-pptx'라고 요청하면 사용."
---

# vertical-pptx — A4 세로(210x297mm) 규격 PPTX

## Purpose
인쇄해서 돌리는 문서형 덱을 A4 세로 규격으로 만들고, 그 결과가 정말 A4 세로인지 파일 바이트로 판정한다.
이 스킬이 소유하는 것은 **규격과 최소 결정론적 레이아웃**이다: 210x297mm·여백·8열 20행 그리드·한글 3슬롯·인쇄 pt·검증·수리.
색 팔레트·차트·아이콘·디자인 감각은 소유하지 않는다. 그건 아래 §위임 에 맡긴다.

self-contained 번들 5파일이고 저장소에 의존성을 하나도 더하지 않는다.

## When to use

- "A4 세로 pptx", "세로형 슬라이드", "인쇄용 pptx", "문서형 덱", "제안서 pptx"를 만들 때.
- 이미 있는 pptx가 진짜 A4 세로인지 판정할 때(치수·`type` 속성·여백·도형 이탈).
- 16:9 덱을 A4 세로로 바꾸고 무엇이 파손됐는지 슬라이드별로 받아야 할 때.
- 마크다운 원고를 그대로 인쇄 규격 덱으로 떨어뜨릴 때.

| 파일 | 역할 |
|---|---|
| `SKILL.md` | 이 문서 |
| `build_a4p.js` | node 빌더(pptxgenjs) + **유일한** 마크다운 → deck JSON 변환기 |
| `build_a4p.py` | python 빌더(python-pptx). 입력은 deck JSON 뿐이고 `--md`가 없다 |
| `verify_a4p.mjs` | 검증기·수리기·`--suggest-deck`. node stdlib만 쓰고 외부 의존성 0 |
| `a4p.test.mjs` | 유닛(`node --test`). 외부 의존성 0으로 상시 실행 |

## Workflow

### 표준 레시피 (4단계)
`--suggest-deck`은 고급 플래그가 아니라 **세 번째 단계**다. 기본 상자에 안 들어가는 본문은 흔하고, 그때마다 왕복하는 것이 정상 워크플로다.

```bash
S=<이 스킬 디렉터리>
F=<빌더가 보고한 fontFile 경로>

# 1) build   마크다운 → deck JSON → pptx
node $S/build_a4p.js --md 원고.md --emit-json > deck.json
node $S/build_a4p.js --in deck.json --out out.pptx

# 2) verify  규격·여백·이탈·오버플로 판정
node $S/verify_a4p.mjs out.pptx --font-file $F

# 3) suggest 오버플로가 있을 때만. rows만 고친 새 deck JSON을 낸다
node $S/verify_a4p.mjs out.pptx --deck deck.json --font-file $F --suggest-deck fixed.json

# 4) rebuild 고친 deck으로 다시 빌드하고 2)로 돌아가 확인
node $S/build_a4p.js --in fixed.json --out out.pptx
node $S/verify_a4p.mjs out.pptx --font-file $F
```

- `--emit-json`에 `--out`을 안 주면 stdout은 deck JSON 전용이 되고 사람이 읽는 표는 stderr로 간다. 그래서 위처럼 `> deck.json` 리다이렉트가 안전하다.
- python 빌더는 같은 deck JSON을 먹는다: `python $S/build_a4p.py --in deck.json --out out.pptx` (마찬가지로 `$S` 기준).

### 수리와 변환 (이미 있는 덱 — 도형은 하나도 움직이지 않는다)
```bash
node $S/verify_a4p.mjs 남의덱.pptx --repair --out fixed.pptx        # sldSz만 A4 세로로 교체
node $S/verify_a4p.mjs 16by9.pptx --convert-a4p --out a4p.pptx      # 위 + 슬라이드별 파손 리포트
```
- 기본은 **새 파일**이다. 원본 덮어쓰기는 `--in-place`로 명시해야 한다.
- `--convert-a4p`는 좁아진 폭 때문에 슬라이드 밖으로 나간 도형을 슬라이드별로 이탈량(mm)과 함께 열거한다. 자동 재배치는 하지 않는다. 어디로 옮겨야 하는지는 이 도구가 아는 정보가 아니다.
- **쓰기 성공과 규격 통과는 다른 주장이다.** 수리 뒤 VERDICT는 원본이 아니라 산출물을 다시 검증한 결과이고, sldSz를 고쳐도 도형이 삐져나와 있으면 여전히 FAIL이다.

### 위임
> 실행 전 `muse.skill_search`로 pptx 문서 스킬(레이아웃·색·차트 담당, 예: artifacts/presentation 계열)을 찾는다. 있으면 레이아웃·색·차트·pptxgenjs 함정은 그쪽에 맡기고 이 스킬은 규격과 검증만 맡는다. 없으면 아래 §위임 불가 시 최소 지식 으로 진행한다. 설치를 요구하며 멈추지 않는다.

조건은 **관측 가능한 능력**이다. 스킬 목록에 pptx 문서 스킬이 보이면 위임하고, 없으면 최소 지식으로 진행한다.

위임한 뒤에도 규격 판정은 이 스킬이 한다. 상대가 만든 덱도 `verify_a4p.mjs`를 통과해야 한다.

### 위임 불가 시 최소 지식

위임 대상이 목록에 없을 때 이 블록만으로 진행한다. **색 팔레트·차트·아이콘·디자인 가이드는 여기 없다. 그건 위임 대상의 영역이다.**

1. **레이아웃을 슬라이드보다 먼저 확정한다.** 슬라이드를 하나라도 추가한 뒤에 크기를 바꾸면 이미 만든 슬라이드가 옛 크기를 따른다.
   ```js
   pptx.defineLayout({ name: 'A4P', width: 210 / 25.4, height: 297 / 25.4 });
   pptx.layout = 'A4P';   // 그 다음에야 addSlide()
   ```
   python-pptx: `prs.slide_width = Emu(7560000)`, `prs.slide_height = Emu(10692000)`, `p:sldSz`의 `type` 속성 제거(기본값 custom).
2. **여백은 사방 10mm 이상.** 1mm = 36000 EMU. 여백 10mm = 360000, 본문 폭 = 6840000, 본문 높이 = 9972000. pptxgenjs의 `x`/`y`/`w`/`h`는 100 이상이면 EMU로, 그 미만이면 인치로 해석된다.
3. **A4 세로 기본 배치 4종** (EMU, 여백 10mm 기준):

   | 배치 | 도형 | x | y | cx | cy |
   |---|---|---|---|---|---|
   | 제목형 | 제목 | 360000 | 360000 | 6840000 | 867600 |
   | 본문형 | 제목 | 360000 | 360000 | 6840000 | 867600 |
   | | 본문 | 360000 | 1371600 | 6840000 | 867600 |
   | 2단 | 좌 | 360000 | 1371600 | 3348000 | 867600 |
   | | 우 | 3852000 | 1371600 | 3348000 | 867600 |
   | 표 | 표 전체 | 360000 | 1371600 | 6840000 | 행 수 x 361800 |

   아래로 쌓을 때 `y = 360000 + 505800 * r`, `n`행 상자의 `cy = 361800 * n + 144000 * (n - 1)`. `y + cy`가 **10332000**을 넘으면 하단 여백 침범.
4. **본문은 10~11pt**(기본 10.5pt). 제목은 본문+6pt, 소제목은 본문+2pt. 줄간 1.2.
5. **한글은 3슬롯 전부 채운다**(`a:latin`·`a:ea`·`a:cs`). pptxgenjs는 `fontFace` 하나면 되고, python-pptx는 `a:ea`·`a:cs`를 직접 주입. 폰트 이름은 그 머신에 실제로 있는 것을 쓴다(맑은 고딕 하드코딩 금지).
6. **색은 `#` 없는 6자리 hex** (`'1A1A1A'`). `'#1A1A1A'`는 안 된다 — 두 라이브러리 모두 이 형식을 요구하고, `#`를 붙이면 색이 조용히 무시되거나 XML이 깨진다.

### 규격 상수 (EMU) — 1mm = 36000 EMU
| 항목 | 식 | m=10 (기본) |
|---|---|---|
| 슬라이드 | `210 * 36000` x `297 * 36000` | **7560000 x 10692000** |
| 본문 폭 / 높이 | `7560000 - 72000m` / `10692000 - 72000m` | 6840000 (190mm) / 9972000 (277mm) |
| 컬럼 폭 (8열) | `(182 - 2m) * 4500` | 729000 (20.25mm) |
| 행 높이 (20행) | `(221 - 2m) * 1800` | 361800 (10.05mm) |

컬럼 `c`에서 `k`열: `x = 36000m + 873000 * c` · `cx = 729000 * k + 144000 * (k - 1)`.
행 `r`에서 `n`행: `y = 36000m + 505800 * r` · `cy = 361800 * n + 144000 * (n - 1)`.
검산: `k=8` → `cx = 6840000`이고 `n=20` → `cy = 9972000`으로 본문 영역과 정확히 일치한다.
`meta.marginMm`은 **10 이상 40 이하의 정수**여야 한다(범위 밖·비정수면 **exit 3**).

### 프리셋 트랩 3종 (실측)
1. PowerPoint의 "A4 용지(210x297mm)" 프리셋 = 10.833 x 7.5in = **9906000 x 6858000** (가로!). Microsoft가 프린터 여백을 미리 빼고 프리셋을 만들어 둬서 이름은 A4인데 인쇄 가능 영역 치수다. 페이지 설정에서 **사용자 지정 21 x 29.7cm**만 쓴다. 검증기는 `PRESET_TRAP` 별도 판정.
2. 반올림한 인치: `8.27in` → cx=**7562088** (+2088). 차이는 0.06mm에 불과하지만 "이 파일이 A4인가"는 이진 질문이고 허용오차가 0이다. 전정밀도 `210 / 25.4`·`297 / 25.4`를 그대로 넘긴다. 검증기의 sldSz 비교에는 허용오차가 없다.
3. python-pptx의 잔존 `type`: 치수는 A4인데 `p:sldSz`에 `type="screen4x3"`가 남는다. **치수만으로는 파일을 판정할 수 없다** — 선언을 믿는 뷰어와 변환기가 있다. 판정 규칙: **속성 부재 또는 `custom`이면 통과, 그 밖의 값이면 실패**.

### 여백과 그리드

여백은 사방 **10mm 이상**이다. 가정용·사무용 프린터 대부분이 가장자리 4~5mm를 물리적으로 인쇄하지 못하고, 재단 없이 배포되는 문서라 잘려도 복구할 방법이 없기 때문이다. 그리드는 **8열 x 20행**, 거터 **4mm**다. 이 그리드는 A4 규격에서 도출되는 값이 아니라 이 스킬이 내린 **레이아웃 결정**이다.

### 행 배정 규칙과 INV-G
**INV-G (기하 불변식)**: 모든 도형의 `x`·`y`·`cx`·`cy`는 `meta.marginMm`·페이지 인덱스·블록 순서·블록 `type`·`bullets.items` 길이·명시된 `rows`·컬럼 스팬의 **순수 함수**다. **텍스트의 내용·길이·폰트·pt는 어떤 좌표에도 들어가지 않는다.**

이 불변식이 두 빌더를 교체 가능하게 만든다. 같은 deck JSON을 node 빌더와 python 빌더에 먹이면 좌표가 EMU 단위로 완전히 같아야 하고, 그 동등성 검사에 폰트 리더가 필요 없다. 그리고 폭 측정이 빌더 출력을 한 바이트도 바꾸지 않으므로 측정은 검증기 단독 소유가 된다.

행 수: `rows(block) = min(18, block.rows ?? default(type))`, `default(head)=1`, `default(body)=2`, `default(bullets)=max(1, items.length)`, 페이지 제목(h1)=2행 고정. **18 클램프**가 없으면 `rows: 19`짜리 덱이 슬라이드 밖 4.05mm로 나간다. **클램프 발동 판정은 `block.rows`가 아니라 `block.rows ?? default(type)`로 한다** — 항목 19개짜리 불릿 블록에 `rows`를 안 적어도 기본값이 19라 클램프가 걸린다. 클램프에 걸린 블록은 `BLOCK_TOO_TALL` 경고와 함께 자기 슬라이드에 혼자 놓인다. **블록은 절대 쪼개지 않는다.** 페이지 채우기는 세는 규칙뿐이다: 블록을 순서대로 훑으며 `used += rows(block)` 하고, 18을 넘기면 새 슬라이드를 연다. **불릿 행 배분**: 항목 `i`(0-based)는 `min(i, n-1)` 행에서 시작하고 남는 행은 전부 마지막 항목이 가져간다. 상자에 안 들어가는 텍스트는 **넘친다(조용히 옮기지 않는다)** — 고치는 길은 `--suggest-deck`뿐이다.

**넘치는 것이 사양인 이유:** 자동 리플로우를 넣는 순간 텍스트 길이가 좌표에 들어가고 INV-G가 깨진다. 그러면 두 빌더의 동등성 검증이 폰트 리더 두 벌을 요구하게 되고, 원고를 한 글자 고칠 때마다 전체 페이지네이션이 움직여 어제 검토한 배치가 오늘 달라진다. 인쇄용 문서에서 그건 규격 위반보다 나쁘다.

`rows: 18`로도 안 들어가면 `rows: 19`를 제안하지 않는다. `BLOCK_TOO_TALL`과 함께 "블록을 나눠라"를 낸다.

**기본 상자 용량** (bodyPt 10.5·줄간 1.2·marginMm 10·Noto Sans CJK KR 기준): 2행 상자 = **24.1mm** ≈ 약 5줄, 한 줄 한글 약 55자 → **약 275자**. 넉넉한 쪽 추정치다. `bodyPt`를 11로 올리면 줄당 글자 수가 약 5% 줄어든다.

### 한글 3슬롯

run의 `a:latin`·`a:ea`·`a:cs` **세 슬롯에 같은 typeface를 넣어야 한다.** `a:ea`가 없으면 한글이 대체 폰트로 떨어져 일부 뷰어에서 tofu(빈 네모)가 나고, 줄바꿈 위치가 달라져 오버플로 판정 자체가 무의미해진다 — python-pptx에서 가장 흔한 한글 깨짐 원인이다.

| 라이브러리 | 동작 | 필요한 조치 |
|---|---|---|
| pptxgenjs | `fontFace` 하나로 3슬롯을 모두 emit | 없음 |
| python-pptx | `run.font.name`은 `a:latin` **하나만** emit | `a:ea`·`a:cs`를 직접 주입 |

**맑은 고딕을 박아 넣지 않는다.** Windows 전용 폰트라 macOS·Linux에서는 대체 폰트로 치환되고, 치환되면 글자 폭이 달라져 줄바꿈 위치가 이동한다. 그러면 그리드에 맞춰 잡은 배치가 무너지고, 오버플로 판정도 함께 무효가 된다.

### 폰트 선택 체인 (하드코딩 금지)
```
--font <이름> → BANKER_PPTX_FONT → meta.font →
Noto Sans CJK KR → Malgun Gothic → Apple SD Gothic Neo → NanumGothic → 시스템 한국어 sans
```
빌더는 **실제로 파일이 존재하는 이름**을 위에서부터 고르고, 고른 이름과 절대경로를 항상 보고한다(stdout 마지막 줄 JSON의 `fontFile`). 명시한 이름이 해석되지 않으면 `FONT_NOT_FOUND` 경고를 남기고 다음으로 내려간다(조용히 바꾸지 않는다). 검증기는 그 경로를 **믿지 않고 대조**한다(폰트 `name` 테이블 패밀리 vs pptx의 `a:latin`) — 경로에 적힌 폰트와 실제 폰트가 다르면 이름 재해석으로 내려간다.

### 본문은 10~11pt인 이유

화면용 덱의 습관대로 18~24pt를 쓰면 A4 한 장에 문단 몇 개밖에 안 들어간다. 인쇄해서 손에 들고 읽는 문서의 본문 크기는 **10~11pt**다(기본값 10.5pt). 출처: <https://practicaltypography.com/point-size.html>(인쇄물 본문 10~12pt), 「행정업무의 운영 및 혁신에 관한 규정」 **제8조**(한국 공문서 용지 규격 210x297mm — 조문 번호만 인용).

### 방향은 한 파일에 섞을 수 없다

**하나의 pptx는 하나의 슬라이드 크기만 갖는다** (`p:sldSz`가 프레젠테이션 전체에 하나뿐). "3페이지만 가로로" 같은 요청을 받으면 **먼저 이 제약을 말하고**, 방향별로 파일을 나누어 각각 빌드한다. 방향이 섞인 deck JSON은 빌더가 **exit 3**으로 거부한다.

### 폭 판정은 하한이다
예측 폭은 **하한(lower bound)**. 커널링 쌍과 줄바꿈 규칙(한국어는 거의 아무 데서나 끊기고 라틴 문자는 아니다)을 재현하지 않기 때문에, 실제 폭은 계산값보다 넓을 수는 있어도 좁을 수는 없다. 그래서 "넘친다"는 판정은 건전하고, "안 넘친다"는 그저 침묵이다 — 라벨은 fail-safe로 설계됐다. `fontSource` 기본값은 `estimate`다. `measured`는 실제 폰트 파일을 열고 `name` 테이블 패밀리가 run의 `a:latin`과 일치함을 확인한 뒤에야 붙는다. `estimate` 모드에서는 **"넘친다"를 단정하지 않는다** — finding은 `unconfirmed` 상태로 "확인 불가(estimate)"라고만 적는다.

### 종료 코드 (세 스크립트 공통)
| 코드 | 뜻 |
|---|---|
| **0** | 통과 (빌드 성공 · 검증 PASS) |
| **1** | 검증 실패 (규격 위반·도형 이탈·오버플로 확정 · 재압축 무결성 실패) |
| **2** | 환경 미비 (pptxgenjs 또는 python-pptx 미도달 · python 3.9 미만) — stdout에 따라 할 수 있는 안내와 함께 |
| **3** | 사용법 오류 (deck 스키마 위반 · `marginMm` 범위 밖 · 방향 혼합 · 인자 오류 · 입력 파일 없음) |

exit 2는 사용자가 그대로 따라 할 수 있는 안내라서 stdout으로 나간다. 나머지 오류는 stderr다.

- **node가 베이스라인이다.** `verify_a4p.mjs`는 node stdlib만 쓴다. python으로 빌드했더라도 그 결과를 판정하려면 `verify_a4p.mjs`를 돌려야 하고, 검증 없는 생성은 이 스킬의 가치가 아니다. 스크립트는 **의존성을 자동 설치하지 않는다.** 런타임 준비는 `vertical-pptx-setup` 스킬이 담당한다.
- 일회성 스크래치 설치: `npm i --no-save --no-audit --no-fund pptxgenjs@4`, `python -m pip install --target <dir> python-pptx fonttools` (`PYTHONPATH`/`NODE_PATH`에 경로 추가).

### 의존성 (자동 설치하지 않는다)

| 도구 | 필요한 곳 | 없으면 |
|---|---|---|
| node (>= 16.7) | `verify_a4p.mjs` 전부 · `build_a4p.js` | 검증 자체가 불가능하다 |
| pptxgenjs (>= 4) | `build_a4p.js` 빌드 경로 | exit 2 + `docs-setup` 안내 |
| python 3.9+ 와 python-pptx | `build_a4p.py` | exit 2 + `docs-setup` 안내 |

## Output Contract
- 산출물: `out.pptx` + `deck.json` (재현 가능한 중간 산물).
- 검증 증거: `verify_a4p.mjs` exit code + VERDICT 줄 + `fontSource` (`--json` 리포트는 finding별 `code`·`slide`·`shape`·`severity`·`status`·`detail`).
- "완료" 전 4-field: ① 변경 파일 ② Evidence(exit code + VERDICT + `fontSource`) ③ 검증 layer ④ Unknown. `fontSource`가 `estimate`면 오버플로에 대해 "통과"가 아니라 "미측정". 픽셀 렌더 검증은 **Unknown** (soffice 부재 시).

## Operating Rules
1. **치수만 보고 판정하지 않는다.** 트랩 3(python-pptx 잔존 `type`) 때문에 선언도 본다.
2. **`8.27 x 11.69`를 쓰지 않는다.** `210 / 25.4`와 `297 / 25.4` 전정밀도를 그대로 넘긴다.
3. **PowerPoint의 "A4 용지" 프리셋을 고르지 않는다.** 그건 가로다.
4. **맑은 고딕을 하드코딩하지 않는다.** Windows 전용이라 치환되면 그리드와 오버플로 판정이 함께 무효가 된다.
5. **`fontSource: estimate`인데 "안 넘친다"로 읽지 않는다.** 그건 판정이 아니라 침묵이다. `--font-file`을 넘겨 `measured`로 올린 뒤 읽는다.
6. **`--suggest-deck`을 `--deck` 없이 부르지 않는다.** 원본 deck JSON이 필수 입력이다. pptx는 (슬라이드, 도형)만 알려 주고 내놓아야 하는 것은 (페이지, 블록)의 `rows`다.
7. **python 빌더에 `--md`를 찾지 않는다.** 마크다운 파서는 `build_a4p.js` 한 벌뿐이다. 두 벌이 되는 순간 같은 원고가 두 개의 덱이 된다.
8. **넘치는 텍스트를 자동으로 옮겨 주길 기대하지 않는다.** 사양상 옮기지 않는다. `--suggest-deck`이 그 자리다.
9. 한 파일에 방향을 섞을 수 없다 — "3페이지만 가로로" 요청이면 먼저 제약을 말하고 파일을 나눠 빌드한다.
10. 각 파일의 전체 플래그는 `--help`로 확인한다(`build_a4p.js --help` · `build_a4p.py --help` · `verify_a4p.mjs --help`).
11. 이 환경의 한계: LibreOffice 시각 렌더 검증은 `vertical-pptx-setup`으로 soffice를 설치했을 때만 가능하다. 없으면 구조·좌표·메트릭 검증으로 대체하고 Unknown으로 표기한다.
12. **`a:ea` 누락.** python-pptx에서 가장 흔한 한글 깨짐 원인이다 (§한글 3슬롯).

## 참고

- `verify_a4p.mjs --json`이 기계 판독용 리포트를 낸다. finding마다 `code`·`slide`·`shape`·`severity`·`status`·`detail`이 붙는다.
- 한글 3슬롯 주입 패턴의 다른 사례: `skills/arch-diagram/build_pptx_template.py`
