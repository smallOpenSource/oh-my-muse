---
name: drydock
description: "어떤 레포든 shipyard 하네스(4 pillars × 5 surfaces)의 용골을 깐다 — 한 번 실행하고, 이후에는 --check로 드리프트 감사. 사용자가 'drydock 해줘', '하네스 깔아줘', 'drydock --check 해줘'라고 요청하면 사용."
---

# drydock: 용골 놓기

## Purpose

- 레포 하나에 **공유 하네스**를 깐다 — 모든 기여자(인간·에이전트)가 같은 디자인 언어를 상속하고 누구나 출하할 수 있게.

## 언제 사용 / 사용 금지

- **사용**: 인간과 에이전트가 함께 빌드하는 새 레포, 지식이 사람 머리·채팅 기록에만 있는 레포, 새 팀원·에이전트 온보딩(읽어서 맥락을 물려받게).
- **금지**: 협업자 없는 throwaway 프로토타입, 이미 이 하네스가 깔린 레포(`--check` 사용).

- 4개 기둥 × 5개 표면:

| 기둥 | 표면 |
|---|---|
| Context (공유 배경) | `CONTEXT.md`(용어집) + `docs/business/` + `docs/adr/` |
| Rules (경계) | `CLAUDE.md`(얇은 진입점: 관례·원칙·인덱스) + `docs/standards/` |
| Tools (조합 가능한 역량) | `.omc/skills/` + `.mcp.json` + `scripts/` |
| Standards (선급 협회) | `design-system/`(토큰·컴포넌트·패턴) + `docs/standards/` |

## Workflow

### 1. 탐지 (덮어쓰기 금지)

쓰기 전에 재고 조사: `CLAUDE.md`? `AGENTS.md`? (규칙: 하나라도 있으면 그 자리에서 확장, 없는 쪽은 한 줄 포인터로 생성 — **둘 다 새로 만들지 않는다**). `CONTEXT.md`, `docs/adr/`, `docs/standards/`, `docs/business/`, `design-system/`, `.omc/skills/`, `.mcp.json`, `scripts/`, `.gitattributes` 중 무엇이 있고 무엇이 없는지. 먼저 지도를 보고한 뒤 행동.

### 2. 문서 언어 확정 (파일 기반 결정)

1. 현재 호출의 명시적 선택이 있으면 우선 (유효한 BCP-47 태그로 정규화).
2. 없으면 `CONTEXT.md` 상단 YAML frontmatter의 `documentLanguage`를 읽는다. 유효하면 그게 권위.
3. 없거나 무효면 `CLAUDE.md` → `README.md` 순으로 검사. 모든 사용 가능 출처가 하나의 모호하지 않은 언어로 일치할 때만 추론.
4. 추론 불가(없음·혼합·충돌·저신뢰·무효·중국어 스크립트 모호 `zh`)면 한 번에 묶어 질문. 추측 금지.
5. 스캐폴딩 전 해결된 태그를 `CONTEXT.md` frontmatter의 `documentLanguage`에 기록. prose·라벨만 해당 언어, 경로·명령·플래그·frontmatter 키·토큰은 바이트 단위 고정.

### 3. 스캐폴드 (없는 표면만 생성)

```
CLAUDE.md                      # 얇은 진입점: 프로젝트 관례·아키텍처 원칙 3-5개·표준 인덱스·ADR 목록·공유 배경 링크·에이전트 가이드
CONTEXT.md                     # 용어집: 용어당 정의·경계·해결된 모호성 하나
.gitattributes                 # * text=auto eol=lf
docs/adr/0001-adopt-shipyard-harness.md
docs/standards/architecture.md  # 모듈 경계·에러 처리·의존 방향·심(seam)과 깊이 — 규칙마다 why 포함
docs/standards/data.md
docs/standards/process.md      # Testing 볼륨 포함 (인터페이스로만 테스트, 독립된 기대값, 한 번에 한 슬라이스)
docs/business/README.md        # 업무 지식: 질문 하나당 글 하나
design-system/README.md        # tokens/·components/·patterns/ (UI 없으면 스텁)
.omc/skills/README.md          # 프로젝트 스킬: ASCII id + 비어 있지 않은 triggers 필수
.mcp.json                      # {"mcpServers": {}} — 실제 필요할 때 추가
scripts/README.md
```

- 탐지에서 없는 것만 만든다. 시드 prose는 "규칙마다 why, 채팅 없이 자립, 출처 명시" 기준을 만족해야 한다.
- 나머지 질문은 언어 확정 후: 패키지/기술 스택 (표준·디자인시스템 시드용), UI 유무, 이슈 트래커 위치 (harbor V1은 GitHub만), intake 소통 권한.

### 4. 거버넌스 루프 연결 (폴더가 아니라 shipyard가 되는 지점)

사용자에게 알리고, 이 흐름들이 뼈대를 채우도록 맡긴다:
- **launch**가 결정이 정착될 때 CONTEXT.md 어휘·ADR·docs/business/를 쓴다.
- **launch C5 침전 / 코드 리뷰**가 반복되는 수정을 docs/standards/·CLAUDE.md 원칙으로 침전시킨다.
- **누구나** .omc/skills/에 프로젝트 스킬 추가 가능 (장벽은 권한이 아니라 skillify 품질 게이트).
- 규칙: **시작은 허락 불필요, 착륙은 shipyard 슬롯으로.** 슬롯을 말할 수 없는 변경은 냄새.

### 5. 보고

- 생성 / 확장 / 의도적 스킵 (각각 이유와 함께)
- 해결된 문서 언어 (`documentLanguage: <tag>`)와 출처 (명시 선택·기존 마커·만장일치 추론)
- 인간 콘텐츠가 가장 필요한 표면 3곳
- 리마인드: 언제든 `--check`로 재실행

### --check 모드

파일시스템과 하네스 지도의 드리프트 감사. 보고 항목: 빠진 표면, 없거나 무효한 `documentLanguage` 태그, 죽은 경로를 가리키는 CLAUDE.md 섹션, 코드에서 안 쓰는 CONTEXT.md 용어, 참조되지 않는 표준. 각 항목에 confidence (`high`=기계적 검사 가능, `low`=휴리스틱)와 조치 가능성. 사용자가 선언한 throwaway/scratch 범위는 제외.

## Output Contract

- 초기 실행: 생성/확장/스킵 목록 + 문서 언어 + 다음 인간 작업 3곳.
- `--check`: 드리프트 발견 목록 (severity·confidence·actionable·증거·조언).

## Operating Rules

- 한계: 원본의 기계적 감사 스크립트(`node scripts/shipyard-audit.mjs`)는 원본 레포에만 존재 — 이 환경에서는 prose 감사로 수동 수행하고, exit code 계약(0=clean, 1=high-confidence actionable, 2=호출 오류)은 보고 형식으로만 유지.
- 한계: 원본의 훅 프리셋(파괴적 git 작업 가드·커밋 타임 품질 게이트)은 Claude Code 훅 전용이므로 이식에서 제외. 이 환경의 cron/hooks는 PreToolUse형 가드와 메커니즘이 달라 대체 불가 — 명시.
- 한계: 시드 companions(en/zh-Hans/zh-Hant) 전체 텍스트는 생략하고 구조·안정 토큰만 유지.
- 절대 새로 지어내지 말 것: 없는 표면을 "있다"고 보고하지 않는다. `low` confidence 발견을 `high`로 올리지 않는다.
