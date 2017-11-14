from django.contrib import admin
from .models import Category ,Page,UserProfile
# Register your models here.


class PageInline(admin.TabularInline):  # 定义内联对象
	model = Page                        # 指定模型
	extra = 5                           # 嵌套数

class CategoryAdmin(admin.ModelAdmin):
	inlines = [PageInline]              # 显示内联

	fieldsets = [              #分组 classes 隐藏字段
		('group1',{'fields':['name'],'classes':['slug']}),
		('group2',{'fields':['views','likes']}),
	]

admin.site.register(Category,CategoryAdmin)
admin.site.register(UserProfile)
