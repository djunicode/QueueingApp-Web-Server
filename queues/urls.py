from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationList, LocationDetails, TeacherList, TeacherDetail, UserList, UserDetail
from .views import StudentList, QueueList, QueueAddItems, QueueDeleteItems, QueueDeleteSpecificItems
from .views import TeacherNameGet, StudentSubscription, GetItemIndex, DeleteStudentSubscription, YouAreNextNotification
from .views import GetSubjectTeachers, TokenMatch, UserLogin, StudentLogin, TeacherLogin, AddSubjects, SendNotificationToSubscribers
from .views import GetTeacherLocatonFromName, QueueDetails, GetTeacherQueues, TeacherAddingQueues, TeacherDeletingQueues


urlpatterns = {
    url(r'^queues/$', LocationList.as_view(), name='create'),
    url(r'^queues/(?P<pk>[0-9]+)/$', LocationDetails.as_view(), name='details'),
    url(r'^queues/teacher/$', TeacherList.as_view()),
    url(r'^queues/teacher/(?P<pk>[0-9]+)/$', TeacherDetail.as_view()),
    url(r'^queues/users/$', UserList.as_view()),
    url(r'^queues/users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
    url(r'^queues/student/$', StudentList.as_view()),
    url(r'^queues/student/(?P<pk>[0-9]+)/$', StudentSubscription.as_view()),
    url(r'^queues/queue/$', QueueList.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/$', QueueDetails.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/delete/$', QueueDeleteItems.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/deletespecific/$', QueueDeleteSpecificItems.as_view()),
    url(r'^queues/teacher/name/(?P<name>[\w ]+)/$', TeacherNameGet.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/index/$', GetItemIndex.as_view()),
    # url(r'^queues/student/subs$', StudentList.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/next/$', YouAreNextNotification.as_view()),
    url(r'^queues/student/(?P<pk>[0-9]+)/deletesub/$', DeleteStudentSubscription.as_view()),
    url(r'^queues/subject/$', GetSubjectTeachers.as_view()),
    url(r'^queues/users/(?P<pk>[0-9]+)/token/$', TokenMatch.as_view()),
    url(r'^queues/users/login/$', UserLogin.as_view()),
    url(r'^queues/student/login/$', StudentLogin.as_view()),
    url(r'^queues/teacher/login/$', TeacherLogin.as_view()),
    url(r'^queues/teacher/(?P<pk>[0-9]+)/subject/$', AddSubjects.as_view()),
    url(r'^queues/queue/notification/$', SendNotificationToSubscribers.as_view()),
    url(r'^queues/teacher/name/$', GetTeacherLocatonFromName.as_view()),
    url(r'^queues/queue/(?P<pk>[0-9]+)/add/$', QueueAddItems.as_view()),
    url(r'^queues/teacher/getqueues/$', GetTeacherQueues.as_view()),
    url(r'^queues/teacher/(?P<pk>[0-9]+)/addqueue/$', TeacherAddingQueues.as_view()),
    url(r'^queues/teacher/(?P<pk>[0-9]+)/deletequeue/$', TeacherDeletingQueues.as_view()),
}


urlpatterns = format_suffix_patterns(urlpatterns)



