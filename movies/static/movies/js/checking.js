// <i class="fas fa-star-half-alt"></i>
// <i class="fas fa-star"></i>
// <i class="far fa-star"></i>
const stars = `
        <fieldset class="rating">
        <input type="radio" @mouseenter="starclick" id="star5" name="rating" value="5" /><label class = "full" for="star5" title="Awesome - 5 stars"></label>
        <input type="radio" id="star4half" name="rating" value="4 and a half" /><label class="half" for="star4half" title="Pretty good - 4.5 stars"></label>
        <input type="radio" id="star4" name="rating" value="4" /><label class = "full" for="star4" title="Pretty good - 4 stars"></label>
        <input type="radio" id="star3half" name="rating" value="3 and a half" /><label class="half" for="star3half" title="Meh - 3.5 stars"></label>
        <input type="radio" id="star3" name="rating" value="3" /><label class = "full" for="star3" title="Meh - 3 stars"></label>
        <input type="radio" id="star2half" name="rating" value="2 and a half" /><label class="half" for="star2half" title="Kinda bad - 2.5 stars"></label>
        <input type="radio" id="star2" name="rating" value="2" /><label class = "full" for="star2" title="Kinda bad - 2 stars"></label>
        <input type="radio" id="star1half" name="rating" value="1 and a half" /><label class="half" for="star1half" title="Meh - 1.5 stars"></label>
        <input type="radio" id="star1" name="rating" value="1" /><label class = "full" for="star1" title="Sucks big time - 1 star"></label>
        <input type="radio" id="starhalf" name="rating" value="half" /><label class="half" for="starhalf" title="Sucks big time - 0.5 stars"></label>
    </fieldset>
    `;


const check_app = new Vue({
    el: '#check_app',
    delimiters: ['${', '}'],
    data: {
        stars:stars,
    },
    methods:{
        choose:function(e){
            const target_tag = e.target;
            const div = document.createElement('div');
            div.id='star';
            div.style.position='absolute';
            div.style.bottom='0';
            div.innerHTML=this.stars;
            target_tag.appendChild(div);
        },
        leave:function(e){
            const target_tag = e.target;
            const remove_target = target_tag.querySelector('#star');
            target_tag.removeChild(remove_target);
        },
        starclick:function(e){
            console.log(e)
        }
    },
})



