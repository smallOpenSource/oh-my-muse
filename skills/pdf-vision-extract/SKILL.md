---
name: pdf-vision-extract
description: "비주얼 위주 PDF를 고해상도 per-page PNG로 변환해 레이아웃 손실 없이 비전 입력으로 읽기. 사용자가 'PDF를 이미지로 읽어줘', '디자인 PDF 추출해줘', 'pdf-vision-extract'라고 요청하면 사용."
---

# pdf-vision-extract

## Purpose

UI 목업·화면 디자인·와이어프레임·대시보드·다이어그램이 든 비주얼 위주 PDF를 고해상도 per-page PNG로
변환해, 사람이 보는 그대로 비전 입력으로 읽는다. 텍스트 추출(`pdftotext` 등)로는 의미가 손실되는
경우와, 인라인 Read 한도(10+ 페이지)를 넘는 PDF에 per-page 비전이 필요할 때 쓴다.

**쓰지 않을 때**: 순수 텍스트 PDF(논문·계약서) — `muse.read`의 페이지 범위 지정이 더 빠르다.

왜 이렇게 하나:
1. 명시적 DPI 제어 (네이티브 Read 파이프라인은 기본값 렌더링)
2. 현재 모델 비전 sweet spot에 맞춘 long-edge
3. 페이지를 개별 주소 지정 → 컨텍스트에 필요한 것만 유지

비전 한도(기준): long edge 최대 약 2576px, 초과분은 다운스케일. 목표 **long edge = 2400px**
(캡 바로 아래, 헤드룸 확보). 참고: 고해상도 이미지 1장당 약 4784 토큰, 토큰 계산식 ≈ `width × height / 750`.

## Workflow

### 1. 입력 확인

```bash
ls -lh <pdf-path>
python3 -c "import fitz; d=fitz.open('<pdf-path>'); print('pages=', d.page_count)"
```

### 2. 출력 디렉터리 정하기

관례: 기존 디자인 에셋 옆, PDF 이름 또는 `UI/` 하위 폴더:
- `docs/design/UI/page-001.png` (단일 source-of-truth PDF)
- `docs/design/<pdf-stem>/page-001.png` (복수 PDF)

### 3. 변환 (PyMuPDF — 우선)

PyMuPDF가 가장 신뢰할 단일 의존성 경로(Poppler·ImageMagick 불필요).

```bash
python3 - <<'PY'
import fitz, os
SRC = "<absolute-pdf-path>"
OUT = "<absolute-output-dir>"
TARGET = 2400  # long edge px
os.makedirs(OUT, exist_ok=True)
doc = fitz.open(SRC)
for i, page in enumerate(doc, start=1):
    long_pt = max(page.rect.width, page.rect.height)
    mat = fitz.Matrix(TARGET / long_pt, TARGET / long_pt)
    pix = page.get_pixmap(matrix=mat, alpha=False)
    pix.save(f"{OUT}/page-{i:03d}.png")
    print(f"[{i}/{doc.page_count}] page-{i:03d}.png {pix.width}x{pix.height}")
PY
```

없으면 설치: `python3 -m pip install --user pymupdf`

### 4. 폴백 툴체인

Python/PyMuPDF 불가 시:

| Tool | Command | Notes |
|------|---------|-------|
| `pdftoppm` (poppler-utils) | `pdftoppm -png -r 200 in.pdf out/page` | 가장 빠르고 안정적 |
| `pdf2image` (Python) | wraps pdftoppm | Poppler 바이너리도 필요 |
| ImageMagick | `convert -density 200 in.pdf out/page-%03d.png` | 느리지만 흔함 |

A4 200 DPI ≈ 1654×2339px. long edge ~2400px이면 **220 DPI**로 올린다.

### 5. 검증

```bash
ls <OUT> | wc -l                # 페이지 수 일치 확인
python3 -c "from PIL import Image; im=Image.open('<OUT>/page-001.png'); print(im.size)"
```

long edge ≈ 2400px 기대.

### 6. 페이지 읽기

개별 PNG를 `muse.read`로 읽는다 — 네이티브 비전 입력으로 보인다. 여러 페이지는 한 턴에
여러 `muse.read` 호출을 병렬로 배치한다.

## Output Contract

- `<OUT>/page-001.png` … `page-NNN.png` (N = PDF 페이지 수, long edge ≈ 2400px)
- 검증: 파일 수 == 페이지 수, 샘플 이미지 크기 확인
- 이후 단계(판독·분석)는 변환된 PNG를 비전 입력으로 수행

## Operating Rules

- **색/폰트 문제**: 흔치 않은 임베디드 폰트라도 PyMuPDF가 벡터를 정상 렌더링한다. OCR 불필요.
- **스캔 PDF**: 페이지 자체가 이미지면 소스 비트맵 DPI가 품질 상한 — 렌더 DPI를 올려도 정보가 늘지 않는다. 검색 가능 텍스트도 필요하면 먼저 `ocrmypdf`.
- **매우 길거나 넓은 페이지**(긴 스크롤 디자인): long-edge clamp가 디테일을 축소할 수 있다. 렌더링 전 세로 타일로 나누는 것을 고려한다.
- **저장소**: 2400px PNG는 장당 ~0.5–1.5MB. 100페이지 UI 덱 ≈ 100MB. 추적하지 않을 거면 출력 디렉터리 하위의 `*.png`를 `.gitignore`에 추가한다.
- **하이브리드 파이프라인(선택)**: 비주얼 + 검색 가능 텍스트가 함께 필요하면 markdown도 추출한다:

```bash
python3 -m pip install --user pymupdf4llm
python3 -c "import pymupdf4llm; print(pymupdf4llm.to_markdown('<pdf>'))" > <OUT>/text.md
```

`.md`에서 라벨을 grep하고 PNG와 교차 참조한다.

- 한계: 이 VM에 `pymupdf`가 없으면 `pip install --user pymupdf`가 선행되어야 한다(네트워크 필요). 오프라인이면 §4 폴백(`pdftoppm` 등 시스템 도구)을 쓴다.
