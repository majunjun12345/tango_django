from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Category,Page
from .forms import CategoryForm,PageForm,UserForm,UserProfileForm
from django.contrib.auth import authenticate,login,logout
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from datetime import datetime

# Create your views here.
# def visitor_cookie_handler(request,response):
# 	visits = int(request.COOKIES.get('visits','1'))
# 	last_visit_cookie = request.COOKIES.get('last_visit',str(datetime.now()))
# 	last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
# 	if (datetime.now() - last_visit_time).seconds > 15:
# 		visits += 1
# 		response.set_cookie('last_visit',str(datetime.now()))
# 	else:
# 		response.set_cookie('last_visit',last_visit_cookie)
# 	response.set_cookie('visits',visits)

def get_sever_side_cookie(request,cookie,default_val=None):
	val = request.session.get(cookie)
	if not val:
		val = default_val
	return val
def visitor_cookie_handler(request):
	visits = int(get_sever_side_cookie(request,'visits','1'))
	last_visit_cookie = get_sever_side_cookie(request,'last_visit',str(datetime.now()))

	last_visit_time = datetime.strptime(last_visit_cookie[:-7],'%Y-%m-%d %H:%M:%S')
	if (datetime.now()-last_visit_time).seconds > 15:
		visits += 1
		request.session['last_visit'] = str(datetime.now())
	else:
		request.session['last_visit'] = last_visit_cookie
	request.session['visits'] = visits

def index(request):
	request.session.set_test_cookie()
	categories = Category.objects.all().order_by('views')[:5]
	pages = Page.objects.all().order_by('views')[:5]
	context = {'categories':categories,'pages':pages}
	visitor_cookie_handler(request)
	context['visits'] = request.session['visits']
	response = render(request,'tango/index.html',context)
	#visitor_cookie_handler(request,response)
	return response

def show_category(request,category_name_slug):
	if request.session.test_cookie_worked():
		print('TEST COOKIES WORKED!')
		request.session.delete_test_cookie()
	category = Category.objects.get(name = category_name_slug)
	print('majun')
	# category的c为小写
	pages = category.page_set.all()       # page_set  page小写
	return render(request,'tango/show_category.html',{'pages':pages,'category':category})

def details(request,category_name_slug,page_name_slug):
	return HttpResponse('ok')

@login_required
def add_category(request):    # 显示需要一个视图函数，提交后跳转到另一个视图函数
	form = CategoryForm()
	if request.method == 'POST':     # 需要 加 ''
		form = CategoryForm(request.POST)
		if form.is_valid:
			form.save(commit = True)    # 直接这样保存到数据库
			return index(request)       # 提交后跳转到首页（视图显示是首页，url还是跳转前的）
		else:
			form = CategoryForm()
	return render(request,'tango/add_category.html',{'form':form})

@login_required
def add_page(request,category_name_slug):
	form = PageForm()
	try:
		category = Category.objects.get(name = category_name_slug)
	except category.DoesNotExit:
		category = None
	if request.method == 'POST':
		form = PageForm(request.POST)
		if form.is_valid():
			page = form.save(commit = False)
			page.category = category
			page.save()
			return show_category(request,category_name_slug)
		else:
			form = PageForm()
	return render(request,'tango/add_page.html',{'form':form,'category':category})

# def register(request):
# 	registered = False
# 	if request.method == 'POST':
# 		user_form = UserForm(data = request.POST)
# 		# 有文件上传的话，应该是（request.POST,request.FILES）,这里没有绑定，可以在下面单独绑定
# 		userprofile_form = UserProfileForm(data = request.POST)
# 		if user_form.is_valid() and userprofile_form.is_valid():
# 			user = user_form.save()   # 这里直接保存,user和user_forn一样
# 			user.set_password(user.password)  # 保存之后再设置密码
# 			userprofile = userprofile_form.save(commit = False)
# 			userprofile.user = user
# 			# 存在键 picture，request.FILES和request.POST一样，是类字典
# 			if 'picture' in request.FILES:
# 					# 其他字段储存在 request.POST 中
# 				userprofile.picture = request.FILES['picture']
# 			userprofile.save()
# 			registered = True
# 	else:
# 		user_form = UserForm()
# 		userprofile_form = UserProfileForm()
# 	return render(request,
# 				'tango/register.html',
# 				{'user_form':user_form,
# 				 'userprofile_form':userprofile_form,
# 				 'registered':registered})

# def user_login(request):
# 	if request.method == 'POST':
# 		username = request.POST.get('username')
# 		password = request.POST.get('password')
# 		user = authenticate(username = username,password = password)
# 		if user:
# 			if user.is_active:
# 				login(request,user)
# 				return HttpResponseRedirect(reverse('tango:index'))
# 			else:
# 				return HttpResponse('your tango account is disabled!')
# 		else:
# 			return HttpResponse('用户名和密码不匹配！')
# 	else:
# 		return render(request,'tango/login.html',{})

# @login_required
# def user_logout(request):
# 	logout(request)
# 	return HttpResponseRedirect(reverse('tango:index'))





