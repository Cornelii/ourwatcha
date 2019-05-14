const app = new Vue({
    el: '#app',
    delimiters: ['${', '}'],
    data: {},
    methods:{},
});


const cardHtml = function(title, context, img_url){
    const card_html = `<div class="col col-sm-4 col-lg-2"><div class="card"><img src="${img_url}" alt="" class="card-img-top img-fluid"><div class="card-body"><div class="card-title">${title}</div><div class="card-text">${context}</div></div></div></div>`;
    return card_html
}

