outer_seen_past=[];

function receive_data(seen_past_outer){
	document.getElementById("test_js").innerHTML=seen_past_outer;
}


//window.onload = function() {		

function init_past(){

past_data = new Vue({
	el: '.my-ajax',
	data:{
		seen_91:true,
		seen_94:true,
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
			outer=this.seen_past+String(this.changing)
			receive_data(outer)
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

function init_past_final(){
	document.getElementById("test_js").innerHTML=outer_seen_past;		
}

