const profile_app = new Vue({
    delimiters: ['${','}'],
    el: '#profile_app',
    data:{
        movies_check:false,
        people_check:false,
        followings_check:false,
    },
    watch:{
        movies_check:function(val){
            if(val){
                this.people_check = false;
                this.followings_check = false;
            }
        },
        people_check:function(val){
            if(val){
                this.movies_check = false;
                this.followings_check = false;
            }
        },
        followings_check:function(val){
            if(val){
                this.movies_check = false;
                this.people_check = false;
            }
        },
    },
    methods:{
        toggle1:function(){
            this.movies_check = true;
        },
        toggle2:function(){
            this.people_check = true;
        },
        toggle3:function(){
            this.followings_check = true;
        }
    }


})