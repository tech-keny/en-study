from django.forms.fields import ImageField
from django.urls.conf import path
from django.views.generic import View
from django.shortcuts import render, redirect
from .models import Post, Ask, Question
from .forms import PostForm, AskForm
from django.contrib.auth.mixins import LoginRequiredMixin

class IndexView(View):
    def get(self, request, *args, **kwargs):
        # post_data = Post.objects.order_by("-id")
        return render(request, 'app/index.html', {
            # 'post_data': post_data,
        })

class StudyView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        return render(request, 'app/study.html', {
            'post_data': post_data,
        })

class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        ask_data = Ask.objects.filter(user=request.user, post=post_data)
        form = AskForm(request.POST or None)
        return render(request, 'app/post_detail.html', {
            'post_data': post_data,
            'ask_data': ask_data,
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = AskForm(request.POST or None)
        post_data = Post.objects.get(id=self.kwargs['pk'])

        if form.is_valid():
            ask_data = Ask()
            ask_data.user = request.user
            ask_data.content = form.cleaned_data['content']
            ask_data.post = post_data
            ask_data.save()
            return redirect('post_detail',self.kwargs['pk'] )

        return render(request, 'app/post_detail.html', {
            'form': form
        })

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        return render(request, 'app/post_form.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.study_time = form.cleaned_data['study_time']
            post_data.level = form.cleaned_data['level']
            post_data.textbook = form.cleaned_data['textbook']
            if request.FILES:
                post_data.image = request.FILES.get('image') 
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('study')

        return render(request, 'app/post_form.html', {
            'form': form
        })

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = PostForm(
            request.POST or None,
            initial={
                'title': post_data.title,
                'study_time': post_data.study_time,
                'level': post_data.level,
                'textbook': post_data.textbook,
                'image': post_data.image,
                'content': post_data.content,
            }
        )

        return render(request, 'app/post_form.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post.objects.get(id=self.kwargs['pk'])
            post_data.title = form.cleaned_data['title']
            post_data.study_time = form.cleaned_data['study_time']
            post_data.level = form.cleaned_data['level']
            post_data.title = form.cleaned_data['title']
            post_data.textbook = form.cleaned_data['textbook']
            if request.FILES:
                post_data.image = request.FILES.get('image') 
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('post_detail', self.kwargs['pk'])

        return render(request, 'app/post_form.html', {
            'form': form
        })

class PostDeleteView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        return render(request, 'app/post_delete.html', {
            'post_data': post_data
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()
        return redirect('study')

class QuestionView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        question_data = Question.objects.all()
        return render(request, 'app/question.html', {
            'question_data': question_data
        })

    def post(self, request, *args, **kwargs):
        pass

