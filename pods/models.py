from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from .fields import OrderField
from django.template.loader import render_to_string
from taggit.managers import TaggableManager


class Pod(models.Model):
    owner = models.ForeignKey(User,
                                related_name='pods_created',
                                on_delete=models.CASCADE)
    tags = TaggableManager()
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    susers = models.ManyToManyField(User,related_name='pods_joined',blank=True)
    file = models.FileField(null=True, blank= True, upload_to='images')
    likes = models.ManyToManyField(User, related_name='pods_liked')

    def total_likes(self):
        return self.likes.count()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title

class Module(models.Model):
    pod = models.ForeignKey(Pod,
                                related_name='modules',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    order = OrderField(blank=True, for_fields=['pod'])

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return f'{self.order}. {self.title}'
        
## discussion model
class Discussion(models.Model):
    pod = models.ForeignKey(Pod,
                                related_name='discussions',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "pod_discussion")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    class Meta:
        ordering = ['updated']
    
    def __str__(self):
        return self.title
####comment

class Comment(models.Model):
    discussion = models.ForeignKey(Discussion,
                                related_name='comments',
                                on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete= models.CASCADE, related_name= "discussion_comment")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['created']
    
    def __str__(self):
        return self.author.username


###
class Content(models.Model):
    module = models.ForeignKey(Module,
                                related_name='contents',
                                on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType,
                                    on_delete=models.CASCADE,
                                    limit_choices_to={'model__in':(
                                                        'text',
                                                        'video',
                                                        'image',
                                                        'file')})
    object_id = models.PositiveIntegerField()
    item = GenericForeignKey('content_type', 'object_id')
    order = OrderField(blank=True, for_fields=['module'])

    class Meta:
        ordering = ['order']

class ItemBase(models.Model):
    owner = models.ForeignKey(User,
                                related_name='%(class)s_related',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract= True
    
    def __str__(self):
        return self.title

    def render(self):
        return render_to_string(f'pods/content/{self._meta.model_name}.html',{'item': self})

class Text(ItemBase):
    content = models.TextField()

class File(ItemBase):
    file = models.FileField(upload_to='files')

class Image(ItemBase):
    file = models.FileField(upload_to='images')

class Video(ItemBase):
    url = models.URLField()