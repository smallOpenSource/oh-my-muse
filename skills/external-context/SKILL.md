---
name: external-context
description: 사용자가 "external-context 해줘", "외부 문서 찾아줘", "<주제> 관련 최신 공식 문서 조사해줘"라고 요청하면 발동. 질의를 2–5개 파셋으로 분해해 document-specialist 서브에이전트를 병렬 실행하고, 출처 인용과 함께 종합하는 스킬.
---

# External Context

## Purpose

- 질의에 대한 외부 문서·레퍼런스·컨텍스트를 가져온다.
- 질의를 2–5개의 독립 파셋으로 분해하고, 파셋별 문서 전문가 에이전트를 **병렬**로 실행한 뒤 종합한다.
- 명시적 호출 전용 — 매직 키워드 트리거 없음.

## Workflow

### 1. 파셋 분해 (Facet Decomposition)

질의를 2–5개의 독립 검색 파셋으로 나눈다:

```markdown
## Search Decomposition

**Query:** <원본 질의>

### Facet 1: <파셋 이름>
- **Search focus:** 무엇을 검색할지
- **Sources:** 공식 문서, GitHub, 블로그 등

### Facet 2: <파셋 이름>
...
```

### 2. 병렬 에이전트 실행

`subagent.spawn`으로 파셋별 document-specialist를 병렬 실행한다 (최대 5개). 역할 프롬프트는 `~/workspace/skills/omc-team/references/agents/document-specialist.md`를 사용한다.

각 워커 프롬프트 예시:
```
너는 Document Specialist다. <파셋 1 설명>을 검색하라. browser.search와 browser.open으로 공식 문서와 예제를 찾고, 모든 출처를 URL과 함께 인용하라.
```

### 3. 종합 출력 포맷

```markdown
## External Context: <질의>

### Key Findings
1. **<발견>** - Source: [제목](url)
2. **<발견>** - Source: [제목](url)

### Detailed Results

#### Facet 1: <이름>
<인용과 함께 집계된 발견>

#### Facet 2: <이름>
<인용과 함께 집계된 발견>

### Sources
- [출처 1](url)
- [출처 2](url)
```

### 예시 호출

- "JWT 토큰 로테이션 best practice (Node.js) 찾아줘"
- "PostgreSQL용 Prisma vs Drizzle 비교해줘"
- "최신 React Server Components 패턴과 컨벤션 조사해줘"

## Output Contract

- 파셋 분해 계획 (2–5개).
- Key Findings (각각 출처 URL 인용).
- 파셋별 상세 결과.
- Sources 목록.

## Operating Rules

1. **최대 5개 병렬** document-specialist 에이전트. Claude Code의 Task tool은 사용하지 않고 `subagent.spawn`을 사용한다.
2. **외부 모델 불가** — 원본의 Codex/Gemini 워커 개념은 이 환경에서 동작하지 않는다. 모든 워커는 Muse 기반 서브에이전트로 실행한다.
3. **출처 인용 필수** — 모든 발견은 URL 출처와 함께. 공식 문서 > 블로그 > Stack Overflow 순으로 신뢰도를 둔다.
4. **명령어 흡수**: 원본 `/oh-my-claudecode:external-context <주제>` 슬래시 커맨드는 단순 디스패치 래퍼였으므로, 이 스킬의 채팅 트리거("외부 문서 찾아줘" 등)로 대체된다. 사용 예시(위의 예시 호출)는 원본 그대로 유지.
