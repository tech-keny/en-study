from django.forms.fields import ImageField
from django.urls.conf import path
from django.views.generic import View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from .models import Level, Post, Ask, Question,Like
from .forms import PostForm, AskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

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
        ask_data = Ask.objects.filter(post=post_data)
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
            'form': form,
        })

class CreatePostView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)
        return render(request, 'app/post_form.html', {
            'form': form,
            
        })
    
    def post(self, request, *args, **kwargs):
        form = PostForm(request.POST or None)

        if form.is_valid():
            post_data = Post()
            post_data.author = request.user
            post_data.title = form.cleaned_data['title']
            post_data.study_time = form.cleaned_data['study_time']
            level = form.cleaned_data['level']
            level_data = Level.objects.get(name=level)
            post_data.level = level_data
            post_data.textbook = form.cleaned_data['textbook']
            if request.FILES:
                post_data.image = request.FILES.get('image') 
            post_data.content = form.cleaned_data['content']
            post_data.save()
            return redirect('study')

        return render(request, 'app/post_form.html', {
            'form': form,
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
            level = form.cleaned_data['level']
            level_data = Level.objects.get(name=level)
            post_data.level = level_data
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

class LevelView(View):
    def get(self, request, *args, **kwargs):
        level_data = Level.objects.get(name=self.kwargs['level'])
        post_data = Post.objects.order_by('-id').filter(level=level_data)
        return render(request, 'app/study.html', {
            'post_data': post_data
        })


@login_required
def like(request, *args, **kwargs):
    post = Post.objects.get(id=kwargs['pk'])
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(post__id=kwargs['pk'], user=request.user)
        liking.delete()
        post.like_num -= 1
        post.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect(reverse_lazy('post_detail', kwargs={'pk': kwargs['pk']}))
    # like
    post.like_num += 1
    post.save()
    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    messages.success(request, 'いいね！しました')
    return HttpResponseRedirect(reverse_lazy('post_detail', kwargs={'pk': kwargs['pk']}))


@login_required
def study_like(request, *args, **kwargs):
    post = Post.objects.get(id=kwargs['pk'])
    is_like = Like.objects.filter(user=request.user).filter(post=post).count()
    # unlike
    if is_like > 0:
        liking = Like.objects.get(post__id=kwargs['pk'], user=request.user)
        liking.delete()
        post.like_num -= 1
        post.save()
        messages.warning(request, 'いいねを取り消しました')
        return redirect(reverse_lazy('study'))
    # like
    post.like_num += 1
    post.save()
    like = Like()
    like.user = request.user
    like.post = post
    like.save()
    messages.success(request, 'いいね！しました')
    return HttpResponseRedirect(reverse_lazy('study'))

