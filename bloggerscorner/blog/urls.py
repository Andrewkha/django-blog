from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.PostListView.as_view(), name='posts'),
    path('post/<int:pk>', views.PostDetailView.as_view(), name='post-detail'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('post/<int:pk>/create', views.CommentCreate.as_view(), name='comment-create')
]
