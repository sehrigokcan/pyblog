from django.contrib import admin

from .models import Article, Comment

# We import our Article model from model.py, Comment modelimizi import ettik

# 1.method---> admin.site.register(Article)
# We have registered our article model.

# 2.method--> we used this method in todolist project

# 3.method--> Decoreter

admin.site.register(Comment)


# Comment modeli sadece kaydettik. model admin yazmadık
# Şimdi teminalden model oluştıracağız makemigrations ve migrate komutlarıyla


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_date']
    # Items that we want to appear in the admin panel table from the elements we created in model.py.

    list_display_links = ['title', 'created_date']
    # adding a link attribute to the desired item from the items shown in the table.

    search_fields = ['title']
    # adding search attribute to the desired item from the item shown in the table

    list_filter = ['created_date']

    # adding filter attribute

    class Meta:
        model = Article
        # This code specific to Django. We have stated that Article class will be customized.

# 1- we need to save this model in the settings.py page in the INSTALLED_APP section.

# 2- Each time we create a new model, we need to run the command 'python manage.py
# makemigrations' from the terminal. After running this command the 0001_initial.py 
# file will occur in under the migrations file.

# 3- When we run the command 'python manage.py migration' from the terminal, the tables -
# will be created  in the admin panel acording to the 0001_initial.py database.
