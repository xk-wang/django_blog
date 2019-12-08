from django.urls import path
from . import views

app_name='blog'
urlpatterns = [
    path('post-list/', views.post_list, name='post_list'),
    path('post-detail/<int:id>/', views.post_detail, name='post_detail'),
    path('post-create/', views.post_create, name='post_create'),
    path('post-safe-delete/<int:post_id>/', views.post_safe_delete, name='post_safe_delete'),
    path('post-modified/<int:post_id>/', views.post_modified, name='post_modified'),
    path('increase_likes/<int:id>/',views.IncreaseLikesViews.as_view(),name='increase_likes'),
]