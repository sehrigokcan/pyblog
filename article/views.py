import random

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Max
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from friendship.models import Follow
from user.models import Profile

from .forms import ArticleForm
from .models import Article


@login_required(login_url="user:login")
def authors(request):
    users = User.objects.all()
    user_list = []
    profile = request.user.profile

    for user in users:
        myUser = model_to_dict(user).copy()

        user_articles = Article.objects.filter(author=user)
        user_followers = Follow.objects.followers(user)
        user_followings = Follow.objects.following(user)
        is_following = Follow.objects.follows(request.user, user)
        user_profile = Profile.objects.get(user=user)

        myUser["articles"] = user_articles
        myUser["followers"] = user_followers
        myUser["followings"] = user_followings
        myUser["is_following"] = is_following
        myUser["profile"] = user_profile
        user_list.append(myUser)

    context = {"users": user_list, "profile":profile}
    return render(request, "authors.html", context)


@login_required(login_url="user:login")
def followAuthor(request):
    recipient = User.objects.get(id=request.POST.get("id"))
    is_following = Follow.objects.follows(request.user, recipient)

    if (is_following):
        Follow.objects.remove_follower(request.user, recipient)
    else:
        Follow.objects.add_follower(request.user, recipient)

    context = {
        "user": recipient,
        "is_following": is_following
    }  # icerik olarak da makale ve like islemimizi don

    if request.is_ajax():  #
        html = render_to_string('articles.html', context, request=request)
        return JsonResponse({'form': html})


@login_required(login_url="user:login")
def like_post(request):  # Like isleminin yapilmasi icin fonksiyonumuz
    article = get_object_or_404(Article, id=request.POST.get('id'))  # Posttan gelen kuallnici idsini ekle
    is_liked = False  # Varsayilan olarak like islemi False

    if article.likes.filter(id=request.user.id).exists():  # Eger likes alaninin icinde  bir kullanci idsi varsa 
        article.likes.remove(request.user)  # bu kullanici idsini sil
        is_liked = False  # Like islemini False yap
    else:
        article.likes.add(request.user)  # degilse kullaniciyi ekle 
        is_liked = True  # like degisenini True yap

    context = {
        "article": article,
        'is_liked': is_liked}  # icerik olarak da makale ve like islemimizi don

    if request.is_ajax():  #
        html = render_to_string('like_section.html', context, request=request)
        return JsonResponse({'form': html})
    


def articles(request):
    keyword = request.GET.get("keyword")
    # name keyword ile girilen veriler alınıyor
    if keyword:
        # bil search işlemi yapılmış ise
        articles = Article.objects.filter(title__contains=keyword)
        # makalelerimizin başliklarında aranan kelimeye göre filitreleme yapıyoruz
        return render(request, "articles.html", {"articles": articles})

    # eğer bir search işlemi yoksa
    articles = Article.objects.all()
    # tüm makaleleri liste halinde alıyoruz

    return render(request, "articles.html", {"articles": articles})


def index(request):
    articles = Article.objects.all()

    latest_articles = Article.objects.order_by("created_date")[:3]

    max_like_count = articles.aggregate(Max('likes'))["likes__max"]
    most_liked_articles = Article.objects.filter(likes=max_like_count)

    if articles:
        articles = random.choices(articles, k=6)

    context = {
        "articles": articles, 
        "most_liked_articles": most_liked_articles,
        "latest_articles": latest_articles
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


@login_required(login_url="user:login")
def creat(request):
    articles = Article.objects.filter(author=request.user)
    # giriş yapan kullanıcıya ait makaleleri filitreleyerek bir obje oluşturduk.
    context = {'articles': articles}

    return render(request, 'creat.html', context)


@login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None)
    # obje oluşturduk. Obje yazı alanlarını POST'dan, dosya alanlarını FILES'dan alacak

    if form.is_valid():
        article = form.save(commit=False)
        # yazar ismi ekleyebilmek için obje oluşturduk ve commit etmedik. aksi halde yazar ismi olmayacağından hata alırdık.
        article.author = request.user
        # giriş yapan kullanıcıyı yazar olarak kaydedecek
        article.save()
        messages.success(request, 'Article has been created successfully.')
        return redirect('article:creat')
        # makale kaydedildikten sonra ana sayfaya yönlendiriliyor

    return render(request, 'addarticle.html', {'form': form})


def detail(request, id):
    # article=Article.objects.filter(id=id).first() bunu alt satırla revize ettik
    article = get_object_or_404(Article, id=id)
    return render(request, 'detail.html', {"article": article})


@login_required(login_url="user:login")
def updateArticle(request, id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance=article)
    # POST'dan gelen bilgiler ve FILES'den gelen bilgiler alınıyor. objedeki bilgiler forma yazılıyor

    if form.is_valid():
        article = form.save(commit=False)
        # yazar ismi ekleyebilmek için obje oluşturduk ve commit etmedik. aksi halde yazar ismi olmayacağından hata alırdık.
        article.author = request.user
        # giriş yapan kullanıcıyı yazar olarak kaydedecek
        article.save()
        messages.success(request, 'Article has been updated successfully.')
        return redirect('article:creat')
        # makale kaydedildikten sonra ana sayfaya yönlendiriliyor

    return render(request, 'update.html', {"form": form})


@login_required(login_url="user:login")
def deleteArticle(request, id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request, "Article has been deleted successfully")
    return redirect('article:creat')
    # 'article:creat' bu metodla tekrar aynı sayfaya dönmeyi sağlamış oluyoruz.


def addComment(request, id):
    return redirect('article:detail', {"id": id})


def reading(request, id):
    reading = ["django", "python", "computer", "tecnology", "data", "web"]
    print(reading[id])

    articles = Article.objects.filter(title__contains=reading[id])
    print(articles)

    return render(request, "reading.html", {"articles": articles})
