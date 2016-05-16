function showAnswer(target, answer, scale) {
    var w = 175 * scale, //width
        h = 175 * scale; //height

    var vis = d3.select(target);

    vis.selectAll("#chart")
        .append("text")
        .text(answer + "%")
        .attr("x", -w)
        .attr("y", -h + 12);
}

function drawChart(target, data, rotate, scale, type) //types: "outerRadius", "exploded", "square", "ellipse"
{
    var w = 354 * scale, //width
        h = 354 * scale, //height
        outer = [155 * scale, 175 * scale], //radius
        pad = 2 * scale, //svg padding
        blue = "#1f78b4",
        gray = "#dddddd",
        darkGray = "#888888"
        ;

    var vis = d3.select(target)
        .data([data])
        .attr("width", w + 2 * pad)
        .attr("height", h + 2 * pad)
        .append("g")
        .attr("transform", "translate(" + (w / 2 + pad) + "," + (h / 2 + pad) + ")")
        .attr("id", "chart");

    var defs = vis.append("defs").attr("id", "clip");

    var pieData = d3.layout.pie()
        .value(function(d) {
            return d.value;
        });

    var background = vis.append("rect")
        .attr("width", 2 * w / 2 + pad)
        .attr("height", 2 * h / 2 + pad)
        .attr("fill", "#ffffff")
        .attr("transform", "translate(" + (-w / 2 - pad) + "," + (-h / 2 - pad) + ")");

    var arc = d3.svg.arc().innerRadius(0);
    var pie = vis.append("g");
    var pieSpin = pie.append("g").attr("transform", "rotate(" + rotate + ")");
    var arcs = pieSpin.selectAll("g.slice")
        .data(pieData)
        .enter()
        .append("g")
        .attr("class", "slice")
        ;
    // var arcGroups = arcs.append("g");

    // explode function from http://stackoverflow.com/questions/27089388/exploded-pie-chart-on-click-with-d3-js
    var explode = function(x) {
        var offset = 20;
        var angle = (x.startAngle + x.endAngle) / 2;
        var xOff = Math.sin(angle)*offset;
        var yOff = -Math.cos(angle)*offset;
        return "translate("+xOff+","+yOff+")";
      }

    // -------------------------- Draw Chart --------------------------
    if (type == "outerRadius")
    {
        arc.outerRadius(function(d) {
            if (d.data.focus)
                return outer[1];
            else
                return outer[0];
        });
    }
    
    if (type == "exploded")
    {
        arc.outerRadius(outer[0]);

        arcs.attr("transform", explode);
    }

    if (type == "square")
    {
        arc.outerRadius(outer[1]);

        var boundary = defs.append("clipPath")
        .attr("id", "boundary");

        boundary.append("rect")
            .attr("x", -outer[1]/2)
            .attr("y", -outer[1]/2)
            .attr("width", outer[1])
            .attr("height", outer[1])
            .attr("fill", "#000000");
    
        pie.attr("clip-path", "url(#boundary)");
    }

    if (type == "ellipse")
    {
        arc.outerRadius(outer[1]);

        var boundary = defs.append("clipPath")
        .attr("id", "boundary");

        boundary.append("ellipse")
            .attr("cx", 0)
            .attr("cy", 0)
            .attr("rx", outer[1]/2)
            .attr("ry", outer[1])
            .attr("fill", "#000000")
            ;
    
        pie.attr("clip-path", "url(#boundary)");
    }

    if (type == "pie")
    {
        arc.outerRadius(outer[0]);
    }

    arcs.append("path")
        .attr("d", arc)
    .attr("fill", function(d) {
        if (d.data.focus)
            return blue;
        else
            return gray;
    })
    // .attr("stroke-width", 20)
    // .attr("stroke", "#FFFFFF")
    ;

}

function makeData(count, dataOptions) {
    var data = [{
        "focus": true,
        "value": dataOptions[count]
    }, {
        "focus": false,
        "value": 100 - dataOptions[count]
    }]

    return data;
}