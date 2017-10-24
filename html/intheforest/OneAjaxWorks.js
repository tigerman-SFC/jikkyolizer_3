function receive_data(data_id){
	document.getElementById("test_js").innerHTML=data_id;
}

window.onload = function() {		
new Vue({
	el: '.my-ajax',
	data:{
		seen_91:true,
		seen_94:true
	},
	methods:{
		delete_history: function(){
			this.seen_91=false
		}
	}
})
}
