
Vue.component('my-component', {
    props:['title','text'],
    template: '<div class="col"><div class="card"><img alt="" class="card-img-top img-fluid"><div class="card-body"><div class="card-title">{{title}}</div><div class="card-text">{{text}}</div></div></div></div>',
});

const app = new Vue({
    el: '#movie_app',
    delimiters: ['${', '}'],
    data: {
        hey: 'Hello World',
        img: '',
        title: 'hey',
        text: '',
    },
});