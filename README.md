ONS Population Change
=====================

What is it?
-----------
A Django project which helps to answer the questions:

* How did the population of local authorities in England and Wales change during the period 2001-2011?
* How accurate were the (now superseded) ONS mid-year population estimates released during this period?

Requirements
------------
* Django 1.7
* Python 2.7

Setup
-----
* Settings:

 Edit PopulationChange/settings.py to taste. As a minimum you will need to add a SECRET_KEY value.

* ONS API Key:

 2011 Census data is sourced from the ONS API ( https://www.ons.gov.uk/ons/apiservice/web/apiservice/home ) which requires an API key. You'll need to sign up for an API key and add it to census_myp/config.py

 Other data is sourced from:
 * Nomis API: http://www.nomisweb.co.uk/api/v01/help
 * Mapit: http://mapit.mysociety.org/
 * or is provided as a fixture, so no API keys are needed.

* Apply migrations:

 ./manage.py migrate

* Import fixtures:

 ./manage.py loaddata myp_superseded.json

Notes
-----
Superseded mid-year population estimates are not available via an API. These have been sourced from http://www.ons.gov.uk/ons/publications/all-releases.html?definition=tcm%3A77-22371 and data is provided as a fixture. Local authority boundaries in England underwent some changes in 2009 (see http://en.wikipedia.org/wiki/2009_structural_changes_to_local_government_in_England ). Data published prior to 2009 has been aggregated to reflect current boundaries. For example, in pre-2009 data, South Bedfordshire and Mid Bedfordshire have been aggregated together into Central Bedfordshire in line with current boundaries for comparative purposes ...and so on.

Author
------
Christopher Shaw