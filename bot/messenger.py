# -*- coding: utf-8 -*-

import logging
import random
import time
import datetime
import json
import urllib2

logger = logging.getLogger(__name__)
#riot = 'RGAPI-e3c527f3-1921-4ee8-9d6e-087aa21deb76'
matt = '31203597'
jake = '45556126'

class Messenger(object):

    def __init__(self, slack_clients):
        self.clients = slack_clients

    def send_message(self, channel_id, msg):
        # in the case of Group and Private channels, RTM channel payload is a complex dictionary
        if isinstance(channel_id, dict):
            channel_id = channel_id['id']
        logger.debug('Sending msg: %s to channel: %s' % (msg, channel_id))
        channel = self.clients.rtm.server.channels.find(channel_id)
        channel.send_message(msg)

    def write_help_message(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:",
            "> `<@" + bot_uid + "> fact` - I'll give you a great fact about Matt! :mott:",
            "> `<@" + bot_uid + "> alternative fact` - I'll give you a great alternative fact about Matt! :mottball:",
            "> `<@" + bot_uid + "> rank` - I'll give you Matt's sad League ranking. :frowning:",
            "> `<@" + bot_uid + "> weather (zip code)` - I'll tell you the current temperature for that zip code! :thermometer:")
        self.send_message(channel_id, txt)

    def write_fact(self, channel_id):
        MATT_BIRTHDAY = datetime.date(1990, 11, 7)
        TODAY = datetime.date.today()
        DIFF = TODAY - MATT_BIRTHDAY
        facts = ['Matt was physically born a boy and mentally a sandwich.', 'Matt has diabetes.', 'Matt and Mott are synonyms.',
            'Matt is ' + str(DIFF.days) + ' days old!', 'Matt is a weird guy, but he is fun.', 'His blood type is O-Negative.',
            'He thought "Giraffe" was spelled "Diraffe" until he was 13.']
        txt = '{}'.format(random.choice(facts))
        self.send_message(channel_id, txt)

    def write_alternative_fact(self, channel_id):
        alt_facts = ["Matt only has 9 toes on his feet, his tenth toe is his penis.", "Matt has the ability to suck his own ear.",
            "Matt invented the sport of penis wrestling, he plays alone.", "Matt was once on the path of going pro in LoL, but diabetes derailed his destiny.",
            "Before becoming diabetic, Matt has straight hair."]
        txt = '{}'.format(random.choice(alt_facts))
        self.send_message(channel_id, txt)

    def write_greeting(self, channel_id, user_id):
        greetings = ['Hi', 'Hello', 'Nice to meet you', 'Howdy', 'Salutations']
        txt = '{}, <@{}>!'.format(random.choice(greetings), user_id)
        self.send_message(channel_id, txt)

    def write_prompt(self, channel_id):
        bot_uid = self.clients.bot_user_id()
        txt = "I'm so sorry, I didn't quite understand... Can I help you? (e.g. `<@" + bot_uid + "> help`)"
        self.send_message(channel_id, txt)

    def write_rank(self, channel_id):
        json_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v2.5/league/by-summoner/' + matt + '/entry?api_key=' + riot)
        games = json.load(json_games)
        tier = games['31203597'][0]['tier']
        division = games['31203597'][0]['entries'][0]['division']
        flex_tier = games['31203597'][1]['tier']
        flex_division = games['31203597'][1]['entries'][0]['division']
        txt = "\nSolo Rank: " + tier + " " + division + "\n" + "Flex Rank: " + flex_tier + " " + flex_division
        self.send_message(channel_id, txt)

    def write_joke(self, channel_id):
        question = "Jake's ranked solo win percentage is ..."
        self.send_message(channel_id, question)
        self.clients.send_user_typing_pause(channel_id)
        json_games_jake = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + jake + '/summary?season=SEASON2017&api_key=' + riot)
        games_jake = json.load(json_games_jake)
        wins = games_jake['playerStatSummaries'][8]['wins']
        losses = games_jake['playerStatSummaries'][8]['losses']
        percentage = ((float(wins) / float(wins + losses)) * 100.0)
        #answer = str('0')
        if percentage < 50.0:
            answer = str(percentage) + "% :laughing:"
        else:
            answer = "Jake has been scripting. :jakepuss:"
        self.send_message(channel_id, answer)
        self.clients.send_user_typing_pause(channel_id)
        json_games_jake_champs = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/45556126/ranked?season=SEASON2017&api_key=' + riot)
        games_jake_champs = json.load(json_games_jake_champs)
        riven_losses = games_jake_champs['champions'][13]['stats']['totalSessionsLost']
        riven_first_blood = games_jake_champs['champions'][13]['stats']['totalFirstBlood']
        extra_joke = "He has also lost " + str(riven_losses) + " games as Riven. :-1:"
        self.send_message(channel_id, extra_joke)
        #self.clients.send_user_typing_pause(channel_id)
        #extra_joke_two = "Also has " + str(riven_first_blood) + " first bloods as Riven. :chart_with_downwards_trend:"
        #self.send_message(channel_id, extra_joke_two)

    def write_weather(self, channel_id, zip_code):
        #zip_code = input("Enter your zip code: ")
        json_location = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + zip_code + '&key=AIzaSyCmnhJXBfU_bi32jVCwbfLeSMEQWU-O68Q')
        location = json.load(json_location)
        lat = location['results'][0]['geometry']['location']['lat']
        lng = location['results'][0]['geometry']['location']['lng']
        json_weather = urllib2.urlopen('https://api.darksky.net/forecast/9298a272f3fb8da43fabcfbdb5288f0f/' + str(lat) + ',' + str(lng))
        weather = json.load(json_weather)
        temperature = weather['currently']['temperature']
        current_temp = "It is currently " + str(temperature) + " degrees fahrenheit."
        self.send_message(channel_id, current_temp)


    def write_error(self, channel_id, err_msg):
        txt = ":face_with_head_bandage: my maker didn't handle this error very well:\n>```{}```".format(err_msg)
        self.send_message(channel_id, txt)

    def demo_attachment(self, channel_id):
        txt = "Beep Beep Boop is a ridiculously simple hosting platform for your Slackbots."
        attachment = {
            "pretext": "We bring bots to life. :sunglasses: :thumbsup:",
            "title": "Host, deploy and share your bot in seconds.",
            "title_link": "https://beepboophq.com/",
            "text": txt,
            "fallback": txt,
            "image_url": "https://storage.googleapis.com/beepboophq/_assets/bot-1.22f6fb.png",
            "color": "#7CD197",
        }
        self.clients.web.chat.post_message(channel_id, txt, attachments=[attachment], as_user='true')
