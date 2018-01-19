from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import LocationList, LocationDetails


urlpatterns = {
    url(r'^queues/$', LocationList.as_view(), name='create'),
    url(r'^queues/(?P<pk>[0-9]+)/$', LocationDetails.as_view(), name='details'),
}


urlpatterns = format_suffix_patterns(urlpatterns)
