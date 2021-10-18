# from django import forms
# from .models import Comment, Post, Level


# class PostForm(forms.Form):
#     level_data = Level.objects.all()
#     level_choice = {}
#     for level in level_data:
#         level_choice[level] = level
#     title = forms.CharField(max_length=200, label='タイトル')
#     study_time = forms.IntegerField(label="平均勉強時間/日")
#     level = forms.ChoiceField(label='レベル', widget=forms.Select, choices=list(level_choice.items())) # 追加
#     textbook = forms.CharField(label="参考書名",max_length=200)
#     image = forms.ImageField(label="参考書表紙", required=False)
#     content = forms.CharField(label='勉強法', widget=forms.Textarea())

# class AskForm(forms.Form):
#     content = forms.CharField(label='質問内容', widget=forms.Textarea())

