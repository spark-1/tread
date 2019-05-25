var line_chart = c3.generate({
    bindto: '#line-chart',
    padding: {
        top: 30,
        bottom: 30,
        left: 100,
        right: 100
    },
    data: {
        columns: line_data,
    }
});

var bar_chart = c3.generate({
   bindto: '#bar-chart',
   padding: {
        top: 30,
        bottom: 30,
        left: 100,
        right: 100
   },
   data: {
       columns: bar_data,
       type: 'bar'
   },
    bar: {
       width: {
           ratio: 0.7
       }
    }
});

var donut_chart = c3.generate({
   bindto: '#donut-chart',
   padding: {
        top: 30,
        bottom: 30,
        left: 50,
        right: 50
   },
   data: {
       columns: donut_data,
       type: 'donut'
   },
    donut: {
       title: "Search rate by gender"
    }
});