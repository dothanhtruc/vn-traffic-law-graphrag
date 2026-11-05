# VN Traffic Law Graph RAG

Hệ thống hỏi đáp Luật Giao thông đường bộ Việt Nam dựa trên Graph RAG, có trích dẫn Điều/Khoản/Điểm
và xét hiệu lực điều khoản theo ngày áp dụng. Đồ án tốt nghiệp — xem `CLAUDE.md` để biết đầy đủ
kiến trúc, quy ước và kế hoạch module.

## Cài đặt

```bash
uv sync
cp .env.example .env   # điền API key
```

Văn bản gốc đặt trong `data/raw/` (không commit).

## Kiểm tra

```bash
uv run ruff check . && uv run ruff format --check .
uv run pytest -q -m "not slow and not gpu"
```
