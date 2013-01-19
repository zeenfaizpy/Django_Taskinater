from tastypie.resources import ModelResource
from tastypie import fields
from task.models import Task
from django.contrib.auth.models import User
from tastypie.authentication import ApiKeyAuthentication
from tastypie.authorization import DjangoAuthorization
from tastypie.models import create_api_key
from django.db import models

models.signals.post_save.connect(create_api_key, sender=User)

class UserResource(ModelResource):
	class Meta:
		queryset = User.objects.all()
		allowed_methods = ['get']

class TaskResource(ModelResource):
	user = fields.ForeignKey(UserResource,'user')
	class Meta:
		queryset = Task.objects.all()
		allowed_methods = ['get']
		authentication = ApiKeyAuthentication()
		authorization = DjangoAuthorization()