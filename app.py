'''
Author: Bereket Siraw
purpose: forwarding students assignment to a private group
order: Mr.Robel Tesfaye English Instructor
date-of-publish:04-07-2021 GC.
Date-of-version-03-release:4/13/2021
version: 03
application: webhook system
api: telegram
'''

from flask import Flask, request

import telegram
import logging
import requests
import io
import os
import datetime
import json
from store import process_data, read_data 
from telegram import ParseMode as ParseMode
from telegram import Update, Bot
from telegram.ext import Updater,CommandHandler,MessageHandler,Filters ,CallbackContext

group_id = ''
domain_name = ""

emojies = [
    "CAACAgIAAxkBAAIES2B3GUvovLnl9ZjV9UStUyCSzrVmAAI3AQACUomRI9UUQKd8bRIaHwQ", ##monkey
    "CAACAgIAAxkBAAIEUGB3G5z19Su_wZW2J8PcDuatzWEpAAKUAAP3AsgPoua-568NrOgfBA", #blue fish
    "CAACAgIAAxkBAAIEXmB3Hujg7vvFSwJLk18DLzemyf08AAJmAAPb234AAZPMw9ANLY9sHwQ" #square white robot
]

uname = "" #username
gname = "" #gname stands for gllobal name
URL = ""
# URL = "https://senaysite.com/hasselfreebot"
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

# CONFIG
TOKEN = ""
PORT = 80

updater = Updater(TOKEN)
bot = telegram.Bot(TOKEN)
app = Flask(__name__)

update_object_key = "message" #[edited_message]this explicitly expressed to enhance the code flexibility/reusability for the future feature

def check_key_exist(test_dict, key):
    try:
       value = test_dict[key]
       return value
    except KeyError:
        return False

def start(update=Update, _= CallbackContext)->None:
    """Inform user about what this bot can do"""
    global uname
    global gname
    uname = update[update_object_key].chat.first_name
    update[update_object_key].reply_text(
        f"Hello <b>{uname}</b>, welcome to our bot, use this format to attach the document:\n\n<code>name: Amanuel Melkamu\nGrade: 10\nSection: A\nAssignment number:14\n\n</code>Put this information as a caption on the document you're attaching. Don't send a text message here, only documents/images are allowed!!!!\nfor further information /help"
, parse_mode=ParseMode.HTML
    )

def help_handler(update= Update, _= CallbackContext)->None:
    """Display a help message"""
    global uname
    if str(update[update_object_key].chat.id) != group_id and str(update[update_object_key].chat['type']) == "private": 
        update[update_object_key].reply_text("\n⭐️Use the correct format as mentioned in /start\n⭐️Don't send a text message!; only documents/images are allowed!!!!\n⭐️File size >20mb isn't allowed\n⭐️Send the document again if you don't recieve a verfication message in a minute after you have submited the assignment", parse_mode=ParseMode.HTML)

def assignment(update, context)->None:
    try:    
        global uname
        global gname
        
        if check_key_exist(update[update_object_key], 'caption') is None:
            raise Exception('There is no caption!!!') ##custome error raised to hundle caption keyerror
        uname = update[update_object_key].chat.first_name
        try:
            gname  = "@"+str(update[update_object_key].chat.username)
        except:
            gname = uname

        if gname == '':
            start(update, context)
        caption = update[update_object_key].caption
        get_url = Bot(TOKEN)
        current_time = str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M'))
        
        if len(list(update[update_object_key].photo))>0:
            fileId = update[update_object_key].photo[len(update[update_object_key].photo)-1]["file_id"]
            url = get_url.get_file(file_id=fileId, timeout=None, api_kwargs=None)
            path = str(url.file_path)
            fileName = "Hasselfreebot"+current_time+path[-5:]
            attachment = bytes(requests.get(path).content)
            # attachment.name = "HasselFreebot:"+str(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            files = {"photo": attachment}
            bot.sendPhoto(chat_id = group_id,
                                photo = attachment,
                                caption = str(caption)+"\nTG-name: "+str(gname),
                                filename =fileName )
        else:
            fileId = update[update_object_key].document.file_id
            url = get_url.get_file(file_id=fileId, timeout=None, api_kwargs=None)
            path = str(url.file_path)
            attachment = bytes(requests.get(path).content)
            fileName = "Hasselfreebot"+current_time+path[-5:]
            bot.sendDocument(chat_id = group_id,
                                document = attachment,
                                filename = str(fileName),
                                caption = str(caption)+"\nTG-name: "+gname
                                )

        update[update_object_key].reply_text(f'''
            Congratz {uname}, 🎊🥳 your assignment succcefully submitted''
        ''')
    except Exception as e:
        update[update_object_key].reply_text('''
            Don't send me a document with no caption or text!!!\nFor further information /help
        ''')

        if str(e) != 'There is no caption!!!':
            b = Bot(TOKEN)
            b.send_message(chat_id='346186168', text=f"[@hasselfreebot]\nSir: There is an error happening in this bot->[{uname}=>{gname}]: {e}")

@app.route('/')
def hello():
    return {
        "result":200,
        "error_code": "None",
        "description": "bot is running",
        "access the bot": "@hasselfreebot"
        }


@app.route('/listen{}'.format(TOKEN), methods=['POST'])
def webhook():
    try:
        update = {}
        update = telegram.Update.de_json(request.get_json(force=True), bot)
        try:
            if check_key_exist(update, "channel_post")!=False: #this bot isn't mean to be used by anonymous channels for the seck of increasing subscribers or DDOS
                channelname = check_key_exist[update,"channel_post"]
                channelname = check_key_exist[channelname, "sender_chat"]
                channelname = check_key_exist[channelname,"username"] if channelname != False else "Anonymous channel"
                channelname = channelname if channelname != False or channelname != "Anonymous channel" else "Anonymous channel"
                update["edited_message"].message("346186168",f"A channel you're forced to be is having a new post {channelname}")
                return {"status":"403"}
        except:
            pass
        global uname
        global gname 
        b = Bot(TOKEN)

        if  check_key_exist(update, update_object_key) is None or check_key_exist(update[update_object_key],'chat') is None and str(update[update_object_key].chat.id) == group_id and str(update[update_object_key].chat['type']) != "private":
            if check_key_exist(update, "edited_message") is not None and check_key_exist(update["edited_message"], 'document') is not None or len(update["edited_message"].photo)>0:
                update['edited_message'].reply_text('''You can't edit/modify
        ''')
            #raise Exception("Hell no this shouldn't happen")
            return {"Say":"Nothing :("}
            
        uname = update[update_object_key].chat.first_name
        try:
            gname  = "@"+str(update[update_object_key].chat.username)
        except:
            gname = uname
        process_data(update[update_object_key].chat.id, gname, uname)
        message = update[update_object_key].text
        
        if check_key_exist(update[update_object_key], 'document') is not None or len(update[update_object_key].photo)>0:
            assignment(update, CallbackContext)
        if message != None:
            if message =='/help':
                help_handler(update, CallbackContext)
            elif message =='/start':
                start(update, CallbackContext)
            elif len(message) >= 7 and message[0:5] == '/send' and str(update[update_object_key].chat.id) == "346186168" and len(message.replace(" ", ""))>6:
                lst = message[6:].split(',')
                b.send_message(chat_id= int(lst[0].replace(" ","")), text=",".join(lst[1:]))
            elif message[0:5] == '/read' and str(update[update_object_key].chat.id) == '346186168':
                txt = read_data()
                it_len = len(txt)
                for i in range(0, it_len):
                    b.send_message(chat_id='346186168', text=txt[i], parse_mode=ParseMode.HTML)
            elif message[0:11]=='/add_member'  and str(update[update_object_key].chat.id) == '346186168':
                msg = message[12:].split(',')
                username = msg[0]
                password = msg[1]
                data = {'username': username, 'password':password}
                res = requests.post(URL+'matric/api/add_userd5711f1db41b58770dc483fd113c56537eda482c', json.dumps(data))
                b.send_message(chat_id='346186168', text=json.loads(res.text)['response'])
            elif message[0:12]=='/list_member'  and str(update[update_object_key].chat.id) == '346186168':
                res = requests.get(URL+'matric/api/list_userd5711f1db41b58770dc483fd113c56537eda482c')
                data_set = json.loads(res.text)
                header = '''<b><u>username || password</u></b>\n'''
                data = [header]
                counter = 0
                for i in range(0,len(list(data_set))):
                    txt = f'''{list(data_set)[i]} || {data_set[list(data_set)[i]]}\n'''
                    if len(data[counter])>=3500:
                        counter+=1
                    else:
                        data[counter] += txt
                for i in range(0,len(data)):
                    print(data[i])
                    b.send_message(chat_id='346186168', text=data[i], parse_mode=ParseMode.HTML)
            elif message[0:9]=='/feedback'  and str(update[update_object_key].chat.id) == '346186168':
                res = requests.get(URL+'matric/api/feedbackd5711f1db41b58770dc483fd113c56537eda482c')
                data_set = json.loads(res.text)
                header = '''<b><u>ip || rate</u></b>\n'''
                data = [header]
                counter = 0
                for i in range(0,len(list(data_set))):
                    txt = f'''{list(data_set)[i]} || {data_set[list(data_set)[i]]}\n'''
                    if len(data[counter])>=3500:
                        data.append(txt)
                        counter+=1
                    else:
                        data[counter] += txt
                for i in range(0,len(data)):
                    b.send_message(chat_id='346186168', text=data[i], parse_mode=ParseMode.HTML)
            elif message[0:14]=='/remove_member'  and str(update[update_object_key].chat.id) == '346186168':
                username = message[15:]
                data = {'username':username}
                res = requests.post(URL+'matric/api/remove_userd5711f1db41b58770dc483fd113c56537eda482c', json.dumps(data))
                b.send_message(chat_id='346186168', text=json.loads(res.text)['response'])
            elif message !='':
                help_handler(update, CallbackContext)
    except Exception as e:
        b = Bot(TOKEN)
        b.send_message(chat_id='346186168', text=f"[@hasselfreebot]\nSir: There is an error happening in this webhook-bot[{uname}=>{gname}]: {e}\nMore detailed: {update}")

    return 'OK'

@app.route('/set_webhook')
def setWebhook():
   s = bot.setWebhook(f'{URL}hasselfreebot/listen{TOKEN}')
   if s:
       return "webhook setup ok"
   else:
       return "webhook setup failed"


if __name__ == '__main__':
   # main()
    #setWebhook()
    app.run(host='0.0.0.0',
            port=PORT,
             threaded=True,
            debug=False)
