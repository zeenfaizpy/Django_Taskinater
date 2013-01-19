from django.conf.urls import patterns, include, url
from tastypie.api import Api
from task.api.resources import TaskResource,UserResource

v1_api = Api(api_name='v1')
v1_api.register(TaskResource())
v1_api.register(UserResource())
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'task.views.home'),
    url(r'^register/$', 'task.views.register'),
    url(r'^user/$', 'task.views.user'),
    url(r'^entertask/$', 'task.views.task_entry'),
    url(r'^viewtask/$', 'task.views.task_view'),
    url(r'^edittask/(\d+)/$', 'task.views.task_edit'),
    url(r'^deletetask/(\d+)/$', 'task.views.task_delete'),
    url(r'^logout/$', 'task.views.log_out'),
    # url(r'^$', 'mytask.views.home', name='home'),
    # url(r'^mytask/', include('mytask.foo.urls')),
    url(r'^owner/$', 'task.views.owner'),
    url(r'^ownerprocess/$', 'task.views.ownerprocess'),
    (r'^api/', include(v1_api.urls)),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
