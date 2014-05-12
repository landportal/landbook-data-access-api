API
===
API Description
---------------
This api is based on `RESTful principles <http:http://en.wikipedia.org/wiki/Representational_state_transfer>`_. So you can access it through normal http requests.

API Security
------------
For security, a basic realm authentication is required, except graphics. Graphics are covered in the next section.

You need to obtain a token: these token then is used to authentication, so you have to authenticate with your username of landportal.info and with the generated token as the password. This token is generated when yoy register yourself in the landportal website, so you can access this token in your account info.

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

**country**
	Represents a country like Italy, France, Spain and so on.
**region**
	Represents a region like Europe or America and it has other regions or countries belonging to it. There is an special region called 'global' with un_code 1, it represents all the world.
**indicator**
	Represents a set of data grouped by the same criteria, e.g.: Women Holders, it contains various observations for various countries.
**observations**
	Represents a data observed or recollected in a moment or period of time
**user**
	Represents a source of data
**organizations**
	Represents an organization that provides data
**datasource**
	Represents a collection of datasets
**dataset**
	Represents a set of indicators with observations
**value**
	Represents a value for an observation
**topic**
	Represents a common topic among various indicators


As said before, api is based in RESTful principles, therefore you can make a petition with your browser or curl, like::

	curl landportal.info/api/countries?format=json

Formats availabe through the format argument are: **JSON**, **XML**, **CSV** and **JSONP**.
In the next table you can see all the URLs defined that you can access with a short description and arguments to modify the result. Variables in the URL are surrounded by '<' and '>':

+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| URI                                                                              | Description                                                                | Arguments                                                                       |
+==================================================================================+============================================================================+=================================================================================+
| landportal.info/api/countries                                                    | All countries                                                              |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/countries/<iso3>                                             | Country with given iso3                                                    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators                                                   | All indicators                                                             |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>                                              | Indicator with the given id                                                |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/top                                          | Top observations of the given indicator with highest values                | top: number of results                                                          |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/average                                      | Average of given indicator                                                 |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/compatible                                   | Show compatible indicators to the one given                                |                                                                                 |
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
| landportal.info/api/organizations/<organization_id>/users/<user_id>              | User with the given id of the given organization                           |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/countries/<iso3>/indicators                                  | Indicators of the given country                                            |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/countries/<iso3>indicators/<indicator_id>                    | Given indicators of the given country                                      |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/observations/<id_first_filter>/<id_second_filter>            | Observations of a region and an indicator or a country and an indicator    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/observations/<id_first_filter>/<id_second_filter>/average    | Average of the observations, same as above one                             |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/observations/<iso3>/starred                                  | Observations of a country if the indicator is starred                      |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions                                                      | All regions                                                                |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/<un_code>                                            | Region with the given un code                                              |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/<id>/countries                                       | Countries with that are part of the given region                           |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/<id>/countries/<iso3>                                | Country with the given iso3 and is part of the given region                |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/<id>/regions                                         | Regions that are part of the given region                                  |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasources                                                  | All datasources                                                            |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasources/<id>                                             | Datasource with the given id                                               |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasets                                                     | All datasets                                                               |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasets/<id>                                                | Dataset with the given id                                                  |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasources/<id>/indicators                                  | Indicators of the given datasource                                         |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasets/<id>                                                | Dataset with the given id                                                  |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/datasources/<id>/indicators/<indicator_id>                   | Indicator with the given id of the given datasource                        |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/values                                                       | All values                                                                 |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/values/<id>                                                  | Value with the given id                                                    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/measurement_units                                            | All measurement units                                                      |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/measurement_units/<id>                                       | Measurement unit with the given id                                         |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/topics                                                       | All topics                                                                 |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/topics/<id>                                                  | Topic with the given id                                                    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/topics/<topic_id>/indicators                                 | Indicators of the given topic                                              |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/topics/<topic_id>/indicators/<indicator_id>                  | Indicator with the given id of the given topic                             |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/<region_id>/countries_with_data                      | Countries that are part of the given region and have observations          |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/countries/iso3>/last_update                                  | Date of the country last update                                            |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/<iso3>/last_update                           | Date of the country last update for the given indicator                    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/observations/<id>                                            | Observations of a country, indicator or region                             |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/observations/<id>/range                                      | Observations of a country, indicator or region, betwenn two dates          | from: beginning date of the interval, end: final date of the interval           |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/range                                        | Observations of the given indicator between two dates                      | from: beginning date of the interval, end: final date of the interval           |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/regions_with_data                            | Regions with observations for the given indicator                          |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/regions_without_data                         | Regions without observations for the given indicator                       |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/average/range                                | Average of the given indicator between two dates                           | from: beginning date of the interval, end: final date of the interval           |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/<iso3>/average/range                         | Average of the given indicator and country between two dates               | from: beginning date of the interval, end: final date of the interval           |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/related                                      | Indicators with relation with the one given                                |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/<id>/<iso3>/tendency                              | Tendency of the given indicator in the given country                       |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/translations                                         | All region translations                                                    |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/regions/translations/<region_id>/<lang_code>                 | Region translation of the given region in the given language               |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/translations                                      | All indicator translations                                                 |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicator/translations/<indicator_id>/<lang_code>            | Indicator translation of the given indicator in the given language         |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/topics/translations                                          | All topic translations                                                     |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/topics/translations/<topic_id>/<lang_code>                   | Topic translation of the given topic in the given language                 |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+
| landportal.info/api/indicators/starred                                           | Indicators that are starred, normally those which are on the main page     |                                                                                 |
+----------------------------------------------------------------------------------+----------------------------------------------------------------------------+---------------------------------------------------------------------------------+


Outputs that can change depending on the language, have another parameter available, this is: lang, so you can use lang=fr to get it on French. Translations are available for: Regions, Countries, Indicators and Topics.

Some example outputs are::

	landportal.info/api/indicators/INDFAOGENDER1
	landportal.info/api/countries/ESP

.. image:: images/indicator.PNG

.. image:: images/country.PNG

Graphics
~~~~~~~~
Graphics are based on a javascript library called `wesCountry <https://github.com/weso/wesCountry>`_. wesCountry uses svg to show the requested graphic. You can access by simply put this URL on your web browser::

	http://landportal.info/api/graphs/barchart?indicator=INDFAOGENDER2&countries=ESP,FRA,ITA&colours=FA5882,2BBBD8,FCD271&xTag=Years&yTag=Values&title=INDFAOGENDER2&description=Women%20Holders

As you can see you can define what kind of chart you want to be showed, available charts are:

* **barchart**: Chart with higher or lower bars for every value
* **linechart**: Chart with dots representing the values. These dots are connected by lines.
* **areachart**: Chart very similar to linechart, but this one colors the area below each line.
* **piechart**: Chart that shows various pies divided with a percentage according to the values in the serie.
* **polarchart**: Chart that shows three or more variables represented on axes starting from the same point.
* **scatterchart**: Chart that shows various points but without connecting the dots
* **table**: Table with the data

Also there are some arguments available to modify graph aspect or data. Available arguments are:

* **indicator**: Id of the indicator to be showed, two indicators separated with comma in the case of scatterchart
* **countries**: Iso3 of the countries to be included, separated by commas
* **colours**: HTML codes without '#' and separated by commas
* **xTag**: Name for the x axis
* **yTag**: Name for the y axis
* **title**: Title for the graph
* **description**: Description for the graph
* **from_time**: Beginning date for the date range to filter data. Format required: 'YYYYMMDD'
* **to_time**: End date for the date range to filter data. Format required: 'YYYYMMDD'

You can see below examples for barchart and piechart:

.. image:: images/bar.PNG

.. image:: images/pie.PNG