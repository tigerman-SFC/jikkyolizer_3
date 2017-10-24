outer_seen_past=[];

function receive_data(seen_past_outer){
	document.getElementById("test_js").innerHTML=seen_past_outer;
}


//window.onload = function() {		

function init_past(){

past_data = new Vue({
	el: '.my-ajax',
	data:{
		changing:0,
		seen_past:outer_seen_past
	},
	methods:{
		delete_history: function(past_id){
			this.seen_past[past_id]=false
			//false_past_data(past_id)
			//outer=this.seen_past+string(this.changing)
			//receive_data(this.seen_past)
			this.changing++
			/*
			var csrftoken = Cookies.get('csrftoken');
			axios.post('/TransportationUser/Delete/', {
				'Delete': past_id,
			},{
				'X-CSRF-Token': csrftoken,
			})
			.then(function (response) {
				console.log('OK');
				})
			.catch(function (error) {
				console.log('NG');
			});
			*/
		}
	}
})

}

function init_past_data(datum_id){
	outer_seen_past[datum_id]=true;    
}

function false_past_data(datum_id){
	outer_seen_past[datum_id]=false;     
}

// using jQuery
function getCookie(name) {
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
var csrftoken = getCookie('csrftoken');
