var chart = c3.generate({
    bindto: '#main-chart',
    padding: {
        top: 30,
        bottom: 30,
        left: 30,
        right: 30
    },
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 50, 20, 10, 40, 15, 25]
        ]
    }
});