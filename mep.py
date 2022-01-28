url = 'https://api.telegram.org/bot5163099822:AAFpEAGU7XmxGqNFlyUES9-b7LAc2aLnna8/'
from urllib import response
import requests
import json
from flask import Flask,request,Response
import os

app = Flask(__name__)

def get_all_updates():
    response = requests.get(url+'getUpdates')
    return response.json()

def get_chat_id(update):
    return update['message']['chat']['id']

def get_last_update(allupdates):
    return allupdates['result']['-1']


def sendmessage(chat_id,text):
    send_data = {'chat_id':chat_id,'text':text}
    response = requests.post(url + 'sendMessage',send_data)
    return response

def read_json(filename='favorites.json'):
    with open(filename,'r') as target:
        data = json.load(target)
    return data

@app.route('/' , methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()
        chat_id = get_chat_id(msg)
        text = msg['message'].get('text','')
        if text == '/start':
            sendmessage(chat_id,'''Hi
            This bot can store your favorite musics and find your wanted musics''')
        elif 'new' in text:
            favorites = read_json()
            username = msg['message']['from']['username']
            if username not in favorites.keys():
                favorites[username] = []
            music = text.split(maxsplit=1)[1]
            favorites[username].append(music)
            write_json(favorites)
            
        elif text =='list':
            favorites = read_json()
            username = msg['message']['from']['username']
            if username not in favorites.keys():
                sendmessage(chat_id,'You don not have any favorites music')
            else:
                for music in favorites[username]:
                    sendmessage(chat_id,music)

        return response('ok',status=200)
    else:
        return '<h1>Hello<h2>'

def write_json(data,filename='favorites.json'):
    with open(filename,'w') as target:
        json.dump(data,target,indent=4,ensure_ascii=False)

def read_json(filename='favorites.json'):
    with open(filename,'r') as target:
        data = json.load(target)
    return data


# data = get_all_updates()
# lastupdate = get_last_update(data)
# print()
write_json({})
app.run(host='0.0.0.0',port=int(os.environ('PORT',5000))) # debug=True5