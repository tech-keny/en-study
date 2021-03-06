from django.http import request
from django.urls import path
from app import views
from app.models import Post
from .views import CommentDeleteView, CommentReplyView
from django.urls import re_path



urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('search', views.SearchView.as_view(), name='search'),
    path('terms', views.TermsView.as_view(), name='terms'),
    path('privacy', views.PrivacyView.as_view(), name='privacy'),
    path('study', views.StudyView.as_view(), name='study'),
    # path('study/level/<str:study_level>/', views.StudyView.as_view(), name='study_level'),
    # path('study/group/<str:study_group>/', views.StudyView.as_view(), name='study_group'),
    path('post/<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/new/', views.CreatePostView.as_view(), name='post_new'), 
    path('post/<int:pk>/edit/', views.PostEditView.as_view(), name='post_edit'), 
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('post/<int:post_pk>/comment/<int:pk>/', CommentDeleteView.as_view(), name='comment_delete'),
    path('post/<int:post_pk>/comment/reply/<int:pk>', CommentReplyView.as_view(), name='comment_reply'),
    path('question/', views.QuestionView.as_view(), name='question'),
    path('question/<int:pk>/reply', views.QuestionReplyView.as_view(), name='question_reply'),
    path('question/<int:pk>/delete', views.QuestionDeleteView.as_view(), name='question_delete'),
    path('level/<str:level>/', views.LevelView.as_view(), name='level'), 
    path('group/<str:group>/', views.GroupView.as_view(), name='group'), 
    path('part/<str:part>/', views.PartView.as_view(), name='part'), 
    path('study_time/<str:study_time>/', views.StudyTimeView.as_view(), name='study_time'), 
    path('post/<int:pk>/like/',views.like,name='like'), # 追記
    path('study/<int:pk>/like/',views.study_like,name='study_like'), # 追記
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('thanks/', views.ThanksView.as_view(), name='thanks'),
    
]

