from django.urls import path
from .views import BlogListCreateView, BlogDetailView

urlpatterns = [
    path('<slug:website_slug>/blogs/', BlogListCreateView.as_view(), name='blog-list-create'),
    path('<slug:website_slug>/blogs/<slug:slug>/', BlogDetailView.as_view(), name='blog-detail'),
]
