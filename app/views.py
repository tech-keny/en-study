from django.urls.conf import path
from django.views.generic import View 
from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Comment, Level, Post, Question,Like,Group,Part,StudyTime
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect

class IndexView(View):
    def get(self, request, *args, **kwargs):
        # post_data = Post.objects.order_by("-id")
        return render(request, 'app/index.html', {
            # 'post_data': post_data,
        })

CommentForm = forms.modelform_factory(Comment, fields=('content', 'user' ,))

class StudyView(generic.ListView):
    model = Post
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")

        return render(request, 'app/study.html', {
            'post_data': post_data,
        })

class PostDetailView(View):
        
    def get(self, request, pk , *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST or None)
        comments = Comment.objects.filter(post=post_data).order_by('-created')
        return render(request, 'app/post_detail.html', {
            'post_data': post_data,
            'form':form,
            'comments': comments,
        })

    def post(self, request, pk, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = Comment()
            comment.user = request.user
            comment.post = post_data
            comment.content = form.cleaned_data['content']
            comment.save()
        
        comments = Comment.objects.filter(post=post_data).order_by('-created')


        return render(request, 'app/post_detail.html', {
            'post_data': post_data,
            'form':form,
            'comments': comments,
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
            group = form.cleaned_data['group']
            group_data = Group.objects.get(name=group)
            post_data.group = group_data
            part = form.cleaned_data['part']
            part_data = Part.objects.get(name=part)
            post_data.part = part_data
            study_time = form.cleaned_data['study_time']
            study_time_data = StudyTime.objects.get(name=study_time)
            post_data.study_time = study_time_data
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
                'group': post_data.group,
                'part': post_data.part,
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
            group = form.cleaned_data['group']
            group_data = Group.objects.get(name=group)
            post_data.group = group_data
            level = form.cleaned_data['level']
            level_data = Level.objects.get(name=level)
            post_data.level = level_data
            part = form.cleaned_data['part']
            part_data = Part.objects.get(name=part)
            post_data.part = part_data
            study_time = form.cleaned_data['study_time']
            study_time_data = StudyTime.objects.get(name=study_time)
            post_data.study_time = study_time_data
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
            'post_data': post_data,
        })

    def post(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        post_data.delete()

        return redirect('study')


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'app/comment_delete.html'
    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post_detail', kwargs={'pk': pk})
    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user
    # def get(self, request, pk , *args, **kwargs):
    #     post_data = Post.objects.get(id=self.kwargs['pk'])
    #     return render(request, 'app/comment_delete.html', {
    #         'post_data': post_data,
    #     })
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post_data = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post_data
            comment.parent = parent_comment
            comment.save()
        
            
            return redirect('post_detail', pk=post_pk)
        comments = Comment.objects.filter(post=post_data).order_by('-created')
        
        return render(request, 'app/post_detail.html', {
            'post_data': post_data,
            'form':form,
            'comments': comments,
        })
        

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
class GroupView(View):
    def get(self, request, *args, **kwargs):
        group_data = Group.objects.get(name=self.kwargs['group'])
        post_data = Post.objects.order_by('-id').filter(group=group_data)
        return render(request, 'app/study.html', {
            'post_data': post_data
        })
class PartView(View):
    def get(self, request, *args, **kwargs):
        part_data = Part.objects.get(name=self.kwargs['part'])  
        post_data = Post.objects.order_by('-id').filter(part=part_data)
        return render(request, 'app/study.html', {
            'post_data': post_data
        })
class StudyTimeView(View):
    def get(self, request, *args, **kwargs):
        study_time_data = StudyTime.objects.get(name=self.kwargs['study_time'])
        post_data = Post.objects.order_by('-id').filter(study_time=study_time_data)
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

