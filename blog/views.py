from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

from .models import NewPost, Comment



# 1. Like post (AJAX)
@login_required
def like_post_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    post_id = request.POST.get('post_id')
    if not post_id:
        return JsonResponse({'error': 'post_id missing'}, status=400)

    post = get_object_or_404(NewPost, id=post_id)
    user = request.user

    if post.likes.filter(id=user.id).exists():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes.count()
    })




# 4. Asosiy sahifa (index)
def index(request):
    # POST request handling (eskisi kabi)
    if request.method == 'POST':
        if 'post_submit' in request.POST:  # Post qo'shish formi
            title = request.POST.get('title')
            description = request.POST.get('description')
            image = request.FILES.get('image')

            if not title or not description:
                messages.error(request, "Title va description bo'sh bo'lmasligi mumkin emas")
            else:
                NewPost.objects.create(
                    author=request.user,
                    title=title,
                    description=description,
                    image=image
                )
                messages.success(request, "Post muvaffaqiyatli yaratildi!")

        elif 'comment_submit' in request.POST:  # Comment formi (oddiy POST)
            text = request.POST.get('comment_text')
            post_id = request.POST.get('post_id')

            if not text:
                messages.error(request, "Izoh yozilmadi")
            else:
                post = get_object_or_404(NewPost, id=post_id)[:2]
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    text=text
                )
                messages.success(request, "Izoh muvaffaqiyatli qo'shildi!")

        return redirect('index')

    # GET request → postlarni ko'rsatish
    posts = NewPost.objects.filter(is_active=True).order_by('-created_at')

    ctx = {
        'posts': posts
    }
    return render(request, 'index.html', ctx)


def index1(request):
    return render(request, 'index1.html')