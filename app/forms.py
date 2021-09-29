from django import forms


class PostForm(forms.Form):
    title = forms.CharField(max_length=200, label='タイトル')
    study_time = forms.IntegerField(label="平均勉強時間/日")
    level = forms.CharField(label="レベル",max_length=200)
    textbook = forms.CharField(label="参考書名",max_length=200)
    image = forms.ImageField(label="参考書表紙", required=False)
    content = forms.CharField(label='勉強法', widget=forms.Textarea())
