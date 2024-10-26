from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializer
from django.contrib.auth.models import User as auth_user
from posts.models import Post
from django.core.paginator import Paginator
from django.http import Http404
from django.urls import reverse
from allauth.account.views import LoginView as AllauthLoginView

class CustomLoginView(AllauthLoginView):
    def get_success_url(self):
        user = self.request.user
        return reverse('user_profile', kwargs={'username': user.username})
# API用ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

def user_list(request):
    users = User.objects.all()  # 全てのユーザーを取得
    return render(request, 'users/user_list.html', {'users': users})

def user_detail(request, user_id):
    user = get_object_or_404(User, id=user_id)  # ユーザーIDで特定のユーザーを取得
    return render(request, 'users/user_detail.html', {'user': user})

def user_profile(request, username):
    try:
        user = get_object_or_404(auth_user, username=username)  # ユーザーを取得
    except Http404:
        # ユーザーが見つからない場合の処理
        return render(request, '404.html', status=404)

    posts = Post.objects.filter(user=user).order_by('-created_at')  # ユーザーの投稿を取得
    paginator = Paginator(posts, 5)  # ページネーションを設定（1ページあたり5件）
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'user': user,
        'page_obj': page_obj,
    }
    return render(request, 'users/user_profile.html', context)