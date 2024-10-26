from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth.models import User
from django.urls import reverse

# API用ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

# テンプレート表示用ビュー
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)  # 投稿IDで特定の投稿を取得
    return render(request, 'posts/post_detail.html', {'post': post})


def post_list(request):
    post_list = Post.objects.all()  # 全ての投稿を取得
    paginator = Paginator(post_list, 10)  # 1ページあたり10件表示
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'posts/post_list.html', {'page_obj': page_obj})

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            form.save_m2m()
            return redirect('post_list')  # 投稿後のリダイレクト先
    else:
        form = PostForm()
    return render(request, 'posts/create_post.html', {'form': form})