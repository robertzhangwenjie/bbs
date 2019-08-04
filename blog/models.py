from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser

class UserInfo(AbstractUser):

    nid = models.AutoField(primary_key=True)
    phone = models.CharField(max_length=11,null=True,unique=True)
    avatar = models.FileField(upload_to="avatars/%Y/%m/%d/",default="avatars/default.png", verbose_name="头像")
    create_time = models.DateTimeField(auto_now_add=True)
    blog = models.OneToOneField(to="Blog",to_field="nid",null=True,on_delete=models.DO_NOTHING)


    def __str__(self):
        return self.username

class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    site = models.CharField(max_length=32, unique=True)
    theme = models.CharField(max_length=32)

    def __str__(self):
        return self.title

class Category(models.Model):
    '''
    博客分类
    '''
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to="Blog",to_field="nid",null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title


class Tag(models.Model):

    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=32)
    blog = models.ForeignKey(to="Blog",to_field="nid",null=True,on_delete=models.SET_NULL)

    def __str__(self):
        return self.title

class Article(models.Model):
    '''
    文章
    '''

    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)

    category = models.ForeignKey(to="Category",to_field="nid",null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(to="UserInfo",to_field="nid",null=True,on_delete=models.SET_NULL)
    tags = models.ManyToManyField(
        to="Tag",
        through="Article2Tag", #定义关联表
        through_fields=("article","tag"), # 定义关联的字段，顺序:第一个是定义该字段的对象
    )

    def __str__(self):
        return self.title


class Article2Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article",to_field="nid",on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag",to_field="nid",on_delete=models.CASCADE)

    class Meta:
        unique_together = (("article","tag"),)

class ArticleDetail(models.Model):
    '''
    文章详情
    '''

    nid = models.AutoField(primary_key=True)
    content = models.TextField()
    article = models.OneToOneField(to="Article",to_field="nid",on_delete=models.CASCADE)


class ArticleUpDown(models.Model):
    '''
    点赞表
    '''
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to="UserInfo",null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(to="Article", null=True, on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True)

    class Meta:
        unique_together = (("article","user"),)

class Comment(models.Model):
    '''
    评论区
    '''

    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to="Article", to_field="nid", on_delete=models.CASCADE)
    user = models.ForeignKey(to="UserInfo", to_field="nid", on_delete=models.CASCADE)
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    parent_comment = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.content

