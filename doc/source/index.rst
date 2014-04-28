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
As said before, api is based in RESTful principles, therefore you can make a petition with your browser or curl like::

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

