var line_chart = c3.generate({
    bindto: '#line-chart',
    padding: {
        top: 30,
        bottom: 30,
        left: 100,
        right: 100
    },
    data: {
        x:'x',
        columns: line_data,
    },
    axis: {
        x: {
            type: 'timeseries',
            tick: {
                format: '%Y-%m-%d'
            }
        }
    }
});

var region_chart = c3.generate({
   bindto: '#region-chart',
   padding: {
        top: 30,
        bottom: 30,
        left: 100,
        right: 100
   },
   data: {
       columns: region_data,
       type: 'bar'
   },
    bar: {
       width: {
           ratio: 1.0
       }
    }
});

// var region_chart = c3.generate({
//    bindto: '#region-chart',
//    padding: {
//         top: 30,
//         bottom: 30,
//         left: 100,
//         right: 100
//    },
//    data: {
//        x:'x',
//        columns: [region_data[1],]
//    },
//     axis: {
//        x: {
//            type: 'category',
//            categories: region_data[0]
//        }
//     }
// });

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
       title: "by gender"
    }
});