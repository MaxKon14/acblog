from django.contrib import admin
from .models import Category, Post

admin.site.empty_value_display = 'Не задано'


class PostInline(admin.TabularInline):
    model = Category.posts.through
    extra = 1


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'is_published',
        'slug',
        'created_at',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('name',)
    list_display_links = ('name',)
    inlines = [PostInline,]


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'id',
        'is_published',
        'pub_date',
        'author',
    )
    list_editable = (
        'is_published',
    )
    search_fields = ('title',)
    list_display_links = ('title',)
    list_filter = ( 'category',)
    filter_horizontal = ('category',)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Post, PostAdmin)
