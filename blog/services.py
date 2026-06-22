from django.shortcuts import get_object_or_404
from .models import Blog, BlogImage, Website


MAX_IMAGES_PER_BLOG = 4


def get_website_by_slug(website_slug: str) -> Website:
    return get_object_or_404(Website, slug=website_slug)


def get_all_blogs(website: Website, content_type: str = Blog.BLOG):
    return Blog.objects.filter(
        website=website,
        content_type=content_type,
        is_published=True,
    ).prefetch_related('images')


def get_blog_by_slug(website: Website, slug: str, content_type: str = Blog.BLOG) -> Blog:
    return get_object_or_404(
        Blog,
        website=website,
        slug=slug,
        content_type=content_type,
        is_published=True,
    )


def create_blog(validated_data: dict, images: list, website: Website, content_type: str = Blog.BLOG) -> Blog:
    if len(images) > MAX_IMAGES_PER_BLOG:
        raise ValueError(f"A blog post can have at most {MAX_IMAGES_PER_BLOG} images.")

    validated_data['content_type'] = content_type
    blog = Blog.objects.create(website=website, **validated_data)

    for image in images:
        BlogImage.objects.create(blog=blog, image=image)

    return blog


def update_blog(blog: Blog, validated_data: dict, images: list, partial: bool = False) -> Blog:
    if images and len(images) > MAX_IMAGES_PER_BLOG:
        raise ValueError(f"A blog post can have at most {MAX_IMAGES_PER_BLOG} images.")

    for attr, value in validated_data.items():
        setattr(blog, attr, value)
    blog.save()

    if images:
        blog.images.all().delete()
        for image in images:
            BlogImage.objects.create(blog=blog, image=image)

    return blog


def delete_blog(blog: Blog) -> None:
    blog.delete()
