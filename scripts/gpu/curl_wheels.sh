#!/usr/bin/env bash
# Chạy TRÊN MÁY THUÊ (gpu.sh setup --curl-wheels gửi script này qua stdin): cài venv dự án từ danh
# sách wheel do scripts/gpu/wheel_urls.py sinh ở local (url<TAB>sha256<TAB>tên file).
#
#   bash -s -- <thư mục repo> <wheels.tsv>
#
# Lý do (M10, 14/11/2026): uv sync trên aidev tải PyPI ~1 MB/s, curl cùng CDN ~67 MB/s. Wheel đã
# tải giữ ở ~/.cache/graphrag/wheels (chạy lại không tải lại); sha256 sai → dừng.
set -euo pipefail
R="$1"
TSV="$2"
W="$HOME/.cache/graphrag/wheels"
mkdir -p "$W"
export PATH="$HOME/.local/bin:$PATH"
tr -d '\r' < "$TSV" > "$TSV.lf"   # file sinh trên Windows có thể có CR
n=$(wc -l < "$TSV.lf")
echo "curl-wheels: $n wheel → $W"
if command -v aria2c >/dev/null; then
    # Phiên GPU 7 (17/11/2026): curl nghẽn ~100 KB/s/kết nối với file lớn (cuBLAS, triton);
    # aria2c 16 kết nối/file tải xong trong vài giây. -c: tải tiếp file dở / bỏ qua file đã đủ.
    awk -F'\t' -v w="$W" '{print $1; print "  out=" $3; print "  dir=" w}' "$TSV.lf" > "$TSV.aria"
    aria2c -q -c -x16 -s16 -j4 --auto-file-renaming=false --max-tries=5 -i "$TSV.aria"
else
    awk -F'\t' -v w="$W" '{print $1; print w "/" $3}' "$TSV.lf" |
        paste - - |
        while IFS=$'\t' read -r u f; do [ -s "$f" ] || printf '%s\n%s\n' "$u" "$f"; done |
        xargs -r -d '\n' -n 2 -P 8 sh -c 'curl -fsSL --retry 3 -o "$1.part" "$0" && mv "$1.part" "$1"'
fi
awk -F'\t' -v w="$W" '{print $2 "  " w "/" $3}' "$TSV.lf" | sha256sum -c --quiet -
echo "curl-wheels: sha256 khớp"
cd "$R"
[ -x .venv/bin/python ] || uv venv -q --python 3.11 .venv
awk -F'\t' -v w="$W" '{print w "/" $3}' "$TSV.lf" |
    xargs uv pip install -q --python .venv/bin/python --no-index --no-deps
# Chính dự án (editable, không kéo dependency; hatchling tải từ index — gói nhỏ).
uv pip install -q --python .venv/bin/python --no-deps -e .
echo "curl-wheels: xong — chạy job bằng: uv run --no-sync python -m …"
