---
name: 3d-intro-build
description: "스크롤 위치에 맞춰 3D 플라이스루 영상이 움직이는 브랜드 인트로를 만듦. media.generate_image로 씬 스틸을, media.generate_video로 dive-in 클립을 만들고(외부 API·키 불필요), 단계별 검토 페이지 판정 뒤에만 다음 단계로 진행. 결과는 엄격한 CSP에서도 도는 페이지. 사용자가 '3d-intro-build 해줘'/'3D 인트로 만들어줘'/'스크롤 fly-through'/'인트로 영상 사이트'라고 요청하면 사용."
---

# 3d-intro-build — 스크롤-스크럽 3D 인트로 제작 (내장 media 파이프라인)

스크롤에 맞춰 카메라가 장면 사이를 날아가는 브랜드 인트로를 만든다.
씬 스틸은 `media.generate_image`로, 영상 클립은 `media.generate_video`(시작 프레임 이미지 입력 지원)로 만든다.
**외부 이미지·영상 API, 키, 크레덴셜이 전혀 필요 없다.**
결과는 scroll-world 엔진으로 배선한 인트로 페이지다. 단독 페이지로 쓰거나 기존 사이트 위에 붙인다.
**페이지 조립은 벤더링된 `references/scrub-engine.js`를 `mountScrollWorld` config로 구동한다 — 직접 스크롤 스크립트를 작성하지 않는다.**

이 스킬은 **오케스트레이션**만 소유한다. 아래 파일은 재구현하지 말고 그대로 부른다.

| 파일 | 맡은 일 |
|---|---|
| `references/curate.mjs` | 검토 페이지(스틸, 클립)와 판정 기록 |
| `references/serve.mjs`, `references/preview-lib.mjs` | 미리보기 서버(빈 포트, 상태 파일, 종료, CSP 헤더) |
| `references/assemble.mjs` | 인트로 페이지 조립(인라인 script, style 없음) |
| `references/intro-fixes.css`, `panel-glass.css`, `step-nav.js`, `step-nav.css` | 엔진 덧씌움(수정 파일은 항상, 나머지는 선택) |
| `references/verify-intro.mjs`, `references/verify.md` | 실제 브라우저 측정과 검증 목록 |

엔진(`references/scrub-engine.js`)과 템플릿(`references/index-template.html`)은 벤더링본이라 **수정하지 않는다**(출처는 `references/NOTICE.md`). 엔진의 결함은 사이트 CSS 와 JS 로 덧씌운다.
`references/azure-adapter.mjs`, `references/video-pool.mjs`는 구 Azure/WAN 백엔드용이라 **사용하지 않는다**(레거시, 삭제하지 않음).
답변은 한글(기술 토큰, 경로, 명령은 영문).

## media 파이프라인 제약 (반드시 지킨다)

- `media.generate_image`: 한 응답에서 **최대 4회** 호출. 씬이 많으면 여러 응답에 나눠 생성한다.
- `media.generate_video`: 한 사용자 메시지에서 **최대 6개** (성공 기준). 클립이 6개를 넘으면 메시지를 나눠 요청받는다.
- 영상 프롬프트는 있는 그대로 전달한다(수식어 덧씌우기 금지). 시작 프레임은 `kind: image`로 넘긴다.
- 생성된 파일은 `output_dir`로 프로젝트 폴더를 지정해 둔다. 기본 미디어 디렉터리에 두지 않는다.

## 원칙

- 생성(스틸·클립)은 단계별 명시적 승인 뒤에만 시작한다.
- 모든 산출물은 그것을 만든 프롬프트 정보와 나란히 보여 준다. 결과만 보여 주지 않는다.
- 단계마다 멈추고 판정을 받는다. 판정 없이 다음 단계로 가지 않는다.
- 미리보기 서버는 쓰지 않는 포트를 그때그때 받아 띄우고, 끝나면 종료한다. 기본 바인드는 `127.0.0.1` 이다. 원격 머신이면 SSH 포트 포워딩으로 보게 한다.
- 커밋, push, 배포는 사용자가 요청할 때만 한다.

**생성 차단선**: Step 2 의 계획 승인 이전에는 스틸을 만들지 않고, Step 3 의 모든 장면 스틸이 승인되기 전에는 클립을 만들지 않는다.

---

## Step 0 - 프리플라이트 (무료)

ffmpeg 가 준비됐는지 먼저 확인한다. media 도구는 별도 설치·크레덴셜이 필요 없다.

```bash
command -v ffmpeg >/dev/null && ffmpeg -version 2>&1 | head -1 || echo "ffmpeg: 미설치"
```

- ffmpeg 가 없으면 `3d-intro-setup` 스킬로 보낸다("3D 인트로 설정해줘"라고 하면 그 스킬 실행).
- 통과해야 다음 단계로 간다.
- 독립 검증(Step 6)에는 Node 용 playwright 패키지와 Chromium 이 필요하다. `setup-playwright` 스킬로 준비한다.

---

## Step 1 - 인터뷰 (무료)

`references/prompts.md` 의 인테이크 체크리스트를 따른다. 아래는 **반드시** 묻는다.

- **SUBJECT** - 대상 비즈니스/제품 + 한 줄 소개.
- **BRAND** - 화면에 표시할 브랜드명.
- **SCENES[] (순서 있는 씬 목록)** - 권장 5~7개. 이야기 순서는 여기서 정한다(예: 문제 제기, 해법, 결론). CTA 는 마지막 장면에만 둔다. 각 씬의 `id`, `label`, `subject`, `eyebrow`, `title`, `body`, `tags[]`.
- **ORIENTATION** - `720x1280`(세로) 또는 `1280x720`(가로). 스틸과 영상 크기가 이 값으로 통일된다.
- **SITE** - 단독 인트로 페이지인지, 기존 사이트 위에 붙이는지. 붙인다면 그 사이트의 CSP, 본문 시작 요소의 선택자(`#main` 같은 것), 고정 헤더의 선택자, 지원 언어.

부수 항목(없으면 기본값)

| 항목 | 기본 | 뜻 |
|---|---|---|
| `PALETTE` | 배경색 하나, accent 하나 | 엔진 테마 색 |
| `TONE`, `STYLE` | clay diorama | 화풍(prompts.md 2절) |
| `CAMERA_FEEL` | 잔잔한 전진 활공 | 카메라 움직임 |
| `MOBILE` | no | yes 면 세로 체인 추가(생성 횟수 약 2배) |
| `STEP_NAV` | no | yes 면 휠 1칸, 키, 스와이프가 정확히 한 장면을 이동(`step-nav.js`) |
| `PANEL` | 없음 | `glass` 면 흐린 유리 문구 패널(`panel-glass.css`) |

---

## Step 2 - 계획과 승인 (무료, 필수, 생성 차단선)

생성 **이전에** 계획 전체를 보여 주고 명시적 승인을 받는다.

- 계획: 장면 목록, 장면별 프롬프트(스타일 서문 + subject), 생성 횟수(스틸 테이크 수, 클립 수), 예상 응답 분할(4장/6클립 제한 기준).
- **명시적 승인이 없으면 여기서 멈춘다.**
- 씬 수나 테이크 수를 줄이는 선택지를 제시할 수 있다.
- 승인된 계획이 이후 단계의 상한이다. 재생성으로 횟수를 넘게 되면 그때 다시 승인을 받는다.

---

## Step 3 - 스틸과 검토 (승인 이후에만)

씬마다 `references/prompts.md` 의 스타일 서문 + 씬 subject 로 프롬프트를 만들되, **스타일 서문은 모든 씬에 글자 그대로 동일**하게 넣어 코히전을 만든다.
`media.generate_image` 로 생성한다(한 응답 4회 제한 — 씬이 많으면 나눠서).

- **변형(권장)** - 씬마다 테이크를 2개 만들면 사용자가 비교해 고를 수 있다.
- 체인 씨앗이 되는 스틸은 크기가 ORIENTATION 과 다르면 영상 전에 리사이즈(ffmpeg `scale`)하거나 재생성한다.

**검토 페이지**(스틸 단계). 프로젝트 dir 에 `curate-input.json` 을 적는다. 테이크마다 만든 조건을 함께 적는다.

```json
{ "title": "Acme", "stage": "stills",
  "scenes": [
    { "id": "s1", "label": "문제 제기", "takes": [
      { "file": "stills/s1-t1.png", "take": 1, "prompt": "…", "negativePrompt": "…",
        "size": "1280x720", "createdAt": "2026-10-10T09:00:00Z" } ] } ] }
```

```bash
node references/curate.mjs <projectDir>          # CURATE http://localhost:<port>/ (백그라운드), 상태 <projectDir>/curate.server.json
node references/curate.mjs --stop <projectDir>   # 끝나면 종료
```
- 장시간 서버는 `muse.exec`의 background 모드로 띄우고 `process.list`/`process.log`로 관리한다. 서버 URL은 사용자에게 안내하고 사용자가 직접 브라우저에서 확인한다.
- 페이지는 산출물마다 카드 하나다. 미리보기, 장면과 테이크 번호, 프롬프트 전문, 제외 프롬프트, 크기, 생성 시각, 파일 경로, sha256 이 함께 보인다. 같은 장면의 테이크는 가로로 나란히 놓인다.
- 사용자는 페이지에서 테이크를 골라 승인하거나, 재생성 메모를 쓰거나, 테이크를 탈락시킨 뒤 "판정 저장" 을 누른다. 결과는 `decisions.json` 의 `stills` 에 남긴다.
- 판정을 대화로 받으면 장면 번호와 테이크 번호로 기록한다.

  ```bash
  node references/curate.mjs --record <projectDir> --scene 2 --verdict approve --take 1
  node references/curate.mjs --record <projectDir> --scene 3 --verdict regenerate --note "글자가 깨짐"
  node references/curate.mjs --record <projectDir> --scene 3 --verdict reject --take 2
  ```

- `regenerate` 인 장면만 다시 만든다. 메모를 스타일 서문 뒤 subject 에 반영하고, 새 테이크를 `curate-input.json` 에 더한다. 그 장면은 `--record --scene <n> --verdict pending` 으로 판정을 되돌린 뒤 페이지를 다시 보여 준다.
- 탈락한 테이크는 지우지 않고 날짜 폴더로 옮긴다: `node references/curate.mjs --archive <projectDir>`(`rejected-YYYYMMDD/`).
- **모든 장면이 `approve` 일 때만** Step 4 로 간다. 각 장면의 영상 씨앗은 그 장면의 `chosen` 이다. 승인되지 않은 테이크에는 클립을 만들지 않는다.

---

## Step 4 - 영상과 클립 검토

**순서 고정**: 시드 스틸 생성 → leg별 **시작/끝 이미지 지정** → 영상 생성. 각 leg의 프롬프트는 **회전(rotation)+줌인(zoom-in)** dive-in 모션으로 3D감을 명시한다(기본 CAMERA_FEEL "잔잔한 전진 활공"과 함께).

연속성은 **forward-chaining** 으로 만든다. 직전 클립의 **실제 마지막 프레임을 톤 변형 없이 그대로** 다음 클립의 첫 프레임으로 넣는다.

- `media.generate_video` 호출 시 `prompt`에 `{kind: "image", value: "<시작 프레임 경로>"}`를 먼저 두고, `{kind: "text", value: "<leg 프롬프트>"}`를 잇는다.
- 시작 프레임 추출: `ffmpeg -sseof -0.15 -i dive-i.mp4 -frames:v 1 -q:v 2 last-i.png`
- 각 leg 렌더 직후, 다음 leg 전에 마지막 프레임을 확인한다. 잔잔한 전진 활공 컷이 아니면 그 leg 를 재생성한다.
- 포스터: 씬 1 = 씬 1 스틸, 씬 i>=2 = 첫 프레임 추출(로딩 시 플래시 없음).
- `intro.json` 의 `connectors` 를 전부 `null` 로 두면 엔진이 인접 dive 를 직접 crossfade 한다.

### 클립 공통

- **클립 검토**: `curate-input.json` 을 `"stage": "clips"` 로 다시 쓴다. 테이크마다 클립 파일, 프롬프트, 길이를 적고 같은 검토 페이지로 판정받는다(클립은 무음 반복 재생된다). 재생성은 지적받은 클립만 한다.
- **영상 생성 비가용 폴백(로컬 렌더)** - media 파이프라인이 막히면 ffmpeg 로컬 렌더로 대체한다. 시작 프레임=시드 스틸, 끝 프레임=줌인+회전된 시드(`zoompan` z 1→1.28 + `rotate` ±0.045rad 사인 스웨이). 시작/끝 지정→영상 생성 순서는 동일하게 지킨다.
- 클립 해상도가 들쭉날쭉하면 `concatClips` 와 엔진이 크기를 맞춘다. 가급적 ORIENTATION 으로 통일한다.

---

## Step 5 - 조립과 미리보기 (무료)

씬, 커넥터, 테마를 `intro.json` 매니페스트로 적고(`assemble.mjs` 헤더에 형식), 조립한 뒤 서빙한다.
카피(`eyebrow`, `title`, `body`, `tags`)와 `theme`, 그리고 선택 항목을 채운다.

| 매니페스트 항목 | 쓰임 |
|---|---|
| `lang` | `<html lang>` |
| `panel: "glass"` | 흐린 유리 문구 패널. 기본값(알파 .36, 흰 글자)은 어두운 장면용이다. 밝은 장면은 `--intro-panel-alpha` 를 .6 이상으로 올리고 Step 6 대비로 확인한다 |
| `stepNav: { "end": "#main" }` | 장면 단위 이동. `end` 는 기존 사이트의 본문 시작(단독 페이지면 생략). 나머지 옵션은 `step-nav.js` 머리말 |

```bash
node references/assemble.mjs <projectDir>                    # <projectDir>/site 에 페이지를 만들고 styleHash 를 알린다
node references/serve.mjs <projectDir>/site                  # PREVIEW http://localhost:<port>/ (백그라운드)
node references/serve.mjs --stop <projectDir>/site           # 끝나면 종료
```
- 장시간 서버는 `muse.exec`의 background 모드로 띄우고 `process.list`/`process.log`로 관리한다. 서버 URL은 사용자에게 안내하고 사용자가 직접 브라우저에서 확인한다(아티팩트 생성 안 함).
- 조립은 벤더링된 `scrub-engine.js`를 `mountScrollWorld` config(`sections`/`connectors`/다크 테마 토큰)로 배선한다 — 직접 만든 스크롤 스크립트로 대체 금지.
- 클립 인코딩: native 해상도, crf 20, `-g 8`, `+faststart`, 무음(`-an`). 엔진이 blob-seek라 Range 미지원 호스트에서도 스크럽된다.
- `serve.mjs`는 mp4를 HTTP Range(206)로 서빙해 스크럽을 매끄럽게 하고, 포트를 자동 잡아 `port.txt`에 기록한다.
- 사이트에 CSP 가 있으면 처음부터 `--csp "<운영 정책>"`(정책을 모르면 `--csp strict`)을 붙여 띄운다.
- 페이지에는 인라인 script, style 이 없다. 설정은 `intro.js`, 테마는 `theme.css`, 엔진 CSS 는 `scrub-engine.css` 다.
- 엔진은 클립을 `fetch` 로 받아 `blob:` 으로 재생한다. CSP 에 `connect-src 'self'`(클립을 다른 출처에서 받으면 그 출처)와 `media-src 'self' blob:` 이 필요하다.
- `intro-fixes.css` 는 항상 붙는다.
- 기존 사이트에 붙이는 미리보기는 반드시 운영과 같은 CSP 헤더로 서빙한다.
- 상태 파일은 `serve.mjs` 가 서빙 폴더 밖(`<site>.server.json`)에, `curate.mjs` 가 프로젝트 폴더(`curate.server.json`)에 둔다. 두 서버 모두 Host 가 localhost 나 IP 주소가 아니면 거절한다(DNS 재바인딩 방지). 종료는 `--stop` 으로 한다.
- 휴대폰 실기기로 볼 때만 `PREVIEW_HOST=0.0.0.0` 을 쓴다. 같은 네트워크에 미공개 산출물이 보인다는 경고가 나온다.
- 사용자 검토를 받는다. 지적이 있으면 카피, 매니페스트, 해당 클립만 고치고 다시 조립한다.

---

## Step 6 - 독립 검증 (무료, 필수)

작성자와 다른 주체가 측정해 판정한다. 쓰기 도구 없는 별도 서브에이전트(검증자)가 맡는다.

```bash
node references/verify-intro.mjs http://localhost:<port>/ --out <projectDir>/verify.json [--header "<사이트 헤더 선택자>"]
```

- 화면 크기마다 새 브라우저 컨텍스트로 잰다. 기본 화면은 1280x800, 1920x1080, 860x900, 390x844 터치, 375x667 터치, 844x390 터치(가로로 든 휴대폰)다.
- 장면마다 패널이 화면 안, 헤더 아래에 있는지, 안내, 건너뛰기, 버튼, 장면 점과 겹치지 않는지, 가로 넘침, 콘솔 오류, 글자 줄 단위 대비(4.5 이상)를 잰다.
- 눈으로 볼 항목은 `references/verify.md` 에 있다.
- 실패가 0 이고 검증자가 APPROVE 해야 Step 7 이나 완료 보고로 간다. 실패가 있으면 고친 뒤 같은 검증자로 다시 잰다.

---

## Step 7 - 통합과 배포 (요청 시에만)

사용자가 기존 사이트 통합이나 배포를 요청했을 때만 한다.

- 백업을 먼저 한다. 백업은 프로젝트의 `backup/` 아래에 둔다. `/tmp` 는 쓰지 않는다.
- `site/` 의 파일을 사이트의 정적 폴더로 옮긴다. `#world` 를 본문 위에 두고, `stepNav.end` 는 본문 시작 요소를 가리킨다.
- 사이트 CSP 에 `connect-src 'self'`, `media-src 'self' blob:`, `style-src` 의 `styleHash` 를 더한다. `scrub-engine.LICENSE.txt`(엔진의 MIT 고지)도 함께 옮긴다.
- 배포 뒤 운영 주소에 `verify-intro.mjs` 를 다시 돌려 결과를 대조해 보고한다.

---

## Step 8 - 정리와 완료 보고

- 서버를 모두 끈다: `curate.mjs --stop <projectDir>`, `serve.mjs --stop <projectDir>/site`. 상태 파일이 남지 않았는지, 포트가 닫혔는지 확인한다.
- 검토 페이지 입력, 임시 캡처처럼 산출물이 아닌 파일은 사용자에게 목록을 보이고 지운다. `decisions.json` 과 탈락 폴더는 기록이라 남긴다.

보고 항목

- 산출물 경로(`site/index.html`)와 프리뷰 URL(포트, 이미 종료했으면 그 사실).
- 씬 수, `seconds`, ORIENTATION, 사용한 스틸/클립 프롬프트 요약.
- 생성 횟수(이미지 n장, 영상 n개 — 4장/6클립 제한 기준).
- 독립 검증 결과(화면 크기별 실패 수, 판정).
- 이음매 품질은 **정직하게** 쓴다. 과장하지 않는다.
  - chain: **near-seamless** 하되 **경미한 톤/디테일 drift** 가 있을 수 있다.
  - 수용 기준은 조립, 서빙된 페이지의 실제 스크럽 경험이다.
- 재생성한 스틸이나 클립이 있으면 그 사유.

## 흔한 함정

- 엄격한 CSP: 엔진이 `<style>` 을 주입하고 클립을 `fetch` 해 `blob:` 으로 재생한다. 조립 결과와 `styleHash`, `connect-src 'self'`, `media-src 'self' blob:` 로 해결한다.
- 로컬 검증은 운영과 같은 CSP 헤더를 붙인 서버로 한다.
- 재빌드 뒤 브라우저 자동화는 새 컨텍스트로 한다.
- 엔진의 `html,body{overflow-x:hidden}` 이 고정 헤더를 깬다. `intro-fixes.css` 가 `clip` 으로 바꾼다.
- 위치 비교는 소수점이 어긋난다(81.3 대 81). 1px 여유를 둔다.
- 움직임 줄이기 설정에서는 엔진이 클립을 받지 않는다.
- 엔진은 높이가 낮은 화면을 고려하지 않는다. `intro-fixes.css` 가 860px 이하에서 문구를 올리고, 높이 500px 이하의 가로 화면에서는 두 단으로 나눈다.
- 엔진의 주 버튼과 상단 CTA 는 글자가 흰색이고 배경이 테마의 글자색이다. 어두운 테마에서는 `intro-fixes.css` 가 글자를 테마 배경색으로 바꾼다.

## Operating Rules

- **생성 차단선 엄수**: Step 2 계획 승인 전에는 스틸을 만들지 않고, Step 3 모든 장면 스틸 승인 전에는 클립을 만들지 않는다
- media 파이프라인 제약: 이미지 한 응답 4회, 영상 한 메시지 6개 — 초과분은 다음 응답/메시지로 나눈다
- 벤더링본(엔진·템플릿) 수정 금지. `azure-adapter.mjs`·`video-pool.mjs`는 레거시라 사용하지 않는다
- 직접 스크롤 스크립트 작성 금지 — 벤더링된 `scrub-engine.js`를 `mountScrollWorld`로 그대로 쓴다
- 큐레이션·프리뷰 서버는 background exec + `process` 도구로 관리. 서버 URL은 사용자에게 안내하고 사용자가 직접 브라우저에서 확인
- 이 스킬에서 직접 파일 편집(`muse.edit`)이 필요하면 사용자 확인 후 수행 — 프로젝트 파일은 사용자 소유

---

관련 스킬: scroll-world — 동일 업스트림(oso95/scroll-world)의 원본 스킬
