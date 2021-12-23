from django.forms.models import ModelForm
from django.urls.conf import path
from django.views.generic import View
from django import forms
from django.shortcuts import render, redirect
from django.views import generic
from django.views.generic import edit, ListView
from django.views.generic.edit import  DeleteView
from django.urls import reverse_lazy
from .models import Comment, Level, Post, Question,Like,Group,Part,StudyTime
from .forms import PostForm, CommentForm, QuestionForm, ContactForm
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import BadHeaderError, EmailMessage
from django.http import HttpResponse
import textwrap
from django.db.models import Q 
from functools import reduce
from operator import and_
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger



class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/index.html', {
        })
class TermsView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/terms.html', {
        })
class PrivacyView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/privacy.html', {
        })

CommentForm = forms.modelform_factory(Comment, fields=('content', 'user' ,))

class StudyView(generic.ListView):
    model = Post
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by("-id")
        rank_data = Post.objects.order_by("-like_num")
        ranking= rank_data[0:3]
        paginator = Paginator(post_data, 5)
        page = request.GET.get('page', 1)
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(1)
      

        return render(request, 'app/study.html', {
            'post_data': post_data,
            'rank_data': rank_data,
            'ranking':ranking,
            'pages': pages
        }) 







class PostDetailView(View):
        
    def get(self, request, pk , *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])
        form = CommentForm(request.POST ,request.FILES or None)
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
        form = PostForm(request.POST ,request.FILES or None)
        return render(request, 'app/post_form.html', {
            'form': form,
            
        })
    
    def post(self, request, *args, **kwargs): 
        if request.method == 'POST':

            form = PostForm(request.POST ,request.FILES or None)
            if form.is_valid():
                post_data = form.save(commit=False)
                post_data.author = request.user
                if request.FILES:
                    post_data.image = request.FILES.get('image') 
                post_data.save()
                form.save_m2m()
                return redirect('study')

            return render(request, 'app/post_form.html', {
                'form': form,
            })


# class CreatePostView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         form = PostForm(request.POST or None)
#         return render(request, 'app/post_form.html', {
#             'form': form,
            
#         })
    
#     def post(self, request, *args, **kwargs): 
#         form = PostForm(request.POST or None)
    

#         if form.is_valid():
#             post_data = Post()
#             post_data.author = request.user
#             post_data.title = form.cleaned_data['title']
#             group = form.cleaned_data['group']
#             group_data = Group.objects.get(name=group)
#             post_data.group = group_data
#             part = form.cleaned_data['part']
#             part_data = Part.objects.get(name=part)
#             post_data.part = part_data
#             study_time = form.cleaned_data['study_time']
#             study_time_data = StudyTime.objects.get(name=study_time)
#             post_data.study_time = study_time_data
#             level = form.cleaned_data['level']
#             level_data = Level.objects.get(name=level)
#             post_data.level = level_data
#             post_data.textbook = form.cleaned_data['textbook']
#             if request.FILES:
#                 post_data.image = request.FILES.get('image') 
#             post_data.content = form.cleaned_data['content']
#             post_data.save()
#             return redirect('study')

#         return render(request, 'app/post_form.html', {
#             'form': form,
#         })







# ↓途中のeditView

class PostEditView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.get(id=self.kwargs['pk'])  
        form = PostForm(request.POST or None, initial={
                'title': post_data.title,
                'study_time': post_data.study_time,
                'level': post_data.level,
                'group': post_data.group,
                'textbook': post_data.textbook,
                'image': post_data.image,
                'content': post_data.content,
            }
        )

        return render(request, 'app/post_form.html', {
          'form':form,
        })
    
    def post(self, request, *args, **kwargs): 
        post_data = Post.objects.get(id=self.kwargs['pk'])
        if request.method == 'POST':

            form = PostForm(request.POST, request.FILES, instance=post_data)
            if form.is_valid():
                form.save()
                # post_data = form.save(commit=False)
                # post_data.author = request.user
                # if request.FILES:
                #     post_data.image = request.FILES.get('image') 
                # post_data.save()
                # form.save_m2m()
                return redirect('study')

            return render(request, 'app/post_form.html', {
                'form': form,
            })

# ↑途中のEditView 

# class PostEditView(LoginRequiredMixin, View):
#     def get(self, request, *args, **kwargs):
#         post_data = Post.objects.get(id=self.kwargs['pk'])
#         form = PostForm(
#             request.POST or None,
#             initial={
#                 'title': post_data.title,
#                 'study_time': post_data.study_time,
#                 'level': post_data.level,
#                 'group': post_data.group,
#                 'part': post_data.part,
#                 'textbook': post_data.textbook,
#                 'image': post_data.image,
#                 'content': post_data.content,
#             }
#         )

#         return render(request, 'app/post_form.html', {
#             'form': form
#         })
    
#     def post(self, request, *args, **kwargs):
#         form = PostForm(request.POST or None)

#         if form.is_valid():
#             post_data = Post.objects.get(id=self.kwargs['pk'])
#             post_data.title = form.cleaned_data['title']
#             group = form.cleaned_data['group']
#             group_data = Group.objects.get(name=group)
#             post_data.group = group_data
#             level = form.cleaned_data['level']
#             level_data = Level.objects.get(name=level)
#             post_data.level = level_data
#             part = form.cleaned_data['part']
#             part_data = Part.objects.get(name=part)
#             post_data.part = part_data
#             study_time = form.cleaned_data['study_time']
#             study_time_data = StudyTime.objects.get(name=study_time)
#             post_data.study_time = study_time_data
#             post_data.title = form.cleaned_data['title']
#             post_data.textbook = form.cleaned_data['textbook']
#             if request.FILES:
#                 post_data.image = request.FILES.get('image') 
#             post_data.content = form.cleaned_data['content']
#             post_data.save()
#             return redirect('post_detail', self.kwargs['pk'])

#         return render(request, 'app/post_form.html', {
#             'form': form
#         })


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
        form = QuestionForm(request.POST or None)
        return render(request, 'app/question.html', {
            'question_data': question_data,
            'form': form
        })

    def post(self, request, *args, **kwargs):
        if request.method == 'POST':
            form = QuestionForm(request.POST or None)

            if form.is_valid():
                question = Question()
                question.user = request.user
                question.content = form.cleaned_data['content']
                question.save()
            
            question_data = Question.objects.all()

            return render(request, 'app/question.html', {
                'form':form,
                'question_data': question_data
            })

class QuestionReplyView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        parent_question = Question.objects.get(pk=pk)
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.user = request.user
            question.parent = parent_question
            question.save()
        
            
        question_data = Question.objects.all()
        
        return render(request, 'app/question.html', {
            'form':form,
            'question_data': question_data
        })

class QuestionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Question
    template_name = 'app/question_delete.html'
    def get_success_url(self):
        return reverse_lazy('question')
    def test_func(self):
        question = self.get_object()
        return self.request.user == question.user



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

class ContactView(View):
    def get(self, request, *args, **kwargs):
        form = ContactForm(request.POST or None)

        return render(request, 'app/contact.html', {
            'form': form
        })
    
    def post(self, request, *args, **kwargs):
        form = form = ContactForm(request.POST or None)

        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            subject = 'お問い合わせありがとうございます。'
            content = textwrap.dedent('''
                ※このメールはシステムからの自動返信です。
                
                {name} 様
                
                お問い合わせありがとうございました。
                以下の内容でお問い合わせを受け付けいたしました。
                内容を確認させていただき、ご返信させて頂きますので、少々お待ちください。
                
                --------------------
                ■お名前
                {name}
                
                ■メールアドレス
                {email}
                
                ■メッセージ
                {message}
                --------------------
                ''').format(
                    name=name,
                    email=email,
                    message=message
                )

            to_list = [email]
            bcc_list = [settings.EMAIL_HOST_USER]

            try:
                message = EmailMessage(subject=subject, body=content, to=to_list, bcc=bcc_list)
                message.send()
            except BadHeaderError:
                return HttpResponse("無効なヘッダが検出されました。")

            return redirect('thanks') 

        return render(request, 'app/contact.html', {
            'form': form
        })


class ThanksView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'app/thanks.html')

class SearchView(View):
    def get(self, request, *args, **kwargs):
        post_data = Post.objects.order_by('-id')
        search_post = request.GET.get('search')


        if search_post:
              exclusion_list = set([' ', '　'])
              query_list = ''
              for word in search_post:
                  if not word in exclusion_list:
                      query_list += word
              query = reduce(and_, [Q(title__icontains=q) | Q(content__icontains=q) | Q(textbook__icontains=q) for q in query_list])
              post_data = post_data.filter(query)
        else:
            # If not searched, return default posts
            post_data = Post.objects.all().order_by("-created")

        return render(request, 'app/study.html', {'post_data': post_data})