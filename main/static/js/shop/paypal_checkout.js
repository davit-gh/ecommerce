var paypalBtnRender;
(paypalBtnRender = function(pci, pmt){    
    // Render the PayPal button
    paypal.Button.render({
        // Set your environment
        env: 'sandbox', // sandbox | production

        // Specify the style of the button
        style: {
          layout: 'vertical',  // horizontal | vertical
          size:   'medium',    // medium | large | responsive
          shape:  'rect',      // pill | rect
          color:  'gold'       // gold | blue | silver | white | black
        },

        funding: {
          allowed: [
            paypal.FUNDING.CARD,
            paypal.FUNDING.CREDIT
          ],
          disallowed: []
        },

        // PayPal Client IDs - replace with your own
        // Create a PayPal app: https://developer.paypal.com/developer/applications/create
        client: {
          sandbox: pci,
          production: '<insert production client id>'
        },

        payment: function (data, actions) {
          return actions.payment.create({
            payment: pmt
          });
        },

        onAuthorize: function (data, actions) {
          return actions.payment.execute()
            .then(function () {
              $.get('/main/paypal_success/', function(resp){
                make_changes(resp);
                window.scrollTo(0,0);
              })
            });
        }
        },
        '#paypal-button-container'
    );
})(paypal_client_id, payment)