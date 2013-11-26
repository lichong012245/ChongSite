from django.db import models
from tinymce.models import HTMLField
from blog.dbarray import IntegerArrayField
from django.forms import ModelForm
from django import forms
from django.template.defaultfilters import slugify
from blog.slugify import unique_slugify
import time
import datetime
from django.contrib.contenttypes import generic
from PIL import Image
import os
from django.core.files.uploadedfile import SimpleUploadedFile
import io

'''blog with threaded comments and tagging system'''

class tagcategory(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class tag(models.Model):
    name = models.CharField(max_length=20,unique=True)
    created=models.DateTimeField(auto_now_add=True)
    category=models.ForeignKey(tagcategory)

    def __str__(self):
        return self.name

class post(models.Model):
    title=models.CharField(max_length=100)
    body=HTMLField()
    created=models.DateTimeField(auto_now_add=True)
    created_year=models.CharField(max_length=4)
    created_month=models.CharField(max_length=2)
    created_year_month=models.CharField(max_length=7)
    tag = models.ManyToManyField(tag)
    slug=models.SlugField(unique=True)

    class Meta:
        ordering = ["created"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        strtime = "".join(str(time.time()).split("."))
        string = "%s-%s" % (strtime[7:], self.title)
        self.slug = slugify(string)
        self.created_year=datetime.date.today().year
        self.created_month='%02d'%datetime.date.today().month
        self.created_year_month=str(self.created_year)+'/'+str(self.created_month)
        super(post, self).save()

class postimage(models.Model):
    image=models.ImageField(upload_to='blog',blank=True, null=True)
    thumbnail=models.ImageField(upload_to='blog/thumbnail/',blank=True, null=True,editable=False)
    post=models.ForeignKey(post)

    def __str__(self):
        return self.image.name

    def save(self):
        THUMBNAIL_SIZE = (128, 128)
        image=Image.open(self.image)
        if image.mode not in ('L', 'RGB'):
          image = image.convert('RGB')
        image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
        temp_handle = io.BytesIO()
        image.save(temp_handle, 'png')
        temp_handle.seek(0)
        suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                temp_handle.read(), content_type='image/png')
        self.thumbnail.save(suf.name+'.png', suf, save=False)
        super(postimage,self).save()



class comment(models.Model):
    content = models.TextField(blank=False)
    author = models.CharField(max_length=20, default='Anonymous')
    email = models.EmailField(blank=True)
    created=models.DateTimeField(auto_now_add=True)
    vote_up=models.IntegerField(null=True,blank=True)
    vote_down=models.IntegerField(null=True,blank=True)
    post = models.ForeignKey(post, null=True)
    path = IntegerArrayField(blank=True, editable=False)
    depth = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.content


class commentForm(ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(
                            attrs={'class': 'parent'}), required=False)

    class Meta:
        model = comment
        fields = ('author','email','content',)

