from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE


class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    study_time = models.IntegerField("平均勉強時間")
    level = models.CharField("レベル", max_length=200)
    textbook = models.CharField("参考書名", max_length=200)
    image = models.ImageField(
        upload_to='images', verbose_name='参考書表紙', null=True, blank=True)  
    content = models.TextField("勉強法")
    updated = models.DateTimeField("更新日", auto_now=True)
    created = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.title

class Ask(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField("質問内容")
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    updated = models.DateTimeField("更新日", auto_now=True)
    created = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.content

class Question(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField("質問内容")
    updated = models.DateTimeField("更新日", auto_now=True)
    created = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.content

