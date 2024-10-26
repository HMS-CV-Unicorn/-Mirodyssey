from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.core.paginator import Paginator

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



def timeline(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/timeline.html', {'posts': posts})