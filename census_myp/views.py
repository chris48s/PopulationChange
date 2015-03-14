# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import Http404
from api_calls import *
from census_myp.models import stat
import json


class Helpers:
	def format_data_for_gcharts(self, data):
		
		result = []
		result.append([str(data['census'][0]['year']), data['census'][0]['value'], None, None])
		
		myplist = []
		for myp in data['myp_revised']:
			myplist.append( [str(myp['year']), None, myp['value']] )
		
		i = 0
		for myp in data['myp_superseded']:
			myplist[i].append(myp['value'])
			i += 1
		
		for myp in myplist:
			result.append(myp)
		
		result.append([str(data['census'][1]['year']), data['census'][1]['value'], None, None])
		result_encoded = json.dumps(result)
		
		return result_encoded
		
	
	
	def validate_ONS_code(self, LACode):
		
		q = stat.objects.filter(LACode=LACode)
		if q:
			return True
		else:
			return False


def index(request):
	
	api_calls = Api_Calls()
	
	try:
		local_auths = api_calls.get_authority_list()
	except:
		raise Http404('failed to retreive local authority list')
	else:
		context = {
			"local_auths": local_auths,
		}
	
	return render(request, 'index.html', context)

def get_chart_json(request):
	
	if 'LA' in request.GET:
		
		helpers = Helpers()
		LACode = request.GET['LA']
		validcode = helpers.validate_ONS_code(LACode)
		
		if validcode:
			api_calls = Api_Calls()
			try:
				data = api_calls.get_census_myp_data(LACode)
			except:
				raise Http404('failed to retreive data')
			else:
				context = {
					"gcharts_json": helpers.format_data_for_gcharts(data),
				}
		else:
			raise Http404('parameter not specified')
	else:
		raise Http404('invalid parameter')
	
	return render(request, 'json', context)
