from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),  # asosiy saxifa uchun
    path('category/<int:category_id>/', category_page, name='category'),
    path('about_dev/', about_dev, name='about_dev'),
    path('search/', search_results, name='search'),
    path('add_article/', add_article, name='add_article'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', register, name='register'),
    path('article/<int:article_id>/', article_detail, name='article'),

    path('article_update/<int:id>/', update_article, name='update'),
    path('article_delete/<int:id>/', delete_article, name='delete'),

    path('add_comment/<int:pk>/', save_comment, name='save_comment'),
    path('my_page/', user_profile, name='my_page'),

    path('add_or_delete_mark/<int:article_id>/<str:action>/',
         add_or_delete_mark,
         name='mark')

]

