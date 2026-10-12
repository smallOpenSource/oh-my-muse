---
name: scroll-world
description: "스크롤-스크럽 'fly through the world' 랜딩 페이지 제작. media.generate_image로 씬 스틸을, media.generate_video(시작 프레임 지정)로 dive-in/connector 클립을 만들고(외부 API·키 불필요), 벤더링 scrub-engine.js를 mountScrollWorld로 배선. 인터뷰 → 승인 게이트 → 씬 스틸 → 클립 → 스크롤 배선. 사용자가 'scroll-world 해줘'/'스크롤 fly-through'/'3D 월드'/'다이오라마 랜딩'이라고 요청하면 사용."
---

# scroll-world — 스크롤-스크럽 "fly through the world" 랜딩 페이지

## Purpose
- 스크롤이 카메라를 움직이는 랜딩 페이지: 각 씬 밖에서 안으로 다이빙 → 다음 씬으로 이어지는 연속 비행, 컷 없음. 미리 렌더링된 영상을 스크롤 위치로 스크럽하는 방식(Apple 스크롤 제품 페이지와 같은 기법)
- 씬 스틸 = `media.generate_image`, 비디오 체인 = `media.generate_video`(시작 프레임 이미지 입력 지원). **외부 이미지·영상 API, 키, 크레덴셜이 전혀 필요 없다.**
- 페이지 배선 = 벤더링된 `references/scrub-engine.js`를 `mountScrollWorld` config로 구동 — 스크롤 스크립트 직접 작성 금지(blob-seek·심 크로스페이드·route rail·linger가 핵심)
- **결정적 규칙: seam(클립 경계)은 반드시 frame-identical.** 어느 커넥터도 렌더링 전에 Step 5의 seam법을 먼저 읽는다. 제일 흔한 실패 = 눈에 보이는 "팝" 발생
- 답변은 한글(기술 토큰·명령어·경로는 영문)

## media 파이프라인 제약 (반드시 지킨다)

- `media.generate_image`: 한 응답에서 **최대 4회** 호출. 씬이 많으면 여러 응답에 나눠 생성한다.
- `media.generate_video`: 한 사용자 메시지에서 **최대 6개** (성공 기준). 초과분은 메시지를 나눠 요청받는다.
- 영상은 **시작 프레임만 지정 가능**(`kind: image`), 끝 프레임 지정은 미지원 — 커넥터는 시작 프레임 체인 + 엔진 크로스페이드로 처리한다(Step 5).
- 생성된 파일은 `output_dir`로 프로젝트 폴더를 지정해 둔다.

## Step 0 — 부트스트랩 (무료 · 차단선)
1. **ffmpeg / ffprobe** — `$PATH`에 없으면 설치 안내 후 **중단**
2. media 파이프라인은 별도 설치·크레덴셜 없이 바로 쓸 수 있다.
3. (선택) 배경 제거용 이미지 도구: PIL / `cwebp` — Step 3 참고

## Step 1 — 인터뷰 (무료)
주제는 사용자가 직접 정한다 — **오픈 질문으로 묻는다**, 가상 선택지 제시 금지. `references/prompts.md` 인테이크 체크리스트 참조.
- **Subject** — 이 월드 주제(사용자 사업/고객/자유 아이디어) + 한 줄 피치 + 브랜드명(없으면 제안)
- **Brand kit** — 사용자가 팔레트+명칭+톤 직접 전달, 또는 에이전트가 제안하고 승인. **hex 4–6개** + 명칭 + 톤 단어 1–2개
- **Art direction** — 기본 "soft matte low-poly **clay diorama**, isometric, tilt-shift miniature, warm light". 대안(flat papercraft, glossy toy, claymation, neon night). 선택 결과는 **모든 씬 프롬프트에 글자 그대로 동일**하게 재사용되는 스타일 서문(=월드 응집력의 핵심)
- **Camera style — 반드시 묻는다.** Step 4 아키텍처 선택을 결정:
  - **Fly through the world** (기본·미니어처/다이오라마 추천): 씬마다 다이빙 → 밖으로 빠져나와 다음 섬으로 호핑 → 아키텍처 B
  - **One continuous walkthrough** (그라운드/포토리얼 추천): 뒤로 당김 없이 한 번의 전진 비행 → 아키텍처 A
  - **Locked isometric glide**: 각도 고정, 월드가 지나감. 가장 차분 → A + locked-iso leg
- **Journey(섹션)** — 주제의 가치 사슬에서 도출해 제안하고 사용자가 편집. 5–7개가 무난. 각 섹션: 디오라마 내용 설명 + eyebrow + headline + body 1줄 + 태그 0–3개. 마지막 = 히어로 제품 + CTA
- **Mobile — 반드시 묻는다, 절대 자동 생성 금지.** "모바일 버전도? 네이티브 **9:16** 포트레이트로 두 번째 체인을 별도 렌더 — 생성 횟수 약 2배". Yes면 portrait 체인 + `clipMobile`/`connectorsMobile`/`stillMobile` 배선 + 모바일 QA 전체. No면 스킵
- **승인 게이트**: 렌더 전에 계획(씬 목록·프롬프트·생성 횟수)을 보여 주고 명시적 승인을 받는다. **승인 전 렌더 금지**

## Step 2 — 씬 스틸 (승인 이후에만)
- 섹션당 1장, 전부 **같은 스타일 서문**. `media.generate_image`로 생성 (한 응답 4회 제한 — 나눠서).
- 프롬프트 형: `<STYLE PREAMBLE, 매번 동일>. On a plain solid <bg> background with a soft contact shadow. <PALETTE hexes>. No text, no letters, no logos, centered, 3:2. Subject: <이 디오라마 내용>`
- **스틸 응집도 검토 후 진행**(같은 앵글·팔레트·빛). 어긋나면 재생성

## Step 3 — (선택) 씬 띄우기
- 단색 박스가 아니라 배경 위를 떠다니게 하고 싶으면 `references/knockout.py`(border-connected flood fill)로 투명화 후 webp 인코딩. 단순하게 가려면 페이지 배경을 씬 배경색과 맞추고 스킵
- 스틸은 **비디오 포스터·지연 로드 폴백**으로도 쓰이니 보관

## Step 4 — 카메라 아키텍처 (Step 1의 CAMERA 선택을 구현)
- **A) Continuous forward take**(그라운드/워크스루 추천): leg를 **순차** 생성. leg 0 = 씬 0 스틸에서 전진 활공. 이후 leg의 시작 프레임 = **이전 leg의 실제 마지막 프레임**(ffmpeg 추출). 커넥터 없음(Step 5 스킵) — leg가 곧 여정
- **B) Dive-in + aerial connector**(디오라마/미니어처 전용): 씬당 다이빙 클립 + Step 5 커넥터(위로 빠져나와 다음 씬 상공으로)
- **Camera grammar**(mid-leg 무브는 컨셉에서 선택, 심에서는 전진만): 심 연속성은 프레임 핸드오프(위치) + 심에서의 속도 연속성(역전 금지)으로 담보. leg는 **항상 느린 전진 drift로 시작하고**, **마지막 ~1초를 같은 전진 drift로 정착**시켜 끝낸다(프롬프트에 두 절 그대로 유지)
- **B의 다이빙** — 씬당 1회: 밖/위에서 시작 → 내부로 하강. 시작 프레임 = **단색 배경 스틸**. 프롬프트: "Single continuous cinematic camera move, no cuts. Begin high and far looking at the whole <scene> from outside … descend and fly inside toward <focal point> … <style>, smooth graceful slow motion. No text."
- 방문자는 스크롤을 **위로도** 올리므로 모든 무브는 역재생도 된다 — 양방향에서 심 속도가 일관돼야 함

## Step 5 — 커넥터 (아키텍처 B 전용 · 심리스 체인의 핵심)
- 아키텍처 A는 스킵(leg 자체가 체인)
- 커넥터 = 씬 i 끝 → 밖으로 빠져나와 → 씬 i+1 시작. **시작점은 반드시 이웃 클립의 실제 렌더링 프레임 — 디오라마 스틸 절대 아님**
  - 이유: 매 생성은 미세하게 다르게 렌더. 정확한 픽셀 핸드오프가 해결책:
    ```
    connector_i start-image = dive_i의 LAST 프레임 (ffmpeg 추출)
    ```
  - media 파이프라인은 끝 프레임 지정을 지원하지 않으므로, 커넥터의 착륙점은 프롬프트("arrive above <scene i+1>, beginning to descend")로 유도하고, 엔진의 **짧은 크로스페이드**(수 프레임)가 잔차를 흡수한다. **실제 프레임 핸드오프가 본체, 크로스페이드는 보조**
  - 추출: `ffmpeg -sseof -0.15 -i dive_i.mp4 -frames:v 1 -q:v 2 dive_i_last.png`
- 커넥터 프롬프트: "Single continuous camera move, no cuts. Pull up and back out of <scene i>, rise into the sky, glide across the connected miniature world, and arrive above <scene i+1>, beginning to descend toward it. Seamless flowing aerial transition. <style>. No text."

## Step 6 — 스크럽용 인코딩
- 핵심: **seek 가능성**. 정적 호스트가 HTTP byte-range를 안 서빙하면 seek가 프레임 0에 고정된다 → **클립을 Blob으로 fetch해 in-memory object URL로 재생**(blob은 항상 fully seekable). 엔진이 이렇게 한다
- **seek 부드럽게 하려고 화질을 희생하지 말 것**: 네이티브 해상도, crf ~20, **작은 GOP(`-g 8`)**, 오디오 제거, faststart, 가벼운 `unsharp`:
  ```bash
  ffmpeg -i src.mp4 -an -vf "unsharp=5:5:0.8:5:5:0.0" \
    -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p \
    -g 8 -keyint_min 8 -sc_threshold 0 -movflags +faststart out.mp4
  ```
- **모바일 인코딩(Step 1에서 opt-in한 경우만)**: 네이티브 9:16 체인의 `-m.mp4` — `scale=720:-2`, `-g 4`, crf 23

## Step 7 — 페이지 조립
- `references/scrub-engine.js`(+ 완전 standalone이면 `references/index-template.html`)를 사용자 프로젝트로 복사하거나 프레임워크에 어댑트. config-driven 바닐라 JS:
  ```js
  mountScrollWorld(document.getElementById('world'), {
    brand: { name: 'Pearl & Co.' },
    diveScroll: 1.3, connScroll: 0.9,
    sections: [
      { id:'farm', label:'The Farms', still:'assets/farm.webp',
        clip:'assets/vid/farm.mp4',
        clipMobile:'assets/vid/farm-m.mp4',
        stillMobile:'assets/farm-m.webp',
        scroll: 1.6, linger: 0.45,
        accent:'#8FB98A', eyebrow:'From leaf to last sip', title:'It starts in the hills.',
        body:'…', tags:['Single-origin','Hand-picked'] },
    ],
    connectors:       ['assets/vid/conn1.mp4', …],
    connectorsMobile: ['assets/vid/conn1-m.mp4', …],
  });
  ```
- 엔진 담당: 다이빙/커넥터 순서 체인, rAF 스무딩 스크럽, blob 로딩, frame-matched crossfade, 섹션별 고정 카피, route rail, `prefers-reduced-motion`, 폰 하드닝
- 테마는 CSS 변수(`--sw-bg`, `--sw-ink`, `--sw-accent`, `--sw-font-*`)

## Step 8 — 심 QA (생략 금지)
- 헤드리스 브라우저로 구동, **심 연속성 검증**:
  - 각 심 바로 전/후 스크롤 위치에서 스크린샷 — 두 프레임이 near-identical이어야 함. 팝이면: 스틸을 핸드오프로 썼거나(Step 5 재수행) 크로스페이드 밴드가 짧음
  - 콘솔 에러 확인, `video.seekable.end(0) > 0`(blob 동작), `currentTime`이 스크롤을 따라가는지
- reduced-motion: 스틸만, 비디오·파티클 없음

## Gotchas (실전 교훈)
- **심 팝** → 디오라마 스틸을 핸드오프로 씀. 항상 실제 렌더링 프레임(Step 5)
- **심 stutter/역재생감** → 심에서 카메라 속도가 역전. grounded walkthrough는 아키텍처 A
- **얼어붙은 비디오(frame 0 고정)** → 호스트가 byte-range 미지원. blob URL(엔진 내장)
- **파일 거대** → `-g 8` + blob (all-intra 금지)
- **소프트/저화질** → 네이티브+crf≤20+`unsharp`
- **다크/커스텀 테마** → 페이지 `:root`/`.sw-root`에 `--sw-bg`·`--sw-ink`·`--sw-accent`·`--sw-font-*` 설정
- **폰에서 빠른 flick 시 프리징** → `-m.mp4`(720p, `-g 4`) + `clipMobile` 배선
- **iOS 블랭크** → 엔진의 포스터 유지+priming을 건드리지 말 것(`playsinline`/`muted` 제거 금지)
- **노치/URL-bar에 가려진 카피** → `env(safe-area-inset-bottom)` + `dvh`, `viewport-fit=cover`

## References
- `references/prompts.md` — 인테이크 체크리스트·스타일 서문 패턴·전 프롬프트 템플릿
- `references/scrub-engine.js` — 벤더링된 포터블 스크럽 엔진. **수정 금지**
- `references/index-template.html` — 엔진을 마운트하는 최소 standalone 페이지
- `references/knockout.py` — 플로팅 씬용 배경 제거
- `references/NOTICE.md` — 벤더링 출처 표기

---

관련 스킬: 3d-intro-build — 같은 계열의 media 파이프라인 적응판 (상호 크로스레퍼런스)
