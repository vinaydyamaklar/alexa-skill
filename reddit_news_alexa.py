from flask import Flask
from flask_ask import Ask, statement, question, session, delegate
import json
import requests
import time
import unidecode

app = Flask(__name__)
ask = Ask(app, "/reddit_reader")


def get_headlines(news):
    user_pass_dict = {'user': 'USERNAME',
                      'passwd': 'PASSWORD',
                      'api_type': 'json'}
    sess = requests.session()
    sess.headers.update({'User-Agent': 'Testing Alexa: Vinay'})
    sess.post('https://wwww.reddit.com/api/login',data = user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/'+news+'/.json?limit=2'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    for listing in data['data']['children']:
        titles.append(unidecode.unidecode(listing['data']['title']))
    titles = '... '.join([i for i in titles])
    return titles


def get_dialog_state():
    return session['dialogState']


@app.route('/')
def homepage():
    return "Hi there, how are you doing?"


@ask.launch
def start_skill():
    welcome_message = 'Hello there, would you like the news?'
    return question(welcome_message)


@ask.intent("YesIntent")
def share_headlines(news_type):
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()

    if news_type is not "None":
        headlines = get_headlines(news_type)
        headline_msg = 'The current news headlines are {}'.format(headlines)
        return statement(headline_msg)
    else:
        no_intent()


@ask.intent("NoIntent")
def no_intent():
    bye_text = 'I am not sure why you asked me to run then, but okay...bye'
    return statement(bye_text)


if __name__ == '__main__':
    app.run(host="0.0.0.0",port=5000)
