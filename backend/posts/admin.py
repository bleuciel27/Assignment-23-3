from django.contrib import admin
from .models import Post, Comment

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'seller', 'price', 'category', 'condition', 'created_at')
    list_filter = ('category', 'condition')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')

    def save_model(self, request, obj, form, change):
        if not change:  # If this is a new object
            obj.seller = request.user
        super().save_model(request, obj, form, change)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content',)
    readonly_fields = ('created_at', 'updated_at')