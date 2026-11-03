---
name: ship-video
description: "URL이나 프롬프트를 받아 20-40초 런치 영상을 만든다. 영상 모델 없이 HTML 필름 한 장을 쓰고, 가상 시계 아래 headless Chromium으로 프레임 단위 렌더링한 뒤 ffmpeg으로 MP4 인코딩한다. OpenComputer 계정 없이 로컬 Playwright와 ffmpeg으로 동작하고, Muse 전용이다. '/ship-video'/'런치 영상'/'ship-video' 시 사용."
argument-hint: "<URL 또는 프롬프트>"
---

# ship-video - URL이나 프롬프트로 런치 영상 만들기

`/ship-video` 로 부른다. URL 하나나 자유 프롬프트를 받아 20-40초짜리 런치 영상을 만든다. 영상 모델을 쓰지 않는다. 필름은 HTML 문서 한 장으로 쓰고, 가상 시계 아래 headless Chromium이 프레임 단위로 그린 뒤 ffmpeg이 MP4로 묶는다.

원본은 diggerhq/shipvideo(LaunchVideo)의 동작 방식이다. 원본은 OpenComputer 에이전트와 Opus 모델을 전제로 하지만, 이 스킬은 그 전제를 빼고 Muse 환경에 맞게 새로 썼다. 원본 문구와 원본 코드를 복사하지 않았다. 원본 저장소에는 LICENSE 파일이 없어, 동작 원리만 내 말로 기술하고 스크립트도 새로 구현했다.

## Muse 환경 적응

- 모델은 Muse 백본만 쓴다. 외부 모델 호출은 없다.
- OpenComputer 계정, CLI, 세션 공유 작업공간은 쓰지 않는다. 로컬 Playwright와 ffmpeg으로 렌더링한다.
- 영상 생성 모델(media.generate_video 등)은 쓰지 않는다. 이 스킬은 그 경로와 무관하게 동작한다.
- 출력은 프로젝트 폴더의 `videos/<job>.mp4` 이다. 서명 다운로드 링크는 없다. 완성본은 파일 첨부로 인도한다.
- 가상 시계는 `scripts/check_scene.py` 와 `scripts/render_video.py` 가 구현한다. 두 스크립트 모두 `__seek(t)` 계약을 따른다.
- 답변은 한글로 한다. 필름 안의 문구는 브리프 언어(또는 원문 페이지 언어)를 따른다.

## 무엇을 만드는가

- 입력: URL 1개 또는 자유 프롬프트.
- 출력: 20-40초 MP4, 1920x1080, 24 또는 30fps, H.264(yuv420p, faststart).
- 비트: 6-10개. 비트당 2-5초. 비트 사이는 깔끔한 컷.
- 타이포 우선: 큰 단어가 무게 있게 착지하고 문장으로 수렴한다. 한 화면에 단어 8개 이하.
- 메커니즘을 보여준다: div, SVG, canvas로 만든 토큰 흐름, 상자를 통과하는 요청, 오르는 카운터, 채워지는 막대, 해결되는 diff, 한 줄씩 나타나는 채팅. 스톡 이미지 느낌은 피한다.
- 리듬: 문제는 빠르게, 이름 앞에서는 숨 고르기, 결말은 자신 있게 유지한다. 입장은 ease-out 계열, 퇴장은 ease-in으로 완화한다. 마지막 프레임은 2초 유지한다.
- 구성: (1) 고통이나 약속으로 여는 훅 2-3비트, (2) 제품 이름 공개, (3) 동작 원리 3비트(비트마다 구체적 시각 1개), (4) 출처가 준 경우에만 증명과 숫자(숫자 지어내기 금지), (5) 엔드 카드: 이름, 한 줄 태그라인, URL 또는 CTA.
- 타이포: 기하학 또는 그로테스크 표시 서체(Inter, Space Grotesk, Manrope, Sora, Syne)와 선택적 세리프 액센트(Instrument Serif, Fraunces) 또는 모노 라벨(JetBrains Mono, IBM Plex Mono). Google Fonts를 `<link>` 로 로딩한다. 표시 크기 자간은 -0.03em에서 -0.05em.
- 색: 비트마다 굵은 배경색 1개, 필름 전체에서 최대 2개, 나머지는 near-black과 near-white. URL 모드에서는 사이트 색을 가져오고, 없으면 자신 있는 팔레트를 고른다. 대비는 높게 잡고, 휴대폰 재생을 전제한다.
- 편집 프레임(권장): 모노 코너 라벨(프로젝트명, 비트 번호, 실제로 세는 타임코드)과 하단 진행 헤어라인.

## 렌더러 계약 (반드시 지킨다)

- 완전한 HTML 문서 1개, 1920x1080. body는 `margin:0; width:1920px; height:1080px; overflow:hidden; position:relative` 로 둔다.
- 시간은 가상 시간뿐이다. 프레임 요청 시에만 시계가 간다. 안무는 다음 둘 중 하나로 짠다. (a) `animation-delay` 와 `animation-fill-mode: both` 를 갖춘 CSS `@keyframes` (요소마다 애니메이션 1개). (b) rAF 인자 t(시작 후 밀리초)를 타임라인으로 쓰는 단일 rAF 루프. 둘을 한 문서에 섞어도 된다. CSS transition 금지, 타이머로 클래스를 토글해 애니메이션을 시작하는 방식 금지, 상태 도출에 Date나 performance.now 사용 금지(rAF t를 쓴다).
- 결정성만 허용한다. Math.random 금지(노이즈가 필요하면 작은 시드 PRNG를 직접 쓴다). `<video>`, `<audio>`, `<iframe>` 금지. 외부 이미지와 외부 스크립트 금지. 인라인 SVG와 canvas는 된다. Google Fonts는 된다.
- 화면을 떠나는 요소는 반드시 퇴장 애니메이션(opacity 0과 fill-mode)으로 보내거나 다음 비트의 풀블리드 배경으로 가린다. 이전 비트 잔상을 남기지 않는다.
- 파일은 60KB 이하를 권장한다. 거대한 스크립트 1개보다 작은 요소 여럿을 선호한다.

## 절차

1. 주제 파악. URL 모드: 페이지를 가져와 제목, 설명, 헤딩(h1-h3), 많이 쓴 hex 색, Google Fonts를 추출한다. 페이지가 얇으면 /docs, /pricing, /about 중 1개를 더 가져온다. 제품명, 한 줄 가치 제안, 구체적 기능 3개, 실제 숫자, 브랜드 색과 폰트를 뽑는다. 프롬프트 모드: 이름과 팔레트가 없으면 취향 있게 지어내고, 구체적 숫자는 주장하지 않는다.
2. 숏 리스트를 먼저 정한다: 비트, 초, 화면 문구, 시각. 그 뒤 HTML 전체를 쓴다.
3. `scripts/check_scene.py` 로 필름 곳곳의 타임스탬프를 검사한다. 보고된 오류와 잘못된 가시 텍스트(이전 비트 잔상, 빈 화면 비트)를 전부 고치고, 깨끗해질 때까지 반복한다.
4. 깨끗해지면 `scripts/render_video.py` 로 한 번만 렌더링한다. 길이, fps, jobId(짧은 이름)를 인자로 준다.
5. 인도: MP4 경로를 단독 행으로 적고, 그 뒤에 영상이 말하는 내용을 한 문장으로 적는다. 그 외는 없다. 렌더가 두 번 실패하면 실패 내용을 평이하게 말한다.
- 무인 동작이 원칙이다. 묻지 않고, 합리적으로 선택하고, 끝까지 마친다. 다만 외부 발송, 게시, 구매 같은 외부 동작은 이 스킬 범위가 아니며 별도 승인이 필요하다.

## 스크립트

- `scripts/check_scene.py <html> <duration> [timestamps...]`: 가상 시계 아래 문서를 로딩하고, 지정 초마다 JS 오류, 실패 요청, 가시 텍스트, body 배경을 보고한다. 타임스탬프를 주지 않으면 3초 간격으로 검사한다. 오류가 있으면 종료 코드 1로 끝난다. 렌더 전에 반드시 실행한다.
- `scripts/render_video.py <html> <duration> <fps> <out.mp4>`: 프레임을 JPEG 파이프로 ffmpeg에 넣어 libx264(medium, crf 18, yuv420p, faststart) MP4를 만든다. 30초 30fps 렌더는 30-40초가 걸린다. 긴 렌더는 백그라운드 실행을 쓴다.
- 전제조건: Python 3, Playwright, Chromium, ffmpeg. Chromium 실행 파일은 `PLAYWRIGHT_CHROMIUM_PATH` 환경 변수로 지정할 수 있고, 없으면 Playwright 번들 Chromium을 쓴다.
- 검증: HTML 200자 이상, 완전한 문서(`<html>` 과 `<body>` 포함), `<video>`, `<audio>`, `<iframe>` 포함 시 거부한다. 길이 3-90초, fps 24 또는 30.

## 갱신과 제거

- 원본: https://github.com/diggerhq/shipvideo
- 원본 갱신이 있으면 위 절차와 렌더러 계약을 원본과 대조하고, 바뀐 동작만 이 스킬에 반영한다. 원본 문구와 원본 코드를 베끼지 않는다.
