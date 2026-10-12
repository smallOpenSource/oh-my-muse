---
name: wiki
description: 사용자가 "wiki에 추가해줘", "위키에서 찾아줘", "wiki 정리해줘", "wiki lint 해줘"라고 요청하면 발동. 세션을 넘나들며 축적되는 지속 마크다운 지식베이스(Karpathy LLM Wiki 모델) 스킬.
---

# Wiki

## Purpose

- 프로젝트·세션 지식을 위한 지속적, 자기 유지(self-maintained) 마크다운 지식베이스. Karpathy의 LLM Wiki 개념에서 영감을 받았다.
- 페이지는 YAML frontmatter를 가진 마크다운, 카테고리별 정리, `[[page-name]]` 위키 링크로 상호 참조한다.
- 카테고리: `architecture`, `decision`, `pattern`, `debugging`, `environment`, `session-log`.

## Workflow

지식은 파일 기반으로 관리한다 (원본의 `wiki_ingest`/`wiki_query` 등은 전용 도구가 아니라 파일 연산으로 수행한다):

- **Pages**: `~/workspace/wiki/*.md` (원본 `.omc/wiki/*.md` → workspace 경로로 치환)
- **Index**: `~/workspace/wiki/index.md` (자동 유지 카탈로그)
- **Log**: `~/workspace/wiki/log.md` (append-only 작업 연대기)

### Operations

| 작업 | 수행 방법 |
|------|-----------|
| **Ingest** | 지식 한 건을 처리해 여러 페이지에 반영. 해당 페이지 파일을 읽고 내용을 병합한 뒤 `index.md`·`log.md` 갱신. |
| **Query** | 키워드 + 태그 매칭으로 검색 (`grep`/`muse.exec` 활용). 매칭 페이지와 스니펫을 반환하고, **답은 LLM이 출처 인용과 함께 종합**한다. |
| **Lint** | 건강 점검: 고아 페이지, 오래된 내용, 깨진 상호 참조, 과대 페이지, 구조적 모순을 탐지해 보고한다. |
| **Quick Add** | 단일 페이지를 빠르게 추가: 새 `*.md` 파일 작성 + 인덱스·로그 갱신. |
| **List / Read / Delete** | `index.md` 읽기 / 특정 페이지 읽기 / 페이지 삭제(삭제는 recoverable 권장 — `trash` 사용 또는 아카이브). |
| **Log** | `~/workspace/wiki/log.md`를 읽어 작업 이력 확인. |

### Quick Add 페이지 템플릿

```markdown
---
title: {제목}
tags: [tag1, tag2]
category: {architecture|decision|pattern|debugging|environment|session-log}
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
---

{내용}

## References
- [[관련-페이지]]
```

## Output Contract

- 수행한 작업(ingest/query/lint/add/delete)과 영향받은 페이지 목록.
- Query 결과: 매칭 페이지 + 스니펫, 출처 인용과 함께 종합된 답변.
- Lint 결과: 발견된 문제 목록(고아·stale·깨진 참조·과대·모순)과 권장 조치.

## Operating Rules

1. **벡터 임베딩 금지** — 쿼리는 키워드 + 태그 매칭만 사용한다.
2. **전용 wiki MCP 도구 없음** — 원본의 `wiki_ingest()`·`wiki_query()`·`wiki_lint()`·`wiki_add()`·`wiki_read()`·`wiki_delete()` 함수 호출 형태는 이 환경에 존재하지 않는다. 대안: 위 Operations 표의 파일 연산(read/write/edit/exec+grep)으로 동일하게 수행한다. 동작 방식(인덱스·로그 유지, `[[링크]]` 문법)은 원문 그대로 보존한다.
3. **세션 종료 자동 캡처 불가** — 원본의 세션 종료 시 자동 캡처(`wiki.autoCapture`, `.omc-config.json` 설정)는 이 환경의 hooks로 대체되지 않는다. 대안: 세션 말미에 수동으로 ingest하거나, 주기 정리가 필요하면 Muse의 `cron`으로 예약한다.
4. **모델 라우팅 개념 미적용** — 원본의 haiku/sonnet/opus/fable 라우팅은 Claude Code 전용이다. 이 환경에서는 `subagent.spawn` 기본 모델을 사용한다.
5. **프로젝트 로컬 지식** — 위키는 프로젝트별 지식 저장소로 취급한다. 민감 정보는 넣지 않는다.
6. **명령어 흡수**: 원본 `/oh-my-claudecode:wiki` 슬래시 커맨드와 트리거 문구("wiki", "wiki this", "wiki add", "wiki lint", "wiki query")는 이 스킬의 채팅 트리거("wiki에 추가해줘" 등)로 대체된다.
