from django.contrib import admin
from .models import BlogModel,Comment

# Register your models here.
admin.site.register(BlogModel)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'blog', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')