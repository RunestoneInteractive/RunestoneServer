var margins = {
    top: 12,
    left: 75,
    right: 24,
    bottom: 24
},
legendPanel = {
    width: 250
},
width = 500 - margins.left - margins.right - legendPanel.width,
    height = (8 * 20) - margins.top - margins.bottom,
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
        }],
        name: 'Sections Read'
    }, {
        data: [{
            student: 'Bob Brown',
            count: 11
        }, {
            student: 'Jack Jackson',
            count: 13
        }, {
            student: 'Macy Millan',
            count: 17
        }, {
            student: 'Sarah Smith',
            count: 9
        }, {
            student: 'Xu Hung',
            count: 4
        }, {
            student: 'Rachel Ru',
            count: 17
        }, {
            student: 'John Hendrick',
            count: 13
        }, {
            student: 'Nick Collans',
            count: 12
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
        }],
        name: 'Exercises Missed'
    }

    ],
    series = dataset.map(function (d) {
        return d.name;
    }),
    dataset = dataset.map(function (d) {
        return d.data.map(function (o, i) {
            // Structure it so that your numeric
            // axis (the stacked amount) is y
            return {
                y: o.count,
                x: o.student
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
        .attr('width', width + margins.left + margins.right + legendPanel.width)
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
    xAxis = d3.svg.axis()
        .scale(xScale)
        .orient('bottom'),
    yAxis = d3.svg.axis()
        .scale(yScale)
        .orient('left'),
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
        return yScale.rangeBand();
    })
        .attr('width', function (d) {
        return xScale(d.x);
    })
        .on('mouseover', function (d) {
        var xPos = parseFloat(d3.select(this).attr('x')) / 2 + width / 2;
        var yPos = parseFloat(d3.select(this).attr('y')) + yScale.rangeBand() / 2;

        d3.select('#tooltip')
            .style('left', xPos + 'px')
            .style('top', yPos + 'px')
            .select('#value')
            .text(d.x);

        d3.select('#tooltip').classed('hidden', false);
    })
        .on('mouseout', function () {
        d3.select('#tooltip').classed('hidden', true);
    })

    /*svg.append('g')
        .attr('class', 'axis')
        .attr('transform', 'translate(0,' + height + ')')
        .call(xAxis);*/

svg.append('g')
    .attr('class', 'axis')
    .call(yAxis);

series.forEach(function (s, i) {
    svg.append('text')
        .attr('fill', 'black')
        .attr('x', width + margins.left + 25)
        .attr('y', i * 25 + 18)
        .text(s);
    svg.append('rect')
        .attr('fill', colors[i])
        .attr('width', 15)
        .attr('height', 15)
        .attr('x', width + margins.left + 5)
        .attr('y', i * 25 + 5);
});