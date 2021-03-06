# -*- coding: utf-8 -*-

import logging
import random
import time
import datetime
import json
import urllib2
import os
import requests

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
#shelby = '31118715'
steve = '530530'
wes = '47884918'
#0:matt, 1:jake, 2:jerry, 3:trevor, 4:dave, 5:justin, 6:nick, 7:raf, 8:surat, 9:steve, 10:wes
summoner_id = ['31203597', '45556126', '19139825', '26767760', '32702702', '45496123', '75821827', '532474', '30852265', '530530', '47884918']

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
        txt = '{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}'.format(
            "I'm your friendly Slack bot written in Python.  I'll *_respond_* to the following commands:",
            "> `hi <@" + bot_uid + ">` - I'll respond with a randomized greeting mentioning your user. :wave:",
            "> `<@" + bot_uid + "> joke` - I'll tell you one of my finest jokes, with a typing pause for effect. :laughing:",
            "> `<@" + bot_uid + "> fact` - I'll give you a great fact about Matt! :mott:",
            "> `<@" + bot_uid + "> alternative fact` - I'll give you a great alternative fact about Matt! :mottball:",
            "> `<@" + bot_uid + "> rank` - I'll give you Matt's sad League ranking. :frowning:",
            "> `<@" + bot_uid + "> weather (zip code)` - I'll tell you the current temperature for that zip code! :thermometer:",
            "> `<@" + bot_uid + "> leaderboard` - I'll show you where you rank among us! :trophy:",
            "> `<@" + bot_uid + "> duo (summoner name) (summoner name)` - I'll give you your duo win percentage!",
            "> `<@" + bot_uid + "> trio (summoner name) (summoner name) (summoner name)` - I'll give you your trio win percentage!",)
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

    def write_rank(self, channel_id, user_id):
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
        json_games_jake = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + summoner_id[1] + '/summary?season=SEASON2017&api_key=' + riot)
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
        if percentage <= 40.0:
            answer = "This is just sad now Jake..." + str(percentage) + "% :crying_cat_face:"
        elif percentage < 50.0:
            answer = str(percentage) + "% :laughing:"
        else:
            answer = "Jake has been scripting. :jakepuss:"
        self.send_message(channel_id, answer)
        #self.clients.send_user_typing_pause(channel_id)
        # json_games_jake_champs = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/45556126/ranked?season=SEASON2017&api_key=' + riot)
        # games_jake_champs = json.load(json_games_jake_champs)
        # riven_losses = games_jake_champs['champions'][13]['stats']['totalSessionsLost']
        # riven_first_blood = games_jake_champs['champions'][13]['stats']['totalFirstBlood']
        # extra_joke = "He has also lost " + str(riven_losses) + " games as Riven. :-1:"
        # self.send_message(channel_id, extra_joke)
        #self.clients.send_user_typing_pause(channel_id)
        #extra_joke_two = "Also has " + str(riven_first_blood) + " first bloods as Riven. :chart_with_downwards_trend:"
        #self.send_message(channel_id, extra_joke_two)

    def write_mastery(self, channel_id):
        masteries_list = []
        message_list= []
        message = 'Mastery leaderboard\n'
        i = -1
        json_matt_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + matt + '/topchampions?api_key=' + riot)
        matt_champID_json = json.load(json_matt_master)
        matt_champID = matt_champID_json[0]['championId']
        matt_points = matt_champID_json[0]['championPoints']
        matt_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(matt_champID) + '?api_key=' + riot)
        matt_champ_json = json.load(matt_champ_url)
        matt_champ = matt_champ_json['name']
        matt_message = 'Matt\'s top champion is ' + str(matt_champ) + ' with ' + str(matt_points) + ' points!\n'
        masteries_list.append(matt_points)
        message_list.append(matt_message)


        json_jake_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + jake + '/topchampions?api_key=' + riot)
        jake_champID_json = json.load(json_jake_master)
        jake_champID = jake_champID_json[0]['championId']
        jake_points = jake_champID_json[0]['championPoints']
        jake_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(jake_champID) + '?api_key=' + riot)
        jake_champ_json = json.load(jake_champ_url)
        jake_champ = jake_champ_json['name']
        jake_message = 'Jake\'s top champion is ' + str(jake_champ) + ' with ' + str(jake_points) + ' points!\n'
        masteries_list.append(jake_points)
        message_list.append(jake_message)


        json_jerry_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + jerry + '/topchampions?api_key=' + riot)
        jerry_champID_json = json.load(json_jerry_master)
        jerry_champID = jerry_champID_json[0]['championId']
        jerry_points = jerry_champID_json[0]['championPoints']
        jerry_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(jerry_champID) + '?api_key=' + riot)
        jerry_champ_json = json.load(jerry_champ_url)
        jerry_champ = jerry_champ_json['name']
        jerry_message = 'Jerry\'s top champion is ' + str(jerry_champ) + ' with ' + str(jerry_points) + ' points!\n'
        masteries_list.append(jerry_points)
        message_list.append(jerry_message)


        json_trevor_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + trevor + '/topchampions?api_key=' + riot)
        trevor_champID_json = json.load(json_trevor_master)
        trevor_champID = trevor_champID_json[0]['championId']
        trevor_points = trevor_champID_json[0]['championPoints']
        trevor_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(trevor_champID) + '?api_key=' + riot)
        trevor_champ_json = json.load(trevor_champ_url)
        trevor_champ = trevor_champ_json['name']
        trevor_message = 'Trevor\'s top champion is ' + str(trevor_champ) + ' with ' + str(trevor_points) + ' points!\n'
        masteries_list.append(trevor_points)
        message_list.append(trevor_message)


        json_dave_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + dave + '/topchampions?api_key=' + riot)
        dave_champID_json = json.load(json_dave_master)
        dave_champID = dave_champID_json[0]['championId']
        dave_points = dave_champID_json[0]['championPoints']
        dave_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(dave_champID) + '?api_key=' + riot)
        dave_champ_json = json.load(dave_champ_url)
        dave_champ = dave_champ_json['name']
        dave_message = 'Dave\'s top champion is ' + str(dave_champ) + ' with ' + str(dave_points) + ' points!\n'
        masteries_list.append(dave_points)
        message_list.append(dave_message)
        time.sleep(11)

        json_justin_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + justin + '/topchampions?api_key=' + riot)
        justin_champID_json = json.load(json_justin_master)
        justin_champID = justin_champID_json[0]['championId']
        justin_points = justin_champID_json[0]['championPoints']
        justin_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(justin_champID) + '?api_key=' + riot)
        justin_champ_json = json.load(justin_champ_url)
        justin_champ = justin_champ_json['name']
        justin_message = 'Justin\'s top champion is ' + str(justin_champ) + ' with ' + str(justin_points) + ' points!\n'
        masteries_list.append(justin_points)
        message_list.append(justin_message)


        json_nick_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + nick + '/topchampions?api_key=' + riot)
        nick_champID_json = json.load(json_nick_master)
        nick_champID = nick_champID_json[0]['championId']
        nick_points = nick_champID_json[0]['championPoints']
        nick_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(nick_champID) + '?api_key=' + riot)
        nick_champ_json = json.load(nick_champ_url)
        nick_champ = nick_champ_json['name']
        nick_message = 'Nick\'s top champion is ' + str(nick_champ) + ' with ' + str(nick_points) + ' points!\n'
        masteries_list.append(nick_points)
        message_list.append(nick_message)


        json_raf_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + raf + '/topchampions?api_key=' + riot)
        raf_champID_json = json.load(json_raf_master)
        raf_champID = raf_champID_json[0]['championId']
        raf_points = raf_champID_json[0]['championPoints']
        raf_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(raf_champID) + '?api_key=' + riot)
        raf_champ_json = json.load(raf_champ_url)
        raf_champ = raf_champ_json['name']
        raf_message = 'Raf\'s top champion is ' + str(raf_champ) + ' with ' + str(raf_points) + ' points!\n'
        masteries_list.append(raf_points)
        message_list.append(raf_message)


        json_surat_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + surat + '/topchampions?api_key=' + riot)
        surat_champID_json = json.load(json_surat_master)
        surat_champID = surat_champID_json[0]['championId']
        surat_points = surat_champID_json[0]['championPoints']
        surat_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(surat_champID) + '?api_key=' + riot)
        surat_champ_json = json.load(surat_champ_url)
        surat_champ = surat_champ_json['name']
        surat_message = 'Surat\'s top champion is ' + str(surat_champ) + ' with ' + str(surat_points) + ' points!\n'
        masteries_list.append(surat_points)
        message_list.append(surat_message)


        json_steve_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + steve + '/topchampions?api_key=' + riot)
        steve_champID_json = json.load(json_steve_master)
        steve_champID = steve_champID_json[0]['championId']
        steve_points = steve_champID_json[0]['championPoints']
        steve_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(steve_champID) + '?api_key=' + riot)
        steve_champ_json = json.load(steve_champ_url)
        steve_champ = steve_champ_json['name']
        steve_message = 'Steve\'s top champion is ' + str(steve_champ) + ' with ' + str(steve_points) + ' points!\n'
        masteries_list.append(steve_points)
        message_list.append(steve_message)
        time.sleep(3)

        json_wes_master = urllib2.urlopen('https://na.api.pvp.net/championmastery/location/NA1/player/' + wes + '/topchampions?api_key=' + riot)
        wes_champID_json = json.load(json_wes_master)
        wes_champID = wes_champID_json[0]['championId']
        wes_points = wes_champID_json[0]['championPoints']
        wes_champ_url = urllib2.urlopen('https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/' + str(wes_champID) + '?api_key=' + riot)
        wes_champ_json = json.load(wes_champ_url)
        wes_champ = wes_champ_json['name']
        wes_message = 'Wes\'s top champion is ' + str(wes_champ) + ' with ' + str(wes_points) + ' points!\n'
        masteries_list.append(wes_points)
        message_list.append(wes_message)

        mastery_message_list = list(zip(masteries_list,message_list))
        mastery_message_list = sorted(mastery_message_list, key=lambda x: x[0], reverse=True)
        emoji = [':crown:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':jakepuss:']
        for x in mastery_message_list:
            i += 1
            message = message + emoji[i] +': ' + x[1]

        self.send_message(channel_id, message)

    def write_leaderboard(self, channel_id):
        self.clients.send_user_typing_pause(channel_id)
        json_matt_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + matt + '?api_key=' + riot)
        games_matt = json.load(json_matt_games)
        json_jake_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + jake + '?api_key=' + riot)
        games_jake = json.load(json_jake_games)
        json_jerry_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + jerry + '?api_key=' + riot)
        games_jerry = json.load(json_jerry_games)
        json_trevor_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + trevor + '?api_key=' + riot)
        games_trevor = json.load(json_trevor_games)
        json_justin_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + justin + '?api_key=' + riot)
        games_justin = json.load(json_justin_games)
        json_raf_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + raf + '?api_key=' + riot)
        games_raf = json.load(json_raf_games)
        json_surat_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + surat + '?api_key=' + riot)
        games_surat = json.load(json_surat_games)
        json_dave_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + dave + '?api_key=' + riot)
        games_dave = json.load(json_dave_games)
        json_nick_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + nick + '?api_key=' + riot)
        games_nick = json.load(json_nick_games)
        json_steve_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + steve + '?api_key=' + riot)
        games_steve = json.load(json_steve_games)
        # json_shelby_games = urllib2.urlopen('https://na.api.pvp.net/api/lol/na/v1.3/stats/by-summoner/' + shelby + '/summary?season=SEASON2017&api_key=' + riot)
        # games_shelby = json.load(json_shelby_games)
        json_wes_games = urllib2.urlopen('https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/' + wes + '?api_key=' + riot)
        games_wes = json.load(json_wes_games)

        #0:matt, 1:jake, 2:jerry, 3:trevor, 4:dave, 5:justin, 6:nick, 7:raf, 8:surat, 9:steve, 10:wes
        games = [games_matt, games_jake, games_jerry, games_trevor, games_dave, games_justin, games_nick, games_raf, games_surat, games_steve, games_wes]
        a_list = []
        for x in range(0, len(games)):
            wins = games[x][0]['wins']
            losses = games[x][0]['losses']
            percent = "%.2f" % ((float(wins)/(wins + losses)) * 100)
        wins_matt = games_matt[0]['wins']
        losses_matt = games_matt[0]['losses']
        percentage_matt = "%.2f" % ((float(wins_matt)/(wins_matt + losses_matt)) * 100)

        wins_jake = games_jake[0]['wins']
        losses_jake = games_jake[0]['losses']
        percentage_jake = "%.2f" % ((float(wins_jake)/(wins_jake + losses_jake)) * 100)

        wins_jerry = games_jerry[0]['wins']
        losses_jerry = games_jerry[0]['losses']
        percentage_jerry = "%.2f" % ((float(wins_jerry)/(wins_jerry + losses_jerry)) * 100)

        wins_trevor = games_trevor[0]['wins']
        losses_trevor = games_trevor[0]['losses']
        percentage_trevor = "%.2f" % ((float(wins_trevor)/(wins_trevor + losses_trevor)) * 100)

        wins_dave = games_dave[0]['wins']
        losses_dave = games_dave[0]['losses']
        percentage_dave = "%.2f" % ((float(wins_dave)/(wins_dave + losses_dave)) * 100)

        wins_justin = games_justin[0]['wins']
        losses_justin = games_justin[0]['losses']
        percentage_justin = "%.2f" % ((float(wins_justin)/(wins_justin + losses_justin)) * 100)

        wins_nick = games_nick[0]['wins']
        losses_nick = games_nick[0]['losses']
        percentage_nick = "%.2f" % ((float(wins_nick)/(wins_nick + losses_nick)) * 100)

        wins_raf = games_raf[0]['wins']
        losses_raf = games_raf[0]['losses']
        percentage_raf = "%.2f" % ((float(wins_raf)/(wins_raf + losses_raf)) * 100)

        wins_surat = games_surat[0]['wins']
        losses_surat = games_surat[0]['losses']
        percentage_surat = "%.2f" % ((float(wins_surat)/(wins_surat + losses_surat)) * 100)

        wins_steve = games_steve[0]['wins']
        losses_steve = games_steve[0]['losses']
        percentage_steve = "%.2f" % ((float(wins_steve)/(wins_steve + losses_steve)) * 100)

        wins_wes = games_wes[0]['wins']
        losses_wes = games_wes[0]['losses']
        percentage_wes = "%.2f" % ((float(wins_wes)/(wins_wes + losses_wes)) * 100)

        # for x in range(0, len(games_matt['playerStatSummaries'])):
        #     if games_matt['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_matt = games_matt['playerStatSummaries'][x]['wins']
        #         losses_matt = games_matt['playerStatSummaries'][x]['losses']
        #         percentage_matt = "%.2f" % ((float(wins_matt) / float(wins_matt + losses_matt)) * 100.0)
        #         kills_total_matt = games_matt['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_matt = "%.2f" % (float(kills_total_matt) / float(wins_matt + losses_matt))
        #         assists_total_matt = games_matt['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_matt = "%.2f" % (float(assists_total_matt)/ float(wins_matt + losses_matt))
        #         cs_total_matt = games_matt['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_matt = "%.2f" % (float(cs_total_matt) / float(wins_matt + losses_matt))
        # for x in range(0, len(games_jake['playerStatSummaries'])):
        #     if games_jake['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_jake = games_jake['playerStatSummaries'][x]['wins']
        #         losses_jake = games_jake['playerStatSummaries'][x]['losses']
        #         percentage_jake = "%.2f" % ((float(wins_jake) / float(wins_jake + losses_jake)) * 100.0)
        #         kills_total_jake = games_jake['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_jake = "%.2f" % (float(kills_total_jake) / float(wins_jake + losses_jake))
        #         assists_total_jake = games_jake['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_jake = "%.2f" % (float(assists_total_jake)/ float(wins_jake + losses_jake))
        #         cs_total_jake = games_jake['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_jake = "%.2f" % (float(cs_total_jake) / float(wins_jake + losses_jake))
        # for x in range(0, len(games_jerry['playerStatSummaries'])):
        #     if games_jerry['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_jerry = games_jerry['playerStatSummaries'][x]['wins']
        #         losses_jerry = games_jerry['playerStatSummaries'][x]['losses']
        #         percentage_jerry = "%.2f" % ((float(wins_jerry) / float(wins_jerry + losses_jerry)) * 100.0)
        #         kills_total_jerry = games_jerry['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_jerry = "%.2f" % (float(kills_total_jerry) / float(wins_jerry + losses_jerry))
        #         assists_total_jerry = games_jerry['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_jerry = "%.2f" % (float(assists_total_jerry)/ float(wins_jerry + losses_jerry))
        #         cs_total_jerry = games_jerry['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_jerry = "%.2f" % (float(cs_total_jerry) / float(wins_jerry + losses_jerry))
        # for x in range(0, len(games_trevor['playerStatSummaries'])):
        #     if games_trevor['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_trevor = games_trevor['playerStatSummaries'][x]['wins']
        #         losses_trevor = games_trevor['playerStatSummaries'][x]['losses']
        #         percentage_trevor = "%.2f" % ((float(wins_trevor) / float(wins_trevor + losses_trevor)) * 100.0)
        #         kills_total_trevor = games_trevor['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_trevor = "%.2f" % (float(kills_total_trevor) / float(wins_trevor + losses_trevor))
        #         assists_total_trevor = games_trevor['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_trevor = "%.2f" % (float(assists_total_trevor)/ float(wins_trevor + losses_trevor))
        #         cs_total_trevor = games_trevor['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_trevor = "%.2f" % (float(cs_total_trevor) / float(wins_trevor + losses_trevor))
        # for x in range(0, len(games_justin['playerStatSummaries'])):
        #     if games_justin['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_justin = games_justin['playerStatSummaries'][x]['wins']
        #         losses_justin = games_justin['playerStatSummaries'][x]['losses']
        #         percentage_justin = "%.2f" % ((float(wins_justin) / float(wins_justin + losses_justin)) * 100.0)
        #         kills_total_justin = games_justin['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_justin = "%.2f" % (float(kills_total_justin) / float(wins_justin + losses_justin))
        #         assists_total_justin = games_justin['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_justin = "%.2f" % (float(assists_total_justin)/ float(wins_justin + losses_justin))
        #         cs_total_justin = games_justin['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_justin = "%.2f" % (float(cs_total_justin) / float(wins_justin + losses_justin))
        # for x in range(0, len(games_surat['playerStatSummaries'])):
        #     if games_surat['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_surat = games_surat['playerStatSummaries'][x]['wins']
        #         losses_surat = games_surat['playerStatSummaries'][x]['losses']
        #         percentage_surat = "%.2f" % ((float(wins_surat) / float(wins_surat + losses_surat)) * 100.0)
        #         kills_total_surat = games_surat['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_surat = "%.2f" % (float(kills_total_surat) / float(wins_surat + losses_surat))
        #         assists_total_surat = games_surat['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_surat = "%.2f" % (float(assists_total_surat)/ float(wins_surat + losses_surat))
        #         cs_total_surat = games_surat['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_surat = "%.2f" % (float(cs_total_surat) / float(wins_surat + losses_surat))
        # for x in range(0, len(games_steve['playerStatSummaries'])):
        #     if games_steve['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_steve = games_steve['playerStatSummaries'][x]['wins']
        #         losses_steve = games_steve['playerStatSummaries'][x]['losses']
        #         percentage_steve = "%.2f" % ((float(wins_steve) / float(wins_steve + losses_steve)) * 100.0)
        #         kills_total_steve = games_steve['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_steve = "%.2f" % (float(kills_total_steve) / float(wins_steve + losses_steve))
        #         assists_total_steve = games_steve['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_steve = "%.2f" % (float(assists_total_steve)/ float(wins_steve + losses_steve))
        #         cs_total_steve = games_steve['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_steve = "%.2f" % (float(cs_total_steve) / float(wins_steve + losses_steve))
        # for x in range(0, len(games_wes['playerStatSummaries'])):
        #     if games_wes['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_wes = games_wes['playerStatSummaries'][x]['wins']
        #         losses_wes = games_wes['playerStatSummaries'][x]['losses']
        #         percentage_wes = "%.2f" % ((float(wins_wes) / float(wins_wes + losses_wes)) * 100.0)
        #         kills_total_wes = games_wes['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_wes = "%.2f" % (float(kills_total_wes) / float(wins_wes + losses_wes))
        #         assists_total_wes = games_wes['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_wes = "%.2f" % (float(assists_total_wes)/ float(wins_wes + losses_wes))
        #         cs_total_wes = games_wes['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_wes = "%.2f" % (float(cs_total_wes) / float(wins_wes + losses_wes))
        # for x in range(0, len(games_dave['playerStatSummaries'])):
        #     if games_dave['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_dave = games_dave['playerStatSummaries'][x]['wins']
        #         losses_dave = games_dave['playerStatSummaries'][x]['losses']
        #         percentage_dave = "%.2f" % ((float(wins_dave) / float(wins_dave + losses_dave)) * 100.0)
        #         kills_total_dave = games_dave['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_dave = "%.2f" % (float(kills_total_dave) / float(wins_dave + losses_dave))
        #         assists_total_dave = games_dave['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_dave = "%.2f" % (float(assists_total_dave)/ float(wins_dave + losses_dave))
        #         cs_total_dave = games_dave['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_dave = "%.2f" % (float(cs_total_dave) / float(wins_dave + losses_dave))
        # for x in range(0, len(games_nick['playerStatSummaries'])):
        #     if games_nick['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_nick = games_nick['playerStatSummaries'][x]['wins']
        #         losses_nick = games_nick['playerStatSummaries'][x]['losses']
        #         percentage_nick = "%.2f" % ((float(wins_nick) / float(wins_nick + losses_nick)) * 100.0)
        #         kills_total_nick = games_nick['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_nick = "%.2f" % (float(kills_total_nick) / float(wins_nick + losses_nick))
        #         assists_total_nick = games_nick['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_nick = "%.2f" % (float(assists_total_nick)/ float(wins_nick + losses_nick))
        #         cs_total_nick = games_nick['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_nick = "%.2f" % (float(cs_total_nick) / float(wins_nick + losses_nick))
        # for x in range(0, len(games_raf['playerStatSummaries'])):
        #     if games_raf['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_raf = games_raf['playerStatSummaries'][x]['wins']
        #         losses_raf = games_raf['playerStatSummaries'][x]['losses']
        #         percentage_raf = "%.2f" % ((float(wins_raf) / float(wins_raf + losses_raf)) * 100.0)
        #         kills_total_raf = games_raf['playerStatSummaries'][x]['aggregatedStats']['totalChampionKills']
        #         kills_per_game_raf = "%.2f" % (float(kills_total_raf) / float(wins_raf + losses_raf))
        #         assists_total_raf = games_raf['playerStatSummaries'][x]['aggregatedStats']['totalAssists']
        #         assists_per_game_raf = "%.2f" % (float(assists_total_raf)/ float(wins_raf + losses_raf))
        #         cs_total_raf = games_raf['playerStatSummaries'][x]['aggregatedStats']['totalMinionKills']
        #         cs_per_game_raf = "%.2f" % (float(cs_total_raf) / float(wins_raf + losses_raf))
        ##Shelby isn't ranked
        # for x in range(0, len(games_shelby['playerStatSummaries'])):
        #     if games_shelby['playerStatSummaries'][x]['playerStatSummaryType'] == 'RankedSolo5x5':
        #         wins_shelby = games_shelby['playerStatSummaries'][x]['wins']
        #         losses_shelby = games_shelby['playerStatSummaries'][x]['losses']
        #         percentage_shelby = ((float(wins_shelby) / float(wins_shelby + losses_shelby)) * 100.0)
        # percentage_list = [('Jerry', percentage_jerry, kills_total_jerry, kills_per_game_jerry, assists_per_game_jerry, cs_per_game_jerry), ('Raf', percentage_raf, kills_total_raf, kills_per_game_raf, assists_per_game_raf, cs_per_game_raf), ('Nick', percentage_nick, kills_total_nick, kills_per_game_nick, assists_per_game_nick, cs_per_game_nick), ('Dave', percentage_dave, kills_total_dave, kills_per_game_dave, assists_per_game_dave, cs_per_game_dave), ('Wes', percentage_wes, kills_total_wes, kills_per_game_wes, assists_per_game_wes, cs_per_game_wes), ('Steve', percentage_steve, kills_total_steve, kills_per_game_steve, assists_per_game_steve, cs_per_game_steve), ('Surat', percentage_surat, kills_total_surat, kills_per_game_surat, assists_per_game_surat, cs_per_game_surat), ('Justin', percentage_justin, kills_total_justin, kills_per_game_justin, assists_per_game_justin, cs_per_game_justin), ('Jake', percentage_jake, kills_total_jake, kills_per_game_jake, assists_per_game_jake, cs_per_game_jake), ('Matt', percentage_matt, kills_total_matt, kills_per_game_matt, assists_per_game_matt, cs_per_game_matt), ('Trevor',percentage_trevor, kills_total_trevor, kills_per_game_trevor, assists_per_game_trevor, cs_per_game_trevor)]
        # sorted_percentage_list = sorted(percentage_list, key = lambda percents:percents[1], reverse = True)

        percentage_list = [('Jerry', percentage_jerry), ('Raf', percentage_raf), ('Nick', percentage_nick), ('Dave', percentage_dave), ('Wes', percentage_wes), ('Steve', percentage_steve), ('Surat', percentage_surat), ('Justin', percentage_justin), ('Jake', percentage_jake), ('Matt', percentage_matt), ('Trevor',percentage_trevor)]
        sorted_percentage_list = sorted(percentage_list, key = lambda percents:percents[1], reverse = True)
        emoji = [':crown:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:', ':jakepuss:']
        # percentage_leaderboard = "Solo Queue Leaderboard\n" + emoji
        # percentage_leaderboard = "Solo Queue Leaderboard\n:crown:: " + str(sorted_percentage_list[0][0]) + ": " + str(sorted_percentage_list[0][1]) + "%, " + str(sorted_percentage_list[0][2]) + " Kills, "+ str(sorted_percentage_list[0][3]) + " K/G, " + str(sorted_percentage_list[0][4]) + " A/G, " + str(sorted_percentage_list[0][5]) + " CS/G" + "\n:two:: " + str(sorted_percentage_list[1][0]) + ": " + str(sorted_percentage_list[1][1]) + "%, " + str(sorted_percentage_list[1][2]) + " Kills, "+ str(sorted_percentage_list[1][3]) + " K/G, " + str(sorted_percentage_list[1][4]) + " A/G, " + str(sorted_percentage_list[1][5]) + " CS/G" + "\n:three:: " + str(sorted_percentage_list[2][0]) + ": " + str(sorted_percentage_list[2][1]) + "%, " + str(sorted_percentage_list[2][2]) + " Kills, "+ str(sorted_percentage_list[2][3]) + " K/G, " + str(sorted_percentage_list[2][4]) + " A/G, " + str(sorted_percentage_list[2][5]) + " CS/G" + "\n:four:: " + str(sorted_percentage_list[3][0]) + ": " + str(sorted_percentage_list[3][1]) + "%, " + str(sorted_percentage_list[3][2]) + " Kills, "+ str(sorted_percentage_list[3][3]) + " K/G, " + str(sorted_percentage_list[3][4]) + " A/G, " + str(sorted_percentage_list[3][5]) + " CS/G" + "\n:five:: " + str(sorted_percentage_list[4][0]) + ": " + str(sorted_percentage_list[4][1]) + "%, " + str(sorted_percentage_list[4][2]) + " Kills, "+ str(sorted_percentage_list[4][3]) + " K/G, " + str(sorted_percentage_list[4][4]) + " A/G, " + str(sorted_percentage_list[4][5]) + " CS/G" + "\n:six:: " + str(sorted_percentage_list[5][0]) + ": " + str(sorted_percentage_list[5][1]) + "%, " + str(sorted_percentage_list[5][2]) + " Kills, "+ str(sorted_percentage_list[5][3]) + " K/G, " + str(sorted_percentage_list[5][4]) + " A/G, " + str(sorted_percentage_list[5][5]) + " CS/G" + "\n:seven:: " + str(sorted_percentage_list[6][0]) + ": " + str(sorted_percentage_list[6][1]) + "%, " + str(sorted_percentage_list[6][2]) + " Kills, "+ str(sorted_percentage_list[6][3]) + " K/G, " + str(sorted_percentage_list[6][4]) + " A/G, " + str(sorted_percentage_list[6][5]) + " CS/G" + "\n:eight:: " + str(sorted_percentage_list[7][0]) + ": " + str(sorted_percentage_list[7][1]) + "%, " + str(sorted_percentage_list[7][2]) + " Kills, "+ str(sorted_percentage_list[7][3]) + " K/G, " + str(sorted_percentage_list[7][4]) + " A/G, " + str(sorted_percentage_list[7][5]) + " CS/G" + "\n:nine:: " + str(sorted_percentage_list[8][0]) + ": " + str(sorted_percentage_list[8][1]) + "%, " + str(sorted_percentage_list[8][2]) + " Kills, "+ str(sorted_percentage_list[8][3]) + " K/G, " + str(sorted_percentage_list[8][4]) + " A/G, " + str(sorted_percentage_list[8][5]) + " CS/G" + "\n:keycap_ten:: " + str(sorted_percentage_list[9][0]) + ": " + str(sorted_percentage_list[9][1]) + "%, " + str(sorted_percentage_list[9][2]) + " Kills, "+ str(sorted_percentage_list[9][3]) + " K/G, " + str(sorted_percentage_list[9][4]) + " A/G, " + str(sorted_percentage_list[9][5]) + " CS/G" + "\n:jakepuss:: " + str(sorted_percentage_list[10][0]) + ": " + str(sorted_percentage_list[10][1]) + "%, " + str(sorted_percentage_list[10][2]) + " Kills, "+ str(sorted_percentage_list[10][3]) + " K/G, " + str(sorted_percentage_list[10][4]) + " A/G, " + str(sorted_percentage_list[10][5]) + " CS/G"

        percentage_leaderboard = "Solo Queue Leaderboard\n:crown:: " + str(sorted_percentage_list[0][0]) + ": " + str(sorted_percentage_list[0][1]) + "%" + "\n:two:: " + str(sorted_percentage_list[1][0]) + ": " + str(sorted_percentage_list[1][1]) + "%" + "\n:three:: " + str(sorted_percentage_list[2][0]) + ": " + str(sorted_percentage_list[2][1]) + "%" + "\n:four:: " + str(sorted_percentage_list[3][0]) + ": " + str(sorted_percentage_list[3][1]) + "%" + "\n:five:: " +  str(sorted_percentage_list[4][0]) + ": " + str(sorted_percentage_list[4][1]) + "%" + "\n:six:: " + str(sorted_percentage_list[5][0]) + ": " + str(sorted_percentage_list[5][1]) + "%" + "\n:seven:: " + str(sorted_percentage_list[6][0]) + ": " + str(sorted_percentage_list[6][1]) + "%" + "\n:eight:: " + str(sorted_percentage_list[7][0]) + ": " + str(sorted_percentage_list[7][1]) + "%" + "\n:nine:: " + str(sorted_percentage_list[8][0]) + ": " + str(sorted_percentage_list[8][1]) + "%" + "\n:keycap_ten:: " + str(sorted_percentage_list[9][0]) + ": " + str(sorted_percentage_list[9][1]) + "%" "\n:jakepuss:: " + str(sorted_percentage_list[10][0]) + ": " + str(sorted_percentage_list[10][1]) + "%"
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
        city = location['results'][0]['address_components'][1]['long_name']
        summary = weather['currently']['summary']
        current_weather = "It is currently " + str(temperature) + " degrees fahrenheit in "+ city + " and the weather is " + str(summary)
        self.send_message(channel_id, current_weather)
    # def common_elements(l1, l2):
    #     result = []
    #     for element in l1:
    #         if element in l2:
    #             result.append(element)
    #     return result

    def write_duo(self, channel_id, person1, person2):
        json_p1Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person1 + '?api_key=' + riot)
        p1Id = json.load(json_p1Id)
        p1 = p1Id['accountId']
        json_p2Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person2 +'?api_key=' + riot)
        p2Id = json.load(json_p2Id)
        p2 = p2Id['accountId']
        json_player1 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p1) + '?queue=420&api_key=' + riot)
        player1 = json.load(json_player1)
        json_player2 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p2) + '?queue=420&api_key=' + riot)
        player2 = json.load(json_player2)
        player1_matchlist = []
        player2_matchlist =[]
        wins = 0
        for x in range(len(player1['matches'])):
            player1_matchlist.append(player1['matches'][x]['gameId'])
        for x in range(len(player2['matches'])):
            player2_matchlist.append(player2['matches'][x]['gameId'])
        common_matches = list(set(player1_matchlist).intersection(player2_matchlist))
        common_matches_length = len(common_matches)
        time_amt = common_matches_length * 2
        time_msg = "You have %d games played together, it will take around %d seconds to figure out your win percentage." % (common_matches_length, time_amt)
        self.send_message(channel_id, time_msg)
        time.sleep(1)
        for x in range(common_matches_length):
            json_match = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matches/' + str(common_matches[x]) + '?api_key='+ riot)
            match = json.load(json_match)
            for i in range(10):
                if match['participantIdentities'][i]['player']['accountId'] == p1 or match['participantIdentities'][i]['player']['accountId'] == p2:
                    p_gameId = match['participantIdentities'][i]['participantId']
            if match['participants'][p_gameId - 1]['stats']['win'] == True:
                wins += 1
        duo_percentage = float(wins)/float(common_matches_length) * 100
        msg = "Win Percent: %.2f%%" % duo_percentage
        self.send_message(channel_id, msg)

    def write_trio(self, channel_id, person1, person2, person3):
        json_p1Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person1 + '?api_key=' + riot)
        p1Id = json.load(json_p1Id)
        p1 = p1Id['accountId']
        json_p2Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person2 +'?api_key=' + riot)
        p2Id = json.load(json_p2Id)
        p2 = p2Id['accountId']
        json_p3Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person3 + '?api_key=' + riot)
        p3Id = json.load(json_p3Id)
        p3 = p3Id['accountId']
        json_player1 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p1) + '?queue=440&api_key=' + riot)
        player1 = json.load(json_player1)
        json_player2 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p2) + '?queue=440&api_key=' + riot)
        player2 = json.load(json_player2)
        json_player3 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p3) + '?queue=440&api_key=' + riot)
        player3 = json.load(json_player3)
        player1_matchlist = []
        player2_matchlist =[]
        player3_matchlist = []
        wins = 0
        for x in range(len(player1['matches'])):
            player1_matchlist.append(player1['matches'][x]['gameId'])
        for x in range(len(player2['matches'])):
            player2_matchlist.append(player2['matches'][x]['gameId'])
        for x in range(len(player3['matches'])):
            player3_matchlist.append(player3['matches'][x]['gameId'])
        common_matches = list(set(player1_matchlist) & set(player2_matchlist) & set(player3_matchlist))
        common_matches_length = len(common_matches)
        time_amt = common_matches_length * 2
        time_msg = "You have %d games played together, it will take around %d seconds to figure out your win percentage." % (common_matches_length, time_amt)
        self.send_message(channel_id, time_msg)
        time.sleep(1)
        for x in range(common_matches_length):
            json_match = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matches/' + str(common_matches[x]) + '?api_key='+ riot)
            match = json.load(json_match)
            for i in range(10):
                if match['participantIdentities'][i]['player']['accountId'] == p1 or match['participantIdentities'][i]['player']['accountId'] == p2 or match['participantIdentities'][i]['player']['accountId'] == p3:
                    p_gameId = match['participantIdentities'][i]['participantId']
            if match['participants'][p_gameId - 1]['stats']['win'] == True:
                wins += 1
        duo_percentage = float(wins)/float(common_matches_length) * 100
        msg = "Win Percent: %.2f%%" % duo_percentage
        self.send_message(channel_id, msg)

    def write_5s(self, channel_id, person1, person2, person3, person4, person5):
        json_p1Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person1 + '?api_key=' + riot)
        p1Id = json.load(json_p1Id)
        p1 = p1Id['accountId']
        json_p2Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person2 +'?api_key=' + riot)
        p2Id = json.load(json_p2Id)
        p2 = p2Id['accountId']
        json_p3Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person3 + '?api_key=' + riot)
        p3Id = json.load(json_p3Id)
        p3 = p3Id['accountId']
        json_p4Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person4 +'?api_key=' + riot)
        p4Id = json.load(json_p4Id)
        p4 = p4Id['accountId']
        json_p5Id = urllib2.urlopen('https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/' + person5 + '?api_key=' + riot)
        p5Id = json.load(json_p5Id)
        p5 = p5Id['accountId']
        json_player1 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p1) + '?queue=440&api_key=' + riot)
        player1 = json.load(json_player1)
        json_player2 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p2) + '?queue=440&api_key=' + riot)
        player2 = json.load(json_player2)
        json_player3 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p3) + '?queue=440&api_key=' + riot)
        player3 = json.load(json_player3)
        json_player4 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p4) + '?queue=440&api_key=' + riot)
        player4 = json.load(json_player4)
        json_player5 = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/' + str(p5) + '?queue=440&api_key=' + riot)
        player5 = json.load(json_player5)
        player1_matchlist = []
        player2_matchlist =[]
        player3_matchlist = []
        player4_matchlist =[]
        player5_matchlist = []
        wins = 0
        for x in range(len(player1['matches'])):
            player1_matchlist.append(player1['matches'][x]['gameId'])
        for x in range(len(player2['matches'])):
            player2_matchlist.append(player2['matches'][x]['gameId'])
        for x in range(len(player3['matches'])):
            player3_matchlist.append(player3['matches'][x]['gameId'])
        for x in range(len(player4['matches'])):
            player4_matchlist.append(player4['matches'][x]['gameId'])
        for x in range(len(player5['matches'])):
            player5_matchlist.append(player5['matches'][x]['gameId'])
        common_matches = list(set(player1_matchlist) & set(player2_matchlist) & set(player3_matchlist) & set(player4_matchlist) & set(player5_matchlist))
        common_matches_length = len(common_matches)
        time_amt = common_matches_length * 2
        time_msg = "You have %d games played together, it will take around %d seconds to figure out your win percentage." % (common_matches_length, time_amt)
        self.send_message(channel_id, time_msg)
        time.sleep(1)
        for x in range(common_matches_length):
            json_match = urllib2.urlopen('https://na1.api.riotgames.com/lol/match/v3/matches/' + str(common_matches[x]) + '?api_key='+ riot)
            match = json.load(json_match)
            for i in range(10):
                if match['participantIdentities'][i]['player']['accountId'] == p1 or match['participantIdentities'][i]['player']['accountId'] == p2 or match['participantIdentities'][i]['player']['accountId'] == p3:
                    p_gameId = match['participantIdentities'][i]['participantId']
            if match['participants'][p_gameId - 1]['stats']['win'] == True:
                wins += 1
        duo_percentage = float(wins)/float(common_matches_length) * 100
        msg = "Win Percent: %.2f%%" % duo_percentage
        self.send_message(channel_id, msg)
        
    def write_duo_db(self, channel_id, person1, person2):
        self.clients.send_user_typing_pause(channel_id)
        person1_match_id = []
        person2_match_id = []
        json_match_list_person1 = requests.get('https://mottbot.herokuapp.com/trevor/dave') #+ str(person1) + '/' + str(person2))
        jsondata = json_match_list_person1.json()
        duo_percentage = jsondata['win_percent']

        self.send_message(channel_id,duo_percentage)
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
