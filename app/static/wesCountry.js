function HashTable(obj)
{
    this.length = 0;
    var items = {};
    var keys = new SortedArray();
    
    
    for (var p in obj) {
        if (obj.hasOwnProperty(p)) {
            items[p] = obj[p];
            this.length++;
        }
    }

    this.setItem = function(key, value)
    {
        var previous = undefined;
        
        if (keys.search(key) != -1) {
            previous = items[key];
        }
        else {
            this.length++;
        }
        
        items[key] = value;
        keys.uniqueInsert(key);
        
        return previous;
    }

    this.getItem = function(key) {
        return keys.search(key) != -1 ? items[key] : undefined;
    }

    this.hasItem = function(key)
    {
        return keys.search(key) != -1;
    }
   
    this.removeItem = function(key)
    {
        if (keys.search(key) != -1) {
            previous = items[key];
            this.length--;
            delete items[key];
            keys.remove(key);
            
            return previous;
        }
        else {
            return undefined;
        }
    }

    this.keys = function()
    {
        return keys;
    }

    this.values = function()
    {
        var values = [];
        var key;
        
        for (var i = 0; i < keys.getArray().length; i++) {
	        key = keys.getArray()[i];
            values.push(items[key]);
        }
        
        return values;
    }

    this.each = function(fn) {
        for (var k in keys) {
                fn(k, items[k]);
        }
    }

    this.clear = function()
    {
        items = {}
        keys = new SortedArray();
        this.length = 0;
    }
}String.format = function(pattern)
{
	for (var i = 1; i < arguments.length; i++)
	{
		var regex = new RegExp('\\{' + (i - 1) + '\\}', 'g');
		pattern = pattern.replace(regex, arguments[i]);
	}
	return pattern;
};

/**
 * wesCountry object.
 * @constructor
 */
var wesCountry = new (function() {
	this.version = "1.0.0.0";
	
	function s4() {
  		return Math.floor((1 + Math.random()) * 0x10000)
    		.toString(16)
        	.substring(1);
	}

	this.guid = function() {
  		return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         	s4() + '-' + s4() + s4() + s4();
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                              MERGING OPTIONS
	////////////////////////////////////////////////////////////////////////////////
	
	this.mergeOptionsAndDefaultOptions = function(options, defaultOptions) {
		if (options) {
			if (typeof options === "string")
				options = { container: options };
		
			var auxOptions = this.clone(defaultOptions);
			
			for (var option in options)
				auxOptions[option] = mergeOptions(auxOptions[option], options[option]);
			
			options = auxOptions;
		}
		else
			options = this.clone(defaultOptions);
			
		return options;
	};
	
	function mergeOptions(to, from) {
		if (from instanceof Array) {
			return from;
		}
		else if (typeof from === "object") {
			for (var option in from) {
				to[option] = mergeOptions(to[option], from[option]);
			}

			return to;
		}
		else
			return from;
	};
	
	this.clone = function(obj) {
		// Not valid for copying objects that contain methods
	    //return JSON.parse(JSON.stringify(obj));
	    if (null == obj || "object" != typeof obj) return obj;
	    
	    var copy = obj.constructor();
	    
	    for (var attr in obj) {
	        if (obj.hasOwnProperty(attr)) copy[attr] = obj[attr];
	    }
	    
	    return copy;
	};
	
	////////////////////////////////////////////////////////////////////////////////
	//                              COLOUR RANGE
	////////////////////////////////////////////////////////////////////////////////	
	
	this.colourRange = function(range, numberOfElements) {
		if (numberOfElements <= range.length)
			return range.slice(0, numberOfElements);
			
		var elementsPerRange = numberOfElements / (range.length - 1);
		
		var colours = [];
	
		for (var i = 0; i < range.length - 1; i++) {
			var colour1 = hexToRGB(range[i]);
			var colour2 = hexToRGB(range[i + 1]);

			for (var j = 0; j < elementsPerRange; j++) {
				var percent = (j / elementsPerRange) * 100;
				colours.push(makeColourGradient(colour1, colour2, percent).cssColour);
			}
		}
		
		return colours;
	};
	
	function hexToRGB(hex) {
    	var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    
    	if (!result) {
    		var result = /^#?([a-f\d]{1})([a-f\d]{1})([a-f\d]{1})$/i.exec(hex);
    		
    		result[1] = result[1] + "" + result[1];	
    		result[2] = result[2] + "" + result[2];	
    		result[3] = result[3] + "" + result[3];	
    	}
    	
    	return result ? {
        	r: parseInt(result[1], 16),
        	g: parseInt(result[2], 16),
        	b: parseInt(result[3], 16)
    	} : null;
	}
	
	function makeColourGradient(colour1, colour2, percent) {
		var newColour = {};

		function makeChannel(a, b) {
			return(a + Math.round((b - a) * (percent / 100)));
		}

		function makeColourPiece(num) {
			num = Math.min(num, 255);   // not more than 255
			num = Math.max(num, 0);     // not less than 0
		
			var str = num.toString(16);
		
			if (str.length < 2) {
				str = "0" + str;
			}
		
			return(str);
		}

		newColour.r = makeChannel(colour1.r, colour2.r);
		newColour.g = makeChannel(colour1.g, colour2.g);
		newColour.b = makeChannel(colour1.b, colour2.b);
		newColour.cssColour = "#" + 
							makeColourPiece(newColour.r) + 
							makeColourPiece(newColour.g) + 
							makeColourPiece(newColour.b);
						
		return(newColour);
	};
})();var jSVG = new (function() {
	function jSVGElement(elementName) {
		var namespace = "http://www.w3.org/2000/svg";
		var version = "1.1";
		var xlink = "http://www.w3.org/1999/xlink";
		
		var defaultSVGOptions = {
			width: 500,
			height: 500,
			version: version
		};
		
		var defaultElementOptions = {
			fill: "black",
			stroke: "none",
			"stroke-width": "1",
			x: "0",
			y: "0",
			width: "10",
			height: "10",
			r: "5",
			cx: "5",
			cy: "5",
			x1: 0,
			x2: 10,
			y1: 0,
			y2: 10
		};
		
		var attr = function(namespace, name, value) {
			this.namespace = namespace;
			this.name = name;
			this.value = value;
		};
		
		var myTag = elementName;
		var myAttributes = {};
		var myEvents = {};
		var myStyle = "";
		var myValue = undefined;
		var myChildNodes = [];
	
		this.svg = function(options) {
			/*if (options) {
				if (typeof options === "string")
					options = { container: options };
				
				//options = mergeOptions(defaultSVGOptions, options);
			}
			else
				options = {};
				*/
			if (!options)
				options = { };
		
			//this = document.createElementNS(namespace, "svg");
			return createElement(null, "svg", options, defaultSVGOptions);
	
			//setAttributes(this, options);
			//this.setAttributeNS("http://www.w3.org/2000/xmlns/", "xmlns:xlink", "http://www.w3.org/1999/xlink");
			
			//var container = options.container;
		
			//if (typeof container === "string")
			//	container = document.querySelector(container);
			
			//container.appendChild(this);
				
			//return this;
		}
		
		this.elementByName = function(name, options) {
			return createElement(this, name, options, defaultElementOptions);
		}	
		
		this.g = function(options) {
			return createElement(this, "g", options, defaultElementOptions);
		}
		
		this.path = function(options) {
			return createElement(this, "path", options, defaultElementOptions);
		}
			
		this.rectangle = function(options) {
			return createElement(this, "rect", options, defaultElementOptions);
		}
		
		this.circle = function(options) {
			return createElement(this, "circle", options, defaultElementOptions);
		}
		
		this.line = function(options) {
			return createElement(this, "line", options, defaultElementOptions);
		}
		
		this.text = function(options) {
			var element = createElement(this, "text", options, defaultElementOptions);
			element.value(options.value);
			
			return element;
		}
		
		this.a = function(options, url) {
			var anchor = createElement(this, "a", options, defaultElementOptions);
			anchor.attribute(xlink, "xlink:href", url);
			return anchor;
		}
	
		this.attribute = function(namespace, name, value) {
			myAttributes[name] = new attr(namespace, name, value);
			return this;
		}
		
		this.attributes = function(attributes) {
			myAttributes = attributes;
			return this;
		}
		
		this.style = function(value) {
			myStyle = value;
			return this;
		}
		
		this.value = function(value) {
			myValue = value;
			return this;
		}
		
		this.event = function(name, action) {
			myEvents[name] = action;
			return this;
		}
		
		this.width = function() {
			return myAttributes.width.value;
		}
		
		this.height = function() {
			return myAttributes.height.value;
		}
		
		this.appendChild = function(node) {
			myChildNodes.push(node);
		}
		
		function createElement(parent, elementName, attributes, defaultAttributes) {
			var element = new jSVGElement(elementName);
			
			setAttributes(element, attributes, defaultAttributes);
			
			if (parent)
				parent.appendChild(element);
				
			return element;
		}
	
		function setAttributes(element, attributes, defaultAttributes) {
			attributes = mergeOptions(defaultAttributes, attributes);
			
			var attrs = {};
			
			for (var attribute in attributes) {
				attrs[attribute] = new attr(null, attribute, attributes[attribute]);
			}
			
			element.attributes(attrs);
		}
		
		function mergeOptions(defaultOptions, options) {
			var mergedOptions = cloneObject(defaultOptions);

			if (options) {
				for (var option in options)
					mergedOptions[option] = options[option];
			}
			
			return mergedOptions;
		}
		
		function cloneObject(obj) {
		    // Not valid for copying objects that contain methods
		    return JSON.parse(JSON.stringify(obj));
		}
		
		this.render = function() {
			var element = document.createElementNS(namespace, myTag);
		
			for (var attribute in myAttributes) {
				var attr = myAttributes[attribute];
				element.setAttributeNS(attr.namespace, attr.name, attr.value);	
			}
			
			element.setAttributeNS(null, "style", myStyle);
			
			for (var event in myEvents) {
				element[event] = myEvents[event];
			}
			
			for (var i = 0; i < myChildNodes.length; i++)
				element.appendChild(myChildNodes[i].render());
			
			if (myValue) {
				var textNode = document.createTextNode(myValue);
				element.appendChild(textNode);
			}
			
			return element;
		}
		
		this.toString = function() {
			var attributes = "";
		
			for (var attribute in myAttributes) {
				var attr = myAttributes[attribute];
				attributes += String.format(' {0}="{1}"', attr.name, attr.value);
			}
			
			var childNodes = "";
			
			for (var i = 0; i < myChildNodes.length; i++)
				childNodes += myChildNodes[i].toString();
		
			return String.format('<{0} xmlns="{1}" {2} style="{3}">{4}{5}</{0}>', 
					myTag, namespace, attributes, myStyle, childNodes, myValue ? myValue : "");
		}
	}
	
	return new jSVGElement();
	
})();String.format = function(pattern)
{
	for (var i = 1; i < arguments.length; i++)
	{
		var regex = new RegExp('\\{' + (i - 1) + '\\}', 'g');
		pattern = pattern.replace(regex, arguments[i]);
	}
	return pattern;
};

String.prototype.toFirstUpperCase = function() {
	var firstLetter = this[0].toUpperCase();
	var stringWithoutFirstLetter = this.substr(1);
	return firstLetter+stringWithoutFirstLetter;
}

if (typeof(exports) === "undefined")
	exports = new Object();
	
if (typeof(wesCountry) === "undefined")
	var wesCountry = {};

wesCountry.charts = new (function() {
	this.defaultOptions = {
		width: 600,
		height: 400,
        chartType: "bar",
        container: "body",
		margins: [10, 20, 10, 5],
		backgroundColour: "none",
		serieColours: ["#FCD271", "#FA5882", "#2BBBD8", "#102E37"],
		overColour: "#333",
		groupMargin: 4,
		barMargin: 8,
		sortSeries: false,
		valueOnItem: {
			show: true,
			margin: 5,
			"font-family": "Helvetica",
			"font-colour": "#aaa",
			"font-size": "16px",
		},
		xAxis: {
			title: "Months",
			colour: "none",
			margin: 10,
			tickColour: "none",
			values: ["Jan", "Feb", "Mar", "Apr", "May"],
			"font-family": "Helvetica",
			"font-colour": "#666",
			"font-size": "16px"
		},
		yAxis: {
			title: "Values",
			colour: "none",
			margin: 10,
			tickColour: "#ccc",
			"font-family": "Helvetica",
			"font-colour": "#aaa",
			"font-size": "16px",
			"from-zero": false
		},
		series: [{
            name: "First",
            values: [-1, 4, 5, 3, 6],
            urls: ["http://www.google.es", "http://www.google.es", "http://www.google.es", "http://www.google.es", "http://www.google.es"]
        }, {
            name: "Second",
            values: [1, 7, 5, 6, 4],
            urls: ["http://www.google.es", "http://www.google.es", "http://www.google.es", "http://www.google.es", "http://www.google.es"]
        }, {
        	name: "Third",
        	values: [0, 1, 2, 3, 4],
        	urls: ["http://www.google.es", "http://www.google.es", "http://www.google.es", "http://www.google.es", "http://www.google.es"]
        }],
        legend: {
	        show: true,
	        itemSize: 1,
	        "font-colour": "#666",
			"font-family": "Helvetica",
			"font-size": "16px"
        },
        tooltip: {
	        show: true,
	        style: {
			    display: "none",
			    padding: "0.8em 0.5em",
			    "font-size": "12px",
			    border: "0.1em solid #ccc",
			    "background-color": "#fff",
			    position: "absolute",
			    color: "#000",
	        }
        },
        events: {
	        "onmouseover": function(serie, pos, value) {
		    	var text = String.format("Series '{0}': ({1}, {2})", serie, pos, value);
		    	console.log(text);
		    	wesCountry.charts.showTooltip(text);
	        },
	        "onmouseout": function() {
	        	wesCountry.charts.hideTooltip();
	        },
	        "onclick": function() {
	        
	        }
        },
        vertex: {
        	show: true
        },
        stroke: {
        	width: 1
        }
	};
	
	////////////////////////////////////////////////////////////////////////////////
	//                                 SORT SERIES
	////////////////////////////////////////////////////////////////////////////////
	
	// We evaluate the number of values of this series than are greater than the other series
	
	this.sortSeries = function(series) {
		series.sort(function(a, b) {
			var values1 = a.values;
			var values2 = b.values;
			var length = Math.max(values1.length, values2.length);
			
			var greatCounter = 0;
			
			for (var i = 0; i < length; i++) {
				var value1 = values1[i] ? values1[i] : 0;
				var value2 = values2[i] ? values2[i] : 0;
				
				if (value1 > value2)
					greatCounter++;
			}
			
			// We suppose that it's greater when han at least the half of the elements greater
			return greatCounter >= length / 2 ? -1 : 1;
		});
		
		return series;
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                                     SVG
	////////////////////////////////////////////////////////////////////////////////
	
	this.getSVG = function(options) {
		var svgOptions = {
			width: options.width,
			height: options.height	
		};
		
		var svg = jSVG.svg(svgOptions);
		
		return svg;
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                                 LEGEND
	////////////////////////////////////////////////////////////////////////////////
	
	this.showLegend = function(container, sizes, options) {
		var length = options.series.length;
	
		var xPos = sizes.width - sizes.marginRight * 0.2;
	
		for (var i = 0; i < length; i++) {
			var yPos = sizes.marginTop + (sizes.legendItemSize + sizes.barMargin) * 2.5 * i;
		
			container.circle({
				cx: xPos,
				cy: yPos,
				r: sizes.legendItemSize
			}).style(String.format("fill: {0}", options.serieColours[i % options.serieColours.length]));
			
			container.text({
				x: xPos - 2 * sizes.legendItemSize,
				y: yPos,
				value: options.series[i].name
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: end;dominant-baseline: middle", 
				options.legend["font-colour"],
				options.legend["font-family"],
				options.legend["font-size"]));
		}
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                                   AXIS
	////////////////////////////////////////////////////////////////////////////////
	
	this.setAxisY = function(container, sizes, options) {
		// Y Axis

		container.line({
			x1: sizes.marginLeft + sizes.yAxisMargin,
			x2: sizes.marginLeft + sizes.yAxisMargin,
			y1: sizes.marginTop,
			y2: sizes.innerHeight + sizes.marginTop - sizes.xAxisMargin
		}).style(String.format("stroke: {0}", options.yAxis.colour));
	
		// Y Axis Ticks
		
		var length = sizes.ticksY + 1;
		
		// Line
		for (var i = 0; i < length; i++) {
			container.line({
				x1: sizes.marginLeft + sizes.yAxisMargin,
				x2: sizes.marginLeft + sizes.innerWidth,
				y1: sizes.marginTop + i * sizes.yTickHeight,
				y2: sizes.marginTop + i * sizes.yTickHeight
			}).style(String.format("stroke: {0}", options.yAxis.tickColour));
		}
			
		// Y Axis Labels
		for (var i = 0; i < length; i++) {	
			container.text({
				x: sizes.marginLeft + sizes.yAxisMargin / 1.8,
				y: sizes.marginTop + i * sizes.yTickHeight,
				value: (sizes.maxValue - i * sizes.valueInc).toFixed(0)
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: end;dominant-baseline: middle", 
				options.yAxis["font-colour"],
				options.yAxis["font-family"],
				options.yAxis["font-size"]));
		}
		
		// Y Axis Title
		var x = sizes.marginLeft;
		var y = sizes.marginTop + (sizes.innerHeight - sizes.xAxisMargin) / 2;
		
		container.text({
			x: x,
			y: y,
			value: options.yAxis.title,
			transform: String.format("rotate(-90 {0}, {1})", x, y)
		}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle", 
				options.yAxis["font-colour"],
				options.yAxis["font-family"],
				options.yAxis["font-size"]));
	}

	this.setAxisX = function(container, sizes, options) {		
		// X Axis
		
		var maxHeight = sizes.innerHeight - sizes.xAxisMargin;
		var minValuePos = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin	
					+ sizes.minValue / (sizes.maxValue - sizes.minValue) * maxHeight;
	
		container.line({
			x1: sizes.marginLeft + sizes.yAxisMargin,
			x2: sizes.marginLeft + sizes.innerWidth,
			y1: minValuePos,
			y2: minValuePos
		}).style(String.format("stroke: {0}", options.xAxis.colour));
		
		// X Axis Ticks
		
		var length = sizes.maxValueLength;
		
		for (var i = 0; i < length; i++) {
			// Line
			
			var xPos = sizes.marginLeft + sizes.yAxisMargin + sizes.groupMargin 
				+ sizes.xTickWidth / 2 + (sizes.xTickWidth + 2 * sizes.groupMargin) * i;
		
			container.line({
				x1: xPos,
				x2: xPos,
				y1: sizes.marginTop,
				y2: sizes.innerHeight + sizes.marginTop - sizes.xAxisMargin
			}).style(String.format("stroke: {0}", options.xAxis.tickColour));
			
			// Label
			
			var value = options.xAxis.values[i] ? options.xAxis.values[i] : "";
			
			container.text({
				x: xPos,
				y: sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin / 2,
				value: value
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle", 
				options.xAxis["font-colour"],
				options.xAxis["font-family"],
				options.xAxis["font-size"]));
		}
		
		// X Axis Title
		
		container.text({
			x: sizes.marginLeft + sizes.yAxisMargin + (sizes.innerWidth - sizes.yAxisMargin) / 2,
			y: sizes.marginTop + sizes.innerHeight + sizes.xAxisMargin / 2,
			value: options.xAxis.title
		}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle", 
				options.xAxis["font-colour"],
				options.xAxis["font-family"],
				options.xAxis["font-size"]));
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                               MAX AXIS VALUES
	////////////////////////////////////////////////////////////////////////////////
	
	this.getMaxAndMinValuesAxisY = function(options) {
		var maxValue = 0, minValue = Number.MAX_VALUE;
		
		var length = options.series.length;
		var valueLength = null;
		var value = null;
		var maxValueLength = 0;
	
		for (var i = 0; i < length; i++) {
			valueLength = options.series[i].values.length;
			
			if (valueLength > maxValueLength)
				maxValueLength = valueLength;
			
			for (var j = 0; j < valueLength; j++) {
				value = options.series[i].values[j];
				
				if (value instanceof Array)
					value = value[1] ? value[1] : 0;
				
				if (value > maxValue)
					maxValue = value;
					
				if (value < minValue)
					minValue = value;
			}
		}
		
		if (options.yAxis["from-zero"] == true && minValue > 0)
			minValue = 0;
		
		
		var maxAndMinValues = this.getNearestNumber(minValue, maxValue);
	
		return { 
			max: maxAndMinValues.max, 
			min: maxAndMinValues.min, 
			valueLength: maxValueLength,
			inc: maxAndMinValues.inc
		};
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                              AUX FUNCTIONS
	////////////////////////////////////////////////////////////////////////////////	
	
	this.setBackground = function(container, sizes, options) {
		container.rectangle({
			x: 0,
			y: 0,
			width: sizes.width,
			height: sizes.height
		}).style(String.format("fill: {0}", options.backgroundColour));
	}	
	
	this.getNearestNumber = function(minValue, maxValue) {
		var pow = getNearestPow(maxValue - minValue);
		
		return  {
			max: Math.ceil(maxValue / pow) * pow,
			min: Math.floor(minValue / pow) * pow,
			inc: pow
		}
	}
	
	function getNearestPow(number) {
		var pow = 0;
	
		if (number < 15) {
			pow = 1;
		}
		else if (number < 30) {
			pow = 5;
		}
		else {
			var numberOfDigits = 1 + Math.floor(Math.log(number) / Math.log(10));
			pow = Math.pow(10, numberOfDigits - 1);
		}
		
		return pow;
	}
	
	function s4() {
  		return Math.floor((1 + Math.random()) * 0x10000)
    		.toString(16)
        	.substring(1);
	}

	this.guid = function() {
  		return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
         	s4() + '-' + s4() + s4() + s4();
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                                   TOOLTIP
	////////////////////////////////////////////////////////////////////////////////
	
	var tooltip = null;
	
	this.createTooltip = function(options) {
		if (options.tooltip.show == true) {
			tooltip = document.getElementById("wesCountryTooltip");
			
			if (!tooltip) {
				tooltip = document.createElement("span");
				tooltip.id = "wesCountryTooltip";
				document.body.appendChild(tooltip);
				
				var style = "";
				
				for (var attr in options.tooltip.style) {
					var element = options.tooltip.style[attr];
						
					style += String.format("{0}:{1};", attr, element);
				}
				
				tooltip.setAttribute("style", style);
			}
		}
		else
			tooltip = null;
	}
	
	this.showTooltip = function(text) {
		if (!tooltip)
			return;
		
    	updateTooltipPos();
    	tooltip.innerHTML = text;
    	tooltip.style.display = "block";
    	window.onscroll = updateTooltipPos;
    }
    
    function updateTooltipPos() {
		if (!tooltip)
			return;    
    
    	var ev = arguments[0]?arguments[0]:event;
    	var x = ev.clientX;
    	var y = ev.clientY;
    	diffX = 24;
    	diffY = 0;
    	tooltip.style.top  = y - 2 + diffY + document.body.scrollTop + "px";
    	tooltip.style.left = x - 2 + diffX + document.body.scrollLeft + "px";
    }

    this.hideTooltip = function() {
		if (!tooltip)
			return;    
    
    	tooltip.style.display = "none";
    }

})();////////////////////////////////////////////////////////////////////////////////
//                                  BAR CHART
////////////////////////////////////////////////////////////////////////////////
	
wesCountry.charts.barChart = function(options) {
	return renderChart();

	function renderChart() {
		// Options and default options
		options = wesCountry.mergeOptionsAndDefaultOptions(options, wesCountry.charts.defaultOptions);	
		options.yAxis["from-zero"] = true;
		
		if (options.sortSeries)
			options.series = wesCountry.charts.sortSeries(options.series);
		
		// SVG creation
		var svg = wesCountry.charts.getSVG(options);
		
		// Size and margins (%)
		var sizes = getSizes(svg, options);
		
		var g = svg.g();

		// Background
	
		wesCountry.charts.setBackground(g, sizes, options); 		
				
		// X Axis & Y Axis		
		wesCountry.charts.setAxisY(g, sizes, options);
		wesCountry.charts.setAxisX(g, sizes, options);
		
		// Values
		var length = sizes.maxValueLength;
		var numberOfSeries = options.series.length;
		
		var barMargin = options.barMargin * sizes.xTickWidth / 100;	
		var groupMargin = options.groupMargin * sizes.xTickWidth / 100;
		
		var barWidth = sizes.barWidth;

		var maxHeight = sizes.innerHeight - sizes.xAxisMargin;
		var minValuePos = sizes.minValue / (sizes.maxValue - sizes.minValue) * maxHeight;
	
		// Values
		
		for (var i = 0; i < length; i++) {
			for (var j = 0; j < numberOfSeries; j++) {
				var serie = options.series[j].name;
				var value = options.series[j].values[i];
				var url = options.series[j].urls ? options.series[j].urls[i] : "";
				var pos = options.xAxis.values[j];
				
				if (!value)
					value = 0;
				
				var xPos = sizes.marginLeft + sizes.yAxisMargin + sizes.groupMargin * (2 * i + 1) + sizes.barMargin
						+ sizes.xTickWidth * i 
						+ (barWidth + 2 * sizes.barMargin) * j;
						
				if (value >= 0)	{
					var yPos = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin
							+ minValuePos
							- (value / (sizes.maxValue - sizes.minValue)) 
							* maxHeight;
				}
				else {
					var yPos = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin
							+ minValuePos
				}
						
				var height = (Math.abs(value) / (sizes.maxValue - sizes.minValue)) 
						* maxHeight;
					
				var rectangleOptions = {
					x: xPos,
					y: yPos,
					width: barWidth,
					height: height,
					serie: serie,
					value: value,
					pos: pos
				};			
				
				var rectangleStyle = String.format("fill: {0}", options.serieColours[j]);
			
				// Events
			
				var onmouseover = function() {
					this.colour = this.style.fill;
					this.style.fill = options.overColour;
					
					options.events.onmouseover(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
				};
											
				var onmouseout = function() { 
					this.style.fill = this.colour;
					options.events.onmouseout(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
				};
				
				var onclick = function() { 
					this.style.fill = this.colour;
					options.events.onclick(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
				};
				
				if (url && url != "") {
					var a = g.a({}, url ? url : "")
					var r = a.rectangle(rectangleOptions).style(rectangleStyle)
					.event("onmouseover", onmouseover).event("onmouseout", onmouseout).event("onclick", onclick);
				}
				else {
					var r = g.rectangle(rectangleOptions).style(rectangleStyle)
					.event("onmouseover", onmouseover).event("onmouseout", onmouseout).event("onclick", onclick);
				}			
			
				// Value on bar
				if (options.valueOnItem.show == true) {
					g.text({
						x: xPos + barWidth / 2,
						y: yPos - (options.height / 100) * options.valueOnItem.margin,
						value: value.toFixed(2)
					}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle;dominant-baseline: middle", 
						options.valueOnItem["font-colour"],
						options.valueOnItem["font-family"],
						options.valueOnItem["font-size"]));
				}
			}
		}
		
		// Legend
		if (options.legend.show)
			wesCountry.charts.showLegend(g, sizes, options);
		
		// Tooltip
		wesCountry.charts.createTooltip(options);			
			
		return svg;
	}
	
	function getSizes(svg, options) {
		var width = svg.width(); 
		var height = svg.height();
		var marginTop = height * options.margins[0] / 100;
		var marginRight = width * options.margins[1] / 100;
		var marginBottom = height * options.margins[2] / 100;
		var marginLeft = width * options.margins[3] / 100;
		var yAxisMargin = options.yAxis.margin * width / 100;
		var xAxisMargin = options.xAxis.margin * height / 100;
		var innerWidth = width - marginLeft - marginRight;
		var innerHeight = height - marginTop - marginBottom;
		
		// Max value & min value
		var maxAndMinValues = wesCountry.charts.getMaxAndMinValuesAxisY(options);
		var maxValue = maxAndMinValues.max;
		var minValue = maxAndMinValues.min > 0 ? 0 : maxAndMinValues.min;
		var maxValueLength = maxAndMinValues.valueLength; 	
		
		var ticksY = (maxValue - minValue) / maxAndMinValues.inc;
		var yTickHeight = ticksY != 0 ? (innerHeight - xAxisMargin) / ticksY : 0;
		var xTickWidth = (innerWidth - yAxisMargin) / maxAndMinValues.valueLength;		
		
		var groupMargin = options.groupMargin * xTickWidth / 100;	
		xTickWidth -= 2 * groupMargin;
			
		var barWidth = xTickWidth / options.series.length;	
		var barMargin = options.barMargin * barWidth / 100;	
		barWidth -= 2 * barMargin;			
				
		var valueInc = ticksY != 0 ? (maxValue - minValue) / ticksY : 0;

		var legendItemSize = options.legend.itemSize * width / 100;

		return {
			width : width,
			height : height,
			marginTop : marginTop,
			marginRight : marginRight,
			marginBottom : marginBottom,
			marginLeft : marginLeft,
			
			innerWidth : innerWidth,
			innerHeight : innerHeight,
			
			yAxisMargin: yAxisMargin,
			xAxisMargin: xAxisMargin,
			
			maxValue: maxValue,
			minValue: minValue,
			maxValueLength: maxValueLength,
			
			ticksY: ticksY,
			yTickHeight: yTickHeight,
			xTickWidth: xTickWidth,
			valueInc: valueInc,
			
			barMargin: barMargin,
			groupMargin: groupMargin,
			barWidth: barWidth,
			
			legendItemSize: legendItemSize
		};
	}		
};////////////////////////////////////////////////////////////////////////////////
//                                  LINE CHART
////////////////////////////////////////////////////////////////////////////////
	
wesCountry.charts.lineChart = function(options) {
	return this.generateLineChart(options, false);
}	

////////////////////////////////////////////////////////////////////////////////
//                                  AREA CHART
////////////////////////////////////////////////////////////////////////////////
	
wesCountry.charts.areaChart = function(options) {
	return this.generateLineChart(options, true);
}
	
// Auxiliary line fuction	
	
wesCountry.charts.generateLineChart = function(options, area) {
	return renderChart();

	function renderChart() {
		// Options and default options
		options = wesCountry.mergeOptionsAndDefaultOptions(options, wesCountry.charts.defaultOptions);	

		if (options.sortSeries)
			options.series = wesCountry.charts.sortSeries(options.series);
		
		// SVG creation
		var svg = wesCountry.charts.getSVG(options);
		
		// Size and margins (%)
		var sizes = getSizes(svg, options);
		
		var g = svg.g();
	
		// Background
	
		wesCountry.charts.setBackground(g, sizes, options); 
				
		// X Axis & Y Axis		
		wesCountry.charts.setAxisY(g, sizes, options);
		wesCountry.charts.setAxisX(g, sizes, options);
				
		// Values
		var length = options.series.length;
		var valueLength = sizes.maxValueLength;
	
		var maxHeight = sizes.innerHeight - sizes.xAxisMargin;
		var zeroPos = sizes.minValue / (sizes.maxValue - sizes.minValue) * maxHeight;
		
		// Iteration
		for (var i = 0; i < length; i++) {
			// Polygon path
			var pathD = "";
			if (area) {
				var path = g.path();
			}
			// Position of zero y line
			var minValue = Math.max(0, sizes.minValue);
			var posZero = getYPos(minValue, sizes, zeroPos, maxHeight);
		
			var lineId = "l" + wesCountry.charts.guid();
			
			for (var j = 0; j < valueLength; j++) {
				var value = options.series[i].values[j];
				var valuePrev = j > 0 ? options.series[i].values[j - 1] : 0;
				var url = options.series[i].urls ? options.series[i].urls[j] : "";
				
				var serie = options.series[i].name;
				var pos = options.xAxis.values[j];
				
				if (!value)
					value = 0;
					
				if (!valuePrev)
					valuePrev = 0;
				
				var xPos = getXPos(j, sizes, zeroPos);
				var yPos = getYPos(value, sizes, zeroPos, maxHeight);
				var xPosPrev = getXPos(j - 1, sizes, zeroPos);	
				var yPosPrev = getYPos(valuePrev, sizes, zeroPos, maxHeight);
				
				var pointOptions = {
					cx: xPos,
					cy: yPos,
					r: 5,
					"class": lineId,
					serie: serie,
					value: value,
					pos: pos
				};
				
				var pointStyle = String.format("fill: {0}", options.serieColours[i % options.serieColours.length]);
				
				var setLineWidth = function(element, stroke) {
					var className = element.getAttribute("class");
					var lines = element.parentNode.querySelectorAll("line." + className);
					var length = lines.length;
				
					for (var k = 0; k < length; k++) {
						lines[k].setAttribute("stroke-width", stroke)
					}	
				};
				
				var onmouseover = function() { 
					this.setAttribute("r", 8);
					setLineWidth(this, 2);
					options.events.onmouseover(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
				};
											
				var onmouseout = function() { 
					this.setAttribute("r", 5); 
					setLineWidth(this, 1);
					options.events.onmouseout(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
				};
				
				var onclick = function() { 
					this.setAttribute("r", 5); 
					setLineWidth(this, 1);
					options.events.onclick(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
				};
				
				if (options.vertex.show) {
					if (url && url != "") {
						var a = g.a({}, url ? url : "")
						a.circle(pointOptions)
						.style(pointStyle).event("onmouseover", onmouseover).event("onmouseout", onmouseout).event("onclick", onclick);
					}
					else {
						g.circle(pointOptions)
						.style(pointStyle).event("onmouseover", onmouseover).event("onmouseout", onmouseout).event("onclick", onclick);
					}
				}
							
				// Value on bar		
				if (options.valueOnItem.show == true) {
					g.text({
						x: xPos,
						y: yPos - (options.height / 100) * options.valueOnItem.margin,
						value: value == 0 ? "0" : value.toFixed(2)
					}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle;dominant-baseline: middle", 
						options.valueOnItem["font-colour"],
						options.valueOnItem["font-family"],
						options.valueOnItem["font-size"])
					);
				}
				
				if (j > 0) {
					g.line({
						x1: xPosPrev,
						x2: xPos,
						y1: yPosPrev,
						y2: yPos,
						"stroke-width": options.stroke.width,
						"class": lineId
					}).style(String.format("stroke: {0}", options.serieColours[i % options.serieColours.length]))
					.event("onmouseover", function() { setLineWidth(this, options.stroke.width * 1.5); })
					.event("onmouseout", function() { setLineWidth(this, options.stroke.width); });
					
					pathD += String.format(" L{0} {1}", xPos, yPos);
				}
				else {
					pathD = String.format("M{0} {1} L{2} {3}", xPos, posZero, xPos, yPos);
				}
			}
			
			pathD += String.format(" L{0} {1} Z", xPos, posZero);
			if (area) {
				path.attribute(null, "d", pathD)
				.style(String.format("stroke: {0}; fill: {0}; opacity: 0.5", options.serieColours[i % options.serieColours.length]));
			}
		}

		// Legend
		if (options.legend.show)
			wesCountry.charts.showLegend(g, sizes, options);
			
		// Tooltip
		wesCountry.charts.createTooltip(options);				
			
		return svg;
	}
	
	function getXPos(pos, sizes, zeroPos) {
		return sizes.marginLeft + sizes.yAxisMargin + sizes.groupMargin 
				+ sizes.xTickWidth / 2 + (sizes.xTickWidth + 2 * sizes.groupMargin) * pos;
	};
	
	function getYPos(value, sizes, zeroPos, maxHeight) {
		return sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin
			+ zeroPos
			- (value / (sizes.maxValue - sizes.minValue)) 
			* maxHeight;
	};
	
	function getSizes(svg, options) {
		var width = svg.width(); 
		var height = svg.height();
		var marginTop = height * options.margins[0] / 100;
		var marginRight = width * options.margins[1] / 100;
		var marginBottom = height * options.margins[2] / 100;
		var marginLeft = width * options.margins[3] / 100;
		var yAxisMargin = options.yAxis.margin * width / 100;
		var xAxisMargin = options.xAxis.margin * height / 100;
		var innerWidth = width - marginLeft - marginRight;
		var innerHeight = height - marginTop - marginBottom;
		
		// Max value & min value
		var maxAndMinValues = wesCountry.charts.getMaxAndMinValuesAxisY(options);
		var maxValue = maxAndMinValues.max;
		var minValue = maxAndMinValues.min;
		var maxValueLength = maxAndMinValues.valueLength; 	
		
		// If max and min Value are the same we set difference
		if (minValue == maxValue) {
			minValue = minValue >= 0 ? 0 : minValue - 2;
			maxValue += 2;
		}
		
		var ticksY = (maxValue - minValue) / maxAndMinValues.inc;
		var yTickHeight = ticksY != 0 ? (innerHeight - xAxisMargin) / ticksY : 0;
		var xTickWidth = (innerWidth - yAxisMargin) / maxAndMinValues.valueLength;		
		
		var groupMargin = options.groupMargin * xTickWidth / 100;	
		xTickWidth -= 2 * groupMargin;
			
		var barWidth = xTickWidth / options.series.length;	
		var barMargin = options.barMargin * barWidth / 100;	
		barWidth -= 2 * barMargin;			
				
		var valueInc = ticksY != 0 ? (maxValue - minValue) / ticksY : 0;

		var legendItemSize = options.legend.itemSize * width / 100;

		return {
			width : width,
			height : height,
			marginTop : marginTop,
			marginRight : marginRight,
			marginBottom : marginBottom,
			marginLeft : marginLeft,
			
			innerWidth : innerWidth,
			innerHeight : innerHeight,
			
			yAxisMargin: yAxisMargin,
			xAxisMargin: xAxisMargin,
			
			maxValue: maxValue,
			minValue: minValue,
			maxValueLength: maxValueLength,
			
			ticksY: ticksY,
			yTickHeight: yTickHeight,
			xTickWidth: xTickWidth,
			valueInc: valueInc,
			
			barMargin: barMargin,
			groupMargin: groupMargin,
			barWidth: barWidth,
			
			legendItemSize: legendItemSize
		};
	}
};////////////////////////////////////////////////////////////////////////////////
//                                  PIE CHART
////////////////////////////////////////////////////////////////////////////////
	
wesCountry.charts.pieChart = function(options) {
	return renderChart();

	function renderChart() {
		// Options and default options
		options = wesCountry.mergeOptionsAndDefaultOptions(options, wesCountry.charts.defaultOptions);	
		
		if (options.sortSeries)
			options.series = wesCountry.charts.sortSeries(options.series);			
		
		// SVG creation
		var svg = wesCountry.charts.getSVG(options);
		
		// Size and margins (%)
		var sizes = getSizes(svg, options);
		
		var g = svg.g();

		// Background
	
		wesCountry.charts.setBackground(g, sizes, options);
		
		// Values
		
		var numberOfPies = sizes.maxValueLength; 
		
		if (numberOfPies == 1) {
			var radius = Math.min(sizes.innerWidth - 2 * sizes.yAxisMargin, sizes.innerHeight - 2 * sizes.xAxisMargin) / 2;
			var startX = sizes.innerWidth / 2;
			var startY = sizes.innerHeight / 2;
			var xInc = 0;
			var yInc = 0;
			var half = 1;
		}
		else if (numberOfPies == 2) {
			var radius = Math.min(sizes.innerWidth - 2 * sizes.yAxisMargin, sizes.innerHeight - 2 * sizes.xAxisMargin) / 4;
			var startX = sizes.marginLeft + radius;
			var startY = sizes.innerHeight / 2;
			var xInc = sizes.innerWidth - 2 * radius;
			var yInc = 0;
			var half = 2;
		}
		else {
			if (numberOfPies > 8)
				numberOfPies = 8;
		
			var radius = Math.min(sizes.innerWidth, sizes.innerHeight - 2 * sizes.xAxisMargin) / 4;
			var half = Math.ceil(numberOfPies / 2);
			
			var startX = sizes.marginLeft + radius;
			var startY = sizes.marginTop + radius
			var xInc = (sizes.innerWidth - half * radius * 2) / (half - 1) + 2 * radius;
			var yInc = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin - radius;
		}
		
		// It's presented in two rows
		
		for (var i = 0; i < numberOfPies; i++) {		
			if (i < half) {
				var cx = startX + xInc * i;
				var cy = startY;
			}
			else {
				var rest = numberOfPies - half;
				
				var divisor = rest < half ? rest + 1 : rest - 1;
				var margin = (sizes.innerWidth - rest * radius * 2) / (divisor);
				xInc = margin + 2 * radius;
				var pieMarginLeft = rest < half ? margin : 0;
			
				var cx = sizes.marginLeft + pieMarginLeft + radius + xInc * (i % half);
				var cy = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin - radius;
			}
			
			// Label
			var labelY = cy + radius + sizes.xAxisMargin / 2;
			var text = options.xAxis.values[i] ? options.xAxis.values[i] : "";
			
			g.text({
				x: cx,
				y: labelY,
				value: text
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle;dominant-baseline: middle", 
				options.xAxis["font-colour"],
				options.xAxis["font-family"],
				options.xAxis["font-size"]));
			
			// Events
	
			var onmouseover = function() {
				this.colour = this.style.fill;
				this.style.fill = options.overColour;
				
				options.events.onmouseover(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
			};
										
			var onmouseout = function() { 
				this.style.fill = this.colour;
				options.events.onmouseout(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
			};
			
			var onclick = function() { 
				this.style.fill = this.colour;
				options.events.onclick(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
			};		
	
			// Pie
			
			var total = 0;
			var numberOfGreaterThanZero = 0;
			
			var length = options.series.length;
			
			for (var j = 0; j < length; j++) {
				var value = Math.abs(options.series[j].values[i]);
				
				if (!value)
					value = 0;
				
				if (value != 0)
					numberOfGreaterThanZero++;
				
				total += value;
			}
				
			var angles = []
		    
		    for(var j = 0; j < length; j++) {
				var value = Math.abs(options.series[j].values[i] / total * Math.PI * 2);
				
				if (!value)
					value = 0;
				
				angles[j] = value; 
		    }

		    if (numberOfGreaterThanZero == 1) {
		    	var colour = "";
		    	var serie = "";
		    	var value = "";
		    	var pos = "";
		    	
		    	for(var j = 0; j < length; j++)
		    		if (angles[j] != 0) {
		    			colour = options.serieColours[j];
		    			serie = options.series[j].name;
		    			value = Math.abs(options.series[0].values[j]).toFixed(2);
		    			pos = options.xAxis.values[i];
			    		break;
		    		}	
		    		
		    	g.circle({
			    	cx: cx,
			    	cy: cy,
			    	r: radius,
			    	serie: serie,
					value: value,
					pos: pos
		    	}).event("onmouseover", onmouseover)
				.event("onmouseout", onmouseout)
				.event("onclick", onclick)	
		    	.style(String.format("fill: {0}", colour));
		    }
		    else {
			    var startangle = 0;
				
				for (var j = 0; j < length; j++) {
					var endangle = startangle + angles[j];
					var value = Math.abs(options.series[j].values[i]).toFixed(2);
					
					var serie = options.series[j].name;
					var url = options.series[j].urls ? options.series[j].urls[i] : "";
					var pos = options.xAxis.values[i];
					
			        // Compute the two points where our wedge intersects the circle
			        // These formulas are chosen so that an angle of 0 is at 12 o'clock
			        // and positive angles increase clockwise.
			        var x1 = cx + radius * Math.sin(startangle);
			        var y1 = cy - radius * Math.cos(startangle);
			        var x2 = cx + radius * Math.sin(endangle);
			        var y2 = cy - radius * Math.cos(endangle);
			        
			        var halfWay = startangle + (endangle - startangle) / 2;
			        var incRadius = radius + (radius / 100) * options.valueOnItem.margin;
			        var xMiddle = cx + incRadius * Math.sin(halfWay);
			        var yMiddle = cy - incRadius * Math.cos(halfWay);
		        
			        // This is a flag for angles larger than than a half circle
			        var big = 0;
			        
			        if (endangle - startangle > Math.PI) 
			        	big = 1;
			        
			        // We describe a wedge with an <svg:path> element
			        // Notice that we create this with createElementNS()
					
			        // This string holds the path details
			        var d = "M " + cx + "," + cy +  // Start at circle center
			            " L " + x1 + "," + y1 +     // Draw line to (x1,y1)
			            " A " + radius + "," + radius +       // Draw an arc of radius r
			            " 0 " + big + " 1 " +       // Arc details...
			            x2 + "," + y2 +             // Arc goes to to (x2,y2)
			            " Z";                       // Close path back to (cx,cy)
			            
					var pathOptions = {
						d: d,
						serie: serie,
						value: value,
						pos: pos
					};	
					
					var path = g.path(pathOptions)
					.event("onmouseover", onmouseover)
					.event("onmouseout", onmouseout)
					.event("onclick", onclick)			            
			        .style(String.format("fill: {0}", options.serieColours[j]));
			        
			        // Value on bar
					if (options.valueOnItem.show == true) {
						g.text({
							x: xMiddle,
							y: yMiddle,
							value: value
						}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle;dominant-baseline: middle", 
							options.valueOnItem["font-colour"],
							options.valueOnItem["font-family"],
							options.valueOnItem["font-size"]));
					}
			        
			        startangle = endangle;
				}
			}
		}
		
		// Legend
		if (options.legend.show)
			wesCountry.charts.showLegend(g, sizes, options);
			
		// Tooltip
		wesCountry.charts.createTooltip(options);				
			
		return svg;
	}
	
	function getSizes(svg, options) {
		var width = svg.width(); 
		var height = svg.height();
		var marginTop = height * options.margins[0] / 100;
		var marginRight = width * options.margins[1] / 100;
		var marginBottom = height * options.margins[2] / 100;
		var marginLeft = width * options.margins[3] / 100;
		var yAxisMargin = options.yAxis.margin * width / 100;
		var xAxisMargin = options.xAxis.margin * height / 100;
		var innerWidth = width - marginLeft - marginRight;
		var innerHeight = height - marginTop - marginBottom;
		
		// Max value & min value
		var maxAndMinValues = wesCountry.charts.getMaxAndMinValuesAxisY(options);
		var maxValue = maxAndMinValues.max;
		var minValue = maxAndMinValues.min;
		var maxValueLength = maxAndMinValues.valueLength; 	
		
		var ticksY = (maxValue - minValue) / maxAndMinValues.inc;
		var yTickHeight = ticksY != 0 ? (innerHeight - xAxisMargin) / ticksY : 0;
		var xTickWidth = (innerWidth - yAxisMargin) / maxAndMinValues.valueLength;		
		
		var groupMargin = options.groupMargin * xTickWidth / 100;	
		xTickWidth -= 2 * groupMargin;
			
		var barWidth = xTickWidth / options.series.length;	
		var barMargin = options.barMargin * barWidth / 100;	
		barWidth -= 2 * barMargin;			
				
		var valueInc = ticksY != 0 ? (maxValue - minValue) / ticksY : 0;

		var legendItemSize = options.legend.itemSize * width / 100;

		return {
			width : width,
			height : height,
			marginTop : marginTop,
			marginRight : marginRight,
			marginBottom : marginBottom,
			marginLeft : marginLeft,
			
			innerWidth : innerWidth,
			innerHeight : innerHeight,
			
			yAxisMargin: yAxisMargin,
			xAxisMargin: xAxisMargin,
			
			maxValue: maxValue,
			minValue: minValue,
			maxValueLength: maxValueLength,
			
			ticksY: ticksY,
			yTickHeight: yTickHeight,
			xTickWidth: xTickWidth,
			valueInc: valueInc,
			
			barMargin: barMargin,
			groupMargin: groupMargin,
			barWidth: barWidth,
			
			legendItemSize: legendItemSize
		};
	}		
};////////////////////////////////////////////////////////////////////////////////
//                                  POLAR CHART
////////////////////////////////////////////////////////////////////////////////
	
wesCountry.charts.polarChart = function(options) {
	return renderChart();

	function renderChart() {
		// Options and default options
		options = wesCountry.mergeOptionsAndDefaultOptions(options, wesCountry.charts.defaultOptions);				
		
		// SVG creation
		var svg = wesCountry.charts.getSVG(options);
		
		// Size and margins (%)
		var sizes = getSizes(svg, options);
		
		var g = svg.g();

		// Background
	
		wesCountry.charts.setBackground(g, sizes, options);
		
		// Axis
		
		var radius = Math.min(sizes.innerWidth - 2 * sizes.yAxisMargin, sizes.innerHeight - 2 * sizes.xAxisMargin) / 2;
		var numberOfVertices = sizes.maxValueLength; 
		var cx = sizes.width / 2;
		var cy = sizes.height / 2;

		// Vertex calculation
		
		var vertices = [];
		
		for (var i = 0; i < numberOfVertices; i++) {
			vertices.push({
				x: cx + radius * Math.cos((2 * Math.PI * i) / numberOfVertices - Math.PI / 2),
				y: cy + radius * Math.sin((2 * Math.PI * i) / numberOfVertices - Math.PI / 2)
			});
		}
		
		// Radius
		
		for (var i = 0; i < numberOfVertices; i++) {
			var vertex = vertices[i];
			
		  	g.line({
		  		x1: cx,
		  		y1: cy,
		  		x2: vertex.x,
		  		y2: vertex.y
		  	}).style(String.format("stroke: {0};", options.yAxis.tickColour));
		}
		
		// Label 
		
		for (var i = 0; i < numberOfVertices; i++) {  	
			var x = cx + (radius + sizes.xAxisMargin / 2) * Math.cos((2 * Math.PI * i) / numberOfVertices - Math.PI / 2);
			var y = cy + (radius + sizes.xAxisMargin / 2) * Math.sin((2 * Math.PI * i) / numberOfVertices - Math.PI / 2);

			var value = options.xAxis.values[i] ? options.xAxis.values[i] : "";

		  	g.text({
				x: x,
				y: y,
				value: value
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle;dominant-baseline: middle", 
				options.xAxis["font-colour"],
				options.xAxis["font-family"],
				options.xAxis["font-size"]));
		}
		
		// Polygon sides
		
		var maxValue = sizes.maxValue;
		var minValue = sizes.minValue;
		
		var pow = 5;
		maxValue =  Math.ceil(maxValue / pow) * pow;
		minValue =  Math.floor(minValue / pow) * pow;
		
		//var ticksY = maxValue - minValue;
		
		//var numberOfAxis = 5;
		var ticksY = 5;
		//maxValue = numberOfAxis.max;

		var radiusInc = radius / ticksY;
		var tickInc = (maxValue - minValue) / ticksY;
		
		for (var i = 0; i <= ticksY; i++) {
			var polygonVertices = [];
			var polygonRadius = radiusInc * i;
		
			// Label (Vertical Number)
			
			g.text({
				x: cx - sizes.xAxisMargin / 2,
				y: cy - polygonRadius,
				value: minValue + i * tickInc
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: end;dominant-baseline: middle", 
				options.yAxis["font-colour"],
				options.yAxis["font-family"],
				options.yAxis["font-size"]));
		
			// Polygon vertex calculation
			
			for (var j = 0; j < numberOfVertices; j++) {
				polygonVertices.push({
					x: cx + polygonRadius * Math.cos((2 * Math.PI * j) / numberOfVertices - Math.PI / 2),
					y: cy + polygonRadius * Math.sin((2 * Math.PI * j) / numberOfVertices - Math.PI / 2)
				});
			}
			
			// Polygon side drawing
			
			for (var j = 0; j < numberOfVertices; j++) {	
				var vertex = polygonVertices[j];
				var vertexPrev = j == 0 ? polygonVertices[numberOfVertices - 1] : polygonVertices[j - 1];
				
			  	g.line({
			  		x1: vertexPrev.x,
			  		y1: vertexPrev.y,
			  		x2: vertex.x,
			  		y2: vertex.y
			  	}).style(String.format("stroke: {0};", options.yAxis.tickColour));
			}
		}
			
		// Values
		
		var zeroRadius = Math.abs(minValue / (maxValue - minValue)) * radius;
		var length = options.series.length;
		var polygonVertices = [];

		// Vertex calculation
		
		for (var i = 0; i < length; i++) {
		
			polygonVertices[i] = new Array();
		
			for (j = 0; j < numberOfVertices; j++) {
				var value = options.series[i].values[j];
				
				if (!value)
					value = 0;
				
				if (value < 0) { 
					//var total = maxValue - minValue;
					//var amount = Math.abs(value) / total;
					//var valueRadius = (amount * radius); 
					var valueRadius = zeroRadius - Math.abs(value / minValue) * zeroRadius;
				}
				else {
					var valueRadius = (value / maxValue) * (radius - zeroRadius) + zeroRadius;
				}
				
				var x = cx + valueRadius * Math.cos((2 * Math.PI * j) / numberOfVertices - Math.PI / 2);
				var y = cy + valueRadius * Math.sin((2 * Math.PI * j) / numberOfVertices - Math.PI / 2);
					
				polygonVertices[i].push({
					x: x,
					y: y
				});
			}
		}	
		
		// Events
		
		var setLineWidth = function(element, stroke) {
			var className = element.getAttribute("class");
			var lines = element.parentNode.querySelectorAll("line." + className);
			var length = lines.length;
	
			for (var k = 0; k < length; k++) {
				lines[k].setAttribute("stroke-width", stroke)
			}	
		};			
		
		var onmouseover = function() { 
			this.setAttribute("r", 8);
			setLineWidth(this, 2);
			options.events.onmouseover(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
		};
									
		var onmouseout = function() { 
			this.setAttribute("r", 5); 
			setLineWidth(this, 1);
			options.events.onmouseout(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
		};
		
		var onclick = function() { 
			this.setAttribute("r", 5); 
			setLineWidth(this, 1);
			options.events.onclick(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
		};			
		
		// Polygon drawing
        
		for (var i = 0; i < length; i++) {
			var lineId = "l" + wesCountry.charts.guid();
            
            var pathD = "";
        
			for (var j = 0; j < numberOfVertices; j++) {
				var vertex = polygonVertices[i][j];
				var vertexPrev = j == 0 ? polygonVertices[i][numberOfVertices - 1] : polygonVertices[i][j - 1];
				var value = options.series[i].values[j];
				var serie = options.series[i].name;
				var pos = options.xAxis.values[j];
			
				if (options.vertex.show) {
					g.circle({
						cx: vertex.x,
						cy: vertex.y,
						r: 5,
						serie: serie,
						value: value,
						pos: pos,
						"class": lineId
					}).style(String.format("fill: {0}", options.serieColours[i % options.serieColours.length]))
					.event("onmouseover", onmouseover).event("onmouseout", onmouseout).event("onclick", onclick);
				}
				
				g.line({
			  		x1: vertexPrev.x,
			  		y1: vertexPrev.y,
			  		x2: vertex.x,
			  		y2: vertex.y,
			  		"class": lineId
			  	}).style(String.format("stroke: {0};", options.serieColours[i % options.serieColours.length]));
                
                pathD += String.format("{0}{1} {2}", j == 0 ? "M" : "L", vertex.x, vertex.y);
			}
            
            if (length > 0) {
                var vertex = polygonVertices[i][0];
                pathD += String.format(" L{0} {1} Z", vertex.x, vertex.y);
            
                g.path({
                    d: pathD
                }).style(String.format("stroke: {0}; fill: {0}; opacity: 0.5", options.serieColours[i % options.serieColours.length]));
            }
		}
	
		// Legend
		if (options.legend.show)
			wesCountry.charts.showLegend(g, sizes, options);
			
		// Tooltip
		wesCountry.charts.createTooltip(options);				
			
		return svg;
	}
	
	function getSizes(svg, options) {
		var width = svg.width(); 
		var height = svg.height();
		var marginTop = height * options.margins[0] / 100;
		var marginRight = width * options.margins[1] / 100;
		var marginBottom = height * options.margins[2] / 100;
		var marginLeft = width * options.margins[3] / 100;
		var yAxisMargin = options.yAxis.margin * width / 100;
		var xAxisMargin = options.xAxis.margin * height / 100;
		var innerWidth = width - marginLeft - marginRight;
		var innerHeight = height - marginTop - marginBottom;
		
		// Max value & min value
		var maxAndMinValues = wesCountry.charts.getMaxAndMinValuesAxisY(options);
		var maxValue = maxAndMinValues.max;
		var minValue = maxAndMinValues.min > 0 ? 0 : maxAndMinValues.min;
		var maxValueLength = maxAndMinValues.valueLength; 	
		
		var ticksY = (maxValue - minValue) / maxAndMinValues.inc;
		var yTickHeight = ticksY != 0 ? (innerHeight - xAxisMargin) / ticksY : 0;
		var xTickWidth = (innerWidth - yAxisMargin) / maxAndMinValues.valueLength;		
		
		var groupMargin = options.groupMargin * xTickWidth / 100;	
		xTickWidth -= 2 * groupMargin;
			
		var barWidth = xTickWidth / options.series.length;	
		var barMargin = options.barMargin * barWidth / 100;	
		barWidth -= 2 * barMargin;			
				
		var valueInc = ticksY != 0 ? (maxValue - minValue) / ticksY : 0;

		var legendItemSize = options.legend.itemSize * width / 100;

		return {
			width : width,
			height : height,
			marginTop : marginTop,
			marginRight : marginRight,
			marginBottom : marginBottom,
			marginLeft : marginLeft,
			
			innerWidth : innerWidth,
			innerHeight : innerHeight,
			
			yAxisMargin: yAxisMargin,
			xAxisMargin: xAxisMargin,
			
			maxValue: maxValue,
			minValue: minValue,
			maxValueLength: maxValueLength,
			
			ticksY: ticksY,
			yTickHeight: yTickHeight,
			xTickWidth: xTickWidth,
			valueInc: valueInc,
			
			barMargin: barMargin,
			groupMargin: groupMargin,
			barWidth: barWidth,
			
			legendItemSize: legendItemSize
		};
	}	
};////////////////////////////////////////////////////////////////////////////////
//                                SCATTER PLOT
////////////////////////////////////////////////////////////////////////////////
	
wesCountry.charts.scatterPlot = function(options) {
	return renderChart();

	function renderChart() {
		// Options and default options
		options = wesCountry.mergeOptionsAndDefaultOptions(options, wesCountry.charts.defaultOptions);	
	
		// SVG creation
		var svg = wesCountry.charts.getSVG(options);
		
		// Size and margins (%)
		var sizes = getSizes(svg, options);
	
		var g = svg.g();
	
		// Background
	
		wesCountry.charts.setBackground(g, sizes, options); 
				
		// X Axis & Y Axis		
		wesCountry.charts.setAxisY(g, sizes, options);
		var sizesX = setAxisX(g, sizes, options);
				
		// Values
		var length = options.series.length;
	
		var maxHeight = sizes.innerHeight - sizes.xAxisMargin;
		var maxWidth = sizes.innerWidth - sizes.yAxisMargin;
		
		var zeroPos = 0;
		
		if (sizes.minValue <= 0 && sizes.maxValue - sizes.minValue != 0)
			zeroPos = sizes.minValue / (sizes.maxValue - sizes.minValue) * maxHeight;
			
		var zeroPosX = 0;
		
		if (sizesX.minValue <= 0)
			zeroPosX = sizesX.xTickWidth * Math.abs(sizesX.minValue);		

		// Events
	
		var onmouseover = function() {
			this.colour = this.style.fill;
			this.style.fill = options.overColour;
			
			options.events.onmouseover(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
		};
									
		var onmouseout = function() { 
			this.style.fill = this.colour;
			options.events.onmouseout(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
		};
		
		var onclick = function() { 
			this.style.fill = this.colour;
			options.events.onclick(this.getAttribute("serie"), this.getAttribute("pos"), this.getAttribute("value"));
		};		
	
		for (var i = 0; i < length; i++) {
			var values = options.series[i].values;
			var valueLength = values.length;
		
			for (var j = 0; j < valueLength; j++) {
				var valueX = values[j][0] ? values[j][0] : 0;
				var valueXPrev = 0;
				
				var value = options.series[i].values[j];
				var serie = options.series[i].name;
				var pos = valueX;
			
				if (j > 0)
					valueXPrev = values[j - 1][0] ? values[j - 1][0] : 0;
				
				if (!valueX)
					valueX = 0;
					
				if (!valueXPrev)
					valueXPrev = 0;			
			
				var valueY = values[j][1] ? values[j][1] : 0;
				var valueYPrev = 0;
				
				if (j > 0)
					valueYPrev = values[j - 1][1] ? values[j - 1][1] : 0;
				
				if (!valueY)
					valueY = 0;
					
				if (!valueYPrev)
					valueYPrev = 0;

				var xPos = sizes.marginLeft + sizes.yAxisMargin
						+ zeroPosX
						+ (sizesX.maxValue - sizesX.minValue == 0 ? 0 : 
							(valueX - sizesX.minValue) / (sizesX.maxValue - sizesX.minValue))
						* maxWidth;

				var yPos = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin
						+ zeroPos
						- (sizes.maxValue - sizes.minValue == 0 ? 1 : 
							(valueY - sizes.minValue) / (sizes.maxValue - sizes.minValue)) 
						* maxHeight;

				g.circle({
					cx: xPos,
					cy: yPos,
					r: 5,
					serie: serie,
					value: value,
					pos: pos
				}).style(String.format("fill: {0}", options.serieColours[i % options.serieColours.length]))
				.event("onmouseover", onmouseover).event("onmouseout", onmouseout).event("onclick", onclick);
			}
		}
		
		// Legend
		if (options.legend.show)
			wesCountry.charts.showLegend(g, sizes, options);
			
		// Tooltip
		wesCountry.charts.createTooltip(options);	
			
		return svg;
	}
	
	function getSizes(svg, options) {
		var width = svg.width(); 
		var height = svg.height();
		var marginTop = height * options.margins[0] / 100;
		var marginRight = width * options.margins[1] / 100;
		var marginBottom = height * options.margins[2] / 100;
		var marginLeft = width * options.margins[3] / 100;
		var yAxisMargin = options.yAxis.margin * width / 100;
		var xAxisMargin = options.xAxis.margin * height / 100;
		var innerWidth = width - marginLeft - marginRight;
		var innerHeight = height - marginTop - marginBottom;
		
		// Max value & min value
		var maxAndMinValues = wesCountry.charts.getMaxAndMinValuesAxisY(options);
		var maxValue = maxAndMinValues.max;
		var minValue = maxAndMinValues.min;
		var maxValueLength = maxAndMinValues.valueLength; 	
		
		var ticksY = (maxValue - minValue) / maxAndMinValues.inc;
		var yTickHeight = ticksY != 0 ? (innerHeight - xAxisMargin) / ticksY : 0;
		var xTickWidth = (innerWidth - yAxisMargin) / maxAndMinValues.valueLength;		
		
		var groupMargin = options.groupMargin * xTickWidth / 100;	
		xTickWidth -= 2 * groupMargin;
			
		var barWidth = xTickWidth / options.series.length;	
		var barMargin = options.barMargin * barWidth / 100;	
		barWidth -= 2 * barMargin;			
				
		var valueInc = ticksY != 0 ? (maxValue - minValue) / ticksY : 0;

		var legendItemSize = options.legend.itemSize * width / 100;

		return {
			width : width,
			height : height,
			marginTop : marginTop,
			marginRight : marginRight,
			marginBottom : marginBottom,
			marginLeft : marginLeft,
			
			innerWidth : innerWidth,
			innerHeight : innerHeight,
			
			yAxisMargin: yAxisMargin,
			xAxisMargin: xAxisMargin,
			
			maxValue: maxValue,
			minValue: minValue,
			maxValueLength: maxValueLength,
			
			ticksY: ticksY,
			yTickHeight: yTickHeight,
			xTickWidth: xTickWidth,
			valueInc: valueInc,
			
			barMargin: barMargin,
			groupMargin: groupMargin,
			barWidth: barWidth,
			
			legendItemSize: legendItemSize
		};
	}	
	
	// For scatter plot
	function setAxisX(container, sizes, options) {		
		// X Axis
		
		var maxHeight = sizes.innerHeight - sizes.xAxisMargin;
		var divisor = sizes.maxValue - sizes.minValue != 0 ? sizes.maxValue - sizes.minValue : 1;
		var zeroPos = sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin	
					+ sizes.minValue / divisor * maxHeight;
	
		container.line({
			x1: sizes.marginLeft + sizes.yAxisMargin,
			x2: sizes.marginLeft + sizes.innerWidth,
			y1: zeroPos,
			y2: zeroPos
		}).style(String.format("stroke: {0}", options.xAxis.colour));
	
		// X Axis Ticks
		
		var maxAndMinValues = getMaxAndMinValuesAxisX(options);
		var maxValue = maxAndMinValues.max;
		var minValue = maxAndMinValues.min; 	
		var maxValueLength = maxAndMinValues.valueLength;
		
		var ticksX = (maxValue - minValue) / maxAndMinValues.inc;
		var xTickWidth = (sizes.innerWidth - sizes.yAxisMargin) / (ticksX);	
		var incX = maxAndMinValues.inc;
			
		var length = ticksX + 1;
	
		for (var i = 0; i < length; i++) {
			// Line
			
			var xPos = sizes.marginLeft + sizes.yAxisMargin + xTickWidth * i;
		
			container.line({
				x1: xPos,
				x2: xPos,
				y1: sizes.marginTop,
				y2: sizes.innerHeight + sizes.marginTop - sizes.xAxisMargin
			}).style(String.format("stroke: {0}", options.xAxis.tickColour));
			
			// Label
			
			var value = minValue + incX * i;
			
			container.text({
				x: xPos,
				y: sizes.marginTop + sizes.innerHeight - sizes.xAxisMargin / 2,
				value: value
			}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle", 
				options.xAxis["font-colour"],
				options.xAxis["font-family"],
				options.xAxis["font-size"]));
		}
		
		// X Axis Title
		
		container.text({
			x: sizes.marginLeft + sizes.yAxisMargin + (sizes.innerWidth - sizes.yAxisMargin) / 2,
			y: sizes.marginTop + sizes.innerHeight + sizes.xAxisMargin / 2,
			value: options.xAxis.title
		}).style(String.format("fill: {0};font-family:{1};font-size:{2};text-anchor: middle", 
				options.xAxis["font-colour"],
				options.xAxis["font-family"],
				options.xAxis["font-size"]));
				
		return {
			"maxAndMinValues": maxAndMinValues,
			maxValue: maxValue,
			minValue: minValue, 	
			maxValueLength: maxValueLength,
		
			ticksX: ticksX,
			xTickWidth: xTickWidth,	
			incX: incX,	
		};
	}	
	
	// For scatter plot
	function getMaxAndMinValuesAxisX(options) {
		var maxValue = 0, minValue = Number.MAX_VALUE;
		
		var length = options.series.length;
		var valueLength = null;
		var value = null;
	
		for (var i = 0; i < length; i++) {
			valueLength = options.series[i].values.length;
			
			for (var j = 0; j < valueLength; j++) {	
				value = options.series[i].values[j][0] ? options.series[i].values[j][0] : 0;
					
				if (value > maxValue)
					maxValue = value;
						
				if (value < minValue)
					minValue = value;
			}
		}
		
		var maxAndMinValues = wesCountry.charts.getNearestNumber(minValue, maxValue);
	
		return { 
			max: maxAndMinValues.max, 
			min: maxAndMinValues.min, 
			inc: maxAndMinValues.inc
		};
	}		
};NodeList.prototype.indexOf = function (element) {
	for(var i=0;i<this.length;i++) {
		if(this[i] == element)
			return i;
	} return -1;
};
////////////////////////////////////////////////////////////////////////////////
//                                  CHART
////////////////////////////////////////////////////////////////////////////////	
wesCountry.charts.chart = function (options) {
	var container;
	container = typeof options.container !== "string" ? options.container : undefined;
	options.container = typeof options.container === "string" ? options.container : wesCountry.charts.defaultOptions.container; 
	options = wesCountry.mergeOptionsAndDefaultOptions(options, wesCountry.charts.defaultOptions);
	var chart;
	
	var chartType = options.chartType ? options.chartType.toLowerCase() : "bar";
	
	switch(chartType) {
		case "bar":
			chart = this.barChart(options);
			break;
		case "line":
			chart = this.lineChart(options);
			break;
		case "pie":
			chart = this.pieChart(options);
			break;
		case "area":
			chart = this.areaChart(options);
			break;
		case "scatter":
			chart = this.scatterPlot(options);
			break;
		case "polar":
			chart = this.polarChart(options);
			break;
	}
	if(container === undefined)
		container = document.querySelector(options.container);
	container.appendChild(chart.render());
	return container.parentNode;
}
////////////////////////////////////////////////////////////////////////////////
//                                MULTI CHART
////////////////////////////////////////////////////////////////////////////////
var optionsSave = [];
var pushIndex = optionsSave.length;
wesCountry.charts.multiChartRemoveData = function (from, numberOf) {
	optionsSave.splice(from, numberOf);
};

wesCountry.charts.setPushIndex = function (index) {
	if(index === "length") {
		pushIndex = optionsSave.length;
	} else {
		pushIndex = index;
	}
};

wesCountry.charts.multiChart = function (optionsReceived, newGraphic, element) {
	var containerReceived = optionsReceived.container;
	optionsReceived.container = "body";
	options = wesCountry.mergeOptionsAndDefaultOptions(optionsReceived, wesCountry.charts.defaultOptions);
	options.container = containerReceived;
	optionsReceived.container = containerReceived;
	if(newGraphic || newGraphic === undefined) {
		var optionsToSave = wesCountry.clone(options);
		optionsToSave.xAxis = wesCountry.clone(options.xAxis);
		optionsSave.splice(pushIndex, 0, optionsToSave);
		wesCountry.charts.setPushIndex("length");
	} else {
		var index = getIndexOfElement(element);
		optionsSave[index].series = wesCountry.clone(options.series);
		options.xAxis = wesCountry.clone(options.xAxis);
	}
	var charts = options.chartType;
	charts = charts instanceof Array ? charts : [charts]; //if not array convert to array
	var container = document.createElement("div");
	if(typeof options.container === "string")
		document.querySelector(options.container).appendChild(container);
	else 
		options.container.appendChild(container);
	createChartSelector();
	createSeriesSelector();
	return createChart();

	function createChartSelector() {	
		var div = document.createElement('div');
		div.className = "chartSelector";
		var ul = document.createElement('ul');
		for(var i=0; i<charts.length;i++) {
			var li = document.createElement('li');	
			var a = document.createElement('a');
			//a.href="#";
			a.className ="inactive";
			a.onclick = onGraphSelected;
			a.innerHTML = charts[i].toFirstUpperCase();
			li.appendChild(a);
			ul.appendChild(li);
		}
		div.appendChild(ul);
		div.querySelector("li a").className= "active";
		container.appendChild(div);
		
		if (charts.length <= 1)
			div.style.display = "none";
	}

	function createSeriesSelector() {
		var div = document.createElement('div');
		div.className = "seriesSelector";
		for(var i=0; i<options.series.length;i++) {
			var input = document.createElement('input');
			var label = document.createElement('label');
			input.id = options.series[i].name + "Checkbox" + wesCountry.charts.guid();
			input.type = "checkbox";
			input.className = "checks";
			input.onchange = onSeriesChanged;
			input.checked = true;
			label.for = input.id;
			label.innerHTML = options.series[i].name;
			div.appendChild(input);
			div.appendChild(label);
		} container.appendChild(div);
	}

	function createChart() {
		var div = document.createElement('div');
		div.className = "chartDiv";
		container.appendChild(div);
		return showChart(div);
	}

	function showChart(div) {
		var typeOfGraph = "bar";
		
		var active = container.querySelector(".active");
		
		if (active && active.innerHTML)
			typeOfGraph = active.innerHTML.toLowerCase();
			
		options.chartType = typeOfGraph;
		if(div === undefined)
			options.container = ".chartDiv";
		else
			options.container = div;
		return wesCountry.charts.chart(options);
	}

	function loadGraph(div) {
		//remove previous chart
		div.querySelector(".chartDiv").innerHTML="";	
		showChart(div.querySelector(".chartDiv"));
	}

	function setSelectedGraphToActive(name, ul) {
		var active = ul.querySelector(".active");
		var inactives = ul.querySelectorAll(".inactive");
		var length = inactives.length;
		for(var i=0;i<length;i++) 
			if(name===inactives[i].innerHTML) 
				inactives[i].className="active";
			else 
				inactives[i].className="inactive";

		if(name!==active.innerHTML)
			active.className="inactive";
	}

	function onGraphSelected() {
		setSelectedGraphToActive(this.innerHTML, this.parentNode.parentNode);
		var div = this.parentNode.parentNode.parentNode.parentNode;
		var recovered = recoverSeriesAndXValuesItem(this.parentNode.parentNode);
		options.series = recovered.series;
		options.xAxis.values = recovered.xAxisValues;
		loadGraph(div);
	}

	function onSeriesChanged() {
		var seriesAndXAxisValues = recoverSeriesAndXValuesItem(this);
		var checkBoxes = this.parentNode.querySelectorAll("input");
		var length = seriesAndXAxisValues.series.length;
		for(var i=0;i<length;i++) 
			if(!checkBoxes[i].checked)
				delete seriesAndXAxisValues.series[i];
		optionSeriesWithoutUndefined();
		putXAxisValuesOnOptions();
		loadGraph(this.parentNode.parentNode); //div of the grap

		function putXAxisValuesOnOptions() {
			options.xAxis.values = seriesAndXAxisValues.xAxisValues;
		} 

		function optionSeriesWithoutUndefined() {
			var seriesReturned = [];
			for(var i=0;i<length;i++) 
				if(seriesAndXAxisValues.series[i] !== undefined)
					seriesReturned.push(seriesAndXAxisValues.series[i]);
			options.series = seriesReturned;
		}
	}

	function recoverSeriesAndXValuesItem(element) {
			var index = getIndexOfElement(element);
			return {
				series: wesCountry.clone(optionsSave[index].series),
				xAxisValues: wesCountry.clone(optionsSave[index].xAxis.values)
			};
	}

	function getIndexOfElement(element) {
		var parent = element.parentNode; //get a div
		var allDivs = document.querySelectorAll("."+parent.className);
		return allDivs.indexOf(parent);
	}
};
Element.prototype.insertAfter = function(newNode) {
    this.parentNode.insertBefore(newNode, this.nextSibling);
};

Array.prototype.pushIfNotExist = function(element) {
    if(this.indexOf(element) < 0 )
        this.push(element);
};


if (typeof (wesCountry) === "undefined")
    var wesCountry = new Object();

wesCountry.data = new (function() {
    var myData = {};
    var options = {};
    var tablePosition = null;
    var tableElement;
    var xAxisValues = {};
    var series = {};
    var times = [];
    var indicators = [];
    var regions = [];

    this.parseJSON = function(receivedOptions) {
        options = wesCountry
                .mergeOptionsAndDefaultOptions(receivedOptions, wesCountry.charts.defaultOptions);
        var json = options.data;
        xAxisValues.time =  new JsonParser(json).parseByTime();
        xAxisValues.indicator =  new JsonParser(json).parseByIndicator();
        xAxisValues.region =  new JsonParser(json).parseByRegion();
        xAxisValues.indicatorAndTime = new JsonParser(json).parseByIndicatorAndTime();
        xAxisValues.indicatorAndRegion = new JsonParser(json).parseByIndicatorAndRegion();
        xAxisValues.timeAndRegion = new JsonParser(json).parseByTimeAndRegion();
        return this;
    };

    this.parseTable = function(receivedOptions, functionName, argumentToGraphic) {
    	var container = receivedOptions.container ? document.querySelector(receivedOptions.container) : document;
        var tables = container.querySelectorAll(".graphs");
        for (var i = 0; i < tables.length; i++) {
            tableElement = tables[i]; //current table
            var headers = tables[i].querySelectorAll("th");
            var rows = tables[i].querySelectorAll("tr");
            var json = [];
            for (var j = 1; j < rows.length; j++) {
                var obj = new Object();
                var data = rows[j].querySelectorAll("td");
                for (var k = 0; k < data.length; k++) {
                    obj[headers[k].className] = data[k].innerHTML;
                }
                json.push(obj);
            }
            receivedOptions.data = json;
            //if (receivedOptions.container === undefined)
                tablePosition = receivedOptions.tablePosition;
            var iterator = this.parseJSON(receivedOptions).iterate()[functionName](argumentToGraphic);
        }

    };

    this.iterate = function() {
        return new Iterator(myData);
    };

    function JsonParser(json) {

        this.parseByIndicator = function() {
            var returned = getHashTable(sortByYear, "indicatorCode", "countryName", "value", "year");
            myData.indicator = returned[0];
            return returned[1];
        };

        this.parseByTime = function() {
            var sortByIndicator = undefined;
            
            var returned = getHashTable(sortByIndicator, "year", "countryName", "value", "indicatorCode");
            myData.time = returned[0];
            return returned[1];
        };

        this.parseByRegion = function() {
            var returned = getHashTable(sortByYear, "countryName", "indicatorCode", "value", "year");
            myData.region = returned[0];
            return returned[1];
        };

        this.parseByIndicatorAndTime = function() {
            var returned = getHashTable(sortByYear, "indicatorCode", "year", "value", "countryName");
            myData.indicatorAndTime = returned[0];
            return returned[1];
        };

        this.parseByIndicatorAndRegion = function() {
            var returned = getHashTable(sortByYear, "indicatorCode", "countryName", "value", "year");
            myData.indicatorAndRegion = returned[0];
            return returned[1];
        };

        this.parseByTimeAndRegion = function() {
            var returned = getHashTable(sortByYear, "year", "countryName", "value", "indicatorCode");
            myData.timeAndRegion = returned[0];
            return returned[1];
        };

        var sortByYear = function(a,b) {
            return a.year - b.year;
        };

        var getHashTable = function(sortFunction, selectorProperty, itemProperty, valueProperty, xAxisValueProperty) {
            var xAxisValues = [];
            var hashTableSelector = new HashTable();
            setTimes();
            setRegions();
            setIndicators();
            for (var i = 0; i < json.length; i++) {
                var indicatorSelector = json[i][selectorProperty];
                if (!hashTableSelector.hasItem(indicatorSelector)) {
                    var filtered = json.filter(filterByIndicator);
                    filtered = filtered.sort(sortFunction);
                    var hashTable = new HashTable();
                    for (var j = 0; j < filtered.length; j++) {
                        if (hashTable.hasItem(filtered[j][itemProperty])) {
                            var values = hashTable.getItem(filtered[j][itemProperty]);
                            values.push(parseFloat(filtered[j][valueProperty]));
                        } else {
                            var values = [parseFloat(filtered[j][valueProperty])];
                        }
                        hashTable.setItem(filtered[j][itemProperty], values);
                        insertXAxisValue(filtered[j][xAxisValueProperty]);
                    }
                    hashTableSelector.setItem(json[i][selectorProperty], hashTable);
                }
            } return [hashTableSelector, xAxisValues];

            function filterByIndicator(element) {
                return element[selectorProperty] === indicatorSelector;
            }

            function insertXAxisValue(value) {
                if (xAxisValues.indexOf(value) < 0)
                    xAxisValues.push(value);
            }

            function setTimes() {
                setGeneric("year", times);
            }

            function setRegions() {
                setGeneric("countryName", regions);
            }

            function setIndicators() {
                setGeneric("indicatorCode", indicators);
            }

            function setGeneric(propertyName, array) {
                for(var i=0;i<json.length;i++)
                    array.pushIfNotExist(json[i][propertyName]);
            }
        };
    }

    function Iterator(data) {

        //selector = time or indicator or region
        this.selectBy = function(selector, graphicFunctionNames) {
            var select = document.createElement('select');
            select.className = "globalSelect";
            var container = typeof options.container === "string" ? 
                    document.querySelector(options.container) : 
                    options.container;
            container.appendChild(select);
            var optionsValues;
            switch(selector) {
                case "indicator":
                    optionsValues = indicators;
                    break;
                case "time":
                    optionsValues = times;
                    break;
                case "region":
                    optionsValues = regions;
                    break;
            } for(var i=0;i<optionsValues.length;i++) {
                var option = document.createElement('option');
                option.innerHTML = optionsValues[i];
                select.appendChild(option);
            } 
            drawFilteredGraphics.bind(this)();
            select.onchange = drawFilteredGraphics.bind(this);

            function getAllModules() {
                return document.querySelectorAll(".chartDiv");
            }

            function getContainerModules() {
                return container.querySelectorAll(".chartDiv");
            }

            function getGlobalFilters() {
                var divs = document.querySelectorAll(".chartDiv");
                var containers = [];
                for(var i=0;i<divs.length;i++)
                        containers.pushIfNotExist(divs[i]
                            .parentNode.parentNode.parentNode);
                return containers;
            }

            function drawFilteredGraphics() {
                var allDivs = getAllModules();
                var divs = getContainerModules();
                var allContainers = getGlobalFilters();
                var filters = {};
                filters[selector] = select.options[select.selectedIndex].innerHTML;
                if(getContainerModules().length <= 0)
                    for(var i=0;i<graphicFunctionNames.length;i++)
                        this[graphicFunctionNames[i]+"Filtered"](filters);
                else {
                    var div = divs[0];
                    var index = allDivs.indexOf(div);
                    wesCountry.charts.multiChartRemoveData(index, divs.length);
                    var length = divs.length;
                    options.container = div.parentNode.parentNode.parentNode;
                    var indexes = [];
                    for(var i=0;i<length;i++) {
                        indexes.push(allDivs.indexOf(divs[i]));
                        divs[i].parentNode.parentNode.remove();
                    }
                    for(var j=0;j<length;j++) {
                        wesCountry.charts.setPushIndex(indexes[j]);
                        this[graphicFunctionNames[j]+"Filtered"](filters);
                        wesCountry.charts.setPushIndex("length");
                    }
                }
            }
        };

        this.byIndicator = function(indicator) {
            var myData = data.indicator;
            series.indicator = [];
            var by = new ByOneFunctions("indicatorSelect");
            by.by(myData, xAxisValues.indicator, series.indicator, indicator);
        };

        this.byIndicatorFiltered = function(filters) {
            var myData = data.indicator;
            series.indicator = [];
            var by = new ByOneFunctions("indicatorSelect");
            by.by(myData, xAxisValues.indicator, series.indicator, filters.indicator, filters.region, filters.time);
        };

        this.byTime = function(time) {
            var myData = data.time;
            series.time = [];
            var by = new ByOneFunctions("timeSelect");
            by.by(myData, xAxisValues.time, series.time, time);
        };

        this.byTimeFiltered = function(filters) {
            var myData = data.time;
            series.time = [];
            var by = new ByOneFunctions("timeSelect");
            by.by(myData, xAxisValues.time, series.time, filters.time, filters.region, filters.indicator);
        };

        this.byRegion = function(region) {
            var myData = data.region;
            series.region = [];
            var by = new ByOneFunctions("regionSelect");
            by.by(myData, xAxisValues.region, series.region, region);
        };

        this.byRegionFiltered = function(filters) {
            var myData = data.region;
            series.region = [];
            var by = new ByOneFunctions("regionSelect");
            by.by(myData, xAxisValues.region, series.region, filters.region, filters.indicator, filters.time);
        };

        this.byIndicatorAndTime = function(indicator, time) {
            var myData = data.indicatorAndTime;
            series.indicatorAndTime = [];
            var by = new ByTwoFunctions("indicatorSelect", "timeSelect");
            by.by(myData, xAxisValues.indicatorAndTime, series.indicatorAndTime, indicator, time);
        };

        this.byIndicatorAndTimeFiltered = function(filters) {
            var myData = data.indicatorAndTime;
            series.indicatorAndTime = [];
            var by = new ByTwoFunctions("indicatorSelect", "timeSelect");
            by.by(myData, xAxisValues.indicatorAndTime, series.indicatorAndTime, filters.indicator, filters.time, filters.region);
        };

        this.byIndicatorAndRegion = function(indicator, region) {
            var myData = data.indicatorAndRegion;
            series.indicatorAndRegion = [];
            var by = new ByTwoFunctions("indicatorSelect", "regionSelect");
            by.by(myData, xAxisValues.indicatorAndRegion, series.indicatorAndRegion, indicator, region);
        };

        this.byIndicatorAndRegionFiltered = function(filters) {
            var myData = data.indicatorAndRegion;
            series.indicatorAndRegion = [];
            var by = new ByTwoFunctions("indicatorSelect", "regionSelect");
            by.by(myData, xAxisValues.indicatorAndRegion, series.indicatorAndRegion, filters.indicator, filters.region, filters.time);
        };

        this.byTimeAndRegion = function(time, region) {
            var myData = data.timeAndRegion;
            series.timeAndRegion = [];
            var by = new ByTwoFunctions("timeSelect", "regionSelect");
            by.by(myData, xAxisValues.timeAndRegion, series.timeAndRegion, time, region);
        };

        this.byTimeAndRegionFiltered = function(filters) {
            var myData = data.timeAndRegion;
            series.timeAndRegion = [];
            var by = new ByTwoFunctions("timeSelect", "regionSelect");
            by.by(myData, xAxisValues.timeAndRegion, series.timeAndRegion, filters.time, filters.region, filters.indicator);
        };

        this.max = function(numberOfItems, indicator, time) {
            var myData = data.indicatorAndTime;
            series.indicatorAndTime = [];
            var by = new ByMaxAndMin(numberOfItems, "max");
            by.by(myData, xAxisValues.indicatorAndTime, series.indicatorAndTime, indicator, time);
        };

        this.min = function(numberOfItems, indicator, time) {
            var myData = data.indicatorAndTime;
            series.indicatorAndTime = [];
            var by = new ByMaxAndMin(numberOfItems, "min");
            by.by(myData, xAxisValues.indicatorAndTime, series.indicatorAndTime, indicator, time);
        };

        this.byOneElementChangingYears = function(indicator, region, time) {
            var myData = data.indicatorAndRegion;
            series.indicatorAndRegion = [];
            var by = new ByOneElementChangingYears();
            by.by(myData, xAxisValues.indicatorAndRegion, series.indicatorAndRegion, indicator, region);
        };

        this.statisticalAggregates = function(indicator, region) {
            var myData = data.indicatorAndRegion;
            series.indicatorAndRegion = [];
            var by = new ByStatisticalAggregates();
            by.by(myData, xAxisValues.indicatorAndRegion, series.indicatorAndRegion, indicator, region);
        };

        this.semaphore = function(colors, limits, time, region) {
            var myData = data.timeAndRegion;
            series.timeAndRegion = [];
            var by = new BySemaphore(colors, limits, "timeSelect", "regionSelect");
            by.by(myData, xAxisValues.timeAndRegion, series.timeAndRegion, time, region);
        };

        function ByOneFunctions(selectClass) {
            var select;
            var mySeries;
            var div;
            var wrapperDiv;
            var indicators;

            this.createSelect = function(div, indicators) {
                select = document.createElement("select");
                div.appendChild(select);
                select.onchange = this.onIndicatorChanged;
                select.className = selectClass;
                for(var i=0;i<indicators.length;i++) {
                    var option = document.createElement("option");
                    option.innerHTML = indicators[i];
                    select.appendChild(option);    
                }
            };

            this.drawSelectedIndicator = function(index, index2, _mySeries, _div, _wrapperDiv, _indicators, newGraphic) {
                mySeries = _mySeries;
                div = _div;
                wrapperDiv = _wrapperDiv;
                indicators = _indicators;
                drawSelectedIndicator(index, newGraphic);
            };

            var drawSelectedIndicator = function(index, newGraphic) {
                options.series = mySeries[index];
                if (select.options.length <= 1) {
                    var element = document.createElement("p");
                    element.innerHTML = indicators[0];
                    select.parentNode.insertBefore(element, select);
                    select.style.display = "none";
                }
                var container = wesCountry.charts.multiChart(options, newGraphic, select);
                container.insertBefore(div, container.childNodes[0]);
                wrapperDiv.appendChild(container);
            };

            this.onIndicatorChanged = function() {
                var div = this.parentNode.parentNode;
                var wrapperDiv = div.parentNode;
                drawSelectedIndicator(select.selectedIndex, false);
                div.remove();
            };

            this.putSeriesByIndicator = function(myData, seriesByIndicator, indicators, countries, i, filter, xAxisValues) {
                var item = getIndexOfXValue();
                for (var c = 0; c < countries.length; c++) {
                    if(filter !== undefined) {
                        seriesByIndicator.push({
                            name: countries[c],
                            values: [myData.getItem(indicators[i]).getItem(countries[c])[item]]
                        });
                    } else {
                        seriesByIndicator.push({
                            name: countries[c],
                            values: myData.getItem(indicators[i]).getItem(countries[c])
                        });
                    }
                }

                function getIndexOfXValue() {
                    for(var i=0;i<xAxisValues.length;i++)
                        if(xAxisValues[i] === filter)
                            return i;
                }
            };

            this.by = new By().by;
        }

        function ByTwoFunctions(selectClass, select2Class) {
            var select;
            var select2;
            var mySeries;
            var div;
            var wrapperDiv;
            var indicators;
            var secondIndicators;

            this.createSelect = function(div, indicators, secondIndicators) {
                select = document.createElement("select");
                select2 = document.createElement("select");
                select.className = selectClass;
                select2.className = select2Class;
                div.appendChild(select);
                div.appendChild(select2);
                select.onchange = this.onIndicatorChanged;
                select2.onchange = this.onIndicatorChanged;
                for(var i=0;i<indicators.length;i++) {
                    var option = document.createElement("option");
                    option.innerHTML = indicators[i];
                    select.appendChild(option);    
                }
                for(var i=0;i<secondIndicators.length;i++) {
                    var option = document.createElement("option");
                    option.innerHTML = secondIndicators[i];
                    select2.appendChild(option);
                }
            };

            this.drawSelectedIndicator = function(index, index2, _mySeries, _div, _wrapperDiv, _indicators, _secondIndicators, newGraphic) {
                mySeries = _mySeries;
                div = _div;
                wrapperDiv = _wrapperDiv;
                indicators = _indicators;
                secondIndicators = _secondIndicators;
                if (select.options.length <= 1) {
                    var element = document.createElement("p");
                    element.innerHTML = indicators[0];
                    select.parentNode.insertBefore(element, select);
                    select.style.display="none";
                }
                if (select2.options.length <= 1) {
                    var element = document.createElement("p");
                    element.innerHTML = secondIndicators[0];
                    select2.parentNode.insertBefore(element, select2);
                    select2.style.display="none";
                }
                drawSelectedIndicator(index, index2, newGraphic);
            };

            var drawSelectedIndicator = function(index, index2, newGraphic) {
                options.series = mySeries[index][index2];
                var container = wesCountry.charts.multiChart(options, newGraphic, select);
                container.insertBefore(div, container.childNodes[0]);
                wrapperDiv.appendChild(container);
            };

            this.onIndicatorChanged = function() {
                var div = this.parentNode.parentNode;
                var wrapperDiv = div.parentNode;
                drawSelectedIndicator(select.selectedIndex, select2.selectedIndex, false);
                div.remove();
            };


            this.putSeriesByIndicator = function(myData, seriesByIndicator, indicators, countries, i, filter, xAxisValues) {
                var item = getIndexOfXValue();
                for (var c = 0; c < countries.length; c++) {
                    if(filter !== undefined) {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: [myData.getItem(indicators[i]).getItem(countries[c])[item]]
                        });
                    } else {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: myData.getItem(indicators[i]).getItem(countries[c])
                        });
                    }
                }

                function getIndexOfXValue() {
                    for(var i=0;i<xAxisValues.length;i++)
                        if(xAxisValues[i] === filter)
                            return i;
                }
            };

            this.by = new By().by;
        }

        function ByMaxAndMin(numberOfItems, method) {
            var select;
            var select2;
            var mySeries;
            var div;
            var wrapperDiv;
            var indicators;
            var secondIndicators;

            this.createSelect = function() {};

            this.drawSelectedIndicator = function(index, index2, _mySeries, _div, _wrapperDiv, _indicators, _secondIndicators, newGraphic) {
                mySeries = _mySeries;
                div = _div;
                wrapperDiv = _wrapperDiv;
                indicators = _indicators;
                secondIndicators = _secondIndicators;
                drawSelectedIndicator(index, index2, newGraphic);
            };

            var drawSelectedIndicator = function(index, index2, newGraphic) {
                options.series = mySeries[index][index2];
                var container = wesCountry.charts.multiChart(options, newGraphic, select);
                container.insertBefore(div, container.childNodes[0]);
                wrapperDiv.appendChild(container);
            };

            this.putSeriesByIndicator = function(myData, seriesByIndicator, indicators, countries, i, filter, xAxisValues) {
                var item = getIndexOfXValue();
                for (var c = 0; c < countries.length; c++) {
                    if(filter !== undefined) {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: [myData.getItem(indicators[i]).getItem(countries[c])[item]]
                        });
                    } else {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: myData.getItem(indicators[i]).getItem(countries[c])
                        });
                    }
                }
                var compare;
                if(method === "max")
                    compare = function(a,b) {
                        return a < b;
                    }
                else if(method === "min")
                    compare = function(a,b) {
                        return a > b;
                    }
                var series = seriesByIndicator[0][0].values;
                for(var i = 0; i < series.length; i++) {
                    for(var j = series.length; j > i; j--) {
                        if(compare(series[i], series[j])) {
                            var temp = series[i];
                            series[i] = series[j];
                            series[j] = temp;
                            temp = xAxisValues[i];
                            xAxisValues[i] = xAxisValues[j];
                            xAxisValues[j] = temp;
                        }
                    }
                }
                series = series.slice(0, numberOfItems);
                function getIndexOfXValue() {
                    for(var i=0;i<xAxisValues.length;i++)
                        if(xAxisValues[i] === filter)
                            return i;
                    }
            };

            this.by = new By().by;
        }

        function ByOneElementChangingYears() {
            var mySeries;
            var div;
            var wrapperDiv;
            var indicators;
            var secondIndicators;
            var years;
            var currentYear;
            var buttonBackward;
            var buttonForward;

            this.createSelect = function(div, indicators, secondIndicators) {
                var indicator = document.createElement("p");
                indicator.innerHTML = indicators[0];
                div.appendChild(indicator);
                var country = document.createElement("p");
                country.innerHTML = secondIndicators[0];
                div.appendChild(country);
                var controlDiv = document.createElement("div");
                div.appendChild(controlDiv);
                buttonBackward = document.createElement("button");
                buttonBackward.innerHTML = String.fromCharCode(8656);
                buttonBackward.disabled = true;
                buttonBackward.onclick = onPreviousYear;
                div.appendChild(buttonBackward);
                currentYear = document.createElement("div");
                currentYear.innerHTML = years[0];
                controlDiv.appendChild(currentYear);
                buttonForward = document.createElement("button");
                buttonForward.innerHTML = String.fromCharCode(8658);
                buttonForward.onclick = onNextYear;
                div.appendChild(buttonForward);
            };

            var onNextYear = function() {
                onYearChanged.bind(this)(1);
            };

            var onPreviousYear = function() {
                onYearChanged.bind(this)(-1);
            };

            var onYearChanged = function(advance) {
                var index = years.indexOf(currentYear.innerHTML)+advance;
                currentYear.innerHTML = years[index];
                var div = this.parentNode.parentNode;
                var wrapperDiv = div.parentNode;
                drawSelectedIndicator(0, index, false);
                div.remove();
                //disable buttons for avoiding errors
                if(index+1 >= years.length) {
                    buttonForward.disabled = true;
                    buttonBackward.disabled = false;
                } else if(index <= 0) {
                    buttonForward.disabled = false;
                    buttonBackward.disabled = true;
                } else {
                    buttonForward.disabled = false;
                    buttonBackward.disabled = false;
                }
            };

            this.drawSelectedIndicator = function(index, index2, _mySeries, _div, _wrapperDiv, _indicators, _secondIndicators, newGraphic) {
                mySeries = _mySeries;
                div = _div;
                wrapperDiv = _wrapperDiv;
                indicators = _indicators;
                secondIndicators = _secondIndicators;
                drawSelectedIndicator(index, index2, newGraphic);
            };

            var drawSelectedIndicator = function(index, index2, newGraphic) {
                var container = document.createElement("p");
                container.innerHTML = mySeries[index][index2][0].values[0];
                container.insertBefore(div, container.childNodes[0]);
                wrapperDiv.appendChild(container);
            };

            this.putSeriesByIndicator = function(myData, seriesByIndicator, indicators, countries, i, filter, xAxisValues) {
                for (var c = 0; c < xAxisValues.length; c++) {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[0],
                            values: [myData.getItem(indicators[i]).getItem(countries[0])[c]]
                        });
                }
                years = xAxisValues;
            };

            this.by = new By().by;
        }

        function ByStatisticalAggregates() {
            var select;
            var select2;
            var mySeries;
            var div;
            var wrapperDiv;
            var indicators;
            var secondIndicators;

            this.createSelect = function() {};

            this.drawSelectedIndicator = function(index, index2, _mySeries, _div, _wrapperDiv, _indicators, _secondIndicators, newGraphic) {
                mySeries = _mySeries;
                div = _div;
                wrapperDiv = _wrapperDiv;
                indicators = _indicators;
                secondIndicators = _secondIndicators;
                drawSelectedIndicator(index, index2, newGraphic);
            };

            var drawSelectedIndicator = function(index, index2, newGraphic) {
                var series =  mySeries[0][0][0].values;
                var statitics = {};
                statitics.sum = series.reduce(function(a,b) {return a+b;});
                statitics.average = statitics.sum / series.length;
                statitics.max = series.reduce(function(a,b) {return a>b ? a : b});
                statitics.min = series.reduce(function(a,b) {return a<b ? a : b});
                series.sort();
                if(series.length % 2 == 0)
                    statitics.median = (series[series.length/2]+series[series.length/2-1])/2;
                else
                    statitics.median = series[(series.length-1) / 2];
                createStatiticsTable();

                function createStatiticsTable() {
                    var table = document.createElement("table");
                    var theader = document.createElement("thead");
                    table.appendChild(theader);
                    var tr = document.createElement("tr");
                    theader.appendChild(tr);
                    var headers = ["Statistical aggregate", "Value"];
                    for(var i=0;i<headers.length;i++) {
                        var td = document.createElement("td");
                        td.innerHTML = headers[i];
                        tr.appendChild(td);
                    }
                    var tbody = document.createElement("tbody");
                    table.appendChild(tbody);
                    for(var a in statitics) {
                        var tr = document.createElement("tr");
                        tbody.appendChild(tr);
                        var td = document.createElement("td");
                        td.innerHTML = a;
                        tr.appendChild(td);
                        td = document.createElement("td");
                        td.innerHTML = statitics[a];
                        tr.appendChild(td);
                    }
                    var container = typeof options.container === "string" ? 
                            document.querySelector(options.container) : 
                            options.container;
                    container.appendChild(table);
                }
            };

            this.putSeriesByIndicator = function(myData, seriesByIndicator, indicators, countries, i, filter, xAxisValues) {
                var item = getIndexOfXValue();
                for (var c = 0; c < countries.length; c++) {
                    if(filter !== undefined) {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: [myData.getItem(indicators[i]).getItem(countries[c])[item]]
                        });
                    } else {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: myData.getItem(indicators[i]).getItem(countries[c])
                        });
                    }
                }

                function getIndexOfXValue() {
                    for(var i=0;i<xAxisValues.length;i++)
                        if(xAxisValues[i] === filter)
                            return i;
                }
            };
            this.by = new By().by;
        }

        function BySemaphore(colors, limits, selectClass, select2Class) {
            var select;
            var select2;
            var mySeries;
            var div;
            var semaphoreDiv;
            var indicators;
            var secondIndicators;
            putLimitsIfNofDefined(); //create limits if not defined by the user
            putColorsIfNotDefined(); //create colors if not defined by the user

            function putLimitsIfNofDefined() {
                if(limits===undefined)
                    limits = []; 
                limits[0] = limits[0]===undefined ? 10 : limits[0];
                limits[1] = limits[1]===undefined ? 100 : limits[1];
            }

            function putColorsIfNotDefined() {
                if(colors===undefined)
                    colors = [];
                colors[0] = colors[0]===undefined ? "#00FF00" : colors[0];
                colors[1] = colors[1]===undefined ? "#FF8000" : colors[1];
                colors[2] = colors[2]===undefined ? "#FF0000" : colors[2];
            }

            this.createSelect = function(div, indicators, secondIndicators) {
                select = document.createElement("select");
                select2 = document.createElement("select");
                select.className = selectClass;
                select2.className = select2Class;
                div.appendChild(select);
                div.appendChild(select2);
                select.onchange = this.onIndicatorChanged;
                select2.onchange = this.onIndicatorChanged;
                for(var i=0;i<indicators.length;i++) {
                    var option = document.createElement("option");
                    option.innerHTML = indicators[i];
                    select.appendChild(option);    
                }
                for(var i=0;i<secondIndicators.length;i++) {
                    var option = document.createElement("option");
                    option.innerHTML = secondIndicators[i];
                    select2.appendChild(option);
                }
            };

            this.drawSelectedIndicator = function(index, index2, _mySeries, _div, _wrapperDiv, _indicators, _secondIndicators, newGraphic) {
                mySeries = _mySeries;
                div = _div;
                wrapperDiv = _wrapperDiv;
                indicators = _indicators;
                secondIndicators = _secondIndicators;
                if (select.options.length <= 1) {
                    var element = document.createElement("p");
                    element.innerHTML = indicators[0];
                    select.parentNode.insertBefore(element, select);
                    select.style.display="none";
                }
                if (select2.options.length <= 1) {
                    var element = document.createElement("p");
                    element.innerHTML = secondIndicators[0];
                    select2.parentNode.insertBefore(element, select2);
                    select2.style.display="none";
                }
                drawSelectedIndicator(index, index2, newGraphic);
            };

            var drawSelectedIndicator = function(index, index2, newGraphic) {
                var series =  mySeries[index][index2][0].values;
                createTable();

                function createTable() {
                    var table = document.createElement("table");
                    var tbody = document.createElement("tbody");
                    table.appendChild(tbody);
                    for(var i=0;i<series.length;i++) {
                        var tr = document.createElement("tr");
                        tbody.appendChild(tr);
                        var td = document.createElement("td");
                        td.innerHTML = xAxisValues.timeAndRegion[i];
                        tr.appendChild(td);
                        td = document.createElement("td");
                        if(series[i] <= limits[0]) 
                            td.style.backgroundColor = colors[0];
                        else if(series[i] > limits[0] && series[i] < limits[1])
                            td.style.backgroundColor = colors[1];
                        else
                            td.style.backgroundColor = colors[2];
                        td.innerHTML = series[i].toFixed(2);
                        tr.appendChild(td);
                    }
                    var container = typeof options.container === "string" ? 
                            document.querySelector(options.container) : 
                            options.container;
                    semaphoreDiv = document.createElement("div");
                    semaphoreDiv.className = "semaphoreDiv";
                    container.appendChild(semaphoreDiv);
                    semaphoreDiv.appendChild(div);
                    semaphoreDiv.appendChild(table);
                }
            };

            this.onIndicatorChanged = function() {
                semaphoreDiv.remove();
                drawSelectedIndicator(select.selectedIndex, select2.selectedIndex, false);
            };


            this.putSeriesByIndicator = function(myData, seriesByIndicator, indicators, countries, i, filter, xAxisValues) {
                var item = getIndexOfXValue();
                for (var c = 0; c < countries.length; c++) {
                    if(filter !== undefined) {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: [myData.getItem(indicators[i]).getItem(countries[c])[item]]
                        });
                    } else {
                        seriesByIndicator[c] = [];
                        seriesByIndicator[c].push({
                            name: countries[c],
                            values: myData.getItem(indicators[i]).getItem(countries[c])
                        });
                    }
                }

                function getIndexOfXValue() {
                    for(var i=0;i<xAxisValues.length;i++)
                        if(xAxisValues[i] === filter)
                            return i;
                }
            };

            this.by = new By().by;
        }

        function By() {
            this.by = function(myData, xAxisValues, mySeries, indicatorFilter, indicatorFilter2, indicatorFilter3) {
                if (myData !== null) {
                    var div = document.createElement("div");
                    div.className = "indicatorSelector";
                    var indicators = indicatorFilter !== undefined ?
                                     myData.keys().array.filter(filterIndicator) :
                                     myData.keys().array;
                    for (var i = 0; i < indicators.length; i++) {
                        var countries = indicatorFilter2 !== undefined ?
                                        myData.getItem(indicators[i]).keys().array.filter(filterSecondIndicator) :
                                        myData.getItem(indicators[i]).keys().array;
                        var seriesByIndicator = [];
                        this.putSeriesByIndicator(myData, seriesByIndicator, indicators, countries, i, indicatorFilter3, xAxisValues);
                        mySeries.push(seriesByIndicator);
                    }
                    this.createSelect(div, indicators, countries);
                    var wrapperDiv = document.createElement("div");
                    setTablePosition();
                    options.xAxis.values = xAxisValues;
                    this.drawSelectedIndicator(0, 0, mySeries, div, wrapperDiv, indicators, countries);
                }

                function filterIndicator(element) {
                    return element === indicatorFilter;
                }

                function filterSecondIndicator(element) {
                    return element === indicatorFilter2;
                }

                function setTablePosition() {
                    if (!tablePosition) {
                        var container = typeof options.container === "string" ? 
                            document.querySelector(options.container) : 
                            options.container;
                        container.appendChild(wrapperDiv);
                    }
                    else {
                        if (tablePosition.toLowerCase() == "below")
                            tableElement.parentNode.insertBefore(wrapperDiv, tableElement);
                        else
                            tableElement.insertAfter(wrapperDiv);
                    }
                }   
            };
        }
    }
})();if (typeof(wesCountry) === "undefined")
	var wesCountry = {};

wesCountry.table = new Object();

////////////////////////////////////////////////////////////////
// Pages
////////////////////////////////////////////////////////////////

wesCountry.table.pages = new (function() {
	var firstShownRow = 0;
	var numberFooterAnchors = 5; // Must be odd

	this.apply = function() {
		var tables = document.querySelectorAll("table.pages");
		var length = tables.length;
		
		for (var i = 0; i < length; i++) {
			var table = tables[i];
			
			// Table properties
			table.isPaged = true;
			
			table.firstShownRow = firstShownRow;
			table.numberFooterAnchors = numberFooterAnchors;
		
			var tBodies = table.tBodies;
			var length = tBodies.length;
			var rowNumber = 0;
			
			for (var j = 0; j < length; j++)
				rowNumber += tBodies[j].rows.length;				

			table.numberOfRows = rowNumber;
			
			var pageLength = (table.numberOfRows == 0) ? 1 : Math.floor(log10(table.numberOfRows)) + 1;
			table.rowsPerPage = Math.pow(10, pageLength - 1);
		
			prepareTable(table);
			
			// Header select
			createHeaderSelect(table);
		}
	}
	
	this.apply();
	
	function prepareTable(table) {
		// Fitst we remove empty rows (Added to complete last page)
		var emptyRows = table.querySelectorAll("tr.empty");
		var length = emptyRows.length;
		
		for (var i = 0; i < length; i++)
			emptyRows[i].parentNode.removeChild(emptyRows[i]);

		// Table properties
		table.numberOfPages = Math.ceil(table.numberOfRows / table.rowsPerPage);

		// If last page has less rows
		var total = table.numberOfPages * table.rowsPerPage;
		var length = table.numberOfColumns > 0 ? table.numberOfColumns : 1;
		var tBodies = table.tBodies;
		
		if (table.numberOfPages > 1 && total > table.numberOfRows && tBodies.length > 0) {
			var rowNumber = table.numberOfRows;
		
			while (total > rowNumber) {
				var tr = document.createElement("tr");
				tr.className = "empty";
				
				for (var i = 0; i < length; i++) {
					var td = document.createElement("td");
					td.innerHTML = "&nbsp";
					tr.appendChild(td);
				}
				
				tBodies[0].appendChild(tr);
				
				rowNumber++;
			}
		}

		table.selectedPage = 1;
		showPage(table);
		
		table.changePage = changePage;
		table.reloadPage = function () {
			showPage(this);
		}
		
		// Footer
		createFooter(table);
	}
	
	function changePage(pageNumber) {
		if (pageNumber > this.numberOfPages || pageNumber < 1)
			return;
			
		this.firstShownRow = (pageNumber - 1) * this.rowsPerPage;
		this.selectedPage = pageNumber;
		
		showPage(this);
	}
	
	function showPage(table) {
		var firstShownRow = table.firstShownRow;
		var rowsPerPage = table.rowsPerPage * 1;
		var tBodies = table.tBodies;		
	
		// We set visible and hidden rows
		var count = 0; // All rows (including empty rows)
		var numberOfRows = 0; // Real rows
		var lastShownRow = firstShownRow + rowsPerPage - 1;
	
		var length = tBodies.length;
		var numberOfColumns = 0;
		
		for (var i = 0; i < length; i++) {
			var rows = tBodies[i].rows;
			var rowNumber = rows.length;
			
			for (var j = 0; j < rowNumber; j++) {
				var row = rows[j];
				var shown = count >= firstShownRow && count <= lastShownRow;
				row.style.display = shown == true ? "table-row" : "none";
				
				if (row.cells.length > numberOfColumns)
					numberOfColumns = row.cells.length;
				
				if (row.className != "empty")
					numberOfRows++;
				
				count++;
			}
		}
		
		// Set footer link as selected
		updateFooter(table);
		
		// Update table properties
		table.numberOfRows = numberOfRows;
		table.numberOfColumns = numberOfColumns;
	}
	
	function updateFooter(table) {
		var selectedPage = table.selectedPage;
		var numberOfPages = table.numberOfPages;
		
		// First link
		var link = table.querySelector("tFoot a.first");
		
		if (link) {
			link.className = selectedPage > 1 ? "not-number first" : "not-number first disabled";
			link.index = selectedPage > 1 ? 1 : -1;
		}
		
		// Previous link
		var link = table.querySelector("tFoot a.previous");
		
		if (link) {
			link.className = selectedPage > 1 ? "not-number previous" : "not-number previous disabled";
			link.index = selectedPage > 1 ? selectedPage - 1 : -1;		
		}
		
		// Next link
		var link = table.querySelector("tFoot a.next");
		
		if (link) {
			link.className = selectedPage < numberOfPages ? "not-number next" : "not-number next disabled";
			link.index = selectedPage < numberOfPages ? selectedPage + 1 : -1;	
		}
		
		// Last link
		var link = table.querySelector("tFoot a.last");
		
		if (link) {
			link.className = selectedPage < numberOfPages ? "not-number last" : "not-number last disabled";
			link.index = selectedPage < numberOfPages ? numberOfPages : -1;		
		}
		
		// Number links
		var links = table.querySelectorAll("tFoot a.number");
		var length = links.length;
		
		// Visible anchors
		var numberOfBubbles = Math.min(table.numberFooterAnchors, length);
		var numberFooterAnchorsHalf = Math.floor(numberOfBubbles / 2);

		var previous = selectedPage > numberFooterAnchorsHalf ? numberFooterAnchorsHalf : selectedPage - 1;
		var next = table.numberFooterAnchors - 1 - previous;
	
		var firstShown = selectedPage - previous;
		var lastShown = selectedPage + next;
		
		if (lastShown > length) {
			firstShown -= lastShown - length;
			lastShown = length;
		}
			
		for (var i = 1; i <= length; i++) {
			var shown = i >= firstShown && i <= lastShown ? "shown" : "hidden";
			var selected = i == selectedPage ? "number selected " : "number ";
			links[i - 1].className = selected + shown;
		}
		
		// Show navigation details
		var first = (selectedPage - 1) * table.rowsPerPage + 1;
		var last = first + table.rowsPerPage - 1 > table.numberOfRows ? table.numberOfRows : first + table.rowsPerPage - 1;
		var details = table.querySelector("tFoot span.details");
		
		if (details)
			details.innerHTML = first + " - " + last + " of " + table.numberOfRows + " items.";
	}
	
	function createFooter(table) {
		var footer = table.querySelector("tFoot.pagination");
	
		if (!footer) {
			var footer = document.createElement("tFoot");
			footer.className = "pagination";
			
			table.appendChild(footer);
			table.navFooter = footer;
		}
		
		footer.innerHTML = "";
		
		var tr = document.createElement("tr");
		footer.appendChild(tr);
		
		var td = document.createElement("td");
		tr.appendChild(td);
		td.colSpan = table.numberOfColumns;
		
		// Navigation details
		var span = document.createElement("span");
		span.className = "details";
		td.appendChild(span);	
		
		var first = table.numberOfRows > 0 ? 1 : 0;
		var last = table.numberOfRows > table.rowsPerPage ? table.rowsPerPage : table.numberOfRows;
		span.innerHTML = first + " - " + last + " of " + table.numberOfRows + " items.";
			
		// First link
		var a = createLink(table, "<<", "not-number first disabled", -1);
		td.appendChild(a);
		
		// Previous link
		var a = createLink(table, "<", "not-number previous disabled", -1);
		td.appendChild(a);
		
		// Number links
		var length = table.numberOfPages;
	
		for (var i = 1; i <= length; i++) {
			var shown = i > table.numberFooterAnchors ? "hidden" : "shown";
			var selected = i == 1 ? "number selected " : "number ";
			var a = createLink(table, i, selected + shown, i);
			td.appendChild(a);
		}
		
		// Next link
		var a = createLink(table, ">", length > 1 ? "not-number next" : "not-number next disabled", length > 1 ? 2 : -1);
		td.appendChild(a);		
		
		// Last link
		var a = createLink(table, ">>", length > 1 ? "not-number last" : "not-number last disabled", length > 1 ? length : -1);
		td.appendChild(a);
	}
	
	function createHeaderSelect(table) {
		var tHead = table.tHead;
		var numberOfRows = table.numberOfRows;
		var length = (numberOfRows == 0) ? 1 : Math.floor(log10(numberOfRows)) + 1;

		if (tHead && length > 1) {
			var tr = document.createElement("tr");
			tr.className = "select";
			tHead.insertBefore(tr, tHead.firstChild);
			
			var th = document.createElement("th");
			th.colSpan = table.numberOfColumns;
			tr.appendChild(th);
			
			var span = document.createElement("span");
			span.className = "show";
			th.appendChild(span);
			
			span.appendChild(document.createTextNode("Show "));
			
			var select = document.createElement("select");
			th.appendChild(select);
			
			select.table = table;
			
			var span = document.createElement("span");
			span.className = "entries";
			th.appendChild(span);
			
			span.appendChild(document.createTextNode(" entries"));
			
			//Options
			var inc = Math.pow(10, length - 1);
			
			for (var i = 1; i <= 4; i++) {
				var number = inc * i;
				
				if (number > numberOfRows)
					break;
				
				createOption(select, number, number);
			}
			
			createOption(select, "all", numberOfRows);
			
			// Handler
			select.onchange = function() {
				var value = this.options[this.selectedIndex].value;
				this.table.rowsPerPage = value;

				prepareTable(this.table);
				table.changePage(1);
			};
		}
	}
	
	function createOption(select, text, value) {
		var option = document.createElement("option");
		option.text = text;
		option.value = value;
		select.appendChild(option);
	}
	
	function log10(val) {
		return Math.log(val) / Math.LN10;
	}

	function createLink(table, text, className, index) {
		var a = document.createElement("a");
		a.className = className;
		a.table = table;
		a.index = index;
		
		a.onclick = function() {
			this.table.changePage(this.index);
		};
		
		var textNode = document.createTextNode(text);
		a.appendChild(textNode);
		
		return a;
	}
})();

////////////////////////////////////////////////////////////////
// Sortable 
////////////////////////////////////////////////////////////////

wesCountry.table.sort = new (function() {	
	this.apply = function() {
		var tables = document.querySelectorAll("table.sortable");
		var length = tables.length;
		
		for (var i = 0; i < length; i++)
			iterateOverRows(tables[i]);
	}
	
	this.apply();
	
	function iterateOverRows(table) {
		var headers = table.tHead.rows;
		//var headers = table.querySelectorAll("tHead tr");
		var length = headers.length;
	
		for (var i = 0; i < length; i++) {
			if (headers[i].className == "select")
				continue;
				
			headers[i].className = "sorter";	
			
			var rowLength = headers[i].cells.length;
		
			for (var j = 0; j < rowLength; j++) {
				headers[i].cells[j].table = table;
				headers[i].cells[j].index = j;
				headers[i].cells[j].sort = "empty";
				
				var img = new Image();
				img.className = "empty";
				headers[i].cells[j].appendChild(img);
				
				headers[i].cells[j].onclick = function() {
					sortRows(this.table, this.index, this);
				};
			}
		}
	}
	
	function sortRows(table, index, header) {
		// Insert rows in array
		
		var rows = new Array();
		
		var length = table.tBodies.length;
		
		for (var i = 0; i < length; i++) {
			var tBody = table.tBodies[i];
		
			for (var j = 0; j < tBody.rows.length; j++) {
				var row = tBody.rows[j];
			
				rows.push(row);
			}
		}
		
		// Sorting		
		if (header.sort == "empty" || header.sort == "down")
			header.sort = "up";
		else
			header.sort = "down";	
		
		rows.sort(function(row1, row2) {
			if (row1.className == "empty" || row2.className == "empty")
				return 1;

			var row1 = row1.cells[index].innerHTML.toString();
			var row2 = row2.cells[index].innerHTML.toString();	
		
			if (row1 < row2)
				return header.sort == "up" ? - 1 : 1;
			else if (row1 > row2)
				return header.sort == "up" ? 1 : -1;
			else
				return 0;
		});
		
		// Update header image
		var img = header.querySelector("img");
		img.className = header.sort;
		
		// Update header image for the rest of columns
		//var tHeader = table.tHead.rows[0].cells;
		var tHeader = table.querySelectorAll("tHead tr.sorter th");
		var length = tHeader.length;
		
		for (var i = 0; i < length; i++)
			if (i != index)
				emptyHeaderSorter(tHeader[i]);
		
		// Delete rows
		var tHead = table.tHead;
		var tFoot = table.tFoot;
		
		while(table.hasChildNodes())
			table.removeChild(table.firstChild);
			
		// Insert head
		table.appendChild(tHead);
		
		// Insert footer
		if (tFoot)
			table.appendChild(tFoot);
		
		// Insert sorted rows
		var tBody = document.createElement('tbody');
		table.appendChild(tBody);
		
		var length = rows.length;
		
		for (var i = 0; i < length; i++)
			tBody.appendChild(rows[i]);
			
		// If table is paged then page 1 is set
		if (table.changePage)	
			table.changePage(1);
	}
	
	function emptyHeaderSorter(header) {
		var img = header.querySelectorAll("img");
		
		if (img && img.length && img.length > 0)
			img[0].className = "empty";
			
		header.sort = "empty";
	}
})();function SortedArray() {
    var index = 0;
    this.array = [];
    var length = arguments.length;
    
    while (index < length) 
    	this.insert(arguments[index++]);
    
	this.length = 0;
	
	this.insert = function (element) {
	    var array = this.array;
	    var index = array.length;
	    array.push(element);
	    
	    this.length = this.array.length;
	
	    while (index) {
	        var i = index, j = --index;
	
	        if (array[i] < array[j]) {
	            var temp = array[i];
	            array[i] = array[j];
	            array[j] = temp;
	        }
	    }
	
	    return this;
	};
	
	this.get = function (index) {
		return this.array[index];
	};
	
	this.getArray = function() {
		return this.array;	
	};
	
	// No repeated elements allowed
	
	this.uniqueInsert = function (element) {
		if (this.search(element) != -1)
			return;
			
		this.insert(element);
	}
	
	this.search = function (element) {
	    var low = 0;
	    var array = this.array;
	    var high = array.length;
	
	    while (high > low) {
	        var index = (high + low) / 2 >>> 0;
	        var cursor = array[index];
	
	        if (cursor < element) low = index + 1;
	        else if (cursor > element) high = index;
	        else return index;
	    }
	
	    return -1;
	};
	
	this.remove = function (element) {
	    var index = this.search(element);
	    if (index >= 0) this.array.splice(index, 1);
	    
	    this.length = this.array.length;
	    
	    return this;
	};
}if (typeof(exports) === "undefined")
	exports = new Object();

var Selector = exports.Selector = function(data, options) {
	var defaultOptions = {
		"ul-class": "default-selector",
		callback: null,
		maxSelectedItems: -1,
		selectedItems: []
	};

	var firstLevelItems = [];
	var selectedItems = new SortedArray();
	var root = null;

	function init() {
		// Merge default options and user options
		options = mergeOptionsAndDefaultOptions(options, defaultOptions);
	
		var list = generateList(data, null, 1, null, null);
		root = list.ul;

		// Set options.selectedItems as selected
		var selectedItems = list.selectedItems;
		var length = selectedItems.length;

		for (var i = 0; i < length; i++)
			selectedItems[i].onclick();
	}
	
	init();
	
	this.render = function() {
		return root;
	}
	
	this.clear = function() {
		var length = root.children.length;
		for (var i = 0; i < length; i++)
			updateElementStatus(root.children[i], null, false);
	}
	
	// List generation
	function generateList(element, parent, level, previousLink, parentLink) {
		var ul = document.createElement("ul");
		ul.className = options["ul-class"];
	
		// Sort children
		element.sort(function(a, b) {
			if (a.label < b.label)
				return -1;
			if (a.label > b.label)
				return 1;
			return 0;
		});
		
		var length = element.length;
		
		var firstChildLink = null;
		
		var selected = false;
		var selectedItems = [];
		
		for (var i = 0; i < length; i++) {
			var child = element[i];
			var childrenLength = child.children && child.children.length ? child.children.length : 0;
			
			var li = document.createElement("li");
			ul.appendChild(li);
			
			// Set parent information
			li.code = child.code;
			li.liParent = parent;
			li.data = child;
			
			// Selection
			li.isSelected = false;
			
			var currentLink = document.createElement("a");
			currentLink.href = "javascript: void(0)"
			currentLink.value = child.label;

			// Check if element is selected
			if (options.selectedItems.indexOf(li.code) != -1) {
				selected = true;
				selectedItems.push(currentLink);
			}

			if (parentLink == null)
				firstLevelItems.push(currentLink);

			// Previous and next links
			currentLink.previousSiblingLink = previousLink;
			currentLink.nextSiblingLink = null;
			currentLink.parentLink = parentLink;
			
			if (previousLink)
				previousLink.nextSiblingLink = currentLink;
	
			if (i == 0)
				firstChildLink = currentLink;
			
			currentLink.className = "circleAndText"
			li.appendChild(currentLink);
			
			// Click event on currentLink div
			// We set the parent of currentLink div (the LI element)
			currentLink.liParent = li;
			
			currentLink.onclick = function(event) { 
				elementClick(this.liParent, options.callback); 
				
				if (event)
					event.stopPropagation();	
			};
						
			// Plus or minus sign to show / hide children
			var plusOrMinus = document.createElement("div");
			plusOrMinus.className = childrenLength > 0 ? "plusOrMinus" : "hidden-plusOrMinus";
			plusOrMinus.innerHTML = "+";
			currentLink.appendChild(plusOrMinus);
				
			if (childrenLength > 0) {
				plusOrMinus.onclick = function(event) { 
					plusMinusClick(this);
					event.stopPropagation();
				}
			}
			
			// Keyboard event for link
			currentLink.plusOrMinus = plusOrMinus;
			
			currentLink.onkeydown = function(event) {
				if (event.keyCode == 13) {
					elementClick(this.liParent, options.callback); 	
					
					event.stopPropagation();
					return false;
				}
				else if (event.keyCode == 38) { // Up arrow key
					if (this.previousSiblingLink)
						this.previousSiblingLink.focus();
				
					event.stopPropagation();
					return false;
				}
				else if (event.keyCode == 40) { // Down arrow key
					// If opened go to first child
					if (this.plusOrMinus.opened && this.firstChildLink)
						this.firstChildLink.focus();
					else if (this.nextSiblingLink)
						this.nextSiblingLink.focus();
					// After last child we move onto next sibling
					else if (this.parentLink.nextSiblingLink)
						this.parentLink.nextSiblingLink.focus();
				
					event.stopPropagation();
					return false;
				}
				else if (event.keyCode == 37 || event.keyCode == 39) { // Left and right keys
					event.stopPropagation();
				
					plusMinusClick(this.plusOrMinus);
				
					event.keyCode = 9; 
					return event.keyCode
				}
			};
			
			var circle = document.createElement("div");
			circle.className = "circle";
			currentLink.appendChild(circle);
			
			var title = document.createElement("div");
			title.className = "title";
			currentLink.appendChild(title)
			
			var text = document.createTextNode(child.label);
			title.appendChild(text);
			
			// Update previous link
			previousLink = currentLink;
			
			if (childrenLength > 0) {			
				// Counter circle
				var counter = document.createElement("span");
				counter.className = "empty-counter";
				circle.appendChild(counter);
			
				text = document.createTextNode("0");
				counter.appendChild(text);
				
				// Set li properties
				li.counter = {
					div: counter,
					value: 0	
				};
				
				// Children
				var childrenUl = generateList(child.children, li, level + 1, previousLink, currentLink);
				li.appendChild(childrenUl.ul);
				
				// Update first child link
				currentLink.firstChildLink = childrenUl.firstChildLink;
				
				// Set plusOrMinus properties
				plusOrMinus.childrenUl = childrenUl.ul;
				
				// Check if any child is selected
				if (childrenUl.selected == true) {
					selected = true;
					// Update + / - symbol
					plusOrMinus.innerHTML = "-";
				}
					
				selectedItems = selectedItems.concat(childrenUl.selectedItems);	
			}
			
			// Set child number
			li.childNumber = child.children ? child.children.length : 0;
		}
		
		// Non top-level elements are initially hidden
		// Unless some child is in options.selectedItems
		if (level > 1 && selected == false)
			ul.style.display = "none";
	
		return {
					ul: ul,
					firstChildLink: firstChildLink,
					selected: selected,
					selectedItems: selectedItems
				};
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                            PLUS / MINUS CLICK
	////////////////////////////////////////////////////////////////////////////////	
	
	function plusMinusClick (element) {
		if (element.innerHTML == "+") {
			element.innerHTML = "&#8212;";
			
			if (element.childrenUl)
				element.childrenUl.style.display = "block";
				
			element.opened = true;
		}
		else {
			element.innerHTML = "+";
			
			if (element.childrenUl)
				element.childrenUl.style.display = "none";
				
			element.opened = false;
		}
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                              ELEMENT CLICK
	////////////////////////////////////////////////////////////////////////////////	
	
	this.selectAll = function() {
		var length = firstLevelItems.length;
		for (var i = 0; i < length; i++)
			elementClick(firstLevelItems[i].liParent, null);
	}
	
	function elementClick(element, callback) {		
		var selected = !element.isSelected;
		
		if (selected && options.maxSelectedItems > 0 && selectedItems.length >= options.maxSelectedItems)
			return;
		
		updateElementStatus(element, callback, selected);
	}
	
	function updateElementStatus(element, callback, selected) {
		setElementStatus(element, selected);
		
		// Add element in its parent's counter
		if (element.liParent) {
			var oldParentCounter = element.liParent.counter.value;
			var parentCounter = selected ? oldParentCounter + 1 : oldParentCounter - 1;
		
			updateElementCounter(element.liParent, parentCounter);
			
			// An element is selected when all its children are selected
			// If an element is unselected then its parent must be unselected
			if (!selected) {
				element.liParent.className = "not-selected";
				element.liParent.isSelected = false;
				
				updateSelectedItems(element.liParent.code, false);
			} 
			else {
				// If you select all an element's children then the element must be selected
				if (parentCounter == element.liParent.childNumber) {
					element.liParent.className = "selected";
					element.liParent.isSelected = true;
					
					updateSelectedItems(element.liParent.code, true);
				}
			}
		}
			
		// Update current node's counter when has children
		// If the element is selected, the counter equals its child number
		// Else it equals 0
		if (element.childNumber > 0)
			updateElementCounter(element, selected ? element.childNumber : 0);
			
		// Callback invocation
		if (callback)
			callback.call(element, element.data, selectedItems);
	}
	
	function setElementStatus(element, status) {
		if (element.tagName.toLowerCase() == "li") {
			element.isSelected = status;
			element.className = status ? "selected" : "not-selected";
			
			// SelectedItems update
			updateSelectedItems(element.code, status);
			
			// Update anchor title
			var value = element.firstChild.value;
			element.firstChild.title = value + (status ? " is selected" : "");
		}
		
		var length = element && element.children && element.children.length ? element.children.length : 0;
		
		for (var i = 0; i < length; i++)
			setElementStatus(element.children[i], status);
	}
	
	function updateElementCounter(element, value) {	
		var counter = element.counter;
		
		counter.value = value;
		counter.div.innerHTML = counter.value; 
		
		counter.div.className = counter.value > 0 ? "counter" : "empty-counter";
		
		// Update anchor title
		var value = element.firstChild.value;
		element.firstChild.title = value + ": " + counter.value + 
			(counter.value != 1 ? " selected countries" : " selected country");
	}

	////////////////////////////////////////////////////////////////////////////////
	//                           UPDATE SELECTED ITEMS
	////////////////////////////////////////////////////////////////////////////////
	
	function updateSelectedItems(code, action) {
		if (code) {
			if (action)
				selectedItems.uniqueInsert(code);	
			else
				selectedItems.remove(code);
		}
	}
	
	////////////////////////////////////////////////////////////////////////////////
	//                              MERGING OPTIONS
	////////////////////////////////////////////////////////////////////////////////
	
	function mergeOptionsAndDefaultOptions(options, defaultOptions) {
		if (options) {
			if (typeof options === "string")
				options = { container: options };
		
			var auxOptions = clone(defaultOptions);
			
			for (var option in options)
				auxOptions[option] = mergeOptions(auxOptions[option], options[option]);
			
			options = auxOptions;
		}
		else
			options = clone(defaultOptions);
			
		return options;
	};
	
	function mergeOptions(to, from) {
		if (from instanceof Array) {
			return from;
		}
		else if (typeof from === "object") {
			for (var option in from) {
				to[option] = mergeOptions(to[option], from[option]);
			}

			return to;
		}
		else
			return from;
	};
	
	function clone(obj) {
		// Not valid for copying objects that contain methods
	    return JSON.parse(JSON.stringify(obj));
	}
};