# Vạt Coffee Box

Ứng dụng quản lý đặt không gian (box) và gọi món cho Vạt Coffee — một dự án Django nhỏ gọn dành cho quản lý đặt phòng, quản lý thực đơn, và theo dõi đơn gọi món.

---

**Ngôn ngữ:** Tiếng Việt

## Tổng quan

Ứng dụng bao gồm các module chính:

- `apps.accounts` - Quản lý người dùng, role (`customer`, `staff`, `admin`), avatar.
- `apps.boxes` - Quản lý các Box (không gian), loại box, trạng thái, hình ảnh.
- `apps.bookings` - Luồng đặt box, trạng thái đặt (pending/confirmed/active/completed/cancelled), yêu cầu hỗ trợ.
- `apps.orders` - Sản phẩm (menu), đơn gọi món và chi tiết món.

Giao diện người dùng (client) đã hoàn thiện theo phong cách thương hiệu (màu nâu ấm). Thư mục template admin/staff được bổ sung để nhanh triển khai giao diện quản trị theo cùng tông màu.

## Yêu cầu hệ thống

- Python 3.10+ (hoặc 3.8+ tương thích với Django 4.2+)
- SQLite (mặc định) hoặc bất kỳ DB Django hỗ trợ

## Cài đặt nhanh (Local)

1. Clone repo và chuyển vào thư mục dự án:

```
git clone <repo-url>
cd vat_coffee_box
```

2. Tạo virtual environment và kích hoạt (Windows PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Cài đặt phụ thuộc:

```bash
pip install -r requirements.txt
```

4. Tạo file cấu hình môi trường (tuỳ chọn):

 - Nếu muốn dùng biến môi trường, tạo `.env` ở gốc dự án và đặt `SECRET_KEY`, `DEBUG`, `ALLOWED_HOSTS`...

5. Chạy migrate và tạo superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
```

6. Chạy server phát triển:

```bash
python manage.py runserver
```

Mở trình duyệt: http://127.0.0.1:8000

## Cấu trúc chính của dự án

- `manage.py` — entry point của Django.
- `config/` — cài đặt Django, `settings.py`, `urls.py`, `wsgi.py`, `asgi.py`.
- `apps/` — các Django apps: `accounts`, `boxes`, `bookings`, `orders`.
- `templates/` — chứa các template người dùng và portal quản trị.
  - `templates/portal/` — giao diện portal admin/staff hiện đang được sử dụng.
- `static/` — chứa CSS, images. Style chính: [static/css/style.css](static/css/style.css)
- `media/` — ảnh tải lên (avatars, boxes, products).

## Sử dụng Docker

Dự án đã có cấu hình Docker cơ bản để đóng gói và gửi cho người khác.

- `Dockerfile` — xây image Django với `gunicorn`.
- `docker-compose.yml` — chạy container ứng dụng.
- `.dockerignore` — loại trừ file không cần thiết khỏi image.
- `.env.example` — mẫu cấu hình môi trường.

### Chạy bằng Docker

```bash
docker build -t vat_coffee_box .
docker run -d -p 8000:8000 --name vat_coffee_box -v %cd%/media:/app/media vat_coffee_box
```

Hoặc với Docker Compose:

```bash
docker-compose up --build
```

### Lưu ý

- Sao chép `.env.example` thành `.env` nếu cần cấu hình môi trường.
- `staticfiles/` là thư mục do `collectstatic` tạo ra khi deploy.

## Các lệnh hữu ích

- Chạy server dev: `python manage.py runserver`
- Migrate DB: `python manage.py migrate`
- Tạo superuser: `python manage.py createsuperuser`
- Tải file tĩnh (production): `python manage.py collectstatic`

## Cấu hình media & static

- `MEDIA_ROOT` mặc định là `media/` (được cấu hình trong `config/settings.py`).
- `STATICFILES_DIRS` trỏ tới `static/`.

Khi debug bật (`DEBUG = True`) các media file được phục vụ bởi Django (setting static URLs được cấu hình trong `config/urls.py`).

## Notes về code hiện tại

- Model user ở `apps/accounts/models.py` mở rộng `AbstractUser` và thêm `role`, `phone`, `avatar`.
- Booking tự động tính `total_price` trong `save()` và có method `remaining_seconds` để hiển thị đồng hồ đếm ngược.
- Views chịu trách nhiệm cập nhật trạng thái booking theo thời gian (ví dụ: chuyển sang `active` khi bắt đầu, `completed` khi quá giờ).

## Triển khai (Production) - gợi ý

1. Sử dụng một WSGI server như `gunicorn` (có trong `requirements.txt`).
2. Dùng `whitenoise` để phục vụ static files, hoặc cấu hình CDN / nginx.
3. Thiết lập biến môi trường an toàn (SECRET_KEY, DEBUG=False, ALLOWED_HOSTS).
4. Sử dụng một RDBMS (Postgres) cho production khi cần hiệu năng / đồng thời.

## Kiểm thử

- Dự án bao gồm các file `tests.py` trong mỗi app. Chạy:

```bash
python manage.py test
```

## Mở rộng & Gợi ý phát triển

- Tạo APIs (Django REST Framework) nếu cần mobile app hoặc SPA frontend.
- Thêm phân quyền chi tiết cho `staff` bằng `groups` hoặc permission custom.
- Tối ưu hóa logic booking bằng cron job / celery để xử lý trạng thái (thay vì cập nhật trong view khi người dùng truy cập).

## Liên hệ

Nếu cần hỗ trợ thêm (thiết kế UI admin/staff responsive, thêm API hoặc deploy), cho tôi biết để tôi triển khai bước tiếp theo.

---

File liên quan nhanh:

- [manage.py](manage.py)
- [requirements.txt](requirements.txt)
- [config/settings.py](config/settings.py)
- [templates/admin/base.html](templates/admin/base.html)
