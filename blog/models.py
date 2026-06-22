from django.db import models
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field


class Website(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Blog(models.Model):
    BLOG = 'blog'
    CASE_STUDY = 'case_study'
    CONTENT_TYPE_CHOICES = [
        (BLOG, 'Blog'),
        (CASE_STUDY, 'Case Study'),
    ]

    website = models.ForeignKey(Website, on_delete=models.CASCADE, related_name='blogs')
    content_type = models.CharField(max_length=20, choices=CONTENT_TYPE_CHOICES, default=BLOG)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    content = CKEditor5Field(config_name='default')
    excerpt = models.TextField(blank=True, default='')
    author = models.CharField(max_length=100, blank=True, default='')
    category = models.CharField(max_length=100, blank=True, default='')
    meta_title = models.CharField(max_length=100, blank=True, default='')
    meta_description = models.CharField(max_length=255, blank=True, default='')
    schema = models.JSONField(blank=True, null=True, default=None)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        unique_together = [['website', 'slug']]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class BlogPost(Blog):
    class Meta:
        proxy = True
        verbose_name = 'Blog'
        verbose_name_plural = 'Blogs'


class CaseStudy(Blog):
    class Meta:
        proxy = True
        verbose_name = 'Case Study'
        verbose_name_plural = 'Case Studies'


class BlogImage(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='blog_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for '{self.blog.title}'"
