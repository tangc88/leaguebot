# -*- coding: utf-8 -*-

import logging
import random
import time
import datetime
import json
import urllib2
import os

logger = logging.getLogger(__name__)
riot = os.environ.get("riot")
geocode = os.environ.get("geocode")
dark_sky = os.environ.get("dark_sky")
matt = '31203597'
jake = '45556126'
jerry = '19139825'
trevor = '26767760'
dave = '32702702'
justin = '45496123'
#currently nick's smurf
nick = '75821827'
raf = '532474'
surat = '30852265'
shelby = '31118715'
steve = '530530'
wes = '47884918'

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
        txt = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> attachment` - I'll demo a post with an attachment using the Web API. :paperclip:",
            "> `<@" + bot_uid + "> fact` - I'll give you a great fact about Matt! :mott:",
            "> `<@" + bot_uid + "> alternative fact` - I'll give you a great alternative fact about Matt! :mottball:",
            "> `<@" + bot_uid + "> rank` - I'll give you Matt's sad League ranking. :frowning:",
            "> `<@" + bot_uid + "> weather (zip code)` - I'll tell you the current temperature for that zip code! :thermometer:",
            "> `<@" + bot_uid + "> leaderboard` - I'll show you where you rank among us! :trophy:")
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
        for x in range(0, len(games_jake['playerStatSummaries'])):
            if games_jake['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins = games_jake['playerStatSummaries'][x]['wins']
                losses = games_jake['playerStatSummaries'][x]['losses']
                percentage = ((float(wins) / float(wins + losses)) * 100.0)
        # elif games_jake['playerStatSummaries'][8]['playerStatSummaryType'] == 'RankedSolo5x5':
        #     wins = games_jake['playerStatSummaries'][8]['wins']
        #     losses = games_jake['playerStatSummaries'][8]['losses']
        #     percentage = ((float(wins) / float(wins + losses)) * 100.0)
        # elif games_jake['playerStatSummaries'][10]['playerStatSummaryType'] == 'RankedSolo5x5':
        #     wins = games_jake['playerStatSummaries'][10]['wins']
        #     losses = games_jake['playerStatSummaries'][10]['losses']
        #     percentage = ((float(wins) / float(wins + losses)) * 100.0)
        # else:
        #     percentage = 51.0
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

    def write_leaderboard(self, channel_id):
        json_matt_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + matt + '/summary?season=SEASON2017&api_key=' + riot)
        games_matt = json.load(json_matt_games)
        json_jake_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + jake + '/summary?season=SEASON2017&api_key=' + riot)
        games_jake = json.load(json_jake_games)
        json_jerry_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + jerry + '/summary?season=SEASON2017&api_key=' + riot)
        games_jerry = json.load(json_jerry_games)
        json_trevor_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + trevor + '/summary?season=SEASON2017&api_key=' + riot)
        games_trevor = json.load(json_trevor_games)
        json_justin_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + justin + '/summary?season=SEASON2017&api_key=' + riot)
        games_justin = json.load(json_justin_games)
        json_raf_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + raf + '/summary?season=SEASON2017&api_key=' + riot)
        games_raf = json.load(json_raf_games)
        json_surat_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + surat + '/summary?season=SEASON2017&api_key=' + riot)
        games_surat = json.load(json_surat_games)
        json_dave_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + dave + '/summary?season=SEASON2017&api_key=' + riot)
        games_dave = json.load(json_dave_games)
        json_nick_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + nick + '/summary?season=SEASON2017&api_key=' + riot)
        games_nick = json.load(json_nick_games)
        json_steve_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + steve + '/summary?season=SEASON2017&api_key=' + riot)
        games_steve = json.load(json_steve_games)
        time.sleep(11)
        # json_shelby_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + shelby + '/summary?season=SEASON2017&api_key=' + riot)
        # games_shelby = json.load(json_shelby_games)
        json_wes_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + wes + '/summary?season=SEASON2017&api_key=' + riot)
        games_wes = json.load(json_wes_games)

        for x in range(0, len(games_matt['playerStatSummaries'])):
            if games_matt['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_matt = games_matt['playerStatSummaries'][x]['wins']
                losses_matt = games_matt['playerStatSummaries'][x]['losses']
                percentage_matt = ((float(wins_matt) / float(wins_matt + losses_matt)) * 100.0)
                kills_total_matt = games_matt['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
                kills_per_game_matt = float(kills_total_matt) / float(wins_matt + losses_matt)
        for x in range(0, len(games_jake['playerStatSummaries'])):
            if games_jake['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_jake = games_jake['playerStatSummaries'][x]['wins']
                losses_jake = games_jake['playerStatSummaries'][x]['losses']
                percentage_jake = ((float(wins_jake) / float(wins_jake + losses_jake)) * 100.0)
        for x in range(0, len(games_jerry['playerStatSummaries'])):
            if games_jerry['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_jerry = games_jerry['playerStatSummaries'][x]['wins']
                losses_jerry = games_jerry['playerStatSummaries'][x]['losses']
                percentage_jerry = ((float(wins_jerry) / float(wins_jerry + losses_jerry)) * 100.0)
        for x in range(0, len(games_trevor['playerStatSummaries'])):
            if games_trevor['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_trevor = games_trevor['playerStatSummaries'][x]['wins']
                losses_trevor = games_trevor['playerStatSummaries'][x]['losses']
                percentage_trevor = ((float(wins_trevor) / float(wins_trevor + losses_trevor)) * 100.0)
        for x in range(0, len(games_justin['playerStatSummaries'])):
            if games_justin['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_justin = games_justin['playerStatSummaries'][x]['wins']
                losses_justin = games_justin['playerStatSummaries'][x]['losses']
                percentage_justin = ((float(wins_justin) / float(wins_justin + losses_justin)) * 100.0)
        for x in range(0, len(games_surat['playerStatSummaries'])):
            if games_surat['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_surat = games_surat['playerStatSummaries'][x]['wins']
                losses_surat = games_surat['playerStatSummaries'][x]['losses']
                percentage_surat = ((float(wins_surat) / float(wins_surat + losses_surat)) * 100.0)
        for x in range(0, len(games_steve['playerStatSummaries'])):
            if games_steve['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_steve = games_steve['playerStatSummaries'][x]['wins']
                losses_steve = games_steve['playerStatSummaries'][x]['losses']
                percentage_steve = ((float(wins_steve) / float(wins_steve + losses_steve)) * 100.0)
        for x in range(0, len(games_wes['playerStatSummaries'])):
            if games_wes['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_wes = games_wes['playerStatSummaries'][x]['wins']
                losses_wes = games_wes['playerStatSummaries'][x]['losses']
                percentage_wes = ((float(wins_wes) / float(wins_wes + losses_wes)) * 100.0)
        for x in range(0, len(games_dave['playerStatSummaries'])):
            if games_dave['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_dave = games_dave['playerStatSummaries'][x]['wins']
                losses_dave = games_dave['playerStatSummaries'][x]['losses']
                percentage_dave = ((float(wins_dave) / float(wins_dave + losses_dave)) * 100.0)
        for x in range(0, len(games_nick['playerStatSummaries'])):
            if games_nick['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_nick = games_nick['playerStatSummaries'][x]['wins']
                losses_nick = games_nick['playerStatSummaries'][x]['losses']
                percentage_nick = ((float(wins_nick) / float(wins_nick + losses_nick)) * 100.0)
        for x in range(0, len(games_raf['playerStatSummaries'])):
            if games_raf['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
                wins_raf = games_raf['playerStatSummaries'][x]['wins']
                losses_raf = games_raf['playerStatSummaries'][x]['losses']
                percentage_raf = ((float(wins_raf) / float(wins_raf + losses_raf)) * 100.0)
        ##Shelby isn't ranked
        # for x in range(0, len(games_shelby['playerStatSummaries'])):
        #     if games_shelby['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_shelby = games_shelby['playerStatSummaries'][x]['wins']
        #         losses_shelby = games_shelby['playerStatSummaries'][x]['losses']
        #         percentage_shelby = ((float(wins_shelby) / float(wins_shelby + losses_shelby)) * 100.0)
        percentage_list = [('Jerry', percentage_jerry), ('Raf', percentage_raf), ('Nick', percentage_nick), ('Dave', percentage_dave), ('Wes', percentage_wes), ('Steve', percentage_steve), ('Surat', percentage_surat), ('Justin', percentage_justin), ('Jake', percentage_jake), ('Matt', percentage_matt, kills_total_matt, kills_per_game_matt), ('Trevor',percentage_trevor)]
        sorted_percentage_list = sorted(percentage_list, key = lambda percents:percents[1], reverse = True)
        percentage_leaderboard = "Solo Queue Leaderboard\n:crown:: " + str(sorted_percentage_list[0][0]) + ": " + str(sorted_percentage_list[0][1]) + "%, " + str(sorted_percentage_list[0][2]) + " Total Kills, "+ str(sorted_percentage_list[0][3]) + " Kills/Game" + "\n:two:: " + str(sorted_percentage_list[1][0]) + ": " + str(sorted_percentage_list[1][1]) + "%" + "\n:three:: " + str(sorted_percentage_list[2][0]) + ": " + str(sorted_percentage_list[2][1]) + "%" + "\n:four:: " + str(sorted_percentage_list[3][0]) + ": " + str(sorted_percentage_list[3][1]) + "%" + "\n:five:: " + str(sorted_percentage_list[4][0]) + ": " + str(sorted_percentage_list[4][1]) + "%" + "\n:six:: " + str(sorted_percentage_list[5][0]) + ": " + str(sorted_percentage_list[5][1]) + "%" + "\n:seven:: " + str(sorted_percentage_list[6][0]) + ": " + str(sorted_percentage_list[6][1]) + "%" + "\n:eight:: " + str(sorted_percentage_list[7][0]) + ": " + str(sorted_percentage_list[7][1]) + "%" + "\n:nine:: " + str(sorted_percentage_list[8][0]) + ": " + str(sorted_percentage_list[8][1]) + "%" + "\n:keycap_ten:: " + str(sorted_percentage_list[9][0]) + ": " + str(sorted_percentage_list[9][1]) + "%" + "\n:jakepuss:: " + str(sorted_percentage_list[10][0]) + ": " + str(sorted_percentage_list[10][1]) + "%"
        self.send_message(channel_id, percentage_leaderboard)

    def write_weather(self, channel_id, zip_code):
        #zip_code = input("Enter your zip code: ")
        json_location = urllib2.urlopen('https://maps.googleapis.com/maps/api/geocode/json?address=' + zip_code + '&key=' + geocode)
        location = json.load(json_location)
        lat = location['results'][0]['geometry']['location']['lat']
        lng = location['results'][0]['geometry']['location']['lng']
        json_weather = urllib2.urlopen('https://api.darksky.net/forecast/' + dark_sky + '/' + str(lat) + ',' + str(lng))
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
