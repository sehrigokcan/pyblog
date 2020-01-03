from ckeditor.fields import RichTextField
from django.db import models


# we are creating model for admin panel

class Article(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # auto.User --> Allows us to retrieve user names from the specified table
    # on_delete -->  Deletes all data when the author name is deleted

    title = models.CharField(max_length=50, verbose_name='Title')
    # The title and the total number of characters were created in the table.
    # The name was then customized to 'verbose name = başlık'.

    # content = models.TextField(verbose_name='Text') bu kısmı overwrite yapıyoruz
    content = RichTextField()
    # The content colunm were created in the table. 
    # The name was then customized to 'verbose name = içerik'.

    created_date = models.DateTimeField(auto_now_add=True, verbose_name='oluşturulma zamanı')
    # The data column were created auto as Instant Current Time
    # The name was then customized to 'verbose name = oluşturulma zamanı'.
    article_image = models.FileField(blank=True, null=True, verbose_name="Add foto")

    likes = models.ManyToManyField("auth.User", related_name="post_likes",
                                   blank=True)  # likes adinda bir alan olusturduk

    # begeni butonu icin  yeni bir alan olusturduk

    def __str__(self):
        return self.title
    # We have customized the name of an object added here. 
    # The object name as Article object (1) will appear as title (başlık).

    # Note: 1-We will save the created Article model to admin.py page.
    # 2-We will continue to customize the admin panel in admin.py.

    # yorum modeli oluşturulacak


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='Article', related_name="comments")
    # ForeignKey ile Article ile ilişkilendirdik. on_delete ile article silinince yourmlar silinsin. related_name ile yorumlara ulaşbileceğimiz isim tanımladık.

    comment_author = models.CharField(max_length=50, verbose_name='name')
    # yorum yazarının isim bilgisi

    comment_content = models.CharField(max_length=200, verbose_name="comment")

    # yorum yazılacak alan bilgileri

    def __str__(self):
        return self.comment_content

    # modeli admin panele kaydedeceğiz.
