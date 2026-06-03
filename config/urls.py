from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from blog.views import ckeditor_image_upload

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('blog.urls')),
    path('ckeditor5/image_upload/', ckeditor_image_upload, name='ck_editor_5_upload_file'),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
