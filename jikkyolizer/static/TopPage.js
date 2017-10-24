outer_seen_past=[];

function receive_data(seen_past_outer){
	document.getElementById("test_js").innerHTML=seen_past_outer;
}


//window.onload = function() {		

function init_past(){
//qs = require('qs');
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

past_data = new Vue({
	el: '.my-ajax',
	data:{
		changing:0,
		seen_past:outer_seen_past
	},
	methods:{
		delete_history: function(past_id){
			this.seen_past[past_id]=false;
			//false_past_data(past_id)
			//outer=this.seen_past+string(this.changing)
			//receive_data(this.seen_past)
			this.changing++;
			//var csrftoken = Cookies.get('csrftoken');
			//csrftoken=document.querySelector('#main > form:nth-child(9) > input[type="hidden"]:nth-child(3)').getAttribute('value');//this works
			//receive_data(csrftoken)
			//axios.post('/TransportationUser/Delete/', qs.stringify({'deleting_id': past_id}))
			var params = new URLSearchParams();
			params.append('deleting_id', past_id);
			axios.post('/TransportationUser/Delete/', params)
			.then(res=> {
				console.log(res);
				console.log('OK');
				//alert(res.data['delet_id']);
				})
			.catch(function (error) {
				console.log('NG');
			});
			
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

