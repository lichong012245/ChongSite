from django.contrib import admin
from blog.models import post,comment,tag,tagcategory,postimage
from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models

class PostImageAdmin(admin.ModelAdmin):
    pass

class ImageInline(admin.TabularInline):
    model = postimage


class PostAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)
    fields = ('title','slug','created','body','tag')
    search_fields = ['title']
    prepopulated_fields = {"slug": ("title",)}
    inlines = [
        ImageInline,
    ]
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE(attrs={'cols': 200, 'rows': 40}, )},
    }


class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ("created",'post_title')
    fields=('post_title','author','email','content','created',)

    def post_title(self,obj):
        return obj.post.title

class TagAdmin(admin.ModelAdmin):
    pass

class TagcategoryAdmin(admin.ModelAdmin):
    pass



admin.site.register(post, PostAdmin)
admin.site.register(comment, CommentAdmin)
admin.site.register(tag, TagAdmin)
admin.site.register(tagcategory, TagcategoryAdmin)
admin.site.register(postimage, PostImageAdmin)