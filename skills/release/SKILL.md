---
name: release
description: "레포 릴리스 규칙을 분석해 .omc/RELEASE_RULE.md에 캐시하고 릴리스를 안내하는 얇은 어시스턴트. 사용자가 'release 해줘', 'release minor 해줘', '버전 올려줘'라고 요청하면 사용."
---

# release: 릴리스 어시스턴트

## Purpose

- 얇고 레포 인식적인 릴리스 어시스턴트. 첫 실행에 프로젝트·CI를 검사해 릴리스 규칙을 도출하고 `.omc/RELEASE_RULE.md`에 저장, 이후에는 그 규칙으로 릴리스를 안내한다.
- 프로젝트별 버전 파일·명령을 하드코딩하지 않는다 — 전부 레포 검사에서 도출.

## Workflow

### Step 0 — 릴리스 규칙 로드 또는 구축

- `.omc/RELEASE_RULE.md`가 없거나 `--refresh`가 있으면 아래 분석을 실행하고 파일 작성.
- 있으면 읽고, 파일의 `last-analyzed` 이후 CI 디렉터리(`.github/workflows/` 등) 변경을 델타 체크 — 바뀐 섹션만 재분석·업데이트하고 변경 보고.

### Step 1 — 레포 분석 (첫 실행·--refresh)

1. **버전 출처**: `package.json`/`pyproject.toml`/`Cargo.toml`/build.gradle/`VERSION` 등에서 현재 버전 문자열을 가진 모든 파일 + 필드/패턴. 릴리스 자동화 스크립트 감지 (`scripts/release.*`, `release-it`, `semantic-release`, `changesets`, `goreleaser` 등).
2. **레지스트리/배포**: npm·PyPI·Cargo·Docker·GitHub Packages. 태그 푸시에 자동 발행하는 CI 스텝은 어느 워크플로·잡인지.
3. **릴리스 트리거**: 태그 푸시(`v*`), `workflow_dispatch`, main 머지, 릴리스 브랜치, 커밋 메시지 패턴.
4. **테스트 게이트**: 테스트 명령 + CI 위치. 발행 전 통과 필수 여부, 우회 플래그.
5. **릴리스 노트/체인지로그**: `CHANGELOG.md` 유무, 컨벤션(Keep a Changelog·Conventional Commits·GitHub 자동 생성), 릴리스 본문 파일.
6. **첫 사용자 체크**: 릴리스 워크플로 유무, 빌드 아티팩트 `.gitignore` 유무, `git tag --list`로 태그 사용 여부.

### Step 2 — `.omc/RELEASE_RULE.md` 작성

```markdown
# Release Rules
<!-- last-analyzed: YYYY-MM-DDTHH:MM:SSZ -->
## Version Sources / Release Trigger / Test Gate / Registry · Distribution / Release Notes Strategy / CI Workflow Files / First-Time Setup Gaps
```

### Step 3 — 버전 결정

인자가 있으면 사용, 없으면: 현재 버전 표시 → patch/minor/major 결과 표시 → 사용자에게 질문. semver 유효성 검증.

### Step 4 — 릴리스 전 체크리스트

규칙에서 도출한 체크리스트 제시 후 사용자 확인: 변경분 커밋·푸시 완료, 타깃 브랜치 CI 녹색, 로컬 테스트 통과, 전 버전 출처에 버전 범프, 릴리스 노트 준비.

### Step 5 — 릴리스 노트 가이드

레포 컨벤션을 적용, 없으면 기본 가이드: 사용자 체감 변경 우선, 타입별 그룹화(New Features·Bug Fixes·Breaking Changes·Deprecations·Internal), 항목당 한 문장+PR/이슈 링크+외부 기여자 크레딧, Breaking changes 최우선+마이그레이션 경로. Conventional Commits면 `git log <prev-tag>..HEAD --no-merges --format="%s"`로 초안 생성 후 사용자가 편집.

### Step 6 — 릴리스 실행

1. 버전 범프 (전 버전 출처 파일).
2. 테스트 (테스트 게이트 명령).
3. 커밋 — `git add <버전 파일> CHANGELOG.md`, `chore(release): bump version to vX.Y.Z`.
4. 태그 — `git tag -a vX.Y.Z -m "vX.Y.Z"` (annotated 권장).
5. 푸시 — `git push origin <branch> && git push origin vX.Y.Z`.
6. CI 인계 — 태그 푸시 트리거면 CI가 나머지 처리, 예상 워크플로 파일 안내.
7. 수동 발행 — CI 자동화 없으면 수동 발행 명령 나열 (`npm publish --access public`, `twine upload dist/*`).

### Step 7 — 첫 설정 제안

Step 1f에서 발견된 gap에 구체적 도움 제안: 릴리스 워크플로 스캐폴드 제안, 첫 태그 안내, `.gitignore` 추가 제안.

### Step 8 — 검증

- CI 상태: `gh run list --workflow=<릴리스 워크플로> --limit=3` (gh 있으면).
- 레지스트리에서 새 버전 확인, `gh release view vX.Y.Z`로 GitHub Release 확인. 성공/실패 보고.

## Output Contract

- 버전 + 체크리스트 통과 여부 + 태그 + CI/레지스트리 확인 결과.

## Operating Rules

- 한계: Step 4~6의 mutation(버전 범프·커밋·태그·푸시)은 사용자 확인 후에만. CI·레지스트리 확인은 `gh` 인증이 있을 때만 가능, 없으면 수동 확인 안내.
- 모노레포/멀티패키지 워크스페이스(npm/pnpm workspaces, Cargo workspace) 감지 시 적응.
- `.omc/RELEASE_RULE.md`는 로컬 캐시 — 공유하려면 커밋, 로컬 유지는 `.gitignore`.
- 절대 새로 지어내지 말 것: 레포에 없는 CI 잡·발행 명령을 꾸며내지 않는다. 검사로 찾은 것만 쓴다.
- commands/release.md 흡수: 해당 파일은 스킬 읽기로의 단순 디스패처라 본문 내용 없음. 트리거 매핑(`/oh-my-claudecode:release [version] [--refresh]` → 채팅 "release [버전] 해줘")만 이 description/Workflow에 반영.
