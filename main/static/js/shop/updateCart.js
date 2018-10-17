function updateElementIndex(el, prefix, ndx) {
		var id_regex = new RegExp('(' + prefix + '-\\d+)');
		var replacement = prefix + '-' + ndx;
		if (el.id) el.id = el.id.replace(id_regex, replacement);
		if (el.name) el.name = el.name.replace(id_regex, replacement);
	}

    
function deleteForm(btn, prefix) {
    $(btn).parents('.item').remove();
    var forms = $('.item');
    $('#id_' + prefix + '-TOTAL_FORMS').val(forms.length);
    for (var i=0, formCount=forms.length; i<formCount; i++) {
	    $(forms.get(i)).find('.count-input').children().each(function() {
	        updateElementIndex(this, prefix, i);
	    });
    }
}

function make_changes(resp){
	var parser = new DOMParser();
    var doc = parser.parseFromString(resp, 'text/html');
    var body = doc.getElementById('body');
	$('#body').html(body);
}

function updateCart(remove=false){
	var data = $('#cart-form').serialize() + "&update_cart=1";
	$.post("", data, function(resp){		
		if (remove){
			var del_chb = $('input[type="checkbox"]').filter(':checked');
			deleteForm(del_chb, 'items');
		}
		make_changes(resp);
		paypalBtnRender(paypal_client_id, payment);
	});
};

function removeItem(element, event){
	$(element).prev().prop('checked',true);
	updateCart(true);
    event.preventDefault();
}

$('#cpn-btn').click(function(){
	var f_data = $(this).parents('form').serialize()
	$.post("", f_data, function(resp){
		make_changes(resp);
	});
});
