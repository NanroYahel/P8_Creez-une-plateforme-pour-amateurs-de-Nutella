$(document).ready(function() {

	var $form = $('form');
	$form.on('submit', function(e){
		if ($('form input:checkbox').is(':checked')){
			$('<p class="product-added"> Le produit a bien été enregistré.</p>').insertBefore(this)
			$(this).remove()
		} else{
			alert("Veuillez cocher la case pour enregistrer le produit.");
			e.preventDefault();
		}
	});
});