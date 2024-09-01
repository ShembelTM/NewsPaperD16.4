from django.urls import path
from .views import PostsList, PostsDetail, NewsFilter, NewsCreate, NewsUpdate, NewsDelete, CategoryListView, subscribe, unsubscribe


urlpatterns = [
   path('', PostsList.as_view(), name='news_list'),
   path('<int:pk>', PostsDetail.as_view(), name='post_detail'),
   path('search', NewsFilter.as_view(), name='search_news'),
   path('create', NewsCreate.as_view(), name='news_create'),
   path('<int:pk>/edit/', NewsUpdate.as_view(), name='news_update'),
   path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
   path('categories/<int:pk>', CategoryListView.as_view(), name='category_list'),
   path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
   path('categories/<int:pk>/unsubscribe/', unsubscribe, name='unsubscribe'),
   ]