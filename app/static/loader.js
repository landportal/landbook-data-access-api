function loadjscssfile(filename, filetype) {
	if (filetype == "js") {
  		var fileref = document.createElement('script');
  		fileref.setAttribute("type","text/javascript");
  		fileref.setAttribute("src", filename);
 	}
 	else if (filetype=="css") {
  		var fileref = document.createElement("link")
  		fileref.setAttribute("rel", "stylesheet")
  		fileref.setAttribute("type", "text/css")
  		fileref.setAttribute("href", filename)
 	}
 
 	if (typeof fileref!="undefined")
  		document.getElementsByTagName("head")[0].appendChild(fileref)
}

loadjscssfile("wesCountry.min.css", "css");
loadjscssfile("wesCountry.min.js", "js");

function callback(data) {
	var id = wesCountry.guid();
	document.write('<div id="landportal-widget-' + id + '"></div>');
	
	var container = document.getElementById('landportal-widget-' + id);
	data.container = '#landportal-widget-' + id;
	data.width = container.offsetWidth;
	data.height = '500';
	var chartType = data.chartType

	if (!chartType)
		wesCountry.maps.createMap(data);
	else
		wesCountry.charts.chart(data);
}