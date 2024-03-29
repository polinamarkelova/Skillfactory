from django.urls import path
from .views import PostsList, PostDetail, NewsCreate, PostUpdate, PostDelete, PostSearch, \
   ArticleCreate, CategoryListView, subscribe


urlpatterns = [
   path('', PostsList.as_view(), name='news_list'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', NewsCreate.as_view(), name='post_create'),
   path('search/', PostSearch.as_view(), name='post_search'),
   path('articles/create/', ArticleCreate.as_view(), name='article_create'),
   path('<int:pk>/edit/', PostUpdate.as_view(), name='post_edit'),
   path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
]
