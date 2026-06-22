from django.urls import path
from .views import (
    BlogListCreateView,
    BlogDetailView,
    CaseStudyListCreateView,
    CaseStudyDetailView,
    ckeditor_image_upload,
)

urlpatterns = [
    path('<slug:website_slug>/blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('<slug:website_slug>/blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
    path('<slug:website_slug>/case-studies/', CaseStudyListCreateView.as_view(), name='case-study-list-create'),
    path('<slug:website_slug>/case-studies/<slug:slug>/', CaseStudyDetailView.as_view(), name='case-study-detail'),
    path('ckeditor5/image_upload/', ckeditor_image_upload, name='ckeditor-image-upload'),
]
