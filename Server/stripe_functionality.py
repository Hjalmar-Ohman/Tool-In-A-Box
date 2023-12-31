from flask import Flask, jsonify, abort, request, redirect
import stripe


SECRET_STRIPE_KEY = "sk_test_51MqGmBBclQZfILgurtsdH1mAsihvmHs51eWmFzBNoqGKE4dGYOPLSQ7BTcKrr9Idy4Mg28Lj8snGjuPpC1oDlMoR00mxgzAKTG"
PUBLIC_STRIPE_KEY = "pk_test_51MqGmBBclQZfILguPT3YglTQxsjnR9gUMF7SgTvW6x0gI8igELaA4c98TwuRZW8Jc6PfdBlsT8LkO3JQzD9vuVj900JUCerBUb"

stripe.api_key = SECRET_STRIPE_KEY


def process_payment(price, quantity, day, week, start_h, finnish_h, tool_id, user):
   
    success = False
    if request.method == "POST":
        data = request.get_json()
    try:
        session = stripe.checkout.Session.create(
         
         customer_email = user.email,
         line_items=[{
           
      'price_data': {
        'currency': 'sek',
        
        'product_data': {
          'name': 'Bokning'
        },
        'unit_amount': price,
      },
      'quantity': quantity,
    
    }],
    
    metadata = {'user_id': user.id, 'day': day, 'week': week, 'start_h': start_h, 'finnish_h': finnish_h, 'tool_id' : tool_id},
    mode='payment',
    success_url='http://localhost:5000',
    cancel_url='http://localhost:5000',
    )
        print(session['id'])

 

    except Exception as e:
        return str(e)

    return jsonify({"session_id": session["id"]})

