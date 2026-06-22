from django.contrib import admin
from .models import Blog, BlogImage, BlogPost, CaseStudy, Website


@admin.register(Website)
class WebsiteAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class BlogImageInline(admin.TabularInline):
    model = BlogImage
    extra = 1
    max_num = 4


class BaseContentAdmin(admin.ModelAdmin):
    inlines = [BlogImageInline]
    exclude = ['content_type']
    list_display = ['title', 'website', 'author', 'category', 'is_published', 'created_at']
    list_filter = ['website', 'is_published']
    search_fields = ['title', 'author', 'category', 'slug']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at']
    content_type = None

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if self.content_type:
            queryset = queryset.filter(content_type=self.content_type)
        return queryset

    def save_model(self, request, obj, form, change):
        if self.content_type:
            obj.content_type = self.content_type
        super().save_model(request, obj, form, change)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        formfield = super().formfield_for_foreignkey(db_field, request, **kwargs)
        if db_field.name == 'website':
            formfield.widget.can_add_related = False
            formfield.widget.can_change_related = False
            formfield.widget.can_delete_related = False
            formfield.widget.can_view_related = False
        return formfield


@admin.register(BlogPost)
class BlogPostAdmin(BaseContentAdmin):
    content_type = Blog.BLOG


@admin.register(CaseStudy)
class CaseStudyAdmin(BaseContentAdmin):
    content_type = Blog.CASE_STUDY
