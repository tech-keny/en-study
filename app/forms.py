from django import forms
from .models import Level,Group,Part, StudyTime


class PostForm(forms.Form):
    level_data = Level.objects.all()
    level_choice = {}
    for level in level_data:
        level_choice[level] = level
    level = forms.ChoiceField(label='レベル', widget=forms.Select, choices=list(level_choice.items())) # 追加
    part_data = Part.objects.all()
    part_choice = {}
    for part in part_data:
        part_choice[part] = part
    part = forms.ChoiceField(label='Part', widget=forms.Select, choices=list(part_choice.items())) # 追加
    study_time_data = StudyTime.objects.all()
    study_time_choice = {}
    for study_time in study_time_data:
        study_time_choice[study_time] = study_time
    study_time = forms.ChoiceField(label='平均勉強時間/日', widget=forms.Select, choices=list(study_time_choice.items())) # 追加
    group_data = Group.objects.all()
    group_choice = {}
    for group in group_data:
        group_choice[group] = group
    group = forms.ChoiceField(label='分類', widget=forms.Select, choices=list(group_choice.items())) # 追加
    title = forms.CharField(max_length=200, label='タイトル')
    textbook = forms.CharField(label="参考書名",max_length=200)
    image = forms.ImageField(label="参考書表紙", required=False)
    content = forms.CharField(label='勉強法', widget=forms.Textarea())

class AskForm(forms.Form):
    content = forms.CharField(label='質問内容', widget=forms.Textarea())

