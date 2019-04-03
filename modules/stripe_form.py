# This is adapted from ``gluons/contrib/stripe.py``, but updated for use with Python 3.
from __future__ import print_function
from hashlib import sha1

import stripe



class StripeForm(object):
    def __init__(self,
                 pk, sk,
                 amount, # in cents
                 description,
                 currency = 'usd',
                 currency_symbol = '$',
                 security_notice = True,
                 disclosure_notice = True,
                 template = None):
        from gluon import current, redirect, URL
        if not (current.request.is_local or current.request.is_https):
            redirect(URL(args=current.request.args,scheme='https'))
        self.pk = pk
        self.sk = sk
        self.amount = amount
        self.description = description
        self.currency = currency
        self.currency_symbol = currency_symbol
        self.security_notice = security_notice
        self.disclosure_notice = disclosure_notice
        self.template = template or TEMPLATE
        self.accepted = None
        self.errors = None
        self.signature = sha1(repr((self.amount, self.description)).encode('utf-8')).hexdigest()

    def process(self):
        from gluon import current
        request = current.request
        if request.post_vars:
            if self.signature == request.post_vars.signature:
                try:
                    self.response = stripe.Charge.create(
                        api_key=self.sk,
                        card=request.post_vars.stripeToken,
                        amount=self.amount,
                        description=self.description,
                        currency=self.currency)
                # See https://stripe.com/docs/api/errors/handling?lang=python. Any errors will cause ``self.errors`` to be True.
                except stripe.error.CardError as e:
                    # Since it's a decline, stripe.error.CardError will be caught.
                    body = e.json_body
                    err = body.get('error', {})
                    self.response = dict(error=err, status=e.http_status)
                except Exception as e:
                    self.response = {'error': {'message': str(e)}}
                else:
                    if self.response.get('paid', False):
                        self.accepted = True
                        return self
            self.errors = True
        return self

    def xml(self):
        from gluon.template import render
        if self.accepted:
            return "Your payment was processed successfully"
        elif self.errors:
            return "There was an processing error"
        else:
            context = dict(amount=self.amount,
                           signature=self.signature, pk=self.pk,
                           currency_symbol=self.currency_symbol,
                           security_notice=self.security_notice,
                           disclosure_notice=self.disclosure_notice)
            return render(content=self.template, context=context)


TEMPLATE = """
<script type="text/javascript" src="https://js.stripe.com/v2/"></script>
<script>
jQuery(function(){
    // This identifies your website in the createToken call below
    Stripe.setPublishableKey('{{=pk}}');

    var stripeResponseHandler = function(status, response) {
      var jQueryform = jQuery('#payment-form');

      if (response.error) {
        // Show the errors on the form
        jQuery('.payment-errors').text(response.error.message).show();
        jQueryform.find('button').prop('disabled', false);
      } else {
        // token contains id, last4, and card type
        var token = response.id;
        // Insert the token into the form so it gets submitted to the server
        var tokenInput = jQuery('<input type="hidden" name="stripeToken" />');
        jQueryform.append(tokenInput.val(token));
        // and re-submit
        jQueryform.get(0).submit();
      }
    };

    jQuery(function(jQuery) {
      jQuery('#payment-form').submit(function(e) {

        var jQueryform = jQuery(this);

        // Disable the submit button to prevent repeated clicks
        jQueryform.find('button').prop('disabled', true);

        Stripe.createToken(jQueryform, stripeResponseHandler);

        // Prevent the form from submitting with the default action
        return false;
      });
    });
});
</script>

<h3>Payment Amount: {{=currency_symbol}} {{="%.2f" % (0.01*amount)}}</h3>
<form action="" method="POST" id="payment-form" class="form-horizontal">

  <div class="form-row form-group">
    <label class="col-sm-2 control-label">Card Number</label>
    <div class="controls col-sm-10">
      <input type="text" size="20" data-stripe="number"
             placeholder="4242424242424242" class="form-control"/>
    </div>
  </div>

  <div class="form-row form-group">
    <label class="col-sm-2 control-label">CVC</label>
    <div class="controls col-sm-10">
      <input type="text" size="4" style="width:80px" data-stripe="cvc"
             placeholder="XXX" class="form-control"/>
      <a href="http://en.wikipedia.org/wiki/Card_Verification_Code" target="_blank">What is this?</a>
    </div>
  </div>

  <div class="form-row form-group">
    <label class="col-sm-2 control-label">Expiration</label>
    <div class="controls col-sm-10">
      <input type="text" size="2" style="width:40px; display:inline-block"
             data-stripe="exp-month" placeholder="MM" class="form-control"/>
      /
      <input type="text" size="4" style="width:80px; display:inline-block"
             data-stripe="exp-year" placeholder="YYYY" class="form-control"/>
    </div>
  </div>

  <div class="form-row form-group">
    <div class="controls col-sm-offset-2 col-sm-10">
      <button type="submit" class="btn btn-primary">Submit Payment</button>
      <div class="payment-errors error hidden"></div>
    </div>
  </div>
  <input type="hidden" name="signature" value="{{=signature}}" />
</form>

{{if security_notice or disclosure_notice:}}
<div class="well">
  {{if security_notice:}}
  <h3>Security Notice</h3>
  <p>For your security we process all payments using a service called <a href="http://stripe.com">Stripe</a>. Thanks to <a href="http://stripe.com">Stripe</a> your credit card information is communicated directly between your Web Browser and the payment processor, <a href="http://stripe.com">Stripe</a>, without going through our server. Since we never see your card information nobody can steal it through us. Stripe is <a href="https://stripe.com/us/help/faq#security-and-pci">PCI compliant</a> and so are we.</p>
  {{pass}}
  {{if disclosure_notice:}}
  <h3>Disclosure Notice</h3>

  <p>We do store other information about your purchase including your name, a description of the purchase, the time when it was processed, and the amount paid. This information is necessary to provide our services and for accounting purposes. We do not disclose this information to third parties unless required to operate our services or accounting purposes.</p>
  {{pass}}
</div>
{{pass}}
"""
