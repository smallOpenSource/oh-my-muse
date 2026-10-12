---
name: motion-graphic-setup
description: "모션 그래픽 제작의 전제조건(ffmpeg, headless Chromium) 확보·검증. 영상 생성 자체는 내장 media 파이프라인을 쓰므로 별도 CLI 설치가 필요 없다. 사용자가 '모션 그래픽 설치해줘'/'motion-graphic-setup'이라고 요청하면 사용."
---

# motion-graphic-setup — 모션 그래픽 제작 환경 점검

`motion-graphic-make` 의 실행 전제조건을 점검한다. 영상 생성은 내장 media 파이프라인을 쓰므로
**별도 CLI·API 키 설치가 필요 없다.** 필요한 로컬 도구는 ffmpeg(인코딩·오디오 신스)와
headless Chromium(HTML 컴포지션 캡처)뿐이다.
**OS·arch·기존 설치 여부를 먼저 감지**해 알맞은 경로를 고른다. 설치는 **멱등**(이미 있으면 skip·검증만).
답변은 한글(기술 토큰 영문).

## Workflow

### 0. 감지 (먼저, 추정 금지)

```bash
echo "OS=$(uname -s)"
echo "ARCH=$(uname -m)"
command -v ffmpeg >/dev/null && ffmpeg -version 2>&1 | head -1 || echo "ffmpeg=미설치"
```

**이미 설치 확인**: `ffmpeg` 가 존재하면 아래 §1 은 건너뛴다. Chromium 은 `setup-playwright` 스킬로 준비한다.

### 1. ffmpeg 확보

**Linux — Ubuntu / Debian** (이 VM의 기본 경로): `sudo apt-get install -y ffmpeg`

**Linux — RHEL8 / Rocky8**: BaseOS/AppStream 미제공(라이선스) → RPM Fusion 필요, 접근 막히면 `ffmpeg-static` 폴백.

**macOS**: `brew install ffmpeg` / **Windows**: `winget install --id Gyan.FFmpeg -e`

**스킬 저장소(`~/workspace/skills/`)에는 ffmpeg 바이너리를 절대 번들하지 않는다.**

### 2. 검증 (보고 의무)

```bash
command -v ffmpeg >/dev/null && ffmpeg -version | head -1 || echo "시스템 ffmpeg 없음"
echo "media 파이프라인: 내장 (키 불필요)"
```

## Operating Rules

- 이 VM은 Linux다. macOS/Windows 절은 다른 머신용 참고로 둔다.
- 영상 생성에 외부 키·CLI가 필요 없다는 점을 사용자에게 분명히 한다.
