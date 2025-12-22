# blogicum/blog/admin.py
from django.contrib import admin

from .models import Category, Location, Post


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("title",)
    list_filter = ("is_published",)


class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "created_at")
    list_editable = ("is_published",)
    search_fields = ("name",)
    list_filter = ("is_published",)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "pub_date",
        "author",
        "category",
        "location",
        "is_published",
        "created_at",
    )
    list_editable = ("is_published",)
    search_fields = ("title", "text")
    list_filter = ("category", "is_published", "pub_date")
    date_hierarchy = "pub_date"


admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Post, PostAdmin)
