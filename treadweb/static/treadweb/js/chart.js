var line_chart = c3.generate({
    bindto: '#line-chart',
    padding: {
        top: 30,
        bottom: 30,
        left: 100,
        right: 100
    },
    data: {
        columns: line_data
    }
});