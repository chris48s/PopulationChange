from django.test import TestCase
import datetime
from api_calls import *
from census_myp.views import *


class HelperTests(TestCase):
	fixtures = ['myp_superseded']
	
	def test_validate_nonsense(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("cheese")
		self.assertFalse(valid)
	
	#a sample of valid codes
	def test_validate_example_valid_code1(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E06000049")
		self.assertTrue(valid)
	def test_validate_example_valid_code2(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E06000057")
		self.assertTrue(valid)
	def test_validate_example_valid_code3(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("W06000001")
		self.assertTrue(valid)
	def test_validate_example_valid_code4(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E09000001")
		self.assertTrue(valid)
	def test_validate_example_valid_code5(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E08000001")
		self.assertTrue(valid)
	def test_validate_example_valid_code6(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E07000004")
		self.assertTrue(valid)
	
	
	#various codes that are conceivably 'valid' codes in some contexts
	#but should be rejected for the purposes of this application
	def test_validate_scotland(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("S12000001")
		self.assertFalse(valid)
	def test_validate_old_style_code(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("00AA")
		self.assertFalse(valid)
	def test_validate_old_code1(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E07000001")
		self.assertFalse(valid)
	def test_validate_old_code2(self):
		helpers = Helpers()
		valid = helpers.validate_ONS_code("E07000233")
		self.assertFalse(valid)
	
	
	#test with some valid input
	#on invalid input, behaviour is undefined
	def test_format_data_for_gcharts(self):
		helpers = Helpers()
		input = {
			"census": 			[	{"value": 59610, "year": "2001"},
									{"value": 61182, "year": "2011"} ],
			"myp_revised":		[	{"value": 60100, "year": 2002},
									{"value": 60000, "year": 2003},
									{"value": 60000, "year": 2004},
									{"value": 59800, "year": 2005},
									{"value": 60300, "year": 2006},
									{"value": 60600, "year": 2007},
									{"value": 60700, "year": 2008},
									{"value": 61000, "year": 2009},
									{"value": 61200, "year": 2010} ],
			"myp_superseded":	[	{"value": 60074, "year": datetime.date(2002, 1, 1)},
									{"value": 60056, "year": datetime.date(2003, 1, 1)},
									{"value": 60089, "year": datetime.date(2004, 1, 1)},
									{"value": 60029, "year": datetime.date(2005, 1, 1)},
									{"value": 60542, "year": datetime.date(2006, 1, 1)},
									{"value": 60868, "year": datetime.date(2007, 1, 1)},
									{"value": 61003, "year": datetime.date(2008, 1, 1)},
									{"value": 61340, "year": datetime.date(2009, 1, 1)},
									{"value": 61630, "year": datetime.date(2010, 1, 1)} ]
		}
		output = helpers.format_data_for_gcharts(input)
		self.assertEqual(output, "[[\"2001\", 59610, null, null], [\"2002\", null, 60100, 60074], [\"2003\", null, 60000, 60056], [\"2004\", null, 60000, 60089], [\"2005\", null, 59800, 60029], [\"2006\", null, 60300, 60542], [\"2007\", null, 60600, 60868], [\"2008\", null, 60700, 61003], [\"2009\", null, 61000, 61340], [\"2010\", null, 61200, 61630], [\"2011\", 61182, null, null]]")



class APICallsTests(TestCase):
	fixtures = ['myp_superseded']
	
	#test with some valid input
	#check 9 results are returned
	def test_get_myp_revised_from_nomis_valid(self):
		api_calls = Api_Calls()
		api_calls.LACode_url = urllib.quote_plus("W06000001")
		result = api_calls._Api_Calls__get_myp_revised_from_nomis()
		self.assertEqual(len(result), 9)
	
	"""
	Nomis actually returns invalid json in this case:
	it has a ] without an opening [
	get_myp_revised_from_nomis currently doesn't handle this cleanly
	because the exception is handled in get_chart_json()
	remove this test??
	
	def test_get_myp_revised_from_nomis_invalid(self):
		api_calls = Api_Calls()
		api_calls.LACode_url = urllib.quote_plus("cheese")
		result = api_calls._Api_Calls__get_myp_revised_from_nomis()
		self.assertEqual(len(result), 0)
	"""
	

	#test with some valid input
	#check 9 results are returned
	def test_get_myp_superseded_from_db_valid(self):
		api_calls = Api_Calls()
		api_calls.LACode = urllib.quote_plus("W06000001")
		result = api_calls._Api_Calls__get_myp_superseded_from_db()
		self.assertEqual(len(result), 9)
	
	#test with some invalid input
	#check 0 results are returned
	def test_get_myp_superseded_from_db_invalid(self):
		api_calls = Api_Calls()
		api_calls.LACode = urllib.quote_plus("cheese")
		result = api_calls._Api_Calls__get_myp_superseded_from_db()
		self.assertEqual(len(result), 0)



class ViewTests(TestCase):
	fixtures = ['myp_superseded']
	
	def test_get_chart_json_noparam(self):
		response = self.client.get('/get_chart_json/')
		self.assertEqual(response.status_code, 404)
		
	def test_get_chart_json_invalidparam(self):
		response = self.client.get('/get_chart_json/', {'LA': 'cheese'})
		self.assertEqual(response.status_code, 404)
		
	def test_get_chart_json_validparam(self):
		response = self.client.get('/get_chart_json/', {'LA': 'E07000223'})
		self.assertEqual(response.status_code, 200)
