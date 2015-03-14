from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^', include('census_myp.urls', namespace="census_myp")),
	url(r'^admin/', include(admin.site.urls)),
)
