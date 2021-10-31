from django.urls import path
from app import views
from .views import CommentDeleteView, CommentReplyView, like

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
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
    path('level/<str:level>/', views.LevelView.as_view(), name='level'), 
    path('group/<str:group>/', views.GroupView.as_view(), name='group'), 
    path('part/<str:part>/', views.PartView.as_view(), name='part'), 
    path('study_time/<str:study_time>/', views.StudyTimeView.as_view(), name='study_time'), 
    path('post/<int:pk>/like/',views.like,name='like'), # 追記
    path('study/<int:pk>/like/',views.study_like,name='study_like'), # 追記
]