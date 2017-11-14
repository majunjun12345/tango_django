from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=128)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)
	slug = models.SlugField(unique = True)
	def save(self,*args,**kwargs):
		self.slug = slugify(self.name)
		super(Category,self).save(*args,kwargs)
	class Meta:
		verbose_name_plural = 'Categories'
	def __str__(self):
		return self.name

class Page(models.Model):
	category = models.ForeignKey(Category)
	title = models.CharField(max_length = 128)
	content = models.TextField(blank = True,null = True)
	views = models.IntegerField(default = 0)
	likes = models.IntegerField(default = 0)
	url = models.URLField(default = 'http://www.baidu.com')
	slug = models.SlugField(unique = True,null = True)
	def save(self,*args,**kwargs):
		self.slug = slugify(self.title)
		super(Page,self).save(*args,**kwargs)
	def __str__(self):
		return self.title

class UserProfile(models.Model):
	user = models.ForeignKey(User)
	website = models.URLField(blank = True)  # blank = True 与 required = False的区别
	picture = models.FileField(upload_to = 'profile_images',blank = True)
	def __str__(self):
		return self.user.username