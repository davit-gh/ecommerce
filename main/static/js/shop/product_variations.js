;(function($){
    $(function() {
    
        var selections = $('select');
    
        var showImage = function(id) {
            var thumb = $(id);
            thumb.click();
        };
    
        // on selection of an option, reduce the list of variations to the one
        // matching all the selected options - if there is one, show it and hide
        // the others
        selections.change(function() {
            var variation = $.grep(variations, function(v) {
                var valid = true;
                $.each(selections, function() {
                    valid = valid && v[this.name] == this[this.selectedIndex].value;
                });
                return valid;
            });
            if (variation.length == 1) {
                $('#variations li').hide();
                $('#variation-' + variation[0].sku).show();
                showImage('#image-' + variation[0].image_id);

            }
        });
        selections.change();
    
    });
})(jQuery);