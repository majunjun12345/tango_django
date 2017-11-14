from django import forms
from .models import Category,Page,UserProfile
from django.contrib.auth.models import User

class CategoryForm(forms.ModelForm):
	# name = forms.CharField(max_length = 128)
	# views = forms.IntegerField()
	# likes = forms.IntegerField()
	# slug = forms.SlugField()
	class Meta:
		model = Category
		fields = ('name',)   # 不是include,不是[]，元祖，有‘，’

class PageForm(forms.ModelForm):
	class Meta:
		model = Page
		fields = ('title',)

class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput())
	class Meta:
		model = User
		fields = ('username','email','password',)  # 写成了paswword导致了严重错误

class UserProfileForm(forms.ModelForm):
	class Meta:
		model = UserProfile
		fields = ('website','picture',)