from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationList, LocationDetails, TeacherList, TeacherDetail, UserList, UserDetail
from .views import StudentList, StudentDetail, QueueList, QueueAddItems


urlpatterns = {
    url(r'^queues/$', LocationList.as_view(), name='create'),
    url(r'^queues/(?P<pk>[0-9]+)/$', LocationDetails.as_view(), name='details'),
    url(r'^queues/teacher/$', TeacherList.as_view()),
    url(r'^queues/teacher/(?P<pk>[0-9]+)/$', TeacherDetail.as_view()),
    url(r'^queues/users/$', UserList.as_view()),
    url(r'^queues/users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^queues/student/$', StudentList.as_view()),
    url(r'^queues/student/(?P<pk>[0-9]+)/$', StudentDetail.as_view()),
    url(r'^queues/queue/$', QueueList.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/$', QueueAddItems.as_view()),
}


urlpatterns = format_suffix_patterns(urlpatterns)
