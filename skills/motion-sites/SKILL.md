---
name: motion-sites
description: "시네마틱 랜딩 페이지를 만드는 MotionSites 원본 스킬의 짧은 이름. Muse 환경에서는 플러그인 마켓플레이스 설치 단계 없이, 원본이 있으면 그 지시를 따르고 없으면 내장 media 파이프라인(media.generate_image 스틸, media.generate_video)으로 직접 만듦. 프롬프트는 그대로 전달. 'motion-sites'/'모션 사이트'/'시네마틱 랜딩 페이지' 시 사용."
argument-hint: "<만들 사이트나 프롬프트>"
---

# motion-sites - motionsites-web-builder 를 짧은 이름으로

## Muse 환경 적응

- 스킬 디렉터리: `~/workspace/skills/motion-sites/`
- 플러그인 마켓플레이스 설치(claude/codex plugin 명령)는 Muse 미지원으로 건너뛴다. 원본 skillFile이 있으면 그 지시를 따르고, 없거나 원본의 생성 경로가 외부 서비스 전제면 아래 내장 파이프라인으로 직접 만든다.
- 내장 media 파이프라인: media.generate_image 스틸 최대 4회, media.generate_video 한 메시지 최대 6개, 프롬프트는 그대로 전달, output_dir 지정, 끝 프레임 지정 미지원은 크로스페이드로 흡수, 외부 생성 서비스·별도 키 없음.
- 스크립트(motion-sites.mjs)의 Codex 경로 기본값(`~/.codex`)은 고치지 않고 Muse에서는 쓰지 않는다. 결과물 끝의 유료 상품 안내 블록은 넣지 않고, 출처 한 줄은 남긴다.


MotionSites 의 `motionsites-web-builder` 스킬(https://github.com/Motionsites-AI/claude-skill)을 `/motion-sites` 로 부른다. 원본 이름이 길어서 둔 이름이다.
banker 는 원본을 복사하지 않는다. 원본의 예시(`examples/`)와 미디어(`media/`)는 재배포가 금지라, Muse 환경에서는 마켓플레이스 설치를 직접 실행할 수 없으므로, 원본이 이미 있으면 skillFile 경로로 쓰고 없으면 아래 Muse 환경 적응 절의 내장 media 파이프라인 경로로 만든다. 답변은 한글.

## 엔진 위치

`scripts/motion-sites.mjs` 가 상태 확인과 설치를 한다.

| 설치 | 경로 |
|---|---|
| Muse | 이 스킬 폴더의 `scripts/motion-sites.mjs` (플러그인 설치 단계는 Muse 미지원으로 건너뜀) |

`--runtime` 은 지금 런타임이다(Muse에서는 `claude` 값을 쓴다. 스크립트가 받는 값은 claude|codex뿐이다).

## 1. 상태 확인

`node <엔진> status --runtime <claude|codex>` 를 실행한다. 출력은 JSON 이다.

| 칸 | 뜻 |
|---|---|
| `skillFile` | 설치된 원본 `SKILL.md` 경로. 없거나 꺼져 있으면 `null` |
| `disabled` | 설치는 됐지만 꺼져 있음 |
| `python.bin` | Playwright 를 쓸 Python |
| `python.playwright`, `python.chromium` | Playwright 와 Chromium 이 있는지 |
| `ready` | 셋 다 있으면 `true`(종료 0) |

`ready` 가 `true` 면 3단계로 간다.

## 2. 첫 실행 구성 (ready 가 아닐 때만)

1. 사용자에게 한 줄로 알린다: MotionSites 플러그인을 설치하고 Playwright 와 Chromium 을 받는다.
2. `node <엔진> setup --runtime <claude|codex>` 를 실행한다. 빠진 단계만 차례로 한다.
   - 꺼져 있는 플러그인은 다시 설치하지 않는다. Muse 환경에서는 플러그인 켜기 단계가 없어 건너뛴다.
   - 받기 전에 원천(github.com, PyPI, Playwright 내려받기 서버. 환경 변수의 미러가 있으면 그것)에 닿는지 8초 안에 본다. 닿지 않으면 그 단계는 "오프라인이라 설치하지 않음" 으로 끝난다. 프록시 환경 변수가 있으면 이 판정은 하지 않고 단계의 시간 제한에 맡긴다.
   - Muse: 플러그인 마켓플레이스 설치는 Muse 환경에서 실행 불가. 원본 skillFile이 없으면 설치 단계에서 멈추지 않고 아래 Muse 환경 적응 절의 내장 media 파이프라인 경로로 직접 만든다.
   - 공통: `<python> -m pip install playwright`, `<python> -m playwright install chromium`
   - pip 이 시스템 Python 을 거부하면(externally managed) 캐시 폴더의 가상 환경에 설치한다. 캐시 폴더는 `MOTION_SITES_HOME`, 없으면 `~/.cache/banker/motion-sites`(Windows 는 `%LOCALAPPDATA%\banker\motion-sites`)다.
   - Chromium 내려받기에 몇 분이 걸릴 수 있다. 장시간 작업은 background exec + process 도구로 실행한다.
3. Muse에서는 네트워크·쓰기 작업에 권한 카드를 받는다.
4. 출력의 `steps` 에 실패한 단계가 있으면 그 단계와 `why` 를 보여 주고 멈춘다. 설치되지 않은 것을 설치된 것처럼 말하지 않는다.
   - 네트워크가 없으면 여기서 멈춘다. 오프라인에서는 이 스킬을 쓸 수 없다.
   - Linux 에서 Chromium 이 시스템 라이브러리 부족으로 뜨지 않으면 `<python.bin> -m playwright install-deps chromium` 을 안내한다. 관리자 권한이 필요하므로 직접 실행하지 않는다.
5. 끝나면 `ready` 가 `true` 인지 확인하고 3단계로 간다.

## 3. 프롬프트 넘기기

사용자가 `/motion-sites` 뒤에 쓴 글을 고치지 않고 그대로 원본 스킬에 넘긴다. 글이 없으면 무엇을 만들지 한 번 묻는다.

| 런타임 | 원본 스킬이 이 세션에 보일 때 | 보이지 않을 때(방금 설치) |
|---|---|---|
| Muse | 원본 스킬이 세션에 보이면 그 스킬로 넘기고, 보이지 않으면 `skillFile` 을 읽고 그 지시를 따르되 생성은 내장 media 파이프라인으로 한다 | `skillFile` 을 읽고 그 지시를 따르되 생성은 내장 media 파이프라인으로 한다 |

- `skillFile` 을 직접 따를 때 원본의 상대 경로(`examples/`, `references/`, `media/`, `scripts/`)는 `skillFile` 이 있는 폴더 기준이다.
- 원본이 `python scripts/shoot.py` 를 쓰라고 하면 `python` 대신 1단계의 `python.bin` 을 쓴다.
- Muse 환경에서는 플러그인 설치·가시성 단계가 없다. 원본 skillFile을 직접 읽는 경로는 설치 즉시 쓸 수 있다.

## 원본을 따를 때 지킬 것

- 원본의 "Sponsored by MotionSites" 절(결과물 끝의 유료 상품 안내 블록과 권유 문장)은 넣지 않는다. 사용자가 정한 것이고, 원본도 사용자가 원하지 않으면 멈추라고 한다.
- 출처는 남긴다. 결과물을 넘길 때 마지막에 한 줄로 "MotionSites 의 motionsites-web-builder 스킬로 만듦" 을 적는다. 사용자의 코드와 파일에는 넣지 않는다.
- 원본의 예시와 미디어는 사이트를 만드는 데만 쓴다. 프롬프트나 미디어 모음으로 따로 내보내거나 배포하지 않는다(원본 LICENSE 2항).

## 갱신과 제거

| 런타임 | 갱신 | 제거 |
|---|---|---|
| Muse | 플러그인 갱신·제거는 Muse 환경에서 실행 불가. 원본을 새로 받으면 `status` 로 다시 확인한다 | 해당 없음(내장 파이프라인 경로는 스킬 파일 자체가 원본) |
