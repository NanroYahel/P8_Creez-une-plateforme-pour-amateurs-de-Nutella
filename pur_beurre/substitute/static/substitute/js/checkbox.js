//--------------------------------------------------------------------------------------------
//Functions added to resolve the problem of non post csrf token when doing ajax post

function getCookie(name) {
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                return decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
}

$.ajaxSetup({
    // Function called befor an ajax request
    beforeSend: function(xhr, settings) {
         // add the header only for the actual website
         // relative URL
         if (!/^https?:.*/.test(settings.url)  && settings.type == "POST") {
             // add the token in the header
             xhr.setRequestHeader("X-CSRFToken",  getCookie('csrftoken'));
         }
     }
});

//-------------------------------------------------------------------------------------------


$(document).ready(function() {

	var $form = $('form');
	//Function to save favorites in ajax 
	//Save the product and display a message instead of the button.
	$form.on('submit', function(e){
		//Prevent action of button
		e.preventDefault();
		var prod_id;
		prod_id = $('input:submit', this).attr("id");

		//Call the view "add_favorite" and return a message instead of the button
		$.ajax({
			url:$(this).attr('action'),
			data:{product_id:prod_id},
			success: function(data){
				$('#'+prod_id).html(data);
			},
		})
		$(this).hide();
	});
});
