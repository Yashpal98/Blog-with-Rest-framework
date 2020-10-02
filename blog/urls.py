from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),
    path('addpost/', views.addPost, name='addPost'),
    path('editPost/<str:slug>', views.editPost, name='editPost'),
    path('deletePost/<int:pk>', views.deletePost, name='deletePost'),

    # API to post comment
    path('postComment/', views.postComment, name='postComment'),
    path('editComment/', views.editComment, name='editComment'),
    path('deleteComment/<int:pk>', views.deleteComment, name='deleteComment'),
]