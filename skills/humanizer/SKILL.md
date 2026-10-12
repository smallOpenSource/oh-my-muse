---
name: humanizer
description: "AI가 쓴 듯한 영문 글의 흔적을 제거해 자연스러운 문체로 윤문. 사용자가 'humanizer'/'자연스럽게 다듬어줘'/'AI 티 나지 않게'/'sound more human'이라고 요청하면 사용."
version: 2.8.0
license: MIT
---

# Humanizer: Remove AI Writing Patterns

## Purpose

AI가 쓴 듯한 영문 글에서 AI 패턴을 찾아내 자연스러운 사람의 문체로 윤문한다. 기준은 Wikipedia의 "Signs of AI writing"(WikiProject AI Cleanup 유지, 원문: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). 전체 패턴 목록(33종)은 `references/patterns.md`에 있다. 이 SKILL.md는 절차·산출물·판정 가이드를 담는다.

## Workflow

### 1. 입력 읽기 + 패턴 식별

`references/patterns.md`의 33종 패턴을 기준으로 입력 전체를 스캔한다.

### 2. Voice Calibration (선택)

사용자가 자신의 글 샘플을 제공하면 먼저 분석한다: 문장 길이 패턴·어휘 수준·단락 시작 방식·구두점 습관·반복 어구·전환 처리. 윤문 시 AI 패턴 제거뿐 아니라 샘플의 패턴으로 대체한다. 샘플이 없으면 기본(자연스럽고 리듬이 다양하며 의견이 있는 문체).

### 3. PERSONALITY AND SOUL (해당될 때만)

블로그·에세이·의견·개인 글에만 적용. 백과·기술·법률·참조 문서는 중립·간결이 올바른 사람의 목소리이므로 의견·1인칭을 주입하지 않는다.

영혼 없는 글의 징후: 문장 길이·구조가 전부 동일, 의견 없음, 불확실성 인정 없음, 적절한 1인칭 부재, 유머·날카로움·개성 부재, 위키/보도자료처럼 읽힘.

대처: 의견을 가져라("I genuinely don't know how to feel about this"는 중립적 나열보다 인간적). 리듬을 바꿔라(짧고 날카로운 문장. 길게 흘러가는 문장. 섞어라). 약간의 어수선함을 허하라(옆길·삽입·덜 다듬어진 생각이 인간적).

### 4. Draft → Audit → Final 루프

1. **draft rewrite**: 입력의 모든 패턴 인스턴스를 자연스러운 대체로 고친다. 삭제가 아니라 **고쳐 쓰기**(원문이 5단락이면 5단락 유지). 핵심 의미 유지, 의도된 어조 유지. 소리 내어 읽었을 때 자연스러운지 확인.
2. **audit**: "What makes the below so obviously AI generated?"에 짧게 답한다(남은 tells 불릿).
3. **final rewrite**: audit에서 지적된 것을 반영. 최종본에 em dash(—)·en dash(–)가 하나도 없는지 스캔(§14 하드 제약).

### 5. 산출

draft, "여전히 AI 같은 점" 불릿, final rewrite, (선택) 변경 요약.

## Output Contract

- 산출물은 **draft → 짧은 audit 불릿 → final rewrite → (선택) 변경 요약** 순서.
- final rewrite에는 em dash(—)·en dash(–)가 없어야 한다.
- 윤문 대상이 영어 텍스트임을 전제로 한다(패턴 목록이 영문 글 기준).

## Operating Rules

- **오탐지 주의**: 아래는 단독으로는 AI의 증거가 아니다. 패턴 **군집**을 볼 것.
  - 완벽한 문법·일관된 스타일 / 격식·비격식 혼합 / 밋밋한 문체 / 학술 어휘 / 서신체 인사말 / 단독 전이 어휘(however 하나) / 단독 곱슬 따옴표 / 단독 em dash / 짧은 강조 문장 하나 / 문장 중간의 "honestly" / 출처 부재 / 깔끔한 서식.
  - em dash 하나는 의미 없음. em dash + rule-of-three + "vibrant tapestry" + "Conclusion" 절이면 자백이다.
- **사람의 글 징후는 보존**: 구체적이고 날조하기 어려운 디테일, 해소되지 않은 양가감정, 시대 한정 레퍼런스, 방어 가능한 1인칭 편집 선택, 다양한 문장 길이, 진짜 삽입·자기정정, 2022-11-30(ChatGPT 공개) 이전 편집물.
- 의미를 바꾸지 않는다. AI-ism을 지우면서 원문이 담던 내용을 전부 유지한다.
- 기술·법률·참조 문체에는 개성 주입을 하지 않는다(중립이 곧 인간적).
- 원본의 `allowed-tools`/`compatibility` 프론트매터는 Claude Code 전용이므로 이식하지 않는다. 이 환경에서는 읽기·쓰기·편집 도구로 동작한다.
- 원본 MIT 라이선스 표기는 생략하지 않는다: 이 스킬의 패턴 목록은 Wikipedia "Signs of AI writing"(WikiProject AI Cleanup) 기반이며, 방법론 출처를 `references/patterns.md`에 명시한다.

## Full Example (축약)

**Before:** "Great question! Here is an essay on this topic. I hope this helps! AI-assisted coding serves as an enduring testament to the transformative potential of large language models, marking a pivotal moment in the evolution of software development..."

**Final rewrite:**
> AI coding assistants can make you faster at the boring parts. Not everything. Definitely not architecture.
>
> They're great at boilerplate: config files, test scaffolding, repetitive refactors. They're also great at sounding right while being wrong. I've accepted suggestions that compiled, passed lint, and still missed the point because I stopped paying attention.
>
> People I talk to tend to land in two camps. Some use it like autocomplete for chores and review every line. Others disable it after it keeps suggesting patterns they don't want. Both feel reasonable.
>
> The productivity metrics are slippery. GitHub can say Copilot users "accept 30% of suggestions," but acceptance isn't correctness, and correctness isn't value. If you don't have tests, you're basically guessing.

**Changes made:** 챗봇 프레이밍·중요성 부풀리기·홍보/-ing 패딩·3개 묶음·유의어 순환·가짜 범위·copula 회피·em dash/이모지/볼드/곱슬 따옴표·정형 Challenges 절·컷오프/완곡 면책·군더더기·권위 행세·막연한 낙관 결말을 제거하고, 다양한 리듬과 구체적 디테일로 재구성.
