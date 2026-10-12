---
name: ask
description: "외부 CLI(Claude/Codex/Gemini/Grok/Cursor) 관점의 어드바이저 요청을 처리. 이 환경에서는 외부 모델 CLI 연동이 불가하므로 병렬 서브에이전트 관점 검토로 대체한다. 사용자가 'codex 관점에서 리뷰해줘', 'gemini 관점으로 UX 제안해줘'처럼 외부 모델 관점의 답변을 요청하면 사용."
---

# ask: 관점별 어드바이저

## Purpose

- 원본: `omc ask` — Claude/Codex/Gemini/Antigravity/Grok/Cursor 로컬 CLI로 프롬프트를 라우팅하고 결과를 ask 아티팩트로 저장하는 어드바이저 스킬.
- **이 환경에서는 외부 모델 CLI 연동이 불가**하므로, 이 스킬은 "관점별 병렬 검토" 대안 워크플로로 이식한다. 외부 모델이 실제로 답하는 것이 아니라, 내부 서브에이전트에 관점을 나눠 맡긴 병렬 검토다.

## Workflow

1. 요청 접수: 사용자가 외부 모델 관점의 검토를 요청하면(예: "codex 관점에서 보안 리뷰해줘", "gemini 관점에서 UX 제안해줘"), 모델 이름이 아니라 **관점**을 추출한다.
2. 관점 매핑 (대표 예시):
   - 보안 리뷰 / 코드 리뷰 관점 → 엄격한 코드 리뷰어 역할
   - UX 제안 관점 → 사용자 경험 설계자 역할
   - 구현 계획 관점 → 아키텍처 설계자 역할
3. `subagent.spawn`으로 각 관점을 별도 서브에이전트에 병렬 위임. 같은 질문이라도 관점별로 서로 다른 답을 내도록 역할을 명시한다.
4. 결과 취합: 관점별 답변을 요약하고 공통점·충돌점을 정리해 전달.

## Output Contract

- 관점별 답변 요약 (관점 레이블과 함께)
- 종합: 공통 지적 + 관점 충돌 시 판단 근거

## Operating Rules

- 한계: 원본의 외부 모델 CLI 라우팅(Claude/Codex/Gemini/Antigravity/Grok/Cursor)과 `omc ask` 래퍼는 이 환경에서 **동작 불가**. `codex`, `gemini`, `cursor-agent` 등 raw CLI를 직접 실행해도 외부 모델이 답하지 않는다.
- 대안: 위 Workflow의 병렬 서브에이전트 관점 검토. "외부 모델의 답변"이라는 표현을 쓰지 말고, 관점별 내부 검토임을 명시한다.
- 아티팩트 저장: 원본 `.omc/artifacts/ask/<provider>-<slug>-<timestamp>.md` → `~/workspace/` 하위 작업 디렉터리에 관점별 결과를 저장.
- commands/ask.md 흡수: 해당 파일은 스킬 읽기로의 단순 디스패처라 본문 내용 없음. 트리거 매핑(`/oh-my-claudecode:ask <provider> <질문>` → 채팅 "xxx 관점에서 답해줘")만 이 description에 반영.
