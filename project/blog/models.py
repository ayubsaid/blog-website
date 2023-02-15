from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=30, unique=True, verbose_name='Название категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Article(models.Model):
    title = models.CharField(max_length=150, unique=True, verbose_name='Заголовок статьи')
    content = models.TextField(verbose_name='Содержание статьи')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фотография',
                              null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    publish = models.BooleanField(default=True, verbose_name='Статус статьи')
    views = models.IntegerField(default=0, verbose_name='Количество просмотров')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 verbose_name='Категория')

    def get_absolute_url(self):
        return reverse('article', kwargs={'article_id': self.pk})

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return "https://www.peerspace.com/resources/wp-content/uploads/2019/02/beverage-3157395_1280.jpg"



    def __str__(self):
        return self.title


    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'






class Developer(models.Model):
    full_name = models.CharField(max_length=40, verbose_name='Имя разработчика')
    job = models.CharField(max_length=30, verbose_name='Профессия')
    bio = models.TextField(verbose_name='О себе')
    photo = models.ImageField(upload_to='photos/developers', null=True, blank=True)

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Разработчик'
        verbose_name_plural = 'Разработчики'






class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Автор')
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name='Комментарий')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.article.title}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'






class Like(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE,
                                verbose_name='Комментарий')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             verbose_name='Автор')

    like = models.BooleanField(default=False, verbose_name='Лайк')
    dislike = models.BooleanField(default=False, verbose_name='Дизлайк')

    def __str__(self):
        return f"{self.user.username} -" \
               f"{self.article.title} -" \
               f"{self.like} -" \
               f"{self.dislike}"

    class Meta:
        verbose_name = 'Лайк и дизлайк'
        verbose_name_plural = 'Лайки и дизлайки'
