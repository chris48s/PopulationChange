import urllib, urllib2, json
from operator import itemgetter
from config import *
from census_myp.models import stat

class Api_Calls:
	
	LACode = ""
	LACode_url = ""
	
	def get_census_myp_data(self, LACode):
		self.LACode = LACode
		self.LACode_url = urllib.quote_plus(LACode)
		
		census_2001_data    = self.__get_census_2001_from_nomis()
		census_2011_data    = self.__get_census_2011_from_ONS()
		myp_revised_data    = self.__get_myp_revised_from_nomis()
		myp_superseded_data = self.__get_myp_superseded_from_db()
		
		#turn this into a useful data structure
		population = {
			'census':			[census_2001_data, census_2011_data],
			'myp_revised':		myp_revised_data,
			'myp_superseded':	myp_superseded_data,
		}
		
		return population
	
	
	def __get_census_2001_from_nomis(self):
		
		json_url = "http://www.nomisweb.co.uk/api/v01/dataset/NM_58_1.data.json?geography="+self.LACode_url+"&date=latest&cell=268501249&measures=20100"
		result = json.load(urllib2.urlopen(json_url))
		
		population = {
			'year': '2001',
			'value': result['obs'][0]['obs_value']['value'],
		}
		
		return population
	
	
	def __get_census_2011_from_ONS(self):
		
		json_url = "http://data.ons.gov.uk/ons/api/data/dataset/KS101EW.json?apikey="+ONS_API_KEY+"&context=Census&geog=2011WARDH&dm/2011WARDH="+self.LACode_url+"&jsontype=json-stat"
		result = json.load(urllib2.urlopen(json_url))
		
		population = {
			'year': '2011',
			'value': result['KS101EW Segment_1']['value']['0'],
		}
		
		return population
	
	
	def __get_myp_revised_from_nomis(self):
		
		json_url = "http://www.nomisweb.co.uk/api/v01/dataset/NM_31_1.data.json?geography="+self.LACode_url+"&sex=7&age=0&measures=20100"
		result = json.load(urllib2.urlopen(json_url))
		
		population = []
		if result['obs']:
			for myp in result['obs']:
				if myp['time']['value'] > 2001 and myp['time']['value'] < 2011:
					population.append({
						'year': myp['time']['value'],
						'value': myp['obs_value']['value'],
					})
				
				#sort by year as an int
				def sort_by_year(tup):
					return (int(tup['year']))
				
				population = sorted(population, key=sort_by_year)
			
		return population
	
	
	def __get_myp_superseded_from_db(self):
		
		population = []
		q = stat.objects.filter(LACode=self.LACode).order_by('year')
		if q:
			for myp in q:
				population.append({
					'year': myp.year,
					'value': myp.population,
				})
		
		return population
	
	
	#build up a list of local authorities in England and Wales
	#using data from Mapit API
	def get_authority_list(self):
		
		local_auths = []
		
		#districts
		json_url = "http://mapit.mysociety.org/areas/DIS"
		result = json.load(urllib2.urlopen(json_url))
		for area in result:
			local_auths.append({ "code": result[area]['codes']['gss'], "name": result[area]['name'] })
		
		#metropolitan districts
		json_url = "http://mapit.mysociety.org/areas/MTD"
		result = json.load(urllib2.urlopen(json_url))
		for area in result:
			local_auths.append({ "code": result[area]['codes']['gss'], "name": result[area]['name'] })
		
		#london boroughs
		json_url = "http://mapit.mysociety.org/areas/LBO"
		result = json.load(urllib2.urlopen(json_url))
		for area in result:
			local_auths.append({ "code": result[area]['codes']['gss'], "name": result[area]['name'] })
		
		#unitary authorities
		json_url = "http://mapit.mysociety.org/areas/UTA"
		result = json.load(urllib2.urlopen(json_url))
		for area in result:
			#get rid of Scottish authorities - the ONS only covers England + Wales
			if result[area]['codes']['gss'][:3]  != 'S12':
				local_auths.append({ "code": result[area]['codes']['gss'], "name": result[area]['name'] })
		
		#sort them by name
		local_auths_sorted = sorted(local_auths, key=itemgetter('name'))
		
		return local_auths_sorted
