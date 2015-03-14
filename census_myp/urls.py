from django.conf.urls import patterns, url
from census_myp import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^get_chart_json/', views.get_chart_json, name='get_chart_json'),
)
