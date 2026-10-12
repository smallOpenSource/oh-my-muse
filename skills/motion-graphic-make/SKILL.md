---
name: motion-graphic-make
description: "10초 내외 내레이션 없는 모션 그래픽(킨네틱 타이포·통계·차트·로고·하단자막·지도)을 만듦. 텍스트 정밀형은 로컬 HTML+CSS → headless 캡처 → ffmpeg 인코딩, 시네마틱형은 media.generate_video. 배경음악+효과음 포함(무음 금지). 사용자가 '모션 그래픽 만들어줘'/'모션 그래픽 제작'/'motion graphics'라고 요청하면 사용."
---

# motion-graphic-make — 모션 그래픽 제작 (내장 파이프라인)

## Purpose

짧고(약 10초 내외, 최대 ~30초) 내레이션 없는 디자인-주도 모션 그래픽을 만든다.
렌더 경로는 둘이다. 텍스트 정확도가 생명인 것(킨네틱 타이포·차트·자막)은 **로컬 HTML+CSS 애니메이션 → headless Chromium 캡처 → ffmpeg 인코딩**으로 결정론적으로 만든다.
배경·분위기 같은 시네마틱 요소는 **`media.generate_video`** 로 만든다. 전제조건(ffmpeg·Chromium) 설치는 `motion-graphic-setup` 스킬이 담당한다.
답변은 한글(기술 토큰 영문).
- **무음 금지** — 배경음악(BGM)+효과음(SFX)을 반드시 포함한다. 외부 모델·다운로드 없이 ffmpeg 로컬 신스로 만든다.

## Workflow

### 0. 전제조건 확인

진행 전 가용성을 먼저 확인하고, 문제가 있으면 **설치부터 안내**한다(추정·임의 재설치 금지):

- `command -v ffmpeg`, headless Chromium(`setup-playwright`로 준비)
- 미확보면 `motion-graphic-setup` 스킬로 설치. 설치·검증 후 이 스킬을 이어서 진행한다.

### 폼 카테고리

| 카테고리 | 내용 | 권장 경로 |
|---|---|---|
| `kinetic-type` | 문구/제목의 모션 타이포그래피 | 로컬 HTML (텍스트 정확) |
| `stat` | 히어로 숫자 카운트업 + 링 | 로컬 HTML |
| `charts` | 막대/선/원형/레이스 차트 | 로컬 HTML |
| `logo-reveal` | 로고 스팅 / 브랜드 락업 | 로컬 HTML 또는 시네마틱 |
| `lower-thirds` | 이름/직함 바, 콜아웃, 소셜 오버레이 | 로컬 HTML |
| `maps` | 지역 하이라이트 · 지점 연결 · 위치 줌 | 시네마틱 + 로컬 오버레이 |

### 이 스킬이 소유하는 것과 소유하지 않는 것

**렌더 경로 A (로컬, 텍스트 정밀형)**: HTML/CSS 애니메이션 작성 → headless Chromium 캡처 → ffmpeg 인코딩. 한글 텍스트가 깨지지 않고, 타이밍이 결정론적이다.
**렌더 경로 B (시네마틱형)**: `media.generate_video`로 배경·전환 클립 생성 (한 메시지 6개 제한 — 초과분은 나눠서).

이 스킬의 역할은 **호출 · 전제조건 확인 · 렌더 승인 게이트 강제**다.

이 스킬이 추가로 소유하는 것:

| 소유 | 내용 |
|---|---|
| 단계 관문 | 계획 승인, 스냅숏 판정, 렌더 승인과 판정, 독립 검증 |
| 검토 페이지 | `references/curate.mjs` — 산출물마다 카드 하나, 그 옆에 구성 지시문 |
| 미리보기 서버 | `references/serve.mjs`, `references/preview-lib.mjs` — 빈 포트, 127.0.0.1, 상태 파일, `--stop`, CSP 헤더 |

검토 페이지와 서버는 `3d-intro-build`와 같은 파일이다(바이트 단위로 동일하게 유지).

### 원칙

- 산출물(스냅숏, 렌더)은 그것을 만든 구성 지시문과 나란히 보여 준다. 결과만 보여 주지 않는다.
- 단계마다 멈추고 판정을 받는다. 판정 없이 다음 단계로 가지 않는다.
- 미리보기 서버는 그때그때 빈 포트로 띄우고, 끝나면 `--stop`으로 끈다. 기본 바인드는 `127.0.0.1`이다.
- 커밋, push, 배포는 사용자가 요청할 때만 한다.

### 흐름

1. **plan** — 사용자 요청(브리프)을 받아 카테고리를 정하고 렌더 경로(A/B/혼합)를 고른다. 계획(전할 메시지, 길이, 장면 구성, 색과 글꼴, 경로 선택 이유)을 사용자에게 보여 주고 승인받는다. 승인 전에는 build로 가지 않는다.
2. **build** —
   - 경로 A: 컴포지션 HTML을 만든다(GSAP·CSS 애니메이션). headless Chromium으로 캡처하고 ffmpeg로 인코딩한다.
   - 경로 B: `media.generate_video`로 클립을 만든다. 프롬프트는 있는 그대로 전달한다(수식어 덧씌우기 금지). `output_dir`는 프로젝트 폴더로 지정한다.
   - 혼합: B 클립을 배경으로, A 오버레이(자막·차트)를 ffmpeg로 합성한다.
3. **audio** — 배경음악(BGM)+효과음(SFX)을 넣어 무음을 금지한다. **ffmpeg 로컬 신스**로 만든다: BGM=은은한 앰비언트 패드(전체 길이, 페이드 인/아웃, 낮은 볼륨), SFX=씬 전환 지점마다 짧은 whoosh. 선언적 클립(`data-start`/`data-duration`/track)으로 배선하고(JS 트리거 없이 seek-safe), ffprobe로 길이·코덱을 검증한다.
4. **스냅숏 검토** — 주요 시점의 정지 화면을 검토 페이지에 올린다. 프로젝트 dir의 `curate-input.json`에 장면마다 그 정지 화면과 구성 지시문(장면별 문구, 타이밍, 강조 요소)을 적는다.
   ```bash
   node references/curate.mjs <projectDir>          # CURATE http://localhost:<port>/ (background exec)
   node references/curate.mjs --record <projectDir> --scene 1 --verdict regenerate --note "링을 더 굵게"
   ```
   판정은 페이지의 "판정 저장"이나 대화(`--record`)로 받아 `decisions.json`에 남긴다. 재생성 요청이 있는 장면만 고치고 다시 올린다. 전부 승인돼야 렌더로 간다.
5. **사용자 승인 게이트** — "미리보기 먼저 볼지, 바로 렌더할지" 하나만 묻는다.
6. **render** — **명시적 렌더 승인 이후에만** 실행한다. 경로 A는 최종 인코딩, 경로 B는 클립 확정(필요시 A와 합성). 렌더 파일을 `"stage": "render"`로 검토 페이지에 올려(무음 반복 재생, `seconds`에 실제 길이) 판정받는다 — 오디오 포함은 ffprobe로 별도 확인(아래 Output Contract).
7. **배치 (선택)** — 사이트에 넣을 때만 한다.
   ```bash
   node references/serve.mjs <siteDir> [--csp strict|"<운영 정책>"]   # 사이트에 CSP가 있으면 같은 헤더로
   node references/serve.mjs --stop <siteDir>
   ```
8. **독립 검증** — 작성자와 다른 검증 주체가 판정한다(별도 서브에이전트 등). 실제 길이, 주요 시점 정지 화면의 글자 깨짐과 가독성, 계획과의 일치를 본다. APPROVE해야 완료로 간다.
9. **정리** — 서버를 모두 `--stop`으로 끄고 포트가 닫혔는지 확인한다. 검토 입력과 임시 캡처는 목록을 보이고 지운다. `decisions.json`은 기록이라 남긴다. 배포는 요청받았을 때만 한다.

**렌더는 사용자의 명시적 승인 없이는 절대 실행하지 않는다** — 승인 전에는 미리보기 단계에서 멈추는 것이 기본값이다.

## Output Contract

- 렌더가 끝나면 산출물 경로, 실제 길이(duration), 사용된 렌더 경로(A/B/혼합), 확인에 쓴 스냅샷 시점, 검토 판정과 독립 검증 결과를 함께 보고한다.
- 오디오 보고: BGM 길이·볼륨, SFX 배치 시점(전환 beats). 최종 MP4에 오디오 스트림 포함을 ffprobe로 확인한다.
- 렌더 없이 미리보기에서 멈췄다면, 어디까지 진행됐고 다음에 무엇을 승인하면 렌더로 이어지는지만 짧게 보고한다.

## Operating Rules

- 렌더 승인 게이트를 우회하지 않는다. 사용자가 "바로 렌더해"라고 명시하면 그 자체가 승인이다.
- 장시간 렌더는 background exec + process 도구(`process.list`/`process.log`/`process.poll`/`process.kill`)로 돌리고, 완료를 기다리며 폴링하지 않는다.
- 경로 B의 텍스트 정확도 한계: AI 생성 영상 안의 문자는 깨질 수 있다 — 정확한 문구가 필요하면 경로 A(로컬 HTML)로 만든다. 이 한계를 사용자에게 숨기지 않는다.
