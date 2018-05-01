$(document).ready(function() {

	var $form = $('form');
	$form.on('submit', function(e){
		if ($('form input:checkbox').is(':checked')){
			alert('Le produit a bien été enregistré ! ')
		} else{
			alert("Veuillez cocher la case pour enregistrer le produit.");
			e.preventDefault();
		}
	});
});