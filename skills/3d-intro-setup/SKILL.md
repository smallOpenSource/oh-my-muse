---
name: 3d-intro-setup
description: "`3d-intro-build` 에 필요한 실행 환경(ffmpeg, Node, Playwright/Chromium)을 점검한다. 이미지·영상 생성은 내장 media 파이프라인을 쓰므로 API 키·크레덴셜이 필요 없다. 'setup-3d-intro'/'3d-intro-setup'/'3D 인트로 설정'/'인트로 제작 환경 준비해줘' 라고 요청하면 사용."
---

# 3d-intro-setup — 3D 인트로 제작 환경 점검

`3d-intro-build` 의 실행 전제조건을 점검한다.
이미지·영상 생성은 내장 media 파이프라인(`media.generate_image`·`media.generate_video`)을 쓰므로
**Azure/WAN/Sora 같은 외부 API 키·크레덴셜은 필요 없다.** 이 스킬은 로컬 도구(ffmpeg 등) 확인까지만 담당한다.
**OS·arch·기존 설치 여부를 먼저 감지**해 알맞은 경로를 고른다. 설치는 **멱등**(이미 있으면 skip·검증만).
답변은 한글(기술 토큰 영문).

## 0. 감지 (먼저 — 추정 금지)

```bash
echo "OS=$(uname -s)"
echo "ARCH=$(uname -m)"
[ -f /etc/os-release ] && . /etc/os-release && echo "distro=$ID ${VERSION_ID}"
command -v node   >/dev/null && echo "node=$(node -v)"        || echo "node=미설치"
command -v ffmpeg >/dev/null && ffmpeg -version 2>&1 | head -1 || echo "ffmpeg=미설치"
```

**이미 확보 확인**: `ffmpeg` 가 있으면 §1 은 건너뛴다. media 파이프라인은 별도 설정 없이 바로 쓸 수 있다.

## 1. ffmpeg 확보

프레임 추출·리사이즈·클립 인코딩에 `ffmpeg` 바이너리를 요구한다.

- Ubuntu/Debian: `sudo apt-get install -y ffmpeg`
- macOS: `brew install ffmpeg`
- RHEL8/Rocky8: BaseOS/AppStream 미포함(라이선스) → RPM Fusion 후 `dnf install -y ffmpeg`
- 전부 막히면(권한/오프라인) `ffmpeg-static` npm 폴백:
  `(cd ~ && npm install --prefix ~/.config/3d-intro/tools ffmpeg-static)`

**스킬 저장소(`~/workspace/skills/`)에는 ffmpeg 바이너리를 절대 번들하지 않는다.**

## 2. 독립 검증용 브라우저 (선택)

Step 6 독립 검증에 Node 용 playwright 패키지와 Chromium 이 필요하다. `setup-playwright` 스킬로 준비한다.

## 3. 검증 (보고 의무)

```bash
command -v ffmpeg >/dev/null && ffmpeg -version | head -1 || echo "ffmpeg 없음"
echo "media 파이프라인: 내장 (키 불필요)"
```

## 함정

- **키를 묻지 않는다**: 구 버전의 이 스킬은 Azure/WAN 키를 받았으나, 현행 백엔드는 내장 media 파이프라인이라 키가 필요 없다. 키 파일(`.env.3d-intro.local` 등)이 남아 있으면 무시해도 된다.
- **생성 한도**: `media.generate_image` 한 응답 4회, `media.generate_video` 한 메시지 6개 — 환경 문제가 아니라 파이프라인 제약이므로 여기서 "고칠" 것이 없다.
