#!/usr/bin/env python

import urllib
import json
import os

import requests

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)

class Response:


    @classmethod
    def doinGetToML(self, uri):
        #DoinGet for the list of objects
        collection=[]
        #uri = "https://api.mercadolibre.com/sites/MCO/search?q=portatil%20asus&price=500000-1000000&limit=9"
        try:
            uResponse = requests.get(uri)
        except requests.ConnectionError:
           return "Connection Errorr"
        Jresponse = uResponse.text
        dataR = json.loads(Jresponse)

        for x in range(0, len(dataR["results"])):
            data = {}
            button={}
            #DoingGet for an object
            item = dataR['results'][x]['id']
            uri2 = "https://api.mercadolibre.com/items/" + item
            try:
                uResponse = requests.get(uri2)
            except requests.ConnectionError:
               return "Connection Error"
            Jresponse = uResponse.text
            dataR2 = json.loads(Jresponse)
            data["image"] = dataR2['pictures'][0]['url']
            data["title"]=dataR["results"][x]["title"]
            data["subtitle"]=dataR['results'][x]['price']
            button['boton1']={"type": "web_url","url": dataR['results'][x]['permalink'],"title": "Ver producto"}
            button['boton2']={"type": "web_url","url": dataR['results'][x]['permalink'],"title": "Ver producto"}
            data["buttons"]=[button['boton1'],button['boton2']]
            #print dataR2['pictures'][0]['url']
            collection.append(data)

        return collection

class Card:

    def __init__(self, collection):
        self.collection = collection


    def createCards(self):
        data = {}
        button = {}
        facebook ={}
        card = {}
        payload = {}
        attachment = {}
        end = {}
        elements =[]
        for x in range(0, len(self.collection)):
            card[x] = {"title": self.collection[x]["title"], "subtitle": self.collection[x]["subtitle"], "image_url": "", "buttons": self.collection[x]["buttons"]}
            elements.append(card[x])
        payload = {"template_type": "generic", "elements" : elements}
        attachment = {"type" : "template", "payload" : payload}
        facebook["attachment"] = attachment
        data["facebook"] = facebook
        end = {"data" : data, "source" : "apiai-onlinestore-shipping"}
        return end

def createButtons(speech, text, option1, option2, option3 ):
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
    end = {"speech": speech, "data" : data}
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
        end = createButtons("En que clase de producto esta interesado?, hay porttiles, celulares, y tablets","En que clase de producto esta interesado?", "portatiles", "celulares", "tablets" )
    elif not marca:
        end = createButtons("Cual marca le llama la atencion? hay lenovo, asus, samsung.","Cual marca le llama la atencion?", "lenovo", "asus", "samsung" )
    elif not gama:
        end = createButtons("De cual gama quiere su producto: baja, media, alta", "De cual gama quiere su producto?", "baja", "media", "alta" )
    elif productos and marca and gama:
        data = {}
        button = {}
        facebook ={}
        card = {}
        payload = {}
        attachment = {}
        end = {}
        elements =[]

        if gama == "baja":
            priceRange = "400000-700000"
        elif gama == "media":
            priceRange = "700001-1500000"
        elif gama == "alta":
            priceRange = "1500001-10500000"

        #Peticion GET para la lista de articulos
        uri = "https://api.mercadolibre.com/sites/MCO/search?q=" + productos + " " + marca + "&price=" + priceRange + "&limit=9"
        resp= Response
        salida = resp.doinGetToML(uri)
        c1 = Card(salida)
        end = c1.createCards()

    return end

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

app.run(debug=True, port=port, host='0.0.0.0')
