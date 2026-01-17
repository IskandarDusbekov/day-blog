from django.contrib import admin
from django.utils.html import format_html

from .models import User, NewPost, Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


# =========================
# USER ADMIN
# =========================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        'email',
        'username',
        'points',
        'streak',
        'level_display',
        'is_staff',
        'is_blocked'
    )

    list_filter = ('is_staff', 'is_blocked')
    search_fields = ('email', 'username')
    ordering = ('-points',)

    fieldsets = BaseUserAdmin.fieldsets + (
        ("Gamification", {
            "fields": ("points", "streak")
        }),
        ("Block status", {
            "fields": ("is_blocked",)
        }),
    )

    def level_display(self, obj):
        return obj.level()
    level_display.short_description = "Level"


# =========================
# POST ADMIN
# =========================
@admin.register(NewPost)
class PostAdmin(admin.ModelAdmin):
    list_display = ('thumbnail', 'title', 'author', 'views', 'total_likes', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at', 'author')
    search_fields = ('title', 'author__email')
    readonly_fields = ('views', 'total_likes', 'created_at')

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="80" style="border-radius:8px;" />', obj.image.url)
        return "(No Image)"
    thumbnail.short_description = 'Rasm'


# =========================
# COMMENT ADMIN
# =========================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'post',
        'short_text',
        'is_blocked',
        'created_at'
    )

    list_filter = ('is_blocked', 'created_at')
    search_fields = ('user__email', 'text')
    ordering = ('-created_at',)

    def short_text(self, obj):
        return obj.text[:30]
    short_text.short_description = "Comment"
