---
name: obsidizer
description: "AI 생성 마크다운 위키를 의미 보존한 채 Obsidian 지식그래프로 정규화·상호링크·백링크(결정적 캐노니컬라이저 obsidize.mjs). 사용자가 '옵시디언화 해줘', '위키 그래프 정리해줘', 'obsidian 최적화해줘'라고 요청하면 사용. 기본 dry-run."
---

# obsidizer — AI 위키를 Obsidian 지식그래프로 정규화

## Purpose

AI가 생성한 마크다운 위키를 **의미 보존**한 채 그래프 관점(`tags`·`[[slug]]` 링크·`links[]`
백링크·Related 푸터)에서 정규화한다 — "vault over file", 노트 하나가 아니라 그래프 속 자리를
최적화한다. 의미 판단(어떤 언급이 진짜 링크인지, 어떤 섹션이 진짜 중복인지)은 LLM이 파일을 직접
편집해 내리고, **결정적 캐노니컬라이저**(`obsidize.mjs`, zero-dep 순수 Node 스크립트)가 마지막
기계적 패스로 바이트 단위 결과를 고정한다.

**모드**: `obsidizer [path]` (기본 dry-run 리뷰&수정) / `obsidizer [path] --apply` (실적용) /
`obsidizer --enable` / `obsidizer --disable` (지속 정규화 — 아래 한계 참조).

## Workflow

### 1. 입력 확보 — 타깃 감지

경로 인자 우선, 없으면 `.omc/wiki/` 감지, 둘 다 없으면 중단. 타깃을 즉시 **프로파일 분류**하고
이 분류가 이후 전부를 게이팅한다:

- **OMC-managed 위키** (`index.md`+`log.md`+9-필드 프론트매터 시그니처): 프론트매터 envelope 9-key 한정 · 위키링크 bare-only · `aliases` 거부
- **일반 Obsidian vault**: 프론트매터 자유 · piped 링크 허용 · `aliases` 조건부 작성

(Muse 환경 기본 타깃: 감지된 `.omc/wiki/`, 없으면 사용자가 지정한 vault 경로.)

### 2. 전체 vault 스캔 (읽기 전용)

모든 `.md` glob (reserved 파일은 개념맵용으로만 읽고 변경 대상에서 제외). 프론트매터/제목/H1/헤딩/
본문 링크/`tags`/`links[]`/Related 푸터 파싱 → 슬러그 인덱스·H1 인덱스·링크 그래프·태그 어휘·
orphan 집합으로 vault 모델 구축.

### 3. 의미 분석 (LLM, dry-run에선 쓰기 없음)

페이지별로 어떤 언급을 기존 슬러그에 링크할지, 어떤 역방향 백링크가 진짜인지, 어떤 섹션이 진짜
중복인지 판단. ghost node 금지 — 존재하지 않는 슬러그로 링크하지 않는다.

### 4. 미리보기 (기본)

`--apply` 없이는 페이지별 변경 요약 + vault 카운트만 제시하고 종료한다.

### 5. 안전 뮤테이션 (`--apply` 시)

스냅샷(`cp -r <vault> <vault>.bak-<ts>`) → LLM이 의미 편집 적용(T3/T4-결정/T5) →
**그 다음 `obsidize.mjs`가 최종 캐노니컬라이즈 1회** 실행(T1→T2→T4-기록→T6→T8-일반 순).
reserved 파일(`index.md`/`log.md`/`environment.md`)은 손대지 않음. rename 없음.

```bash
node obsidize.mjs <vault-path> [--profile=auto|omc|generic] [--dry-run] [--json]
```

### 6. 검증

신규 broken-ref 0 · orphan ≤ 베이스라인 · rename 0 · OMC 프로파일이면 bare-form grep 0 +
9-필드 프론트매터 grep 0 · 캐노니컬라이저 멱등 자가검사(2회 실행 diff 0).

## Output Contract

4-field 보고:
- **변경**: 적용된 변환 요약(어떤 페이지에 어떤 T#). 변환 규칙 표:

| # | 변환 | 레이어 |
|---|---|---|
| T1 | H1==title 단일화, 헤딩레벨 스킵 금지, 빈줄 정규화 | canonicalizer |
| T2 | `tags` 정규화(선행 `#` 제거·dedup·결정적 순서) | canonicalizer |
| T3 | 본문 `[[slug]]` 보강 — 기존 슬러그만. OMC 프로파일은 bare form만 | LLM(의미) |
| T4 | `links[]` 상호성 — 누락된 진짜 역방향 백링크 추가 → de-orphan (monotonic, 삭제 없음) | LLM 결정·canonicalizer 기록 |
| T5 | 페이지 내 섹션 dedup — 바이트 동일 중복 블록만 축약, 고유 사실 전량 보존 | LLM(의미) |
| T6 | Related 푸터(OMC 프로파일 한정) — 해소 가능한 링크를 정렬·dedup·bare form으로 렌더. cap(12)은 **추가분만** 제한, 기존 푸터 링크는 캡 초과여도 유지 | canonicalizer |
| T7 | rename | **안 함** |
| T8 | `aliases` — 일반 vault만 조건부 적용(아래 별칭 정책), OMC 트리 거부 | canonicalizer |
| T9/T10/T12 | inline `Key:: Value`·Canvas-MOC·MOC 허브 **생성** | 보류(보존만) |
| T11 | Excalidraw | 매 버전 보존만, 절대 생성 안 함 |

- **Evidence**: 카운트(스캔 페이지 수·추가 링크 수·해소 orphan 수·병합 중복 수·추가 alias 수·불변 파일 수).
- **검증**: 위 §6 항목.
- **Unknown**: 보류 기능·진짜 관계가 없어 남겨둔 orphan·바이트로 단언하지 않는 의미 판단 편차.

## Operating Rules

- **기본 = dry-run.** `--apply` 전까지 아무것도 쓰지 않는다. 미리보기 없는 자동 변형은 금지.
- **결정성 주장의 범위**: 바이트 멱등은 **캐노니컬라이저에만** 귀속. 의미 판단(링크·dedup 선택)은 실행마다 달라질 수 있어 **Unknown**으로 보고하며 절대 바이트로 단언하지 않는다.
- **타임스탬프 무잡음**: `created`는 절대 안 건드림. `updated`는 직렬화된 내용이 실제로 바뀔 때만(바이트 diff 게이트) 갱신.
- **모든 쓰기는 원자적**: 유니크 temp + 배타 생성 + fsync + rename. 절대 in-place bare write가 아니다. read-back CAS는 lost update 창을 `rename` 한 번으로 줄일 뿐 없애지 못한다 — 이 잔여 race는 **수용**이다.
- **해소 가능한 bare-form 링크는 삭제하지 않는다**(예외: (1) 대상 파일이 없는 broken-ref, (2) OMC 프로파일에서 bare slug가 아닌 형태). 푸터를 다시 그리기 전에 본문의 해소 가능한 위키링크를 `links[]`에 합집합으로 흡수한다 — 이 흡수가 없으면 수기 푸터 링크가 조용히 사라진다.
- **`links[]` 항목은 어느 경로에서도 지우지 않는다**(정렬·dedup만). 본문은 재작성하지 않는다(추가·포맷만).
- **`%%obsidizer:ignore%%` 옵트아웃**: 파일 어디든 이 마커가 있으면 프로파일 무관하게 그 페이지를 통째로 건너뛴다(리포트에 `ignored`로 집계). 건너뛴 페이지도 vault 모델에는 남는다.
- **사실을 날조하지 않는다**: `cssclasses`·Excalidraw·Canvas·MOC를 절대 지어내지 않는다. **`cssclasses`는 어느 프로파일에서도 쓰지 않는다** — OMC 트리에선 destructive strip이고, 일반 vault에서도 문서 안에 출처가 없는 값이라 쓰면 날조가 된다.
- **보존 전용 표면**: `## Update (<ts>)` 섹션·body-inline `Key:: Value`·sibling `.canvas`·`.excalidraw.md`는 절대 재포맷/재작성하지 않는다.
- **프론트매터 순서**: OMC 프로파일은 9-필드 고정 순서 보존. 일반 프로파일은 기존 키·순서를 그대로 두고 `aliases`만 맨 끝에 조건부 추가.

### 별칭(aliases) 정책

**일반 vault만** 캐노니컬라이저가 기계적으로 작성. 유일한 출처는 노트 자신의 **H1** — 절대 날조하지
않는다. 아래 6조건을 **모두** 만족해야 `aliases: ["<H1 텍스트>"]`를 쓴다: (1) 프로파일==일반 vault
(2) 프론트매터 블록 존재 + H1 정확히 1개 (3) `norm(H1) !== norm(basename)` (4) `norm(H1)`이 다른
노트의 basename과 겹치지 않음 (5) H1 텍스트가 vault 전체에서 유일 (6) 기존 `aliases` 키 없음.
`norm(x)` = 소문자화 → `[^a-z0-9]+`를 `-`로 축약 → 앞뒤 `-` 제거(64자 cap **없음** — OMC `titleToSlug`의 cap을 흉내내면 긴 제목의 유효한 별칭을 부당하게 억제한다). 항상 큰따옴표 quote + FLOW 형식 +
맨 끝에 추가. **OMC-managed 트리에는 쓰지 않는다(거부이지 보류가 아니다)** — `parseFrontmatter`가
9-key를 재구성하는 READ 시점에 조용히 사라지는 silent loss + piped link 소비처의 silent corruption,
파괴적 실패 모드는 어떤 노력으로도 정당화되지 않는다.

### 한계 (조용히 누락하지 않음)

- **`--enable`/`--disable` 지속 정규화**: 원본은 banker 플러그인의 `hooks/hooks.json`에
  PostToolUse로 등록된 hook + `<wikiDir>/.obsidizer` 플래그 파일이 스위치였다. 이 Muse 환경에는
  해당 hook 표면(wiki_ingest/wiki_add 쓰기 도구)이 없으므로 **hook 자동 발화는 동작하지 않는다**.
  가장 가까운 대안: 내 `hooks`에 파일 변경 감시 hook을 등록하거나, `cron`으로 주기 실행해
  `<vault>/.obsidizer` 플래그가 있을 때 `obsidize.mjs`를 돌린다. `--enable`은 "이후 모든 위키 생성이
  obsidizer 양식을 따른다"를 뜻하지 않는다 — 기계적 정규화만 자동 적용하고, 의미 보강(어떤 언급을
  링크할지 등)은 절대 자동화하지 않는다.
- **검증 도구**: 원본의 `wiki_lint`(OMC MCP, 읽기 전용)는 이 환경에 없다. 대안은 캐노니컬라이저
  멱등 자가검사 + broken-ref/bare-form grep 기반 자체 검증이다.
- **프로파일 기본 타깃**: 원본 Codex/OMX 런타임의 "사용자 지정 vault 경로" 분기는 참고 수준으로 축소 —
  이 환경에서는 경로 인자 또는 `.omc/wiki/` 감지를 쓴다.
- **hook 경로 거부 근거**: hook이 LLM에 지시를 주입하는 것 자체는 기술적으로 가능하지만, obsidizer는 품질 근거로 거부한다 — (1) 강제가 아닌 soft-honored일 뿐, (2) 미리보기 없는 자동 변형 → dry-run-기본 원칙과 충돌, (3) 자동 경로에 LLM 판단이 들어가 결정성 붕괴, (4) 세션 가로챔(저장만 요청했는데 그래프 큐레이션이 끼어듦).

ARGUMENTS: [path] [--apply] | --enable | --disable
