const currentLocation = location;
const getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const movieDetailApp = new Vue({
    el:'#movie_detail_app',
    delimiters: ['${','}'],
    data: {
        comments:[],
        api_url:'http://127.0.0.1:8000/api/v1/',
        current_path:currentLocation.pathname,
        user_content:'',
        user_score:null,
    },
    created: function(){
        this.loadComments();
    },
    methods:{
        loadComments: async function() {
            const comment_url = this.api_url + `movies/${this.movie_id}/comments/`;
            const res = await fetch(comment_url, {method:'GET'});
            const parsed = await res.json();
            console.log(parsed);
            this.comments = parsed;
        },
        postComment:async function(){
            let csrftoken = getCookie('csrftoken');
            // const headers = new Headers();
            // headers.append('X-CSRFToken', csrftoken);
            const comment_url = this.api_url + `movies/${this.movie_id}/comments/`;
            const data = {
                'content':this.user_content,
                'score':this.user_score,
                'movie':this.movie_id,
            };

            const res = await fetch(comment_url, {
                method:'POST',
                headers:{
                    'Content-Type':'application/json',
                    'X-CSRFToken': csrftoken,
                },
                credentials:'same-origin',
                body:JSON.stringify(data),
            });

            if (res.status === 200) {
                this.loadComments();
            }
        }
    },
    computed:{
        movie_id:function(){
            this.comments=[];
            return this.current_path.slice(8,16);
        }
    }

})