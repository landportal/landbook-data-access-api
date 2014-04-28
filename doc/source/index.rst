.. landportal-data-access-api documentation master file, created by
   sphinx-quickstart on Fri Apr 25 11:18:55 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to landportal-data-access-api's documentation!
======================================================

Welcome to the documentacion of landportal-data-access-api, in the next sections you can see how to use the api. This api allows users to reuse data in order to reuse this information. License?

Contents:

.. toctree::
   :maxdepth: 2

API Description
---------------
This api is based on `RESTful principles <http:http://en.wikipedia.org/wiki/Representational_state_transfer>`_. So you can access it through normal http requests.

API Security
------------
For security, a basic realm authentication is required, except graphics. Graphics are covered in the next section.

You need to obtain a token in: these token then is used...

API Structure
-------------
Api is divided in two main sections: entities and graphics.

* **Entities** are normal elements that make sense alone in Landportal context. Also they can be mixed up in order to give more complex data.
* **Graphics** are visual representations of the data e.g., bar chart of women holders in different countries. They can be customized by the user and even sended to another user that will see the customized graph.

API Usage
---------
Entities
~~~~~~~~
The entities available are the next:

country
	Represents a country like Italy, France, Spain and so on.
region
	Represents a region like Europe or America and it have other regions or countries belonging to it. There is an special region called 'global' with un_code 1, it represents all the world.
indicator
	Represents a set of data grouped by the same criteria, e.g.: Women Holders, it contains various observations for various countries.
observations
	Represents a data observed or recollected in a moment or period of time
user
	Represents a source of data
organizations
	Represents an organization that provides data
datasource
	To complete
dataset
	To complete
value
	Represents a value for an observation
topic
	To complete


As said before, api is based in RESTful principles, therefore you can make a petition with your browser or curl like::

	curl landportal.info/api/countries?format=json

Formats availabe through the format argument are: **JSON**, **XML**, **CSV** and **JSONP**.
In the next table you can see all the URLs defined that you can access with a short description and arguments to modify the result. Variables in the URL are surrounded by '<' and '>':

+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| URI                                                                              | Description                                                                | Arguments                                                                        |
+==================================================================================+============================================================================+=================================================================================+
| landportal.info/api/countries                                                    | All countries                                                              |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/countries/<iso3>                                             | Country with given iso3                                                    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators                                                   | All indicators                                                             |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>                                              | Indicator with the given id                                                |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/top                                          | Top observations of the given indicator with highest values                                                                           | top: number of results                                                       |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/average                                      | Average of given indicator                                                 |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/compatible                                   | Show compatible indicators to the one given                                                                            |                                                                              |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/users                                                        | All users                                                                  |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/users/<id>                                                   | User with the given id                                                     |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/organizations                                                | All organizations                                                          |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/organizations/<id>                                           | Organization with the given id                                             |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/organizations/<id>/users                                     | Users of the given organization                                            |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/users/<id>                                                   | User with the given id                                                     |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+

Graphics
~~~~~~~~
Graphics are based on a javascript library called `wesCountry <https://github.com/weso/wesCountry>`_, that uses svg to show the requested graphic. You can access by simply put this URL on your web browser::

	http://landportal.info/api/graphs/barchart?indicator=INDFAOGENDER2&countries=ESP,FRA,ITA&colours=FA5882,2BBBD8,FCD271&xTag=Years&yTag=Values&title=INDFAOGENDER2&description=Women%20Holders

As you can see you can define what kind of chart you want to be showed, available charts are:

* **barchart**: Chart with higher or lower bars for every value
* **linechart**: Chart with dots representing the values. These dots are connected by lines.
* **areachart**: Chart very similar to linechart, but these one colors the area below each line.
* **piechart**: Chart that shows various pies divided with a percentage according to the values in the serie.
* **polarchart**: 
* **scatterchart**:
* **table**: Table with the data

Also there are some arguments available to modify graph aspect or data. Available arguments are:

* **indicator**: Id of the indicator to be showed
* **countries**: Iso3 of the countries to be included, separated by commas
* **colours**: HTML codes without '#' and separated by commas
* **xTag**: Name for the x axis
* **yTag**: Name for the y axis
* **title**: Title for the graph
* **description**: Description for the graph
* **from_time**: Beginning date for the date range to filter data. Format required: 'YYYYMMDD'
* **to_time**: End date for the date range to filter data. Format required: 'YYYYMMDD'

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

