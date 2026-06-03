import cloudinary
import cloudinary.uploader
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import BlogSerializer, BlogSummarySerializer, BlogCreateSerializer
from . import services


@staff_member_required
@require_POST
def ckeditor_image_upload(request):
    image = request.FILES.get('upload')
    if not image:
        return JsonResponse({'error': {'message': 'No image provided'}}, status=400)

    cloudinary_config = settings.CLOUDINARY_STORAGE
    cloudinary.config(
        cloud_name=cloudinary_config['CLOUD_NAME'],
        api_key=cloudinary_config['API_KEY'],
        api_secret=cloudinary_config['API_SECRET'],
    )

    image.seek(0)
    result = cloudinary.uploader.upload(image, folder='blog_inline_images')
    return JsonResponse({'url': result['secure_url']})


class BlogListCreateView(APIView):

    def get(self, request, website_slug):
        website = services.get_website_by_slug(website_slug)
        blogs = services.get_all_blogs(website)
        serializer = BlogSummarySerializer(blogs, many=True, context={'request': request})
        return Response(serializer.data)

    def post(self, request, website_slug):
        website = services.get_website_by_slug(website_slug)
        serializer = BlogCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        images = serializer.validated_data.pop('images', [])
        blog_data = serializer.validated_data

        try:
            blog = services.create_blog(blog_data, images, website)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(
            BlogSerializer(blog, context={'request': request}).data,
            status=status.HTTP_201_CREATED,
        )


class BlogDetailView(APIView):

    def get(self, request, website_slug, slug):
        website = services.get_website_by_slug(website_slug)
        blog = services.get_blog_by_slug(website, slug)
        serializer = BlogSerializer(blog, context={'request': request})
        return Response(serializer.data)

    def put(self, request, website_slug, slug):
        website = services.get_website_by_slug(website_slug)
        blog = services.get_blog_by_slug(website, slug)
        serializer = BlogCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        images = serializer.validated_data.pop('images', [])

        try:
            blog = services.update_blog(blog, serializer.validated_data, images)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(BlogSerializer(blog, context={'request': request}).data)

    def patch(self, request, website_slug, slug):
        website = services.get_website_by_slug(website_slug)
        blog = services.get_blog_by_slug(website, slug)
        serializer = BlogCreateSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        images = serializer.validated_data.pop('images', [])

        try:
            blog = services.update_blog(blog, serializer.validated_data, images, partial=True)
        except ValueError as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(BlogSerializer(blog, context={'request': request}).data)

    def delete(self, request, website_slug, slug):
        website = services.get_website_by_slug(website_slug)
        blog = services.get_blog_by_slug(website, slug)
        services.delete_blog(blog)
        return Response(status=status.HTTP_204_NO_CONTENT)
