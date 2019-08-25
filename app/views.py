from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment, Noticias
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
import requests
from bs4 import BeautifulSoup


# Create your views here.

def principal(request):
    noticias = Noticias.objects.all()
    return render(request, 'app/oi.html', { 'noticias' : noticias })

def login(request):
    return render(request, 'registration/login.html')


def post_list(request): 
    posts = Post.objects.filter()
    return render(request, 'app/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'app/post_detail.html', {'post': post})

@login_required
def post_new(request):
     if request.method == "POST":
         form = PostForm(request.POST)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm()
     return render(request, 'app/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
     post = get_object_or_404(Post, pk=pk)
     if request.method == "POST":
         form = PostForm(request.POST, instance=post)
         if form.is_valid():
             post = form.save(commit=False)
             post.author = request.user
             post.save()
             return redirect('post_detail', pk=post.pk)
     else:
         form = PostForm(instance=post)
     return render(request, 'app/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'app/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)

@login_required
def publish(self):
    self.published_date = timezone.now()
    self.save()

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'app/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('post_detail', pk=comment.post.pk)

def campeonatosFIBA(request):
    return render(request, 'app/campeonatosFIBA.html')

def campeonatosNBA(request): 
    return render(request, 'app/campeonatosNBA.html')

def origem(request): 
    return render(request, 'app/origem.html')

def regras(request): 
    return render(request, 'app/regras.html')

def montandoNoticias(self):
    Noticias.objects.all().delete()
    page = requests.get("https://globoesporte.globo.com/basquete/")
    soup = BeautifulSoup(page.content, 'html.parser')
    links = soup.find_all('div', class_='feed-post-body-title gui-color-primary gui-color-hover')
    lista_links = []
    for x in range(0, 3):
        tag = links[x].find('a', class_='feed-post-link gui-color-primary gui-color-hover')
        if tag is not None:
            link = tag['href']
            if link not in lista_links:
                lista_links.append(link)
                page2 = requests.get(link)
                soup2 = BeautifulSoup(page2.content, 'html.parser')
                resumo = soup2.find('h2', class_='content-head__subtitle')
                if resumo:
                    resumo = resumo.get_text()
                titulo = soup2.find('title').get_text()
                TAGimage = soup2.find('div', class_='progressive-img')
                TAGimage = str(TAGimage)
                image = TAGimage.split('data-max-size-url="', 1)[1]
                image = image.split('" data-min-size=', 1)[0]
                Noticias.objects.create(link=link, titulo=titulo, resumo=resumo, imagem=image)
    return redirect('principal')

