from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path  
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('apps.boxes.urls')),
    path('', include('apps.accounts.urls')),
    path('bookings/', include('apps.bookings.urls')),
    path('orders/', include('apps.orders.urls')),
    path('portal/', include('apps.boxes.admin_urls')),
]

# # Cấu hình media để hiển thị ảnh
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# # Cấu hình media để hiển thị ảnh
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    ]
else:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)