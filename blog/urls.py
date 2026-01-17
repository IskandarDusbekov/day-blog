from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index1/', views.index1, name='index1'),

    # AJAX endpoints
    path('like-post/', views.like_post_ajax, name='like_post_ajax'),
    # path('comments/add/<int:post_id>/', views.add_comment_ajax, name='add_comment_ajax'),
    # path('comments/get/<int:post_id>/', views.get_comments_ajax, name='get_comments_ajax'),
]