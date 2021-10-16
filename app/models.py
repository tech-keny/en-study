from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import CustomUser


class Level(models.Model):
    name = models.CharField("レベル", max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    study_time = models.IntegerField("平均勉強時間")
    level = models.ForeignKey(Level, verbose_name='レベル', on_delete=models.CASCADE) # 追加
    textbook = models.CharField("参考書名", max_length=200)
    image = models.ImageField(
        upload_to='images', verbose_name='参考書表紙', null=True, blank=True)  
    content = models.TextField("勉強法")
    created = models.DateTimeField("作成日", auto_now_add=True)
    like_num = models.IntegerField(default=0)

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


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name="comments", on_delete=CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    content = models.TextField(default='ここに入力')
    created = models.DateTimeField("作成日", auto_now_add=True)
    def __str__(self):
      return '%s - %s' % (self.post.title, self.user)


class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

