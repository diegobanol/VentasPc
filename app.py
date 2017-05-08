#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

def createButtons(text, option1, option2, option3 ):
    data = {}
    button = {}
    facebook ={}
    card = {}
    payload = {}
    attachment = {}
    end = {}
    elements =[]
    button['boton1'] = {"type": "postback", "title": option1, "payload": option1}
    button['boton2'] = {"type": "postback", "title": option2, "payload": option2}
    button['boton3'] = {"type": "postback", "title": option3, "payload": option3}
    buttons= [button['boton1'], button['boton2'], button['boton3']]
    payload = {"template_type": "button", "text": text, "buttons" : buttons}
    attachment = {"type" : "template", "payload" : payload}
    facebook["attachment"] = attachment
    data["facebook"] = facebook
    end = {"speech": "Barack Hussein Obama", "displayText": "Barack Hussein Obama","data" : data}

    return end

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "asesorDeVentas": #Cambiar por action en el intent
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    productos = parameters.get("Productos")
    marca = parameters.get("Marca")
    gama = parameters.get("gama")
    if not productos:
        end = createButtons("En que clase de producto esta interesado?", "portatiles", "celulares", "tablets" )
    elif not marca:
        end = createButtons("Cual marca le llama la atencion", "lenovo", "asus", "samsung" )
    elif not gama:
        end = createButtons("De cual gama quiere su producto", "baja", "media", "alta" )
    elif productos and marca and gama:
        data = {}
        button = {}
        facebook ={}
        card = {}
        payload = {}
        attachment = {}
        end = {}
        elements =[]

        for x in range(0, 4):
            button['boton1'] = {"type": "web_url","url": "http://articulo.mercadolibre.com.co/MCO-438399752-portatil-lenovo-ideapad-510-core-i7-4gb-1tb-video-2gb-w10-_JM","title": "Ver Producto"}
            button['boton2'] = {"type": "postback", "title": "Hola", "payload": "Hola" }
            buttons= [button['boton1'], button['boton2']]
            card[x] = {"title": "Portatil Lenovo Ideapad 510 Core I7 4gb 1tb Video 2gb W10 ", "subtitle": "2.459.900", "image_url": "https://http2.mlstatic.com/portatil-lenovo-ideapad-510-core-i7-4gb-1tb-video-2gb-w10-D_NQ_NP_395915-MCO25330287897_022017-O.webp", "buttons": buttons}
            #elements = [card['carta1']]
            elements.append(card[x])
        payload = {"template_type": "generic", "elements" : elements}
        attachment = {"type" : "template", "payload" : payload}
        facebook["attachment"] = attachment
        data["facebook"] = facebook
        end = {"data" : data, "source" : "apiai-onlinestore-shipping"}
        #return end

        # return {"data": {
        #     "facebook": {
        #     "attachment": {
        #     "type": "template",
        #     "payload": {
        #     "template_type": "button",
        #     "text": "Are you looking for something to watch, or do you want to see more options? Type or tap below.",
        #     "buttons": [
        #     {
        #     "type": "postback",
        #     "title": "On Now",
        #     "payload": "On Now"
        #     },
        #     {
        #     "type": "postback",
        #     "title": "On Later",
        #     "payload": "On Later"
        #     },
        #     {
        #     "type": "postback",
        #     "title": "More Options",
        #     "payload": "More Options"
        #     }
        #     ]
        #     }
        #     }
        #     }}}
        # button['boton1'] = {"type": "postback", "title": "portatiles", "payload": "portatiles"}
        # button['boton2'] = {"type": "postback", "title": "celulares", "payload": "celulares" }
        # button['boton3'] = {"type": "postback", "title": "camaras", "payload": "camaras" }
        # buttons= [button['boton1'], button['boton2'], button['boton3']]
        # #card['carta1'] = {"title": "Cual producto quiere?", "buttons": buttons}
        # #elements = [card['carta1']]
        # payload = {"template_type": "button", "text": "Are you looking for.", "buttons": buttons}
        # attachment = {"type" : "template", "payload" : payload}
        # facebook["attachment"] = attachment
        # data["facebook"] = facebook
        # end = {"data" : data}

    return end

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')




        #speech = "The cost of shipping to " #+ productos + " is http://img.bbystatic.com/BestBuy_US/store/ee/2017/com/pr/SOL-11169-LenovoUpdate/lenovo_section4-img.png" #+ str(cost[zone]) + " euros."
        # return {
        #     #"speech": speech,
        #     #"displayText": speech,
        #     "data": {
        #         "facebook":{
    	# 	  "attachment": {
    	# 	    "type": "template",
    	# 	    "payload": {
    	# 	      "template_type": "generic",
    	# 	      "elements": [
    	# 		{
    	# 		  "title": "Rainbow Six Siege",
    	# 		  "subtitle": "Blitz Guide",
    	# 		  "image_url": "http://img.youtube.com/vi/36q5NnL3uSM/0.jpg",
    	# 		  "buttons": [
    	# 		    {
    	# 		      "type": "web_url",
    	# 		      "url": "https://www.youtube.com/watch?v=36q5NnL3uSM",
    	# 		      "title": "Watch video"
    	# 		    },
    	# 		    {
    	# 		      "type": "postback",
        #           		      "title": "Hola",
        #           		      "payload": "Hola"
    	# 		    }
    	# 		  ]
    	# 		}]
    	# 	    }
    	# 	  }
        #        }
        #     },
        #     # "contextOut": [],
        #     "source": "apiai-onlinestore-shipping"
        # }
