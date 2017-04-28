#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


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
    productos = parameters.get("Productos")  #Cambiar por entity a recibir
    marca = parameters.get("Marca")
    gama = parameters.get("gama")

    #cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}
    
    if productos and marca and gama:
        speech = "The cost of shipping to " #+ productos + " is http://img.bbystatic.com/BestBuy_US/store/ee/2017/com/pr/SOL-11169-LenovoUpdate/lenovo_section4-img.png" #+ str(cost[zone]) + " euros."
    else:
        return {}

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        "data": {
            "facebook":{ #{[
                #{
                #    "text":"Pick a color:"
                #}
                #{
                #    "attachment": {
                #        "type": "image",
                #         "payload": {
                #             "url": "https://www.testclan.com/images/testbot/siege/weapons/assault-rifles.jpg"
                #         }
                #    }
                #}
            #]}
            "attachment":{
              "type":"template",
              "payload":{
                "template_type":"generic",
                "elements":[
                   {
                    "title":"Welcome to Peter\'s Hats",
                    "image_url":"https://www.testclan.com/images/testbot/siege/weapons/assault-rifles.jpg",
                    "subtitle":"We\'ve got the right hat for everyone.",
                    "default_action": {
                      "type": "web_url",
                      "url": "https://peterssendreceiveapp.ngrok.io/view?item=103",
                      "messenger_extensions": true,
                      "webview_height_ratio": "tall",
                      "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                    },
                    "buttons":[
                      {
                        "type":"web_url",
                        "url":"https://petersfancybrownhats.com",
                        "title":"View Website"
                      },{
                        "type":"postback",
                        "title":"Start Chatting",
                        "payload":"DEVELOPER_DEFINED_PAYLOAD"
                      }              
                    ]      
                  }
                ]
              }
            }
          }  
        },
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=True, port=port, host='0.0.0.0')
