from django import forms
from django.db.models import fields, query
from django.forms import widgets
from .models import Level,Group,Part, StudyTime,Comment, Post
from django.forms.models import ModelForm
from django.forms.widgets import CheckboxSelectMultiple


class PostForm(forms.ModelForm):

    part = forms.ModelMultipleChoiceField(queryset=Part.objects,widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post 
        
        fields = ["level","part","study_time","group","title","textbook","image","content"]


# class PostForm(forms.Form):
#     level_data = Level.objects.all()
#     level_choice = {}
#     for level in level_data:
#         level_choice[level] = level
#     level = forms.ChoiceField(label='レベル', widget=forms.Select, choices=list(level_choice.items())) # 追加
#     part_data = Part.objects.all()
#     part_choice = {}  
#     for part in part_data:
#         part_choice[part] = part
#     part = forms.MultipleChoiceField(label='Part', widget=forms.SelectMultiple, choices=list(part_choice.items())) # 追加
#     study_time_data = StudyTime.objects.all()
#     study_time_choice = {}
#     for study_time in study_time_data:
#         study_time_choice[study_time] = study_time
#     study_time = forms.ChoiceField(label='平均勉強時間/日', widget=forms.Select, choices=list(study_time_choice.items())) # 追加
#     group_data = Group.objects.all()
#     group_choice = {}
#     for group in group_data:
#         group_choice[group] = group
#     group = forms.ChoiceField(label='分類', widget=forms.Select, choices=list(group_choice.items())) # 追加
#     title = forms.CharField(max_length=200, label='タイトル')
#     textbook = forms.CharField(label="参考書名",max_length=200)
#     image = forms.ImageField(label="参考書表紙", required=False)
#     content = forms.CharField(label='勉強法', widget=forms.Textarea())



class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.Textarea(
            attrs={'rows': '3',
                  'placeholder': 'Say Something...'}
        ))
    class Meta:
        model = Comment
        fields = ['content']

