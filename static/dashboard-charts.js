DashboardCharts = DashboardCharts();
function DashboardCharts(){
    return {
        studentActivity: studentActivity,
        exerciseAttempts: exerciseAttempts,
        donutChart: donutChart
    }

    function studentActivity(data) {
        var margins = {
            top: 12,
            left: 100,
            right: 24,
            bottom: 24
        },
        width = 400 - margins.left - margins.right,
            height = (10 * 24) - margins.top - margins.bottom,
            
            dataset = [{
                data: [{
                    student: 'Bob Brown',
                    count: 4
                }, {
                    student: 'Jack Jackson',
                    count: 10
                }, {
                    student: 'Macy Millan',
                    count: 7
                }, {
                    student: 'Sarah Smith',
                    count: 7
                }, {
                    student: 'Xu Hung',
                    count: 4
                }, {
                    student: 'Rachel Ru',
                    count: 8
                }, {
                    student: 'John Hendrick',
                    count: 6
                }, {
                    student: 'Nick Collans',
                    count: 5
                }, {
                    student: 'Tim Collans',
                    count: 2
                }, {
                    student: 'Gina Kidder',
                    count: 7
                }],
                name: 'Sections Read'
            }, {
                data: [{
                    student: 'Bob Brown',
                    id: 'bbrown',
                    count: 11
                }, {
                    student: 'Jack Jackson',
                    id: 'bbrown',
                    count: 13
                }, {
                    student: 'Macy Millan',
                    id: 'bbrown',
                    count: 17
                }, {
                    student: 'Sarah Smith',
                    id: 'bbrown',
                    count: 9
                }, {
                    student: 'Xu Hung',
                    id: 'bbrown',
                    count: 4
                }, {
                    student: 'Rachel Ru',
                    id: 'bbrown',
                    count: 17
                }, {
                    student: 'John Hendrick',
                    id: 'bbrown',
                    count: 13
                }, {
                    student: 'Nick Collans',
                    id: 'bbrown',
                    count: 12
                }, {
                    student: 'Tim Collans',
                    count: 9
                }, {
                    student: 'Gina Kidder',
                    count: 7
                }],
                name: 'Exercises Correct'
            }, {
                data: [{
                    student: 'Bob Brown',
                    count: 3
                }, {
                    student: 'Jack Jackson',
                    count: 6
                }, {
                    student: 'Macy Millan',
                    count: 1
                }, {
                    student: 'Sarah Smith',
                    count: 4
                }, {
                    student: 'Xu Hung',
                    count: 0
                }, {
                    student: 'Rachel Ru',
                    count: 2
                }, {
                    student: 'John Hendrick',
                    count: 1
                }, {
                    student: 'Nick Collans',
                    count: 3
                }, {
                    student: 'Tim Collans',
                    count: 5
                }, {
                    student: 'Gina Kidder',
                    count: 8
                }],
                name: 'Exercises Missed'
            }

            ],
            dataset = data,
            series = dataset.map(function (d) {
                return d['name'];
            }),
            dataset = dataset.map(function (d) {
                return d.data.map(function (o, i) {
                    // Structure it so that your numeric
                    // axis (the stacked amount) is y
                    return {
                        y: o['count'],
                        x: o['student']
                    };
                });
            }),
            stack = d3.layout.stack();

        stack(dataset);

        var dataset = dataset.map(function (group) {
            return group.map(function (d) {
                // Invert the x and y values, and y0 becomes x0
                return {
                    x: d.y,
                    y: d.x,
                    x0: d.y0
                };
            });
        }),
            svg = d3.select('body').selectAll('#studentchart')
                .append('svg')
                .attr('width', width + margins.left + margins.right)
                .attr('height', height + margins.top + margins.bottom)
                .append('g')
                .attr('transform', 'translate(' + margins.left + ',' + margins.top + ')'),
            xMax = d3.max(dataset, function (group) {
                return d3.max(group, function (d) {
                    return d.x + d.x0;
                });
            }),
            xScale = d3.scale.linear()
                .domain([0, xMax])
                .range([0, width]),
            students = dataset[0].map(function (d) {
                return d.y;
            }),
            _ = console.log(students),
            yScale = d3.scale.ordinal()
                .domain(students)
                .rangeRoundBands([0, height], .1),
            xAxis = d3.svg.axis().scale(xScale).orient('bottom'),
            yAxis = d3.svg.axis().scale(yScale).orient('left'),
            colors = ['#009DD9','#00CC66','#CCCC33'],//d3.scale.category10(),
            groups = svg.selectAll('g')
                .data(dataset)
                .enter()
                .append('g')
                .style('fill', function (d, i) {
                return colors[i];
            }),
            rects = groups.selectAll('rect')
                .data(function (d) {
                return d;
            })
                .enter()
                .append('rect')
                .attr('x', function (d) {
                return xScale(d.x0);
            })
                .attr('y', function (d, i) {
                return yScale(d.y);
            })
                .attr('height', function (d) {
                return yScale.rangeBand()-4;
            })
                .attr('width', function (d) {
                return xScale(d.x);
            })
                .on('mouseover', function (d) {
                var xPos = parseFloat(d3.select(this).attr('x'));/// 2 + width / 2;
                var yPos = parseFloat(d3.select(this).attr('y'));// + yScale.rangeBand() / 2;

                d3.select('#dash-chart-tooltip')
                    .style('left', xPos + margins.left + 'px')
                    .style('top', yPos + margins.top + 'px')
                    .select('#value')
                    .text(d.x);

                d3.select('#dash-chart-tooltip').attr('hidden', null);
            })
                .on('mouseout', function () {
                d3.select('#dash-chart-tooltip').attr('hidden', true);
            })
            /*svg.append('g')
                .attr('class', 'axis')
                .attr('transform', 'translate(0,' + height + ')')
                .call(xAxis);*/
        svg.append('g')
            .attr('class', 'axis')
            .call(yAxis);
        svg.selectAll("text")
    .filter(function(d){ return typeof(d) == "string"; })
    .style("cursor", "pointer")
    .style("text-decoration","underline")
    .on("click", function(d){
        document.location.href = "studentreport?id=" + d;
    });
    }

    function exerciseAttempts(data) {
        var margin = {top: 20, right: 20, bottom: 30, left: 40},
    width = 500 - margin.left - margin.right,
    height = 150 - margin.top - margin.bottom;

var x = d3.scale.ordinal()
    .rangeRoundBands([0, width], .1);

var y = d3.scale.linear()
    .range([height, 0]);

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom");

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")
    .ticks(10);

var svg = d3.select("#chart-exercise-attempts").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
console.log(data);


x.domain(data.map(function(d) { return d.attempts; }));
  y.domain([0, d3.max(data, function(d) { return d.frequency; })]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)
    .append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("# Students");

  svg.selectAll(".bar")
      .data(data)
    .enter().append("rect")
      .attr("class", "bar")
      .attr("x", function(d) { return x(d.attempts); })
      .attr("width", x.rangeBand())
      .attr("y", function(d) { return y(d.frequency); })
      .attr("height", function(d) { return height - y(d.frequency); });

function type(d) {
  d.frequency = +d.frequency;
  return d;
}

    }

    function donutChart(data, chartId){
        var width = 100,
            height = 100,
            radius = Math.min(width, height) / 2;

        var color = d3.scale.ordinal()
            .range(["#CCCCCC","#CC3300", "#CCCC33", "#00CC66"]);

        var arc = d3.svg.arc()
            .outerRadius(radius - 5)
            .innerRadius(radius - 25);

        var pie = d3.layout.pie()
            .sort(null)
            .value(function(d) { return d.count; });

        var svg = d3.select(chartId).append("svg")
            .attr("width", width)
            .attr("height", height)
          .append("g")
            .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");

        var g = svg.selectAll(".arc")
            .data(pie(data))
            .enter().append("g")
              .attr("class", "arc");

        g.append("path")
            .attr("d", arc)
            .style("fill", function(d) { return color(d.data.type); })
            .on('mouseover', function (d) {
                var xPos = parseFloat(d3.select(this).attr('x'));/// 2 + width / 2;
                var yPos = parseFloat(d3.select(this).attr('y'));// + yScale.rangeBand() / 2;
console.log(d);
                d3.select('#dash-chart-tooltip')
                    .style('left', xPos + 'px')
                    .style('top', yPos + 'px')
                    .select('#value')
                    .text(d.value);
                });

        g.append("text")
            .attr("transform", function(d) { return "translate(" + arc.centroid(d) + ")"; })
            .attr("dy", ".35em")
            .text(function(d) { if (d.data.count == 0) { return "" } else { return d.data.count; } });

        function type(d) {
          d.count = +d.count;
          return d;
        }

    }
}

