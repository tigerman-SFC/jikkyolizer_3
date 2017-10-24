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



voice_ajax = new Vue({
	el:'.jikkyo',
	data:{
		during:0,
		rest:0,
		this_voice:'test-4.wav',
		next_voice:'jikkyo_0.wav',
		outer_voice:'/voices/test-4.wav'
	},
	methods:{
		go_to_next_voice:function(){
			last_voice = this.this_voice;
			this.this_voice=this.next_voice;
			var params = new URLSearchParams();
			params.append('used_voice', last_voice);
			this.outer_voice = '/voices/' + this.this_voice;
			start_new_voice();
			//alert(last_voice);
			/*
			axios.post('/jikkyolizer/jikkyo_sox/new_voice/',params)
			.then(res=>{
				console.log(res);
				console.log('OK');
				alert(res.data);
			})
			.catch(function (error){
				console.log('NG');
			});
			*/
		}
	}
})

}


