from . import views
from django.urls import path

urlpatterns=[
    path('create/',views.post_create,name="create"),
    path('feed/',views.feed,name="feed"),
    path('like',views.like_post,name="like"),
    path('delete/<int:id>/',views.delete,name="delete")
]