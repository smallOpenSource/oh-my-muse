---
name: skill-up
description: "업스트림 플러그인 5종 최신판을 받아 실사용 스킬에 이식·갱신하는 전체 워크플로. git clone/pull → ~/workspace/skills-upstream/ 스테이징 → diff 병합 이식 → 미디어 스킬을 내장 media 파이프라인 기준으로 정정 → 검증 → 백업 정리. 사용자가 'skill-up 해줘'/'스킬 업데이트해줘'/'플러그인 최신판으로 갱신해줘'라고 요청하면 사용."
---

# skill-up — 업스트림 플러그인 이식·갱신

## Purpose

5개 업스트림 저장소의 최신판을 받아(`~/workspace/skills-upstream/`에 스테이징),
실사용 스킬(`~/workspace/skills/`)에 diff 병합으로 이식하고,
이미지·영상 스킬은 내장 media 파이프라인 기준으로 정정한다.
**`~/workspace/skills/`에 원본을 직접 clone·덮어쓰기 하지 않는다** — 여긴 내 환경에 맞게
적응시킨 라이브러리다. 답변은 한글(기술 토큰 영문).

## 업스트림 목록

| 저장소 | URL | 가져올 것 |
|---|---|---|
| banker_plugins | https://github.com/smallOpenSource/banker_plugins.git | `skills/` (60개) |
| oh-my-claudecode | https://github.com/Yeachan-Heo/oh-my-claudecode.git | `skills/` + `agents/` (`.omc/`·`dist/`·`src/`는 빌드 산출물이라 무시) |
| superpowers | https://github.com/obra/superpowers.git | `skills/` (14개) |
| harness | https://github.com/revfactory/harness.git | `skills/` (evolve, harness) |
| scroll-world | https://github.com/oso95/scroll-world.git | `skills/` (scroll-world) |

## Step 0 — 스테이징 (clone/pull)

```bash
U=~/workspace/skills-upstream
mkdir -p "$U"
declare -A REPOS=(
  [banker_plugins]=https://github.com/smallOpenSource/banker_plugins.git
  [oh-my-claudecode]=https://github.com/Yeachan-Heo/oh-my-claudecode.git
  [superpowers]=https://github.com/obra/superpowers.git
  [harness]=https://github.com/revfactory/harness.git
  [scroll-world]=https://github.com/oso95/scroll-world.git
)
for n in "${!REPOS[@]}"; do
  if [ -d "$U/$n/.git" ]; then git -C "$U/$n" pull --ff-only
  else git clone "${REPOS[$n]}" "$U/$n"; fi
done
```

- 주의: `/root/workspace`는 `/home/hatch/workspace`의 심링크 — 경로를 어디서 적어도 같은 곳이다.
- `git clone` 실패("already exists")가 나면 이미 받아둔 것이니 `git pull`로 전환한다.

## Step 1 — 백업

```bash
cp -a ~/workspace/skills ~/workspace/skills-backup-$(date +%Y%m%d)
```

- `cp: failed to preserve ownership` 경고는 컨테이너 fs 제약으로 나는 겉모양 문제 — 내용은 정상 복사된다. 무시한다.

## Step 2 — 병합 이식 (3개 그룹, 병렬 가능)

서브에이전트 3개로 나눠 병렬 수행한다. 각 그룹 지시문에 아래 병합 규칙을 그대로 넣는다.

**그룹 A (banker)**: `$U/banker_plugins/skills/` → `~/workspace/skills/`
**그룹 B (OMC)**: `$U/oh-my-claudecode/skills/` → `~/workspace/skills/`,
`$U/oh-my-claudecode/agents/` → `~/workspace/skills/team/references/agents/`
**그룹 C (신규)**: superpowers·harness·scroll-world의 `skills/` → `~/workspace/skills/` 신규 이식

### 병합 규칙 (맹목 덮어쓰기 금지)

1. 대상에 같은 이름이 있으면 diff 후 병합: 원본의 실질 신규 내용(새 섹션·수정·레퍼런스)은 취하고, 내 Muse 환경 적응 서술은 보존.
2. 대상에 없는 신규 스킬은 원본을 가져와 환경 적응 후 설치.
3. 내 스킬 중 원본에 없는 것은 **절대 삭제하지 않는다**.
4. 이름 불일치는 SKILL.md frontmatter `name:` 필드로 대조 (改名 사례: `harness-factory` vs `setup-harness-factory`).
5. **보호 커스텀** (절대 지우지 않음):
   - `3d-intro-build`·`motion-graphic-make`: 무음 금지(BGM+효과음), `scrub-engine.js`를 `mountScrollWorld`로 구동, 직접 스크롤 스크립트 작성 금지, ffmpeg 로컬 렌더 폴백.

### 환경 적응 원칙

- Claude Code 전제(tmux 세션 안에서 실행, 외부 모델 CLI 연동, hooks) → 내 환경으로 대체하거나 한계 명시.
  (tmux → background exec + `process` 도구, 외부모델 관점 → 서브에이전트 병렬 검토, hooks → 미지원 명시)
- 문체는 기존 스킬과 일치 (간결 한국어, 기술 토큰 영문).

## Step 3 — 미디어 스킬 정정

아래 5개는 외부 이미지·영상 API 기준으로 쓰여 있으므로, 내장 media 파이프라인 기준으로 다시 쓴다.

| 스킬 | 정정 내용 |
|---|---|
| 3d-intro-build | Azure/WAN/Sora 제거 → `media.generate_image`(스틸), `media.generate_video`(시작 프레임 지정 클립). 키·비용 추정 삭제, 단계별 승인 게이트 유지 |
| 3d-intro-setup | 키 받는 절차 삭제 → ffmpeg·Chromium 점검만 |
| motion-graphic-make | hyperframes 위임 삭제 → 텍스트 정밀형은 로컬 HTML→headless 캡처→ffmpeg, 시네마틱형은 `media.generate_video`. 무음 금지(BGM+SFX ffmpeg 신스) 유지 |
| motion-graphic-setup | CLI 설치 절차 삭제 → ffmpeg·Chromium 점검만 |
| scroll-world | Higgsfield/Monid/Seedance 제거 → `media.generate_image`/`media.generate_video`. 끝 프레임 지정 미지원은 크로스페이드로 흡수한다고 정직히 명시 |

**media 파이프라인 제약** (스킬 본문에 반드시 포함):
- `media.generate_image`: 한 응답 최대 4회
- `media.generate_video`: 한 사용자 메시지 최대 6개 (성공 기준)
- 영상 프롬프트는 있는 그대로 전달 (수식어 덧씌우기 금지)
- 생성 파일은 `output_dir`로 프로젝트 폴더 지정 (기본 미디어 디렉터리 사용 금지)

**정직한 한계 명시**: 영상 끝 프레임 지정 미지원, AI 생성 영상 내 문자 깨짐 가능성은 로컬 HTML 경로로.

## Step 4 — 검증

```bash
ls ~/workspace/skills | wc -l                                    # 개수 확인
for d in ~/workspace/skills/*/; do head -5 "$d/SKILL.md" | grep -q "^name:" || echo "BROKEN: $d"; done
grep -rli "azure\|hyperframes\|higgsfield\|monid\|seedance" ~/workspace/skills/*/SKILL.md  # 레거시 언급만 남아야 함
grep -c "mountScrollWorld\|무음 금지" ~/workspace/skills/3d-intro-build/SKILL.md ~/workspace/skills/motion-graphic-make/SKILL.md  # 커스텀 보존 확인
```

- frontmatter `name:` = 디렉터리명 일치 확인.
- 벤더 참조는 "레거시라 사용하지 않는다"는 주석 형태로만 남아야 한다.

## Step 5 — 백업 정리

- 검증이 끝난 뒤 **사용자 확인을 받고** `~/workspace/skills-backup-YYYYMMDD/` 를 제거한다.
- 확인 없이 `rm -rf` 하지 않는다.

## 보고

- 그룹별 처리 결과(업데이트/신규/유지 수), 보호 커스텀 보존 여부, 검증 결과, 백업 경로를 간결하게 보고한다.

## Gotchas

- 스테이징을 건너뛰고 `~/workspace/skills/`에 직접 clone하면 실사용본이 오염된다 — Step 0 경로를 항상 먼저 확인한다.
- OMC 저장소의 `.omc/`·`dist/`·`src/`는 빌드 산출물 — 원본은 최상위 `skills/`·`agents/`만 쓴다.
- `git pull --ff-only` 실패(로컬 변경 있음) 시: 스테이징은 읽기 전용이 원칙이라 로컬 변경이 있으면 보고하고 덮어쓴다.
- chown/chmod 실패는 컨테이너 fs 제약 — 둘 다 root라 기능 영향 없음. 맞추려다 시간 쓰지 않는다.
