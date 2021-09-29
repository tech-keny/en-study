from django.urls import path
from app import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('study', views.StudyView.as_view(), name='study'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'), # 追加
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'), # 追加
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
]
