from blog.models import post, comment, commentForm, tag,tagcategory
from django.forms import ModelForm
from django import forms
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView, DetailView, FormView, View, TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import os
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import ModelFormMixin
from django.views.generic.dates import MonthArchiveView,ArchiveIndexView
from django.views.generic.list import MultipleObjectMixin
from django.core.urlresolvers import reverse
from django.db import connection
from django.db.models import Count
from blog.query_clean import get_query
from blog.form import SearchForm
from django.core.cache import get_cache

BASE_DIR = os.path.abspath(os.path.dirname(__file__)).replace('\\', '/')


class PostWithComment(SingleObjectMixin,FormView):
    template_name='blog/post_detail.html'
    form_class=commentForm
    model=post

    def post(self,request,*args,**kwargs):
        form = commentForm(request.POST or None)
        self.object=self.get_object()
        if request.method == "POST":
             if form.is_valid():
                temp = form.save(commit=False)
                temp.post=self.object
                parent = form['parent'].value()

                if parent == '':
                    #Set a blank path then save it to get an ID
                    temp.path = []
                    temp.save()
                    temp.path = [temp.id]
                else:
                    #Get the parent node
                    node = comment.objects.get(id=parent)
                    temp.depth = node.depth + 1
                    temp.path = node.path

                    #Store parents path then apply comment ID
                    temp.save()
                    temp.path.append(temp.id)

                #Final save for parents and children
                temp.save()
        ##comment_tree = comment.objects.all().order_by('path')
        return super(PostWithComment, self).post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('postdetailwithcomment', kwargs={'slug': self.object.slug})


class TagListView(ListView):
    model=post
    paginate_by = 4
    template_name='blog/tag_list.html'

    def get_queryset(self):
        self.tag= get_object_or_404(tag,name=self.args[0])
        return post.objects.filter(tag=self.tag)

    def get_context_data(self,tag="",**kwargs):
        context = super(TagListView, self).get_context_data(**kwargs)
        context['tag']=self.tag
        date_agg=post.objects.values('created_year_month').annotate(created_count=Count('id')).order_by('-created_year_month')
        context['date_agg']=date_agg
        post_dic=post.objects.values('created_year_month','title','slug')
        context['post_dic']=post_dic
        return context





class Postlist(ListView):
    model=post
    paginate_by = 2

    def get_queryset(self):
        query_string = ''
        if ('search' in self.request.GET) and self.request.GET['search'].strip():
           query_string = self.request.GET['search']
           entry_query = get_query(query_string, ['title', 'body',])
           queryset = post.objects.filter(entry_query).order_by('-created')
           self.request.session['searchset']=queryset

        else:
           if self.request.session.get('searchset') and ('page' in self.request.GET):
               queryset=self.request.session['searchset']
           else:
               queryset=post.objects.all().order_by('-created')
               if self.request.session.get('searchset'):
                 del self.request.session['searchset']
        return queryset



    def get_context_data(self, **kwargs):
        context=super(ListView,self).get_context_data(**kwargs)
        date_agg=post.objects.values('created_year_month').annotate(created_count=Count('id')).order_by('-created_year_month')
        context['date_agg']=date_agg
        post_dic=post.objects.values('created_year_month','title','slug')
        context['post_dic']=post_dic
        context['form']=SearchForm()
        return context







class PostDetail(DetailView):
    model=post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['form'] = commentForm()
        post=self.object
        comment_tree = post.comment_set.all().order_by('path')
        context['comment_tree']=comment_tree
        return context


class PostDetailWithComment(View):

    def get(self, request, *args, **kwargs):
        view = PostDetail.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = PostWithComment.as_view()
        return view(request, *args, **kwargs)

class PostMonthArchiveView(MonthArchiveView):
    queryset=post.objects.all()
    date_field = "created"
    make_object_list = True
    allow_future = True

    def get_context_data(self, **kwargs):
        context=super(MonthArchiveView,self).get_context_data(**kwargs)
        date_agg=post.objects.values('created_year_month').annotate(created_count=Count('id')).order_by('-created_year_month')
        context['date_agg']=date_agg
        post_dic=post.objects.values('created_year_month','title','slug')
        context['post_dic']=post_dic
        return context





class PostArchiveIndexView(ArchiveIndexView):
    model=post
    date_field='created'
    template_name_suffix = '_archiveindex'
    paginate_by = 10

class tagmap(ListView):
    model=tagcategory
    template_name='blog/tag_map.html'

    def get_context_data(self, **kwargs):
        context=super(ListView,self).get_context_data(**kwargs)
        date_agg=post.objects.values('created_year_month').annotate(created_count=Count('id')).order_by('-created_year_month')
        context['date_agg']=date_agg
        post_dic=post.objects.values('created_year_month','title','slug')
        context['post_dic']=post_dic
        return context



