
$(function(){

    const root = "https://blockchain.info/";
    var input_address = $('#address').text();
    var form = $('#checkoutForm');

    function checkBalance() {
        $.ajax({
            type: "GET",
            url: root + 'q/getreceivedbyaddress/'+input_address, 
            data : {format : 'plain'},
            success: function(response) {

                if (!response) return;

                var value = parseInt(response);
                if (value > 0) {
                    $('.stage-ready').hide();
                    $('.stage-paid').removeClass('hidden').html($('.stage-paid').html().replace('[[value]]', value / 100000000));
                    form.submit();
                } else {
                    setTimeout(checkBalance, 5000);
                }
            }
        });
    }

    try {
        ws = new WebSocket('wss://ws.blockchain.info/inv');

        if (!ws) return;

        ws.onmessage = function(e) {
            try {
                var obj = $.parseJSON(e.data);

                if (obj.op == 'utx') {
                    var tx = obj.x;
                    var result = 0;
                    for (var i = 0; i < tx.out.length; i++) {
                        var output = tx.out[i];
                        if (output.addr == input_address) {
                            result += parseInt(output.value);
                        }
                    }
                }

                $('.stage-ready').hide();
                $('.stage-paid').removeClass('hidden').html($('.stage-paid').html().replace('[[value]]', value / 100000000));
                form.submit();
                ws.close();
            } catch(e) {
                console.log(e);
            }
        };

        ws.onopen = function() {
            ws.send('{"op":"addr_sub", "addr":"'+ input_address +'"}');
        };
    } catch (e) {
        console.log(e);
    }
    setTimeout(checkBalance, 5000); 

    //............................................................//
    //This part is intented for copying BTC amount and BTC address//
    //............................................................//
    $('.tobecopied').tooltip({trigger: 'manual'});
    var clipboard = new ClipboardJS('.tobecopied');
    clipboard.on('success', function(e) {
        var tt = $(e.trigger);
        tt.tooltip('show');
        setTimeout(function(){
          tt.tooltip( 'hide' );
        }, 2000); 
    });
    clipboard.on('error', function(e) {
        console.log(e);
    });
});
