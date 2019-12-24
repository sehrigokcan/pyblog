from django.shortcuts import render, redirect, get_object_or_404
                                            # sayfa yoksa 404 gönderecek fonksiyon import ettik
from .forms import ArticleForm
from django .contrib import messages
from .models import Article
from django.contrib.auth.decorators import login_required


def articles(request):
    keyword=request.GET.get("keyword")
    # name keyword ile girilen veriler alınıyor
    if keyword:
        # bil search işlemi yapılmış ise
        articles=Article.objects.filter(title__contains=keyword)
        # makalelerimizin başliklarında aranan kelimeye göre filitreleme yapıyoruz
        return render(request, "articles.html", {"articles": articles})
        
    #eğer bir search işlemi yoksa    
    articles=Article.objects.all()
    # tüm makaleleri liste halinde alıyoruz
    return render(request, "articles.html", {"articles":articles})

def index(request):
    context = {
               
    }
    return render(request, 'index.html', context)
    

def about(request):
    return render(request, 'about.html')

@ login_required(login_url="user:login")
def creat(request):
    articles=Article.objects.filter(author=request.user)
    #giriş yapan kullanıcıya ait makaleleri filitreleyerek bir obje oluşturduk.
    context={
        'articles':articles
    }
    return render(request, 'creat.html',context)

@ login_required(login_url="user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None, request.FILES or None) 
    # obje oluşturduk. Obje yazı alanlarını POST'dan, dosya alanlarını FILES'dan alacak

    if form.is_valid():
        article= form.save(commit=False)
        # yazar ismi ekleyebilmek için obje oluşturduk ve commit etmedik. aksi halde yazar ismi olmayacağından hata alırdık.
        article.author=request.user
        # giriş yapan kullanıcıyı yazar olarak kaydedecek
        article.save()
        messages.success(request,'Article has been created successfully.')
        return redirect('article:creat')
        # makale kaydedildikten sonra ana sayfaya yönlendiriliyor

    return render(request, 'addarticle.html',{'form':form})   

def detail(request,id):
    #article=Article.objects.filter(id=id).first() bunu alt satırla revize ettik
    article =get_object_or_404(Article,id=id)
    return render(request, 'detail.html',{"article":article})

@ login_required(login_url="user:login")
def updateArticle(request,id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None, instance = article)
    # POST'dan gelen bilgiler ve FILES'den gelen bilgiler alınıyor. objedeki bilgiler forma yazılıyor

    if form.is_valid():
        article= form.save(commit=False)
        # yazar ismi ekleyebilmek için obje oluşturduk ve commit etmedik. aksi halde yazar ismi olmayacağından hata alırdık.
        article.author=request.user
        # giriş yapan kullanıcıyı yazar olarak kaydedecek
        article.save()
        messages.success(request,'Article has been updated successfully.')
        return redirect('article:creat')
        # makale kaydedildikten sonra ana sayfaya yönlendiriliyor
    return render(request, 'update.html',{"form":form})

@ login_required(login_url="user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article,id=id)
    article.delete()
    messages.success(request,"Article has been deleted successfully")
    return redirect('article:creat')
    # 'article:creat' bu metodla tekrar aynı sayfaya dönmeyi sağlamış oluyoruz.


def addComment(request,id):
    return redirect('article:detail' ,{"id":id})
    