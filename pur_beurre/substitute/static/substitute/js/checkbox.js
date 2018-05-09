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
	$form.on('submit', function(e){
		e.preventDefault();
		if ($('form input:checkbox').is(':checked')){
			var prod_id;
			prod_id = $('input:checkbox', this).attr("value");
			$.ajax({
				url:$(this).attr('action'),
				data:{product_id:prod_id},
				success: function(data){
					$('#'+prod_id).html(data);
				},
			})
			$(this).hide();
		} else{
			alert("Veuillez cocher la case pour enregistrer le produit.");
			e.preventDefault();
		}
	});
});
