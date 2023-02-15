from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Category, Article, Developer, Like
from .forms import *

from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):  # asosiy saxifa uchun 'view' hisoblanib (request) argumentini
    # ya'ni foydalanuvchidan so'rovni qabul qiladi
    categories = Category.objects.all()
    # SELECT * FROM categories;
    # categories = cursor.fetchall()
    articles = Article.objects.all()
    # SELECT * FROM articles;
    # articles = cursor.fetchall()
    context = {  # Tepadagi MB dan so'rov jo'natish orqali olingan
        # ma'lumotlarni front-end qismiga, ya'ni ko'rsatilgan html
        # saxifasiga jo'natish uchun lug'at ma'lumotlar
        # turidagi 'context' nomli o'zgaruvchi
        'title': 'Главная страница',
        # 'title' kalitini ostiga qiymat sifatida
        # 'Главная страница' ma'lumoti saqlab qo'yildi
        'categories': categories,
        # 'categories' kalitini ostiga qiymat sifatida
        # categories o'zgaruvchisini ichida ma'lumotlar bazasida so'rov orqali olingan
        # barcha ma'lumotlar saqlab qo'yildi  ---> kategoriyalr
        'articles': articles.order_by('-created_at')
        # 'articles' kalitini ostiga qiymat sifatida
        # articles o'zgaruvchisini ichida ma'lumotlar bazasida so'rov orqali olingan
        # barcha ma'lumotlar saqlab qo'yildi  ---> maqolalar
    }
    return render(request, 'blog/index.html', context)
    # return ---> funksiya qaytaradigan natija
    # index funksiyasi barcha qilingan ishlardan keyin
    # natija sifatida 'render' metodi orqali
    # foydalanuvchi tomonidan jo'natilgan so'rovga javob sifatida
    # 'blog' directory ichidagi 'index.html' saxifasiga
    # 'context' nomli o'zgaruvchiga barcha jo'natilishi
    # kerak bo'lgan ma'lumotlarni solib
    # chizib berayapti


def category_page(request, category_id):  # so'rov, category_id
    # foydalanuvchi kategoriya tugmasini ustiga bosganda
    # bosilgan kategoriya bo'yicha foydalanuvchiga barcha maqolalrni qaytarib beradi
    articles = Article.objects.filter(category_id=category_id)
    articles = articles.order_by('-created_at')
    # SELECT * FROM articles WHERE category_id = ?; (category_id, )
    # articles = cursor.fetchall()  --->
    # o'sha shartga javob beruvchi hamma ma'lumotlarni oladi
    category = Category.objects.get(pk=category_id)  # ---> html saxifa uchun chiroyli
    #       title ya'ni nom yasash uchun olindi
    # SELECT * FROM categories WHERE pk = ?; (category_id, )
    # category = cursor.fetchone() --->
    # o'sha shartga javob beruvchi bitta ma'lumotni oladi
    categories = Category.objects.all()
    # SELECT * FROM categories;
    # categories = cursor.fetchall()
    context = {  # Tepadagi MB dan so'rov jo'natish orqali olingan
        # ma'lumotlarni front-end qismiga, ya'ni ko'rsatilgan html
        # saxifasiga jo'natish uchun lug'at ma'lumotlar
        # turidagi 'context' nomli o'zgaruvchi
        'title': f"Категория: {category.title}",
        # 'title' kaliti ostida qiymat sifatida
        # formatlangan satrlar orqali "Категория: category o'zgaruvchisi orqali
        # oloinayotgan o'sha kategoriyani title ---> nomi"
        'articles': articles,
        # 'articles' kaliti ostida qiymat sifatida
        # MB ga filter so'rovi jo'natish orqali olingan
        # ma'lumotlar joylandi
        'categories': categories
        # 'categories' kaliti ostiga qiymat sifatida
        # MB ga all so'rovi jo'natish orqali olingan
        # ma'lumotlar joylandi
    }
    return render(request, 'blog/index.html', context)
    # return ---> funksiya qaytaradigan natija
    # category_page funksiyasi (view ---> ofitsant)
    # barcha ishlarni qilib bo'lgandan keyin
    # natija sifatida 'render' metodi orqali
    # 'blog' directory ichidagi 'index.html' saxifasiga
    # 'context' nomli o'zgaruvchiga barcha jo'natilishi
    # kerak bo'lgan ma'lumotlarni solib
    # 'index.html' saxifasini qaytadan chizib beradi


def about_dev(request):  # 'about_dev' nomli view ochildi ---> (request)
    # sabab 'О разработчике' tugmasi bosilganda
    # 'about_dev.html' saxifasini foydalanuvchiga natija sifatida qaytarish uchun

    developers = Developer.objects.all()

    context = {
        'title': 'About developers',
        'developers': developers
    }

    return render(request, 'blog/about_dev.html', context)
    # return ---> funksiya (view) qaytaradigan natija
    #


def search_results(request):  # sabab ---> qidiruv logikasini amalga oshirish
    # word = foydalanuvchidan kelayoytgan so'rov ---> request
    # GET ---> foydalanuvchi jo'natayotgan so'rov turi --->
    # so'rov turi aniqlandi ---> method of form in _navbar.html is method="get"
    # get ---> olmoq ---> metod
    word = request.GET.get('q')
    # word = 'Статья 1'
    articles = Article.objects.filter(
        Q(title__icontains=word) | Q(content__icontains=word)
    )
    # QUERY ---> so'rov Q() | Q()
    # SELECT * FROM articles
    # WHERE title = 'Статья 1' OR content = 'Статья 1'
    # 'Статья 1' in title OR 'Статья 1' in 'Статья 1'
    # title = "Здравствуйте. Добро пожловать на Статья 1"
    # cursor.fetchall()

    context = {
        'title': f"Поиск по статьям !",
        'articles': articles.order_by('-created_at')
    }
    return render(request, 'blog/index.html', context)


def add_article(request):
    # foydalanuvchiga maqola qo'shish imkoniyatini berish uchun
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            article = Article.objects.create(**form.cleaned_data)
            article.save()
            return redirect('index')
        else:
            pass
    else:
        form = ArticleForm()

    context = {
        'title': 'Создать статью',
        'form': form
    }

    return render(request, 'blog/article_form.html', context)


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request, user)
                messages.success(request, 'ВЫ успешно авторизовались !')
                return redirect('index')
            else:
                messages.error(request, 'Не верное имя пользователя или пароль !')
                return ('login')
        else:
            messages.error(request, 'Не верное имя пользователя или пароль !')
            return ('login')
    else:
        form = LoginForm()
    context = {
        'title': 'Авторизация',
        'form': form
    }

    return render(request, 'blog/user_login.html', context)


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    messages.warning(request, 'Вы вышли из аккаунта !')
    return redirect('index')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Регистрация прошла успешно ! Войдите в аккаунт !")
            return redirect('login')
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('register')
    else:
        form = RegistrationForm()

    context = {
        'title': 'Регистрация',
        'form': form
    }

    return render(request, 'blog/register.html', context)


def article_detail(request, article_id):
    article = Article.objects.get(pk=article_id)
    article.views += 1
    article.save()

    context = {
        'title': article.title,
        'article': article
    }
    if request.user.is_authenticated:
        context['comment_form'] = CommentForm()
    context['comments'] = Comment.objects.filter(article=article)

    user = request.user
    if user.is_authenticated:
        # get ---> mavjud bo'lgan baxoni (like yoki dislike)
        # create ---> False bo'lgan tarzda 2 ta baxo yaratiladi (like=False, dislike=False)
        mark, created = Like.objects.get_or_create(user=user, article=article)
        if created:
            context['like'] = False
            context['dislike'] = False
        else:
            context['like'] = mark.like
            context['dislike'] = mark.dislike
    else:
        context['like'] = False
        context['dislike'] = False

    marks = Like.objects.filter(article=article)
    likes_count = len([i for i in marks if i.like])
    dislikes_count = len([i for i in marks if i.dislike])
    context['likes_count'] = likes_count
    context['dislikes_count'] = dislikes_count

    return render(request, 'blog/article_detail.html', context)


@login_required(login_url='login')
def update_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == "POST":
        form = ArticleForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article', id)
        else:
            for field in form.errors:
                messages.error(request, form.errors[field].as_text())
            return redirect('update', id)
    else:
        form = ArticleForm(instance=article)

    context = {
        'title': 'Обновление статьи',
        'form': form
    }
    return render(request, 'blog/article_form.html', context)


@login_required(login_url='login')
def delete_article(request, id):
    article = Article.objects.get(id=id)
    if request.method == 'POST':
        article.delete()
        return redirect('index')
    context = {
        'article': article
    }
    return render(request, 'blog/confirm_delete.html', context)


def save_comment(request, pk):
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.article = Article.objects.get(pk=pk)
        comment.user = request.user
        comment.save()
        messages.success(request, 'Ваш комментарий добавлен !')
        return redirect('article', pk)


@login_required(login_url='login')
def user_profile(request):
    return render(request, 'blog/user_profile.html')







@login_required(login_url='login')
def add_or_delete_mark(request, article_id, action):
    user = request.user
    if user.is_authenticated:
        article = Article.objects.get(pk=article_id)
        mark, created = Like.objects.get_or_create(user=user, article=article)
        if action == 'add_like':
            mark.like = True
            mark.dislike = False
        elif action == 'add_dislike':
            mark.like = False
            mark.dislike = True
        elif action == 'delete_like':
            mark.like = False
        elif action == 'delete_dislike':
            mark.dislike = False
        mark.save()
        return redirect('article', article.pk)
    else:
        return redirect('login')
