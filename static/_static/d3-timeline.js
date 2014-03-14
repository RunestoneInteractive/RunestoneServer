(function () {
  d3.timeline = function() {
    var DISPLAY_TYPES = ["circle", "rect"];
 
    var hover = function () {},
        mouseover = function () {},
        mouseout = function () {},
        click = function () {},
        scroll = function () {},
        orient = "bottom",
        width = null,
        height = null,
        tickFormat = { format: d3.time.format("%I %p"), 
          tickTime: d3.time.hours, 
          tickInterval: 1, 
          tickSize: 6 },
        colorCycle = d3.scale.category20(),
        colorPropertyName = null,
        display = "rect",
        beginning = 0,
        ending = 0,
        margin = {left: 30, right:30, top: 30, bottom:30},
        stacked = false,
        rotateTicks = false,
        timeIsRelative = false,
        itemHeight = 20,
        itemMargin = 5,
        showTodayLine = false,
        showTodayFormat = {marginTop: 25, marginBottom: 0, width: 1, color: colorCycle}
      ;
 
    function timeline (gParent) {
      var g = gParent.append("g");
      var gParentSize = gParent[0][0].getBoundingClientRect();
 
      var gParentItem = d3.select(gParent[0][0]);
 
      var yAxisMapping = {},
        maxStack = 1,
        minTime = 0,
        maxTime = 0;
      
      setWidth();
 
      // check if the user wants relative time
      // if so, substract the first timestamp from each subsequent timestamps
      if(timeIsRelative){
        g.each(function (d, i) {
          d.forEach(function (datum, index) {
            datum.times.forEach(function (time, j) {
              if(index==0 && j==0){
                originTime = time.starting_time;               //Store the timestamp that will serve as origin
                time.starting_time = 0;                        //Set the origin
                time.ending_time = time.ending_time - originTime;     //Store the relative time (millis)
              }else{
                time.starting_time = time.starting_time - originTime;
                time.ending_time = time.ending_time - originTime;
              }
            });
          });
        });
      }
 
      // check how many stacks we're gonna need
      // do this here so that we can draw the axis before the graph
      if (stacked || (ending == 0 && beginning == 0)) {
        g.each(function (d, i) {
          d.forEach(function (datum, index) {
 
            // create y mapping for stacked graph
            if (stacked && Object.keys(yAxisMapping).indexOf(index) == -1) {
              yAxisMapping[index] = maxStack;
              maxStack++;
            }
 
            // figure out beginning and ending times if they are unspecified
            if (ending == 0 && beginning == 0){
              datum.times.forEach(function (time, i) {
                if (time.starting_time < minTime || (minTime == 0 && timeIsRelative == false))
                  minTime = time.starting_time;
                if (time.ending_time > maxTime)
                  maxTime = time.ending_time;
              });
            }
          });
        });
 
        if (ending == 0 && beginning == 0) {
          beginning = minTime;
          ending = maxTime;
        }
      }
 
     var scaleFactor = (1/(ending - beginning)) * (width - margin.left - margin.right);
     var zoomFactor = 1;
     
     var xScale = d3.time.scale()
           .domain([beginning, ending])
           .range([margin.left, width - margin.right]);

     // add the label
     g.each(function(d, i) {
       d.forEach( function(datum, index){
        var hasLabel = (typeof(datum.label) != "undefined");

         if (hasLabel) {
           gParent.append('text')
             .attr("class", "timeline-label")
             .attr("transform", "translate(" + 0 + "," + (itemHeight/2 + margin.top + (itemHeight + itemMargin) * yAxisMapping[index])+")")
             .text(hasLabel ? datum.label : datum.id);
         }
         
         if (typeof(datum.icon) != "undefined") {
           gParent.append('image')
             .attr("class", "timeline-label")
             .attr("transform", "translate("+0 +"," + (margin.top + (itemHeight + itemMargin) * yAxisMapping[index])+")")
             .attr("xlink:href", datum.icon)
             .attr("width", margin.left)
             .attr("height", itemHeight);
         }
       });
    });

    // draw the axis
    hours = d3.time.hour.range(beginning, ending+1);
    
    numberOfTicks = hours.length;
    while (numberOfTicks > width/100) {
       numberOfTicks = Math.round(numberOfTicks/2);
    }

    var xAxis = d3.svg.axis()
         .scale(xScale)
         .orient(orient)
         .ticks(numberOfTicks)
         .tickSize(tickFormat.tickSize, 1);

    g.append("g")
        .attr("class", "axis")
         .attr("transform", "translate(" + 0 + "," + (margin.top + (itemHeight + itemMargin) * maxStack)+")");

    function renderAxes (){
       // draw the axis
       g.select(".axis").call(xAxis); 
    }

    // clip path
    g.append('defs').append('clipPath')
      .attr('id', 'plot-area')
      .append('rect')
      .attr('x', margin.left)
      .attr('y', margin.top)
      .attr('height', 1000)
      .attr('width', width);

    // draw the chart
    g.each(function(d, i) {
     d.forEach( function(datum, index){
      for (var i = 0; i < datum.times.length; i++) {
        // eliminate the data whose time is out of domain
        if (datum.times[i].starting_time >= beginning && datum.times[i].starting_time <= ending) {
          var data = [];
          data[0] = datum.times[i];

          g.append("g")
          .attr('id', 'chart')
          .attr('clip-path', 'url(#plot-area)')
          .selectAll(".display")
          .data(data)
          .enter()
          .append(display)
          .attr("class", "display")
          .attr("y", getStackPosition)
          .attr("cy", getStackPosition)
          .attr("r", itemHeight/2)
          .attr("height", itemHeight)
          .style("fill", function(d, i){
            if (d.color) return d.color;
            if( colorPropertyName ){ 
             return colorCycle( datum[colorPropertyName] ) 
            } 
            return colorCycle(index);  
          })
          .on("mousemove", function (d, i) {
            hover(d, index, datum);
          })
          .on("mouseover", function (d, i) {
            mouseover(d, i, datum);
          })
          .on("mouseout", function (d, i) {
            mouseout(d, i, datum);
          })
          .on("click", function (d, i) {
            click(d, index, datum);
          })
          .append("title")
          .text(function(d){
             return d.hover_text;
          });
       
          function getStackPosition(d, i) {
            if (stacked) {
             return margin.top + (itemHeight + itemMargin) * yAxisMapping[index];
            } 
            return margin.top;
          }
        }
      };
     });
    });
    
    function renderData (){
      g.selectAll(".display")
        .attr('x', function(d, i){
          return xScale(d.starting_time);
        })
        .attr("width", function (d, i) {
          return Math.max(3, xScale(d.ending_time) - xScale(d.starting_time));
        })
        .attr('cx', function(d, i){
          return xScale(d.starting_time);
        });
    }
     
     renderAxes()
     renderData()
      
     function move() {
       var x = Math.min(0, Math.max(gParentSize.width - width, d3.event.translate[0]));
       zoom.translate([x, 0]);
       g.attr("transform", "translate(" + x + ",0)");
       scroll(x*scaleFactor, xScale);
     }
     
     function changeScale(){
        console.log('scale', d3.event.scale, 'old_scale', zoomFactor);
        console.log('translate', d3.event.translate);
        zoomFactor = d3.event.scale;
        xScale.range([margin.left, width*zoomFactor - margin.right])
     }
     
     function zoomOrmove(){
           renderAxes();
           renderData();
     }
     
     var zoom = d3.behavior.zoom().x(xScale).scaleExtent( [0,1000] ).scale( 1 ).on("zoom", zoomOrmove);
 
     gParent
       .attr("class", "scrollable")
       .call(zoom);
 
      
      if (rotateTicks) {
        g.selectAll("text")
          .attr("transform", function(d) {
            return "rotate(" + rotateTicks + ")translate("
              (this.getBBox().width/2+10) + "," // TODO: change this 10
              this.getBBox().height/2 + ")";
          });
      }
 
      var gSize = g[0][0].getBoundingClientRect();
      setHeight();
 
      if( showTodayLine )
      {
        var todayLine = xScale(new Date());
        gParent.append("svg:line")
          .attr("x1", todayLine)
          .attr("y1", showTodayFormat.marginTop)
          .attr("x2", todayLine)
          .attr("y2", height - showTodayFormat.marginBottom)
          .style("stroke", showTodayFormat.color)//"rgb(6,120,155)")
          .style("stroke-width", showTodayFormat.width); 
      }
 
      function getXPos(d, i) {
        return margin.left + (d.starting_time - beginning) * scaleFactor;
      }
 
      function setHeight() {
        if (!height && !gParentItem.attr("height")) {
          if (itemHeight) {
            // set height based off of item height
            height = gSize.height + gSize.top - gParentSize.top;
            // set bounding rectangle height
            d3.select(gParent[0][0]).attr("height", height);
          } else {
            throw "height of the timeline is not set";
          }
        } else {
          if (!height) {
            height = gParentItem.attr("height");
          } else {
            gParentItem.attr("height", height);
          }
        }
      }
 
      function setWidth() {
        if (!width && !gParentSize.width) {
          throw "width of the timeline is not set. As of Firefox 27, timeline().with(x) needs to be explicitly set in order to render";
        } else if (!(width && gParentSize.width)) {
          if (!width) {
            width = gParentItem.attr("width");
          } else {
            gParentItem.attr("width", width);
          }
        }
        // if both are set, do nothing
      }
    }
 
    timeline.margin = function (p) {
      if (!arguments.length) return margin;
      margin = p;
      return timeline;
    }
 
    timeline.orient = function (orientation) {
      if (!arguments.length) return orient;
      orient = orientation;
      return timeline;
    }
    
    timeline.itemHeight = function (h) {
      if (!arguments.length) return itemHeight;
      itemHeight = h;
      return timeline;
    }
 
    timeline.itemMargin = function (h) {
      if (!arguments.length) return itemMargin;
      itemMargin = h;
      return timeline;
    }
 
    timeline.height = function (h) {
      if (!arguments.length) return height;
      height = h;
      return timeline;
    }
 
    timeline.width = function (w) {
      if (!arguments.length) return width;
      width = w;
      return timeline;
    }
 
    timeline.display = function (displayType) {
      if (!arguments.length || (DISPLAY_TYPES.indexOf(displayType) == -1)) return display;
      display = displayType;
      return timeline;
    }
 
    timeline.tickFormat = function (format) {
      if (!arguments.length) return tickFormat;
      tickFormat = format;
      return timeline;
    }
 
    timeline.hover = function (hoverFunc) {
      if (!arguments.length) return hover;
      hover = hoverFunc;
      return timeline;
    }
 
    timeline.mouseover = function (mouseoverFunc) {
      if (!arguments.length) return mouseoverFunc;
      mouseover = mouseoverFunc;
      return timeline;
    }
 
    timeline.mouseout = function (mouseoverFunc) {
      if (!arguments.length) return mouseoverFunc;
      mouseout = mouseoverFunc;
      return timeline;
    }
 
    timeline.click = function (clickFunc) {
      if (!arguments.length) return click;
      click = clickFunc;
      return timeline;
    }
    
    timeline.scroll = function (scrollFunc) {
      if (!arguments.length) return scroll;
      scroll = scrollFunc;
      return timeline;
    }
 
    timeline.colors = function (colorFormat) {
      if (!arguments.length) return colorCycle;
      colorCycle = colorFormat;
      return timeline;
    }
 
    timeline.beginning = function (b) {
      if (!arguments.length) return beginning;
      beginning = b;
      return timeline;
    }
 
    timeline.ending = function (e) {
      if (!arguments.length) return ending;
      ending = e;
      return timeline;
    }

    timeline.rotateTicks = function (degrees) {
      rotateTicks = degrees;
      return timeline;
    }
 
    timeline.stack = function () {
      stacked = !stacked;
      return timeline;
    }
 
    timeline.relativeTime = function() {
      timeIsRelative = !timeIsRelative;
      return timeline;
    }

    timeline.showToday = function () {
      showTodayLine = !showTodayLine;
      return timeline;
    }

    timeline.showTodayFormat = function(todayFormat) {
      if (!arguments.length) return showTodayFormat;
      showTodayFormat = todayFormat;
      return timeline;
    }

    timeline.colorProperty = function(colorProp) {
      if (!arguments.length) return colorPropertyName;
      colorPropertyName = colorProp;
      return timeline;
    }
    
    return timeline;
  };
 })();