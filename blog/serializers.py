from rest_framework import serializers
from .models import Blog, BlogImage


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'uploaded_at']


class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content',
            'author', 'category', 'is_published',
            'created_at', 'updated_at', 'images',
        ]


class BlogCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'author', 'category', 'is_published', 'images']

    def validate_images(self, images):
        if len(images) > 4:
            raise serializers.ValidationError("A blog post can have at most 4 images.")
        return images
