const currentLocation = location;
const movieDetailApp = new Vue({
    el:'#movie_detail_app',
    delimiter: ['${','}'],
    data: {
        comments:[],
        api_url:'http://127.0.0.1:8000/api/v1/',
        current_path:currentLocation.pathname,
    },
    methods:{

    },
    created: async function(){
        const comment_url = this.api_url + `movies/${this.movie_id}/comments/`;
        console.log(comment_url);
        const res = await fetch(comment_url, {method:'GET'});
        console.log(res.data);
        this.comments = res.data;
    },
    computed:{
        movie_id:function(){
            return this.current_path.slice(8,16);
        }
    }

})