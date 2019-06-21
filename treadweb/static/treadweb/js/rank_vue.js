function setVideo(count, video_id) {
    var video_cmp = {
        template: '<iframe width="500" height="281" src="https://www.youtube.com/embed/'+video_id
            +'" frameborder="0" allow="accelerometer; encrypted-media; gyroscope; picture-in-picture" allowfullscreen>' +
            '</iframe>'
    }

    new Vue({
        delimiters: ['${', '}'],
       el: '#video'+count,
        data: {
           isSet: true,
        },
        components: {
           'video-component': video_cmp
        },
        methods: {
           setting: function() {
               this.isSet = !this.isSet;
           }
        }
    });
}