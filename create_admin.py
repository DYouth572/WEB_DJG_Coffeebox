import os
import django

# Khởi chạy cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Thông tin tài khoản bạn muốn tạo (Có thể sửa lại theo ý bạn)
username = 'admin'
email = 'admin@vat.com'
password = 'quanly01'  # Nên đặt mật khẩu có cả chữ hoa, chữ thường và số

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(">>> Đã tạo tài khoản Superuser thành công!")
else:
    print(">>> Tài khoản Admin đã tồn tại từ trước.")
