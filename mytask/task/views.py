from django.http import HttpResponse,HttpResponseRedirect
from django.core.context_processors import csrf
from django.core import serializers
from django.utils import simplejson
from django.forms.models import model_to_dict
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from task.models import UserProfileForm,UserForm,LoginForm,TaskForm,Task
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User

def home(request):
	if request.method == 'POST' and request.POST:
		l = LoginForm(request.POST)
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username,password=password)
		if user is not None:
			if user.is_active:
				login(request,user)
				if user.is_staff:
					return HttpResponseRedirect(reverse("task.views.owner"))
				else:
					return HttpResponseRedirect(reverse("task.views.user"))
			else:
				l = LoginForm()
				d = dict(lform = l,status="Your Account Is Diabled.Contact Admin.")
				d.update(csrf(request))
				return render_to_response('login.html',d)
		else:
			l = LoginForm()
			d = dict(lform = l,status="Invalid Username/Password")
			d.update(csrf(request))
			return render_to_response('login.html',d)
	else:
		l = LoginForm()
		d = dict(lform = l)
		d.update(csrf(request))
		return render_to_response('login.html',d)

def register(request):
	if request.method == 'POST' and request.POST:
		u = UserForm(request.POST)
		up = UserProfileForm(request.POST)
		if u.is_valid() and up.is_valid():
			user = u.save(commit = False)
			user.set_password(u.cleaned_data['password'])
			user.is_active = True
			user.is_staff =  False
			user.is_superuser = False
			user.save()
			userpro = up.save(commit = False)
			userpro.user = user
			userpro.save()
			return HttpResponseRedirect(reverse("task.views.home"))
		else:
			d = dict(user=u,userpro=up)
			d.update(csrf(request))
			return render_to_response('register.html',d)
	else:
		u = UserForm()
		up = UserProfileForm()
		d = dict(user = u,userpro = up)
		d.update(csrf(request))
		return render_to_response('register.html',d)

def user(request):
	if request.user.is_authenticated():
		user =  request.user
		tform = TaskForm()
		d = dict(user=user,tform = tform)
		d.update(csrf(request))
		return render_to_response('user.html',d)

	else:
		return HttpResponse("No Authentication")

def owner(request):
	if request.user.is_authenticated():
		if request.user.is_staff:
			userr =  request.user
			user = User.objects.filter(is_staff=False)
			d = dict(user=user,userr=userr)
			return render_to_response('owner.html',d)
	else:
		return HttpResponse("No Authentication")

def ownerprocess(request):
	if request.method == 'POST':
		username = request.POST['username']
		r = Task.objects.filter(user_id=username)
		json = serializers.serialize("json", r)
		#resp = { 'username' : username }
		#json = simplejson.dumps(resp, ensure_ascii=False)
		return HttpResponse(json, mimetype='application/json')
	else:
		return HttpResponse("No POST Method")

def log_out(request):
	logout(request)
	return HttpResponseRedirect(reverse("task.views.home"))

def task_entry(request):
	if request.user.is_authenticated():
		if request.method=="POST" and request.POST:
			t = TaskForm(request.POST)
			if t.is_valid():
				task = t.save(commit=False)
				task.user = request.user
				task.save()
				return HttpResponse("Data Saved To Task")
			else:
				return HttpResponse("Reenter Task in Form")
		else:
			return HttpResponseRedirect(reverse("task.views.user"))
	else:
		return HttpResponse("No Authentication")


def task_view(request):
	if request.user.is_authenticated():
		user=request.user
		task = Task.objects.filter(user=user)
		d=dict(user=user,task=task)
		return render_to_response('task_details.html',d)
	else:
		return HttpResponse("No Authentication")

def task_edit(request,pk):
	if request.user.is_authenticated():
		user=request.user
		task = Task.objects.get(pk=pk)
		if request.method=="POST" and request.POST:
			t = TaskForm(request.POST)
			if t.is_valid():
				t = TaskForm(request.POST,instance=task)
				t.save()
				return HttpResponseRedirect(reverse("task.views.task_view"))
			else:
				return HttpResponse("Validation Error")
		else:
			tform = TaskForm(instance=task)
			d=dict(user=user,tform=tform)
			d.update(csrf(request))
			return render_to_response('task_edit.html',d)
	else:
		return HttpResponse("No Authentication")

def task_delete(request,pk):
	if request.user.is_authenticated():
		user=request.user
		task = Task.objects.get(pk=pk)
		task.delete()
		return HttpResponseRedirect(reverse("task.views.task_view"))
	else:
		return HttpResponse("No Authentication")