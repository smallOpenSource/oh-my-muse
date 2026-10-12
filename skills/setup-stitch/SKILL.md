---
name: setup-stitch
description: "Google 의 디자인 생성 서비스인 Stitch 의 MCP 프록시를 `claude mcp add`(Codex 는 `codex mcp add`)로 등록. 시크릿은 커밋하지 않음. 'setup-stitch'/'stitch 설치'/'stitch mcp' 또는 `/banker:setup` 시 사용."
---

# setup-stitch — Stitch MCP 프록시 등록

Stitch(withgoogle) 디자인 생성 MCP 를 프록시로 Claude Code 에 붙인다. Node(npx) 필요.
**★시크릿(API key)은 사용자만 입력·환경변수로 — 채팅/로그/커밋에 절대 노출 금지.** 답변은 한글.

## 0. 사전
- Node/npx 설치 확인(`node -v`).
- API key 발급: https://stitch.withgoogle.com/settings (사용자가 직접).

## 1. mac / linux — 프록시 스크립트 + MCP 등록
> key 는 채팅/기록에 남기지 말고, 사용자가 **자기 터미널**에서 `YOUR_STITCH_API_KEY` 를 실제 키로 교체.
```bash
mkdir -p ~/bin
cat > ~/bin/stitch-proxy.sh <<'EOF'
#!/bin/bash
export STITCH_API_KEY="YOUR_STITCH_API_KEY"   # ← 발급 키로 교체 (이 파일 커밋 금지)
exec npx -y @_davideast/stitch-mcp proxy
EOF
chmod +x ~/bin/stitch-proxy.sh

claude mcp remove stitch 2>/dev/null            # 기존 있으면 제거
claude mcp add stitch -- ~/bin/stitch-proxy.sh
claude mcp list                                  # stitch: … - ✔ Connected 기대
```
키를 평문 파일에 두기 싫으면 `STITCH_API_KEY` 를 `~/.bashrc`(비커밋) 등에 export 하고 스크립트는 참조만.

**Codex CLI:** 같은 프록시 스크립트를 Codex에도 붙인다 — `claude mcp` 대신 `codex mcp` 를 쓴다.
```bash
codex mcp remove stitch 2>/dev/null
codex mcp add stitch -- ~/bin/stitch-proxy.sh
codex mcp list                                   # stitch 연결 확인
```

> `skill_search` 결과에 Stitch 관련 스킬이 없으므로 위 수동 등록 안내를 유지한다.
> **Muse 환경 한계**: 이 환경에는 `claude mcp add`/`codex mcp add` 같은 CLI 등록 명령이 없다. 프록시 스크립트 생성까지만 자동 수행하고, 실제 MCP 연결은 사용자의 설정(UI/커넥터 설정)을 통해 등록하도록 안내하거나 부모 에이전트에게 위임한다. 등록 후에는 세션 갱신이 필요할 수 있다.

## 2. windows
`~/bin` 셸 스크립트 대신 **WSL2** 권장(위 절차 그대로). native 면 `.cmd` 래퍼에 `set STITCH_API_KEY=…` 후
`npx -y @_davideast/stitch-mcp proxy` 실행, `claude mcp add stitch -- cmd /c <래퍼>.cmd`.

## 3. 검증·보고
- `claude mcp list` 에서 `stitch` 가 **✔ Connected**.
- 미연결: key 오타 / npx 네트워크 / Node 부재 점검. MCP 반영엔 세션 갱신 필요할 수 있음.

## 함정
- **시크릿**: API key 를 리포트·로그·커밋에 노출 금지. 스크립트는 `~/bin`(repo 밖).
- npx 첫 실행은 패키지 다운로드로 지연 가능.
- `YOUR_STITCH_API_KEY` 미교체면 연결 실패 → 교체 확인.
- **Muse 환경 한계**: 이 환경에서는 프록시 스크립트 생성까지만 자동 수행이 가능하다. `claude mcp add`/`codex mcp add` 같은 CLI 등록은 이 환경에서 지원되지 않으므로, 등록 자체는 사용자가 설정 화면에서 하거나 부모 에이전트에게 위임한다. Codex CLI 전용 등록 흐름은 축소한다.
