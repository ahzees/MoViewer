from django.contrib import admin
from django.urls import path
from Comments.views import add_comment
from Comments.views import CommentApiView

urlpatterns = [
    path('add_comment/<slug:movie_slug>',add_comment,name='add_comment'),
    path('api/v1/comments', CommentApiView.as_view())
]
