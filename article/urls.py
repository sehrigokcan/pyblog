from django.urls import path
from . import views

app_name = 'article'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('creat/', views.creat, name='creat'),
    path('creat/addarticle', views.addArticle, name='addarticle'),
    path('articles/article/<int:id>', views.detail, name= 'detail'),
    path('articles/update/<int:id>', views.updateArticle, name= 'update'),
    path('articles/delete/<int:id>', views.deleteArticle, name= 'delete'),
    path('articles/', views.articles, name= 'articles'),
    path('articles/comment/<int:id>', views.addComment, name= 'comment'),
]