# AI Text Analyzer

Backend FastAPI nhận một đoạn văn bản, gọi OpenAI API để tóm tắt/phân tích cảm xúc/trích từ khóa, sau đó lưu kết quả vào PostgreSQL.

Nếu đây là lần đầu bạn làm đồ án backend, hãy đọc `HUONG_DAN_NGUOI_MOI.md` trước rồi quay lại README này để chạy project.

## Kiến trúc

```text
Client/Postman
      |
      v
FastAPI: POST /analyze -----> OpenAI Responses API
      |
      v
PostgreSQL: bảng analyses
```

## Cấu trúc thư mục

```text
ai-text-analyzer/
├── app/
│   ├── api/routes.py          # Endpoint HTTP
│   ├── services/ai_service.py # Gọi AI API
│   ├── config.py              # Đọc biến môi trường
│   ├── database.py            # Kết nối SQLAlchemy
│   ├── models.py              # Bảng PostgreSQL
│   ├── schemas.py             # Kiểm tra request/response
│   └── main.py                # Khởi tạo FastAPI
├── tests/test_api.py
├── compose.yml
├── Dockerfile
└── .env.example
```

## 1. Chuẩn bị

Cài Docker Desktop và tạo OpenAI API key. Sao chép file môi trường trong PowerShell:

```powershell
cd D:\ai-text-analyzer
Copy-Item .env.example .env
notepad .env
```

Thay `replace-with-your-openai-api-key` bằng key thật. Không commit file `.env` lên Git.
Mặc định dự án dùng `gpt-6-luna`, model gọn và tiết kiệm cho tác vụ phân tích văn bản; bạn có thể đổi bằng biến `OPENAI_MODEL`.

## 2. Chạy bằng Docker

```powershell
docker compose up --build
```

Mở Swagger UI tại <http://localhost:8000/docs>. Kiểm tra nhanh:

```powershell
Invoke-RestMethod http://localhost:8000/health
```

## 3. Gọi endpoint `/analyze`

Trong Postman:

- Method: `POST`
- URL: `http://localhost:8000/analyze`
- Body → raw → JSON

```json
{
  "text": "FastAPI giúp xây dựng API bằng Python nhanh và rõ ràng."
}
```

Hoặc dùng PowerShell:

```powershell
$body = @{ text = "FastAPI giúp xây dựng API bằng Python nhanh và rõ ràng." } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8000/analyze -ContentType "application/json" -Body $body
```

Xem lịch sử gần nhất:

```powershell
Invoke-RestMethod http://localhost:8000/analyses
```

## 4. Chạy test cục bộ

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -q
```

Test dùng SQLite và giả lập AI, vì vậy không tốn token và không cần PostgreSQL/OpenAI key.

## 5. Hiểu luồng xử lý

1. Pydantic kiểm tra `text` dài từ 1 đến 10.000 ký tự.
2. `ai_service.py` gọi OpenAI Responses API.
3. AI trả JSON gồm `summary`, `sentiment`, `keywords`.
4. SQLAlchemy ghi kết quả vào bảng `analyses`.
5. FastAPI trả bản ghi vừa tạo cho client.

## 6. Lộ trình hoàn thiện đồ án

1. Chạy local và chụp Swagger/Postman cho báo cáo.
2. Thêm Alembic để quản lý migration database.
3. Thêm API key/JWT cho người dùng của chính ứng dụng.
4. Thêm rate limit, logging và xử lý retry khi AI lỗi.
5. Viết frontend đơn giản gọi URL public.
6. Deploy API và PostgreSQL lên nền tảng cloud; đặt `DATABASE_URL`, `OPENAI_API_KEY`, `OPENAI_MODEL` trong secret/env của nền tảng.
7. Thay URL localhost trong Postman/frontend bằng URL cloud và kiểm thử lại.

## API hiện có

| Method | Path | Mục đích |
|---|---|---|
| GET | `/health` | Kiểm tra server |
| POST | `/analyze` | Phân tích và lưu văn bản |
| GET | `/analyses?limit=20` | Xem lịch sử |

## Ghi chú triển khai

- Docker image chỉ đóng gói backend; PostgreSQL chạy ở service `db` khi phát triển.
- Khi deploy production, ưu tiên PostgreSQL managed và không đưa mật khẩu/key vào source code.
- Skeleton dùng `create_all` để học nhanh. Trước khi làm production, chuyển sang Alembic migration.
- OpenAI API có chi phí riêng; đặt giới hạn độ dài và theo dõi usage.
- Cách gọi AI theo [OpenAI Responses API](https://developers.openai.com/api/reference/python/resources/responses/methods/create); model mặc định theo [tài liệu GPT-6 Luna](https://developers.openai.com/api/docs/models/gpt-6-luna).

