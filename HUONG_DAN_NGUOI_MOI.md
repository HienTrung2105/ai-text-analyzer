# Hướng dẫn AI Text Analyzer cho người làm đồ án lần đầu

Tài liệu này dành cho bạn nếu đây là lần đầu làm backend, API, database và Docker. Không cần học hết mọi thứ rồi mới bắt đầu. Hãy đọc từng phần, chạy được ví dụ, sau đó mới chuyển sang phần tiếp theo.

## 1. Đồ án này thực sự làm gì?

Người dùng gửi một đoạn văn bản. Backend chuyển văn bản đó cho AI. AI trả về:

- bản tóm tắt;
- cảm xúc: tích cực, trung lập hoặc tiêu cực;
- các từ khóa quan trọng.

Backend lưu cả văn bản và kết quả vào PostgreSQL, sau đó trả kết quả cho người dùng.

```text
Postman/Frontend
      |
      | HTTP + JSON
      v
FastAPI backend -----> OpenAI API
      |
      v
PostgreSQL
```

Hãy nhớ câu ngắn này: **client gửi request → backend xử lý → AI phân tích → database lưu → backend trả response**.

## 2. Những nền tảng cần hiểu

### 2.1 Python

Python là ngôn ngữ được dùng để viết backend. Trước mắt bạn chỉ cần hiểu:

- biến: `name = "An"`;
- hàm: `def analyze(text): ...`;
- class: khuôn mẫu mô tả một loại dữ liệu;
- import: dùng code từ file hoặc thư viện khác;
- exception: lỗi xảy ra khi chương trình chạy.

Ví dụ:

```python
def count_characters(text: str) -> int:
    return len(text)


result = count_characters("Xin chào")
print(result)
```

Bạn chưa cần học Python nâng cao như decorator, metaclass hoặc thuật toán phức tạp.

### 2.2 Client và server

- **Client** là nơi gửi yêu cầu: Postman, trình duyệt hoặc frontend.
- **Server/backend** nhận yêu cầu, chạy logic và trả kết quả.

Trong đồ án này, FastAPI là server. Postman hoặc Swagger là client dùng để kiểm thử.

### 2.3 HTTP và API

API là cách các chương trình nói chuyện với nhau. Một request thường có:

- method: hành động muốn thực hiện;
- URL: địa chỉ endpoint;
- headers: thông tin bổ sung;
- body: dữ liệu gửi lên.

Các method cần biết:

| Method | Ý nghĩa thường dùng | Ví dụ trong project |
|---|---|---|
| GET | Lấy dữ liệu | `GET /analyses` |
| POST | Tạo/xử lý dữ liệu mới | `POST /analyze` |
| PUT/PATCH | Cập nhật dữ liệu | Chưa có |
| DELETE | Xóa dữ liệu | Chưa có |

Các status code quan trọng:

| Code | Ý nghĩa |
|---|---|
| 200 | Thành công |
| 201 | Đã tạo dữ liệu thành công |
| 422 | Dữ liệu gửi lên không hợp lệ |
| 500 | Server gặp lỗi |
| 502 | Backend không lấy được kết quả hợp lệ từ dịch vụ AI |

### 2.4 JSON

JSON là định dạng trao đổi dữ liệu phổ biến của API.

Request gửi tới `/analyze`:

```json
{
  "text": "Hôm nay tôi học FastAPI và cảm thấy rất hào hứng."
}
```

Response dự kiến:

```json
{
  "summary": "Người viết đang hào hứng khi học FastAPI.",
  "sentiment": "positive",
  "keywords": ["FastAPI", "học tập", "hào hứng"],
  "id": 1,
  "input_text": "Hôm nay tôi học FastAPI và cảm thấy rất hào hứng.",
  "model": "gpt-6-luna",
  "created_at": "2026-10-21T10:00:00Z"
}
```

JSON dùng dấu ngoặc kép cho tên thuộc tính và chuỗi. Không được có dấu phẩy thừa ở phần tử cuối.

### 2.5 Database và PostgreSQL

Database lưu dữ liệu để khi server tắt rồi mở lại, lịch sử vẫn còn. PostgreSQL là hệ quản trị database được dùng trong đồ án.

Project có bảng `analyses`. Có thể hình dung bảng như Excel:

| id | input_text | summary | sentiment | keywords | model | created_at |
|---|---|---|---|---|---|---|
| 1 | Văn bản gốc | Bản tóm tắt | positive | danh sách từ khóa | tên model | thời gian |

- Một hàng là một lần phân tích.
- Một cột là một thuộc tính.
- `id` dùng để phân biệt từng bản ghi.

SQLAlchemy là thư viện giúp code Python làm việc với database mà không phải viết toàn bộ câu lệnh SQL bằng tay.

### 2.6 Biến môi trường và API key

Thông tin bí mật không được viết trực tiếp trong source code. Project đọc chúng từ file `.env`.

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/text_analyzer
OPENAI_API_KEY=sk-key-cua-ban
OPENAI_MODEL=gpt-6-luna
```

File `.env` đã nằm trong `.gitignore`. Tuyệt đối không gửi API key lên GitHub, ảnh chụp màn hình hoặc báo cáo.

### 2.7 Docker

Ứng dụng thường cần đúng phiên bản Python, thư viện và database. Docker đóng gói môi trường này thành container để chạy giống nhau trên nhiều máy.

Trong `compose.yml` có hai service:

- `api`: backend FastAPI;
- `db`: PostgreSQL.

Docker Compose khởi động cả hai và tạo mạng nội bộ để chúng kết nối với nhau.

## 3. Làm quen với cấu trúc project

```text
ai-text-analyzer/
├── app/
│   ├── api/routes.py
│   ├── services/ai_service.py
│   ├── config.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── tests/test_api.py
├── .env.example
├── compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

Đọc file theo thứ tự sau:

1. `app/main.py`: nơi ứng dụng được tạo và gắn các route.
2. `app/api/routes.py`: định nghĩa URL và xử lý request.
3. `app/schemas.py`: quy định JSON vào/ra phải có hình dạng nào.
4. `app/services/ai_service.py`: gửi văn bản tới OpenAI.
5. `app/models.py`: mô tả bảng `analyses`.
6. `app/database.py`: tạo kết nối database.
7. `app/config.py`: đọc cấu hình từ `.env`.

Đừng cố hiểu mọi dòng ngay lần đầu. Mục tiêu đầu tiên là trả lời được: “file này chịu trách nhiệm gì?”.

## 4. Chuẩn bị máy

Bạn nên có:

1. Visual Studio Code để đọc và sửa code.
2. Docker Desktop để chạy backend và PostgreSQL.
3. Postman để gọi API; có thể dùng Swagger thay Postman lúc đầu.
4. Một OpenAI API key có billing/quota phù hợp.

Kiểm tra trong PowerShell:

```powershell
python --version
docker --version
docker compose version
```

Máy hiện đã nhận lệnh `python`, nhưng tại thời điểm tạo tài liệu chưa nhận lệnh `docker`. Vì vậy bạn cần cài và mở Docker Desktop trước khi chạy project bằng Docker.

## 5. Chạy project lần đầu

### Bước 1: Mở thư mục

```powershell
cd D:\ai-text-analyzer
code .
```

Nếu lệnh `code` chưa hoạt động, mở VS Code và chọn **File → Open Folder**, sau đó chọn `D:\ai-text-analyzer`.

### Bước 2: Tạo file cấu hình

```powershell
Copy-Item .env.example .env
notepad .env
```

Thay giá trị `OPENAI_API_KEY` bằng key thật rồi lưu file.

### Bước 3: Khởi động

Đảm bảo Docker Desktop đang chạy, sau đó:

```powershell
docker compose up --build
```

Lần đầu sẽ lâu hơn vì Docker phải tải image và cài thư viện. Khi thấy Uvicorn chạy trên cổng 8000, đừng đóng cửa sổ PowerShell đó.

### Bước 4: Kiểm tra Swagger

Mở trình duyệt tại:

```text
http://localhost:8000/docs
```

Thử theo thứ tự:

1. Chọn `GET /health`.
2. Nhấn **Try it out**.
3. Nhấn **Execute**.
4. Nếu nhận `{"status":"ok"}`, server đang hoạt động.
5. Chọn `POST /analyze` và gửi một đoạn văn ngắn.
6. Chọn `GET /analyses` để xem bản ghi đã được lưu.

### Bước 5: Dừng project

Nhấn `Ctrl+C` tại terminal đang chạy, sau đó:

```powershell
docker compose down
```

Lệnh trên dừng container nhưng giữ dữ liệu PostgreSQL. Nếu dùng `docker compose down -v`, volume database sẽ bị xóa; chưa nên dùng khi bạn còn cần dữ liệu.

## 6. Theo dõi một request trong source code

Khi gửi `POST /analyze`, luồng chạy như sau:

1. FastAPI tìm hàm `analyze()` trong `app/api/routes.py`.
2. `AnalyzeRequest` trong `app/schemas.py` kiểm tra trường `text`.
3. Route gọi `analyze_with_ai()` trong `app/services/ai_service.py`.
4. AI service gọi OpenAI Responses API và chuyển JSON thành `AnalysisResult`.
5. Route tạo một object `Analysis` theo model trong `app/models.py`.
6. SQLAlchemy ghi object đó vào PostgreSQL.
7. FastAPI chuyển object thành JSON và trả cho client.

Đây là phần quan trọng nhất để thuyết trình đồ án. Hãy tập giải thích lại bằng lời của bạn mà không nhìn tài liệu.

## 7. Bài tập làm quen theo mức độ

### Bài 1: Đổi tên ứng dụng

Mở `.env` và đổi:

```env
APP_NAME=Do An Phan Tich Van Ban Cua Toi
```

Khởi động lại project và xem tên trên Swagger.

### Bài 2: Thử validation

Gửi body có `text` rỗng:

```json
{
  "text": ""
}
```

Quan sát status `422`. Sau đó tìm `min_length=1` trong `app/schemas.py` để hiểu nguyên nhân.

### Bài 3: Đổi giới hạn lịch sử

Gọi:

```text
GET /analyses?limit=5
```

Sau đó tìm biến `limit` trong `app/api/routes.py`.

### Bài 4: Thêm trường độ dài văn bản

Khi đã hiểu project, thử thêm cột `character_count`:

1. thêm trường vào model database;
2. thêm trường vào response schema;
3. tính bằng `len(payload.text)`;
4. lưu cùng bản ghi;
5. cập nhật test.

Đây là bài tập tốt để hiểu quan hệ giữa schema, model và route.

### Bài 5: Thêm endpoint lấy một bản ghi

Mục tiêu:

```text
GET /analyses/1
```

Nếu không tìm thấy `id`, trả status `404`.

## 8. Chạy test

Test giúp biết thay đổi mới có làm hỏng tính năng cũ hay không.

Nếu chạy test ngoài Docker:

```powershell
cd D:\ai-text-analyzer
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Test hiện dùng SQLite và hàm AI giả, nên không gọi OpenAI thật và không tốn token.

Khi làm xong một thay đổi nhỏ, hãy chạy test trước khi chuyển sang phần khác.

## 9. Những lỗi người mới thường gặp

### `docker` is not recognized

Docker Desktop chưa được cài, chưa chạy hoặc terminal chưa được mở lại sau khi cài.

### Không mở được `localhost:8000`

Kiểm tra terminal có báo lỗi không và Docker Desktop có đang chạy không:

```powershell
docker compose ps
docker compose logs api
```

### PostgreSQL chưa sẵn sàng

Xem log database:

```powershell
docker compose logs db
```

Service `api` đã được cấu hình chờ healthcheck của `db`, nhưng database vẫn có thể lỗi nếu thiếu dung lượng hoặc Docker gặp vấn đề.

### `OPENAI_API_KEY chưa được cấu hình`

Kiểm tra file có tên chính xác là `.env`, không phải `.env.txt`, và key không còn là giá trị mẫu.

### OpenAI trả lỗi quota hoặc authentication

- kiểm tra key có đúng không;
- kiểm tra tài khoản API có quota/billing không;
- không nhầm gói ChatGPT với OpenAI API billing;
- không đăng key vào nơi công khai.

### Port 8000 đã được sử dụng

Đổi phần ports trong `compose.yml`, ví dụ:

```yaml
ports:
  - "8001:8000"
```

Sau đó truy cập `http://localhost:8001/docs`.

## 10. Lộ trình học 7 buổi

### Buổi 1: Python cơ bản

Học biến, kiểu dữ liệu, list, dict, `if`, vòng lặp, hàm và import. Viết vài hàm xử lý chuỗi.

### Buổi 2: HTTP, JSON và FastAPI

Hiểu GET/POST, request/response, status code. Chạy `/health` và tạo một endpoint thử nghiệm.

### Buổi 3: Pydantic và cấu trúc project

Đọc `schemas.py`, thử request đúng/sai và theo dõi luồng `/analyze`.

### Buổi 4: PostgreSQL và SQLAlchemy

Hiểu bảng, hàng, cột, khóa chính. Gửi vài request rồi xem lịch sử bằng `/analyses`.

### Buổi 5: OpenAI API

Đọc prompt trong `ai_service.py`, thử nhiều loại văn bản và so sánh kết quả. Theo dõi chi phí API.

### Buổi 6: Docker và test

Hiểu image, container, volume và service. Chạy `pytest`, sửa một tính năng nhỏ rồi test lại.

### Buổi 7: Deploy và chuẩn bị báo cáo

Deploy backend, cấu hình database/secret, gọi URL công khai bằng Postman và chuẩn bị sơ đồ kiến trúc.

## 11. Checklist trước khi deploy

- [ ] `/health` hoạt động.
- [ ] `/analyze` trả kết quả hợp lệ.
- [ ] `/analyses` hiển thị dữ liệu đã lưu.
- [ ] API key không nằm trong Git.
- [ ] Test chạy thành công.
- [ ] Docker build thành công.
- [ ] Có xử lý trường hợp AI hoặc database lỗi.
- [ ] Biết cách xem log.
- [ ] Chuẩn bị biến môi trường trên cloud.
- [ ] Sau deploy đã thử URL public bằng Postman.

## 12. Cách trình bày đồ án

Bạn có thể trình bày theo thứ tự:

1. **Bài toán:** người dùng cần phân tích nhanh một đoạn văn.
2. **Giải pháp:** FastAPI nhận dữ liệu, OpenAI phân tích, PostgreSQL lưu lịch sử.
3. **Kiến trúc:** trình bày sơ đồ client → backend → AI/database.
4. **Demo:** gọi `/analyze`, xem response, sau đó gọi `/analyses`.
5. **Docker:** giải thích cách đóng gói backend và database.
6. **Cloud:** cho thấy cùng API hoạt động bằng URL công khai.
7. **Hạn chế:** chi phí AI, phụ thuộc mạng, chưa có đăng nhập và rate limit.
8. **Hướng phát triển:** frontend, authentication, dashboard, thống kê và nhiều loại phân tích hơn.

## 13. Từ điển nhanh

| Thuật ngữ | Giải thích ngắn |
|---|---|
| Backend | Phần xử lý phía server |
| Endpoint | Một URL cung cấp chức năng API |
| Request | Dữ liệu client gửi đến server |
| Response | Dữ liệu server trả về |
| Schema | Quy định hình dạng dữ liệu |
| Model | Mô tả dữ liệu hoặc bảng database |
| ORM | Cách thao tác database bằng object trong code |
| Migration | Theo dõi thay đổi cấu trúc database |
| Container | Môi trường cô lập chạy ứng dụng |
| Image | Khuôn dùng để tạo container |
| Volume | Nơi Docker lưu dữ liệu lâu dài |
| Environment variable | Cấu hình nằm ngoài source code |
| API key | Chuỗi bí mật dùng để xác thực với dịch vụ API |
| Deploy | Đưa ứng dụng lên server/cloud để người khác truy cập |

## 14. Nguyên tắc học project này

1. Chạy được trước, hiểu từng phần sau.
2. Mỗi lần chỉ sửa một thay đổi nhỏ.
3. Đọc thông báo lỗi từ dòng cuối rồi lần ngược lên.
4. Sau mỗi thay đổi, gọi API và chạy test.
5. Không copy code mà không biết file đó chịu trách nhiệm gì.
6. Không đưa secret lên GitHub.
7. Ghi lại lỗi và cách sửa; phần này rất hữu ích khi viết báo cáo.

Mốc đầu tiên của bạn không phải là deploy. Mốc đầu tiên là tự chạy được `/health`, sau đó tự gửi được một request `/analyze` và giải thích được dữ liệu đã đi qua những file nào.

