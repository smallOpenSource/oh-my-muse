#!/bin/bash
# 텍스트 파일의 UTF-8 유효성 검사. push 전 실행: bash scripts/check-utf8.sh
# 종료 코드 0 = 전부 정상, 1 = 깨진 파일 존재
bad=0
while IFS= read -r -d '' f; do
  if ! python3 -c "open('$f', encoding='utf-8', errors='strict').read()" 2>/dev/null; then
    echo "BROKEN: $f"; bad=1
  fi
done < <(git ls-files -z '*.md' '*.txt' '*.json' '*.yaml' '*.yml')
[ $bad -eq 0 ] && echo "UTF-8 OK"
exit $bad
