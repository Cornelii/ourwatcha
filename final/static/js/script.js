const sess_storage_check = sessionStorage

const nav_app = new Vue({
    delimiters:['${','}'],
    el:'#nav-app',
    data:{
        base_url:location.origin+'/api/v1/movies/',
        user_search_input:'',
        movies:'',
        target_movies:[],
        origin_loc:location.origin,
        search_flag: true,
        loading_full:false,
        storage: sess_storage_check,
    },
    methods:{
        searching:async function(){
            if(this.search_flag) {
                const res = await axios.get(this.base_url);
                this.movies = res.data;
                this.storage.setItem('movies', JSON.stringify(res.data));
                this.search_flag = false;
            }

        },
        movie_url:function(movie_id){
            const url = `${this.origin_loc}/movies/${movie_id}/`;
            console.log(url);
            return `${this.origin_loc}/movies/${movie_id}/`
        }
    },
    // mounted: async function(){
    //         const res = await axios.get(this.base_url);
    //         console.log(res.data);
    //         this.movies=res.data;
    //     },
    watch:{
        user_search_input:function(){
            this.target_movies=[];
            if (this.user_search_input) {
                for (movie of this.movies) {
                    if (movie.title.includes(this.user_search_input)) {
                        this.target_movies.push(movie);
                    }
                }
            }
        }
    },
    beforeMount:function(){
        try {
            if (this.storage.getItem('movies')){
                this.search_flag = false;
                this.movies = JSON.parse(this.storage.getItem('movies'));
            }
        }catch{}
    }
}

)