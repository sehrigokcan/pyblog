from django import forms

from .models import Article


# article.py'de oluşturduğumuz form modeli import ettik

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'article_image']
        # seçilen articlede ekranda görünecek kısımlar belirlendi
