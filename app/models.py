from django.conf import settings
from django.db import models
from django.db.models.deletion import CASCADE
from accounts.models import CustomUser
from multiselectfield import MultiSelectField


class Part(models.Model):
    name = models.CharField("Part", max_length=50)

    def __str__(self):
        return self.name
class StudyTime(models.Model):
    name = models.CharField("平均勉強時間/日", max_length=50)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField("分類", max_length=50)

    def __str__(self):
        return self.name
class Level(models.Model):
    name = models.CharField("レベル", max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField("タイトル", max_length=200)
    level = models.ForeignKey(Level, verbose_name='レベル', on_delete=models.CASCADE) # 追加
    group = models.ForeignKey(Group, verbose_name='分類', on_delete=models.CASCADE) # 追加
    part = models.ManyToManyField(Part, verbose_name='Part') # 追加
    study_time= models.ForeignKey(StudyTime, verbose_name='平均勉強時間/日',on_delete=models.CASCADE) # 追加
    textbook = models.CharField("参考書名", max_length=200)
    image = models.ImageField(
        upload_to='images', verbose_name='参考書表紙', null=True, blank=True)  
    content = models.TextField("勉強法")
    created = models.DateTimeField("作成日", auto_now_add=True)
    like_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title




class Question(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField("質問内容")
    updated = models.DateTimeField("更新日", auto_now=True)
    created = models.DateTimeField("作成日", auto_now_add=True)

    def __str__(self):
        return self.content


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField('ここに入力')
    # parent = models.ForeignKey('self', verbose_name='親コメント', null=True, blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField("作成日", auto_now_add=True)
    active = models.BooleanField(default=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')

    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created').all()
        
    @property
    def is_parent(self):
        if self.parent is None:
            return True
        return False
    class Meta:
        # sort comments in chronological order by default
        ordering= ('created',)
    def __str__(self):
        return 'Comment by {}'.format(self.content)
    

class Like(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='like_user')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

