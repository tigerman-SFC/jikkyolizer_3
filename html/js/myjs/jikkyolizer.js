trigger_next_voice = function(){
	//alert('i');
	media = document.getElementsByClassName('jikkyo_voice');
	//alert('a');
	rest_time = media[0].duration - media[0].currentTime;
	//alert(rest_time);
	if (rest_time == 0) { voice_ajax.go_to_next_voice();}
}

function watch_rest_time(){
	//alert('y');
	setInterval(trigger_next_voice,1000);
}

function start_new_voice(){
	media = document.getElementsByClassName('jikkyo_voice');
	media[0].load();
	media[0].play();
}

function init_voice(){

axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
past_voice = ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''];

voice_ajax = new Vue({
	el:'.jikkyo',
	data:{
		during:0,
		rest:0,
		this_voice:'9999998',
		next_voice:'9999999',
		outer_voice:'/voices/jikkyo-9999998.wav'
	},
	methods:{
		go_to_next_voice:function(){
			last_voice = this.this_voice;
			this.this_voice=this.next_voice;
			var params = new URLSearchParams();
			for(i=0;i<24;i++){
				past_voice[i] = past_voice[i+1];
			}
			past_voice[24] = this.this_voice;
			for(i=0;i<25;i++){
				params.append('used_voice'+String(i), past_voice[i]);
			}
			this.outer_voice = '/voices/jikkyo-' + this.this_voice + '.wav';
			start_new_voice();
			console.log(past_voice);
			axios.post('/jikkyolizer/jikkyo_sox/new_voice/',params)
			.then(res=>{
				console.log(res);
				console.log('OK');
				//alert(res.data);
				this.next_voice = res.data;
			})
			.catch(function (error){
				console.log('NG');
			});
		}
	}
})

}


