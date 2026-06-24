from rest_framework import serializers
from .models import Blog, BlogImage, ContactQuery


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ['id', 'image', 'uploaded_at']


class BlogSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, read_only=True)

    class Meta:
        model = Blog
        fields = [
            'id', 'title', 'slug', 'content', 'excerpt',
            'author', 'category', 'meta_title', 'meta_description', 'schema',
            'is_published', 'created_at', 'updated_at', 'images',
        ]


class BlogSummarySerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Blog
        fields = ['slug', 'title', 'excerpt', 'image']

    def get_image(self, obj):
        first_image = obj.images.first()
        if first_image:
            request = self.context.get('request')
            return request.build_absolute_uri(first_image.image.url) if request else first_image.image.url
        return None


class BlogCreateSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.ImageField(),
        required=False,
        write_only=True,
    )

    class Meta:
        model = Blog
        fields = [
            'title', 'slug', 'content', 'excerpt', 'author',
            'category', 'meta_title', 'meta_description', 'schema',
            'is_published', 'images',
        ]

    def validate_images(self, images):
        if len(images) > 4:
            raise serializers.ValidationError("A blog post can have at most 4 images.")
        return images


class CaseStudySerializer(BlogSerializer):
    class Meta(BlogSerializer.Meta):
        fields = ['content_type', *BlogSerializer.Meta.fields]


class CaseStudySummarySerializer(BlogSummarySerializer):
    class Meta(BlogSummarySerializer.Meta):
        fields = ['content_type', *BlogSummarySerializer.Meta.fields]


class CaseStudyCreateSerializer(BlogCreateSerializer):
    class Meta(BlogCreateSerializer.Meta):
        fields = ['content_type', *BlogCreateSerializer.Meta.fields]


class ContactQueryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactQuery
        fields = ['name', 'email', 'number', 'project_detail']


class ContactQuerySerializer(serializers.ModelSerializer):
    website = serializers.SlugRelatedField(read_only=True, slug_field='slug')

    class Meta:
        model = ContactQuery
        fields = ['id', 'website', 'name', 'email', 'number', 'project_detail', 'created_at']
