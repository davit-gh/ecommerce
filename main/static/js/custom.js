$(function() {

    $('#more>a').click(function(e){
      var nextpage = $(this).data("next-page");
      var num_shown = $('#num_shown').text();
      $.get("",{"page": nextpage},function(resp){
        var parser = new DOMParser();
        var doc = parser.parseFromString(resp, 'text/html');
        // We append the loaded products to the div of current products
        var loaded_products = doc.getElementById('products-div').innerHTML
        $('#products-div').append(loaded_products);
        // We replace 'Load more' button in case we reached the last pagination 
        // page and the button is disabled in loaded page
        var moreBtn= doc.getElementById('more').innerHTML;
        $('#more').html(moreBtn);
        // We change the number of shown products by adding the number
        // of loaded products
        var next_num_shown = doc.getElementById('num_shown').textContent
        $('#num_shown').text(parseInt(num_shown) + parseInt(next_num_shown))
      });
      e.preventDefault();
    });

    var sameShipping = $('#id_same_billing_shipping');
    var shipping_fields = $("[id^='id_shipping_detail']");
    // show/hide shipping fields on change of "same as" checkbox and call on load
    sameShipping.change(function() {
        
        if (sameShipping.prop('checked')){
          $('#shipping_fields').hide();  
          shipping_fields.removeAttr('required');
        } else {
          $('#shipping_fields').show();  
          shipping_fields.attr('required', 'required');
        }
    }).change();

    //clears option checkboxes in shop.includes.left_sidebar.html template
    $(".clear-btn").click(function(e){
      $(e.target).parents('.panel').find("input:checkbox").removeAttr('checked');
      return false;
    });
});