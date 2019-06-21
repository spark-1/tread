function search_keyword(keyword) {
    if(typeof keyword == 'undefined') {
        keyword = document.getElementById('keyword_text').value
    }
    var WCExist = false;
    axios.get('/tread/search/'+keyword)
        .then(function (response) {
            var lineData = response.data.line_result;
            var regionData = response.data.region_result;
            var genderData = response.data.gender_result;
            console.log(response);
            if(response.data.WC_exists == 'yes')
                WCExist = true;
            else
                WCExist = false;

            var lineComponent = {
                template:  '<div id="banner" class="container">' +
                    '<div class="title"><h2>Recent Searches</h2></div>' +
                    '<div id="line-chart"></div></div>'
            }
            var regionComponent = {
                template: '<div id="right-border" class="chart-content">' +
                            '<div class="title"><h2>Trend By Region</h2></div>' +
                            '<div id="region-chart"></div></div>'
            }
            var genderComponent = {
                template: '<div class="chart-content">' +
                            '<div class="title"><h2>남/녀 검색 비율</h2></div>' +
                            '<div id="donut-chart"></div></div>'
            }
            var wordcloudComponent = {
                template:     '<div class="container align-center">' +
                            '<img src="../../static/treadweb/img/wordcloud.png"/></div>'
            }
            new Vue({
                el: '#page-wrapper',
                data: {
                    WC_exist: WCExist
                },
                components: {
                    'line-chart-component': lineComponent,
                    'region-chart-component': regionComponent,
                    'gender-chart-component': genderComponent,
                    'wordcloud-component': wordcloudComponent
                },
            });

            if(typeof lineData !== 'undefined' && lineData.length > 0) {
                var line_chart = c3.generate({
                    bindto: '#line-chart',
                    padding: {
                        top: 30,
                        bottom: 30,
                        left: 100,
                        right: 100
                    },
                    data: {
                        x: 'x',
                        columns: lineData,
                    },
                    axis: {
                        x: {
                            type: 'timeseries',
                            tick: {
                                format: '%Y-%m-%d'
                            }
                        }
                    },
                    interaction: {
                        enabled: false
                    }
                });
            }
            if(typeof regionData !== 'undefined' && regionData.length > 0) {
                var region_chart = c3.generate({
                    bindto: '#region-chart',
                    padding: {
                        top: 30,
                        bottom: 30,
                        left: 100,
                        right: 100
                    },
                    data: {
                        columns: regionData,
                        type: 'pie'
                    },
                    interaction: {
                        enabled: false
                    }
                });
            }

            if(typeof genderData !== 'undefined' && genderData.length > 0) {
                var donut_chart = c3.generate({
                    bindto: '#donut-chart',
                    padding: {
                        top: 30,
                        bottom: 30,
                        left: 50,
                        right: 50
                    },
                    data: {
                        columns: genderData,
                        type: 'donut'
                    },
                    donut: {
                        title: "by gender"
                    },
                    interaction: {
                        enabled: false
                    }
                });
            }
        })
        .catch(function (error) {
            console.log(error);
        });
}

