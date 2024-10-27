from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets
from .models import Post
from .serializers import PostSerializer
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm
from django.contrib.auth.models import User

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


# views.py
import requests
import time
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .forms import ImageGenerationForm
from django.contrib.auth.decorators import login_required

@login_required
def generate_image_view(request):
    if request.method == 'POST':
        form = ImageGenerationForm(request.POST, request.FILES)
        if form.is_valid():
            prompt = form.cleaned_data.get('description')
            location = form.cleaned_data.get('location')
            print(prompt, flush=True)
            print(location, flush=True)
            print(settings.STABILITY_API_TOKEN, flush=True)
            
            # Stability AI APIの設定
            api_url = "https://api.stability.ai/v2beta/stable-image/generate/sd3"
            headers = {
                "authorization": f"Bearer sk-BjPGEtjnOKHqyBwyj80xy0S3fU25lpBFxiSuOosYNdUf9myQ",
                "accept": "image/*"
            }
            data = {
                "model_id": "sd3.5-large-turbo",
                "prompt": f"{prompt}, {location}",
                "output_format": "jpeg",
                "height": 720,
                "width": 720,
                "samples": 1,
                "steps": 40,
                "aspect_ratio": "16:9"
            }
            retries = 5
            wait_time = 120

            for attempt in range(1, retries + 1):
                response = requests.post(api_url, headers=headers, files={"none": ''}, data=data)
                if response.status_code == 200:
                    # 生成した画像を直接ユーザーに返却
                    return HttpResponse(response.content, content_type="image/jpeg")
                elif response.status_code == 503:
                    time.sleep(wait_time)
                else:
                    return JsonResponse({'status': 'error', 'message': response.text})

            # すべての再試行が失敗した場合
            return JsonResponse({'status': 'error', 'message': '画像生成に失敗しました。後でお試しください。'})

        # バリデーションに失敗した場合
        print("Form validation failed:", form.errors, flush=True)
        return JsonResponse({'status': 'error', 'message': '入力内容にエラーがあります。再度確認してください。'})

    else:
        # GETリクエストの場合はフォームを表示
        form = ImageGenerationForm()
    return render(request, 'generate_image.html', {'form': form})
