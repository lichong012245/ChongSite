# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'tagcategory'
        db.create_table('blog_tagcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('blog', ['tagcategory'])

        # Adding model 'tag'
        db.create_table('blog_tag', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20, unique=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.tagcategory'])),
        ))
        db.send_create_signal('blog', ['tag'])

        # Adding model 'post'
        db.create_table('blog_post', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('body', self.gf('tinymce.models.HTMLField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('created_year', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('created_month', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('created_year_month', self.gf('django.db.models.fields.CharField')(max_length=7)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, unique=True)),
        ))
        db.send_create_signal('blog', ['post'])

        # Adding M2M table for field tag on 'post'
        m2m_table_name = db.shorten_name('blog_post_tag')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm['blog.post'], null=False)),
            ('tag', models.ForeignKey(orm['blog.tag'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'tag_id'])

        # Adding model 'postimage'
        db.create_table('blog_postimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(null=True, blank=True, max_length=100)),
            ('thumbnail', self.gf('django.db.models.fields.files.ImageField')(null=True, blank=True, max_length=100)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['blog.post'])),
        ))
        db.send_create_signal('blog', ['postimage'])

        # Adding model 'comment'
        db.create_table('blog_comment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=20, default='Anonymous')),
            ('email', self.gf('django.db.models.fields.EmailField')(blank=True, max_length=75)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True, auto_now_add=True)),
            ('vote_up', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('vote_down', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['blog.post'])),
            ('path', self.gf('blog.dbarray.IntegerArrayField')(blank=True)),
            ('depth', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('blog', ['comment'])


    def backwards(self, orm):
        # Deleting model 'tagcategory'
        db.delete_table('blog_tagcategory')

        # Deleting model 'tag'
        db.delete_table('blog_tag')

        # Deleting model 'post'
        db.delete_table('blog_post')

        # Removing M2M table for field tag on 'post'
        db.delete_table(db.shorten_name('blog_post_tag'))

        # Deleting model 'postimage'
        db.delete_table('blog_postimage')

        # Deleting model 'comment'
        db.delete_table('blog_comment')


    models = {
        'blog.comment': {
            'Meta': {'object_name': 'comment'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '20', 'default': "'Anonymous'"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'depth': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'email': ('django.db.models.fields.EmailField', [], {'blank': 'True', 'max_length': '75'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('blog.dbarray.IntegerArrayField', [], {'blank': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'null': 'True', 'to': "orm['blog.post']"}),
            'vote_down': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'vote_up': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'blog.post': {
            'Meta': {'object_name': 'post', 'ordering': "['created']"},
            'body': ('tinymce.models.HTMLField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'created_month': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'created_year': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'created_year_month': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'unique': 'True'}),
            'tag': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['blog.tag']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'blog.postimage': {
            'Meta': {'object_name': 'postimage'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.post']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'null': 'True', 'blank': 'True', 'max_length': '100'})
        },
        'blog.tag': {
            'Meta': {'object_name': 'tag'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['blog.tagcategory']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True', 'auto_now_add': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20', 'unique': 'True'})
        },
        'blog.tagcategory': {
            'Meta': {'object_name': 'tagcategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['blog']