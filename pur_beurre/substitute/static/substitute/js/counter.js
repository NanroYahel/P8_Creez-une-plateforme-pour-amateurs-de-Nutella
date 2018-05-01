$(document).ready(function() {

	//Function to restart at the main page after connexion of the user
	setInterval(function(){
		var counter = Number($('#counter').text());

		if (counter > 0){
			counter = counter - 1;
			$('#counter').text(counter);
		} else {
			var url = "/";
			document.location.href = url;
		};

	},1000);


});