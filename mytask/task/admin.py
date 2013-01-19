from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from task.models import Task,UserProfile
from tastypie.admin import ApiKeyInline
from tastypie.models import ApiAccess, ApiKey

class UserProfileInline(admin.StackedInline):
	model = UserProfile
	can_delete = False
	verbose_name_plural = 'Profile'

class UserAdmin(UserAdmin):
	inlines = (UserProfileInline,)

admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Task)
admin.site.register(ApiKey)