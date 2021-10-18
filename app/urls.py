from django.urls import path
from app import views
from .views import like

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('study', views.StudyView.as_view(), name='study'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'), 
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'), 
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('question/', views.QuestionView.as_view(), name='question'),
    path('level/<str:level>/', views.LevelView.as_view(), name='level'), 
    path('post/<int:pk>/like/',views.like,name='like'), # 追記
    path('study/<int:pk>/like/',views.study_like,name='study_like'), # 追記
]