from django.db import models
from django.contrib.auth.models import AbstractUser

# =========================
# USER
# =========================
class User(AbstractUser):
    email = models.EmailField(unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    # GAMIFICATION
    points = models.PositiveIntegerField(default=0)
    streak = models.PositiveIntegerField(default=0)

    # BLOCKED STATUS
    is_blocked = models.BooleanField(default=False)

    def level(self):
        """Ballga qarab darajani qaytaradi"""
        if self.points < 100:
            return "Beginner"
        elif self.points < 300:
            return "Bronze"
        elif self.points < 700:
            return "Silver"
        elif self.points < 1500:
            return "Gold"
        else:
            return "Master"

    def __str__(self):
        return self.email


# =========================
# POST
# =========================
class NewPost(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    title = models.CharField(max_length=150)
    description = models.TextField(max_length=1000)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    views = models.PositiveIntegerField(default=0)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    is_active = models.BooleanField(default=True)  # Admin orqali bloklash mumkin

    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()


    def __str__(self):
        return self.title


# =========================
# COMMENT
# =========================
class Comment(models.Model):
    post = models.ForeignKey(
        NewPost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(max_length=500)
    is_blocked = models.BooleanField(default=False)  # Admin orqali bloklash
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.text}"
