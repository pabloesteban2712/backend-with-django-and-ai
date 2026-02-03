from django.urls import path
from main.controllers import article

urlpatterns = [
       path('create', article.save, name="createArticle"),
       path('articles<int:page>', article.getArticles, name="getArticles"),
       path('article<int:id>', article.getArticle, name="getArticle"),
       path('delete<int:id>', article.deleteArticle, name="deleteArticle"),
       path('articles-by-user<int:userId>', article.getArticlesByUser, name="articleByUser"),
       path('generate/<str:theme>', article.generate, name="generate_article")
]
