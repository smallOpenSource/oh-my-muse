---
name: play-qa
description: "Godot HTML5 웹게임을 실제 브라우저에서 직접 플레이하며 렌더·입력·시작 결함을 QA(playwright). 사용자가 '게임 직접 플레이해서 QA해줘', '네가 직접 플레이해봐', 'play-qa'라고 요청하면 사용."
---

# play-qa: 에이전트가 직접 브라우저에서 게임을 플레이·QA

## Purpose

헤드리스 CI(GREEN)와 "CLICK to start" 라벨이 **구조적으로 못 잡는** 결함 — 입력 손맛이 아니라
*렌더·HUD·입력 반영·시작·소프트락* — 을 **에이전트가 실제 브라우저에서 게임을 직접 플레이**하며
객관적으로 잡는다. (실증: 이 스킬이 '탭/클릭으로 8게임 중 7개가 시작조차 안 되는' 터치기기 쇼스토퍼를
잡았다. 헤드리스는 못 봤다.)

## 언제

- 오너가 "네가 직접 플레이/qa해봐", "게임 테스트해봐" 류로 위임.
- **실기기 손맛 플레이테스트 직전** 객관 점검(시작조차 안 되는 결함부터 거른다).
- 게임 코드 수정 후 end-to-end 검증.

## Workflow

### 0. 전제조건: playwright (없으면 설치부터)

진행 전 설치 여부를 먼저 확인하고, 없으면 **설치부터** 한다(추정·임의 재설치 금지):

```bash
ls "${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}" 2>/dev/null | grep -qi chromium && echo ok
python3 -c "import playwright; print('py-playwright ok')"
```

미설치면 직접 설치한다 (원본의 `setup-playwright` 스킬은 이 워크스페이스에 없으므로 아래 표준 절차로 대체):

```bash
python3 -m pip install --user playwright
python3 -m playwright install chromium --with-deps  # --with-deps는 sudo 필요, 없으면 생략
```

**chrome/playwright 임의 재설치 금지** — 이미 설치된 것은 그대로 쓴다.

### 1. 환경 설정

- Playwright 실행: `PLAYWRIGHT_BROWSERS_PATH=$BROWSERS_PATH DISPLAY=$DISPLAY python`.
  chromium은 `launch(args=["--enable-unsafe-swiftshader","--no-sandbox"])`.
- 몽타주용 **PIL은 별도 python3 환경**에 있을 수 있음(playwright env엔 없음 → 몽타주는 별도 python으로).
- 서빙: 로컬 스테이징 빌드 경로 또는 라이브 URL(`$GAME_URL`). 로컬은 in-process `socketserver`로
  **COOP/COEP 헤더 + `.wasm`→`application/wasm`** 필수.
- 뷰포트 **720×1280**(세로) · context `has_touch=True` · wasm 부팅 로컬 ~12s / 라이브 ~15s(환경별 조정).

### 2. 플레이 사이클 (게임마다)

1. **서빙** (로컬 staged 또는 라이브 URL).
2. load → 부팅 대기 → **시작**(아래 입력 함정!) → **코어루프 구동**(게임별 제스처) →
   스크린샷(타이틀 + 플레이 후반) → 콘솔 에러 수집.
3. **몽타주**: PIL 있는 python으로 N게임 후반 상태를 1장으로 → `muse.read`로 일괄 판독 →
   이상한 것만 개별 풀해상도 확대.
4. **진단**: 실제결함 / 합성입력한계 / 주관(오너) 3분류.
5. **수정 루프**(실제결함만): 코드수정 → 독립리뷰(author≠reviewer) → **재export(웹빌드 스크립트)** →
   in-browser 재검증 → 배포(사람승인 게이트) → 라이브 재검증.
6. 주관 항목 → 플레이테스트 체크리스트로 오너에게.

### 3. 게임별 구동 제스처 (장르별 예시)

bullet-heaven=드래그 이동(자동사격) · merge=상단 DRAG 드롭 · onebutton=held click/Space 패리(타이밍
정밀=합성한계) · driver=←/→ 키 · stacker=탭/Space 드롭 · slingshot=당겨 DRAG-릴리즈(정밀조준=합성한계) ·
gridfit=트레이→격자 DRAG(픽업=합성한계) · ward=가로 DRAG 잉크배리어.

## Output Contract

- 게임별: 타이틀 스크린샷 + 플레이 후반 스크린샷 + 콘솔 에러 수집 결과
- 몽타주 1장(N게임 후반 상태 일괄 판독용)
- 진단 리포트: **실제결함 / 합성입력한계 / 주관(오너 실기기)** 3분류
- 실제결함은 수정 루프(재export → in-browser 재검증)까지, 주관 항목은 플레이테스트 체크리스트로 전달

## Operating Rules

### 객관(잡는다) vs 주관(오너 몫) — 정직하게 구분

- **잡는다**: 부팅·렌더·HUD 겹침/글리프 tofu·깨진 에셋/이미지·콘솔 `SCRIPT ERROR`/`pageerror`·입력 반영·
  코어루프 진행(점수/조각 등 프록시)·소프트락·**타이틀 시작 실패**·글리치.
- **못 잡는다(=오너 실기기)**: 손맛/타이밍 체감·오디오 음색(디바이스 없음)·정밀 조준/타이밍/픽업이 필요한
  진행. **합성입력이 못 한 진행 = 자동화 한계지 결함 아님** — '결함'으로 단정 금지, 한계로 표기.

### ★ 입력 함정 (하드-원 교훈 — 모르면 멀쩡한 게임을 '고장'으로 오판)

- **시작은 HELD click**: `mouse.move(x,y); mouse.down(); wait(~250ms); mouse.up()`.
  **instant `click()` 금지** — ① 폴링형 입력(예: onebutton의 `Input.is_mouse_button_pressed`)은
  instant down+up을 프레임 사이에서 놓침 ② Godot 캔버스 포커스.
- **타이틀 `mouse_filter=STOP` 버그류 (실제 적발된 결함)**: 타이틀 풀스크린 `ColorRect`/`Label`은
  Godot 기본 `mouse_filter=STOP`이라 클릭/탭을 *삼켜* `_unhandled_input` 시작핸들러에 도달 못 함 →
  **키보드 Space만 시작**(터치기기엔 Space 없음 = 데드엔드). **증상: click/tap엔 시작 안 되고 Space엔
  시작되면 이 버그.** 수정 = `_show_title()` 끝에 타이틀 Control(단 `Button` 제외)을
  `MOUSE_FILTER_IGNORE`로.
- **드롭/드로우/조준은 DRAG**(down+move+up), bare click 아님(머지 '드롭'=상단 드래그). 드래그는
  인게임에서 잘 먹지만 bare click은 안 먹을 수 있다.
- **시작 후 맹목 Space 금지**: Space가 일부 게임을 **PAUSE**시킨다(타이틀=시작, 인게임=일시정지일 수
  있음 — 화면 우상단 `❚❚` 확인).
- **헤드리스 맹점**: env-게이트 오토데모는 `_start_game()`를 *직접 호출* → 입력-시작 경로 우회 →
  헤드리스는 시작/입력 버그를 **구조적으로 못 봄**. in-browser만이 잡는다.
- **헤드리스 desktop Godot AUTOSHOTS는 일부 env서 GL 크래시**(rc139/segfault) → 웹빌드 in-browser로 대체.
- 캔버스는 DOM이 아니라 canvas 렌더 → 점수/HUD는 DOM 스크랩 불가, **스크린샷 판독**으로만 평가.

### 하드 제약

- 비밀값 출력/커밋 금지 · 배포=사람승인 · 게임플레이 바이트 변경 시 author≠reviewer 독립리뷰 · 웹빌드 <20MB.
- 합성입력 미진행을 결함으로 단정 금지(한계 표기) · 주관 손맛/음색/난이도는 오너 실기기 몫임을 명시.
- 참조: 프로젝트의 게임 빌드 노트(in-browser 플레이테스트 방법론) · 플레이테스트 체크리스트(손맛 루브릭).

### Muse 환경 한계·대안

- 원본의 `setup-playwright` 스킬 위임 경로는 이 워크스페이스에 해당 스킬이 없으므로, 위 §0의 직접
  설치 절차로 대체한다. 이 VM에는 현재 playwright 미설치 상태임을 확인했다 — 첫 실행 시 설치가 필요하다.
- 장시간 플레이 세션은 `muse.exec`의 background 모드 + `process.list`/`process.log`/`process.poll`/
  `process.kill`로 관리한다.
- 브라우저 조작이 필요한 단계는 이 환경의 브라우저 도구를 쓴다 — `browser.open`은 텍스트 페치용이므로
  실제 플레이 조작(클릭·드래그·키 입력)은 playwright 스크립트로 수행한다.
