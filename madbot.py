#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#--------------------  [O_o]  ---------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
#--------------------------------------------------#

import irclib
import ircbot
import urllib
import urllib2
import MySQLdb
import BeautifulSoup
import json
import unicodedata
from urllib2 import urlopen, URLError, HTTPError
from json import loads
from random import randrange
from django.utils.encoding import smart_str, smart_unicode
from settings import settings

(
    bot_owner, bot_name, bot_description, server_irc, server_port,
    channels, nickserv_pass, mysql_host, mysql_user, mysql_pass,
    mysql_db, meteo_api_key, geoips_api_key, google_api_key,
    admin_users, database_user, database_pass, database_url,
    team_users, bad, slap, hit, sex, kiss, options, utils, help
) = settings()

class bot(ircbot.SingleServerIRCBot):

    def __init__(self):
        ircbot.SingleServerIRCBot.__init__(
                self, [(server_irc, server_port)],
                bot_name, bot_description)

        self.owner = [bot_owner, bot_name]
        self.timer = None

    def on_welcome(self, serv, ev):
        serv.privmsg("nickserv", "identify "+nickserv_pass)
        serv.privmsg("chanserv", "set irc_auto_rejoin ON")
        serv.privmsg("chanserv", "set irc_join_delay 0")
        serv.join(channels)

    def on_kick(self, serv, ev):
        chan =  ev.target()
        serv.join(chan)

    def on_privmsg(self, serv, ev):
        author = irclib.nm_to_n(ev.source())
        message = ev.arguments()[0].strip()
        arguments = message.split(' ')
        nombreArg = len(arguments)

        #---[ OWNER OPTIONS ]---#
        if (author == bot_owner):
            if nombreArg == 1 and '!exit' == arguments[0]:
                serv.disconnect("See you later girls, just need a break !")
            elif nombreArg == 1 and '!exit' != arguments[0]:
                serv.privmsg(author, "n00b :p !")
            elif '!say' == arguments[0]:
                serv.privmsg(arguments[1], message.replace('!say', '')\
                    .replace(arguments[1], '')[2:])
            elif '!act' == arguments[0]:
                serv.action(arguments[1], message.replace('!act', '')\
                    .replace(arguments[1], '')[2:])
            elif '!j' == arguments[0]:
                serv.join(message[3:])
            elif '!p' == arguments[0]:
                serv.part(message[3:])
            else:
                serv.privmsg(author, "n00b "+author+" ! "
                    "Tu causes à ton bot là !")
        else:
            serv.privmsg(author, "Hey "+author+", t'as craqué ou quoi ? "\
                "Tu causes à un bot là, spice de n00b !")

    def on_pubmsg(self, serv, ev):
        db = MySQLdb.connect(
            host=mysql_host, user=mysql_user,
            passwd=mysql_pass, db=mysql_db)

        cur = db.cursor()
        author = irclib.nm_to_n(ev.source())
        chan = ev.target()
        chan_verif = (ev.target(), self.channels[ev.target()])
        message = ev.arguments()[0].strip()
        arguments = message.split(" ")
        nombreArg = len(arguments)
        droit = randrange(1,9)

        #---[ AUTHOR LEVEL ]---#
        if author in self.owner:
            level = "9"
        elif author in admin_users:
            level = "8"
        elif chan_verif[1].has_user(author)\
                and chan_verif[1].is_oper(author):
            level = "5"
        elif chan_verif[1].has_user(author)\
                and chan_verif[1].is_halfoper(author):
            level = "4"
        elif chan_verif[1].has_user(author)\
                and chan_verif[1].is_voiced(author):
            level = "3"
        else:
            level = "1"

        #---[ TARGET LEVEL ]---#
        if nombreArg >= 2:
            if arguments[1] in self.owner:
                target = "9"
            elif arguments[1] in admin_users:
                target = "8"
            elif chan_verif[1].has_user(arguments[1])\
                    and chan_verif[1].is_oper(arguments[1]):
                target = "5"
            elif chan_verif[1].has_user(arguments[1])\
                    and chan_verif[1].is_halfoper(arguments[1]):
                target = "4"
            elif chan_verif[1].has_user(arguments[1])\
                    and chan_verif[1].is_voiced(arguments[1]):
                target = "3"
            else:
                target = "1"

        #---[ ERRORS MESSAGES ]---#
        def error_message():
            serv.action(
                chan, "slaps "+author+" ! Bad request ("+arguments[0]\
                .replace("!", "")+"), try something like !help :p")

        def powa_message():
            serv.action(
                chan, "slaps "+author+" ! You are not allowed to use this"\
                " option ("+error.replace("!", "")+"), you need more powa !")

        def modif_powa_message():
            serv.action(
                chan, "slaps "+author+" ! You are not "\
                "allowed to modify "+arguments[1]+" powa !")

        def n00b_message():
            serv.action(chan, "slaps "+author+" ! You need help ? :p")

        def unknow_message():
            serv.action(
                chan, "slaps "+author+" ! n00b, "+arguments[1]+\
                " is not on this channel !")

        def nothing_message():
            serv.privmsg(chan, "Nothing found ! Sorry about this :p")

        for error in options:
            if error == arguments[0] and level <= "2":
                powa_message()
                break

        #---[ HELP ]---#
        if "!help" == arguments[0] and level > "2" and nombreArg == 1:
            for x in range(0, 65):
                serv.privmsg(author, help[x])
                x = x + 1

        #---[ DATABASE ]---#
        if "!add" == arguments[0] and level > "2":
            if author in team_users:
                if nombreArg == 1:
                    error_message()
                else:
                    try:
                        ID_imdb = arguments[1]
                        ID_user = irclib.nm_to_n(ev.source())
                        url = database_url
                        username = database_user
                        password = database_pass
                        p = urllib2.HTTPPasswordMgrWithDefaultRealm()
                        p.add_password(None, url, username, password)
                        handler = urllib2.HTTPBasicAuthHandler(p)
                        opener = urllib2.build_opener(handler)
                        urllib2.install_opener(opener)
                        values = dict(imdb=ID_imdb, user=ID_user)
                        data = urllib.urlencode(values)
                        req = urllib2.Request(url, data)
                        rsp = urllib2.urlopen(req)
                        content = rsp.read()
                        serv.privmsg(
                            chan, ("> Release added in Database "\
                            ": "+database_url+" !"))
                    except (HTTPError,ValueError,IOError) as e:
                        serv.privmsg(chan, str(e))
                        pass
            else:
                serv.action(
                    chan, "slaps "+author+" ! You are not allowed "\
                    "to use this option, only for team members !")

        #------------------#
        #---  SERVICES  ---#
        #------------------#

        #---[ METEO ]---#
        def meteo():
            try:
                id = message[7:].replace(' ', '+')
                data_id =  loads(urlopen("http://autocomplete"\
                    ".wunderground.com/aq?query="+id).read())
                city = data_id["RESULTS"][0]["name"]
                city_id = data_id["RESULTS"][0]["l"]
                data = loads(urlopen(\
                    "http://api.wunderground.com/api/"+meteo_api_key+
                    "/forecast"+city_id+".json").read())
                weather = smart_str(data["forecast"]["txt_forecast"]\
                    ["forecastday"][0]["fcttext_metric"])
                serv.privmsg(chan, "Weather in "+city+" : "+weather)
            except (ValueError, KeyError, TypeError, IndexError) as e:
                serv.privmsg(chan, ("JSON Error : "+str(e)))
                pass

        #---[ MAPS DISTANCE ]---#
        def dist():
            try:
                id = message[6:].split(' / ')
                origin = id[0].replace(' ', '+')
                destination = id[1].replace(' ', '+')
                data = loads(urlopen(\
                    "https://maps.googleapis.com/maps/api/"\
                    "directions/json?origin="+origin+"&destination"\
                    "="+destination+"&key="+google_api_key).read())
                km = smart_str(data["routes"][0]["legs"][0]\
                    ["distance"]["text"])
                time = smart_str(data["routes"][0]["legs"][0]\
                    ["duration"]["text"])
                start = smart_str(data["routes"][0]["legs"][0]\
                    ["start_address"])
                end = smart_str(data["routes"][0]["legs"][0]\
                    ["end_address"])
                serv.privmsg(chan, start+" to "+end+" : "+km+" - "+time)
            except (ValueError, KeyError, TypeError, IndexError) as e:
                serv.privmsg(chan, ("JSON Error : "+str(e)))
                pass

        #---[ IP FINDER ]---#
        def ip():
            arg = message[4:].replace(' ', '')
            if arg.replace('.', '').isdigit():
                info = arg
            else:
                try:
                    soup = BeautifulSoup.BeautifulSoup(urlopen(
                        "http://www.topwebhosts.org/tools/lookup.php?"\
                        "query="+arg+"&submit=Search"))
                    for items in soup.findAll( 'blockquote' ):
                        resp = items.find("font", attrs={'color':'blue'})
                        info = resp.contents[0].strip()
                except (HTTPError,ValueError,IOError) as e:
                    serv.privmsg(chan, str(e))
                    pass
            if info.replace('.', '').isdigit():
                try:
                    data = loads(urlopen("http://api.geoips.com/ip/"+info+\
                        "/key/"+geoips_api_key+\
                        "/output/json/hostname/true").read())
                    owner = smart_str(
                        data["response"]["location"]["owner"])
                    host = smart_str(
                        data["response"]["location"]["hostname"])
                    city = smart_str(
                        data["response"]["location"]["city_name"])
                    country = smart_str(
                        data["response"]["location"]["country_name"])
                    continent = smart_str(
                        data["response"]["location"]["continent_name"])
                    serv.privmsg(
                        chan, owner+" - "+city+" - "+country+" "\
                        "- "+continent+" ("+info+" - "+host+")")
                except (ValueError, KeyError, TypeError, IndexError) as e:
                    serv.privmsg(chan, ("JSON Error : "+str(e)))
                    pass
            else:
                nothing_message()

        #---[ SOUS-TITRES.EU ]---#
        def srt():
            try:
                id = message[5:].replace(' ', '+')
                soup = BeautifulSoup.BeautifulSoup(urlopen(\
                    "https://www.sous-titres.eu/search.html?q="+id))
                if not soup.findAll('li', 'noResult'):
                    for items in soup.findAll('h3'):
                        link = items.find('a')
                        link.get('href')
                        serv.privmsg(
                            chan, ("%s : https://www.sous-titres.eu/%s" %\
                            (unicodedata.normalize('NFKD', link\
                            .contents[0]).encode('ascii','ignore'), link\
                            ["href"])))
                        break
                else:
                    nothing_message()
            except (HTTPError,ValueError,IOError) as e:
                serv.privmsg(chan, str(e))
                pass

         #---[ SUB-SYNCHRO ]---#
        def sub():
            try:
                id = message[5:].replace(' ', '+')
                soup = BeautifulSoup.BeautifulSoup(urlopen(\
                    "http://www.subsynchro.com/?q="+id))
                if not soup.find('li', 'aucun'):
                    for items in soup.findAll('li', 'col1'):
                        link = items.find('a')
                        link.get('href')
                        name = items.find('img')
                        name.get('title')
                        serv.privmsg(
                            chan, ("%s : http://www.subsynchro.com/%s" %\
                            (name["title"], link["href"])))
                        break
                else:
                    nothing_message()
            except (HTTPError,ValueError,IOError) as e:
                serv.privmsg(chan, str(e))
                pass

         #---[ IMDB ]---#
        def imdb():
            try:
                id = message[6:].replace(' ', '+')
                soup = BeautifulSoup.BeautifulSoup(urlopen(\
                    "http://www.imdb.com/find?q="+id+"&s=tt"))
                if not soup.findAll('div', 'findNoResults'):
                    for items in soup.findAll('td', 'result_text'):
                        link = items.find('a')
                        link.get('href')
                        serv.privmsg(
                            chan, ("%s : http://www.imdb.com%s" %\
                            (unicodedata.normalize('NFKD', link\
                            .contents[0]).encode('ascii','ignore'),
                            link["href"][:-17])))
                        break
                else:
                    nothing_message()
            except (HTTPError,ValueError,IOError) as e:
                serv.privmsg(chan, str(e))
                pass

         #---[ TMDB MOVIES ]---#
        def tmdb():
            try:
                id = message[6:].replace(' ', '+')
                soup = BeautifulSoup.BeautifulSoup(urlopen\
                    ("http://www.themoviedb.org/search/movie?query="+id))
                if soup.findAll('ul', 'search_results movie'):
                    for items in soup.findAll('div', 'poster'):
                        link = items.find("a")
                        data = items.find("img")
                        link.get("href")
                        link.get("title")
                        cover = data.get("src").split('/')[-1:]
                        serv.privmsg(
                            chan, ("%s : http://www.themoviedb.org%s" %\
                            (link["title"], link["href"])))
                        serv.privmsg(
                            chan, ("Cover : http://image.tmdb.org/t/p/"\
                            "original/%s" % (cover[0])))
                        break
                else:
                    nothing_message()
            except (HTTPError,ValueError,IOError) as e:
                serv.privmsg(chan, str(e))
                pass

        #---[ TMDB TV ]---#
        def tv():
            try:
                id = message[4:].replace(' ', '+')
                soup = BeautifulSoup.BeautifulSoup(urlopen(
                    "http://www.themoviedb.org/search/tv?query="+id))
                if soup.findAll('ul', 'search_results tv'):
                    for items in soup.findAll('div', 'poster'):
                        link = items.find("a")
                        data = items.find("img")
                        link.get("href")
                        link.get("title")
                        cover = data.get("src").split('/')[-1:]
                        serv.privmsg(
                            chan, ("%s : http://www.themoviedb.org%s" %\
                            (link["title"], link["href"])))
                        serv.privmsg(
                            chan, ("Cover : http://image.tmdb.org/t/p"\
                            "/original/%s" % (cover[0])))
                        break
                else:
                    nothing_message()
            except (HTTPError,ValueError,IOError) as e:
                serv.privmsg(chan, str(e))
                pass

        #---[ ALLOCINE ]---#
        def allo():
            try:
                id = message[6:].replace(' ', '+')
                soup = BeautifulSoup.BeautifulSoup(urlopen(\
                    "http://www.allocine.fr/recherche/1/?q="+id))
                if not soup.findAll('script', id='noresults'):
                    for items in soup.findAll('div', 'vmargin10t'):
                        link = items.find("a")
                        data = items.find("img")
                        link.get("href")
                        data.get("alt")
                        serv.privmsg(
                            chan, ("%s : http://www.allocine.fr/%s" %\
                            (data["alt"], link["href"])))
                        break
                else:
                    nothing_message()
            except (HTTPError,ValueError,IOError) as e:
                serv.privmsg(chan, str(e))
                pass

         #---[ GOOGLE ]---#
        def google():
            url = "http://www.google.com/search?q="+message[8:]\
                .replace(' ', '+')
            serv.privmsg(chan, url)

        #---[ GOOGLE IMAGES ]---#
        def img():
            url = "https://www.google.com/search?site=imghp&tbm=isch&s"\
                "ource=hp&biw=1920&bih=969&q="+message[5:]\
                .replace(' ', '+')
            serv.privmsg(chan, url)

        #---[ YOUTUBE ]---#
        def tub():
            url = "http://www.youtube.com/results?search_query"\
                "="+message[5:].replace(' ', '+')
            serv.privmsg(chan, url)

         #---[ DAILYMOTION ]---#
        def daily():
            url = "http://www.dailymotion.com/fr/relevance/search"\
                "/"+message[7:].replace(' ', '+')
            serv.privmsg(chan, url)

        #---[ SOUNDCLOUD ]---#
        def sound():
            url = "https://soundcloud.com/search?q="+message[7:]\
                .replace(' ', '+')
            serv.privmsg(chan, url)

        #---[ UTILITAIRES PROCESS ]---#
        for option in utils:
            if option == arguments[0] and level > "2":
                if nombreArg == 1:
                    error_message()
                    break
                else:
                    fonction = eval(option.replace('!', ''))
                    fonction()
                    break

        #-----------------#
        #---  FANTASY  ---#
        #-----------------#

        #---[ BAD WORDS ]---#
        for mot in bad:
            if mot in message.lower() :
                serv.kick(
                    chan, author, "w00ps, you said something wrong,"\
                    " <"+mot+"> is not allowed here !")
                break

        #---[ QUiZZ ]---#
        def select_question():
            serv.privmsg(chan, "Quizz : vous avez 30 secondes pour répondre"\
                ", attention à l'orthographe ! Bonne chance !")
            for x in range(0,3236):
                try:
                    select = random.choice(open('quizz.txt').readlines())
                except IOError:
                    serv.privmsg(chan, "Error, file quizz.txt not found on "\
                        "owner's system !")
                    pass
                break
            self.quizz = select.split(" | ")
            serv.privmsg(chan, "> "+self.quizz[0])
            self.timer = threading.Timer(30.0, end)
            self.timer.start()

        def end():
            soluce = self.quizz[1].replace('Ã¢', 'â').replace('Ã©', 'é')\
                .replace('Ã¨', 'è').replace('Ãª', 'ê').replace('Ã«', 'ë')\
                .replace('Ã§', 'ç').replace('Ã¹', 'ù').replace('Ã»', 'û')\
                .replace('Ã®', 'î').replace('Ã¯', 'ï').replace('Ã´', 'ô')\
                .replace('Å“', 'œ').replace('Ã', 'à')
            serv.privmsg(chan, "Bande de n00bs, la réponse était : "+soluce)
            self.quizz = None
            self.timer = None

        if '!quizz' == arguments[0] and level > "2":
            if self.timer != None:
                serv.privmsg(
                    chan, "n00b "+author+" ! A quizz is already running :p")
            else:
                if nombreArg == 1:
                    import time, random, threading
                    select_question()
                else:
                    error_message()

        try:
            if self.quizz[1].replace('-', ' ').replace('.', '').strip()\
                    .lower() == message.replace('-', ' ').strip().lower():
                serv.privmsg(
                    chan, "Bien joué "+author+" ! La bonne réponse"\
                        " est bien : "+self.quizz[1])
                self.quizz = None
                self.timer.cancel()
                self.timer = None
        except (AttributeError, TypeError):
            pass

        #---[ QUOTE ]---#
        if '!quote' == arguments[0] and level > "2":
            if (nombreArg == 2) and ((chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users)):
                try:
                    cur.execute("SELECT * FROM quote WHERE user = %s ORDER "\
                        "BY RAND() LIMIT 1", arguments[1])
                    record = cur.fetchone()
                    if not record:
                        nothing_message()
                    else:
                        serv.privmsg(chan, record[2])
                except MySQLdb.Error, e:
                    serv.privmsg(chan, "MySql Error : "+str(e))
                    pass
                cur.close()
            elif nombreArg == 1:
                try:
                    cur.execute("SELECT * FROM quote ORDER BY RAND() LIMIT 1")
                    record = cur.fetchone()
                    if not record:
                        nothing_message()
                    else:
                        serv.privmsg(chan, record[2])
                except MySQLdb.Error, e:
                    serv.privmsg(chan, "MySql Error : "+str(e))
                    pass
                cur.close()
            else:
                if nombreArg != 3:
                    error_message()
                elif (chan_verif[1].has_user(arguments[1]))\
                        or (arguments[1] in self.owner)\
                        or (arguments[1] in admin_users):
                    if arguments[2] == "all":
                        try:
                            cur.execute("SELECT * FROM quote WHERE user ="\
                                " %s", arguments[1])
                            record = cur.fetchall()
                            if not record:
                                nothing_message()
                            else:
                                for row in record:
                                    serv.privmsg(
                                        chan, row[2]+" [Quoted by"\
                                        " "+row[3]+" on "+str(row[4])+"]")
                        except MySQLdb.Error, e:
                            serv.privmsg(chan, "MySql Error : "+str(e))
                            pass
                        cur.close()
                    elif arguments[2].isdigit():
                        try:
                            cur.execute("SELECT * FROM quote WHERE user ="\
                                " %s ORDER BY id ASC LIMIT %s,1",\
                                [arguments[1],int(arguments[2])-1])
                            record = cur.fetchone()
                            if not record:
                                nothing_message()
                            else:
                                serv.privmsg(chan, record[2])
                        except MySQLdb.Error, e:
                            serv.privmsg(chan, "MySql Error : "+str(e))
                            pass
                        cur.close()
                    else:
                        error_message()
                else:
                    unknow_message()

        #---[ QUOTE_ADD ]---#
        if '!quoteadd' == arguments[0] and level > "2":
            if nombreArg <= 2:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                try:
                    cur.execute("SELECT * FROM quote WHERE user = %s"\
                        " AND text = %s", [arguments[1],\
                        arguments[1]+" : "+message.replace('!quoteadd', '')\
                        .replace(arguments[1], '')[2:]])
                    record = cur.fetchone()
                    if not record:
                        try:
                            cur.execute("INSERT INTO quote(user, text,"\
                                " author)VALUES(%s, %s, %s)",\
                                [arguments[1],arguments[1]+" "\
                                ": "+message.replace('!quoteadd', '')\
                                .replace(arguments[1], '')[2:],author])
                            db.commit()
                            serv.privmsg(
                                chan, "nice job "+author+\
                                ", new quote added !")
                        except MySQLdb.Error, e:
                            serv.privmsg(chan, "MySql Error : "+str(e))
                    else:
                        serv.privmsg(
                            chan, "n00b "+author+" ! "\
                            "This quote already exist !")
                except MySQLdb.Error, e:
                    serv.privmsg(chan, "MySql Error : "+str(e))
                    pass
                cur.close()
            else:
                unknow_message()

        #---[ QUOTE_DEL ]---#
        if '!quotedel' == arguments[0] and level == "9":
            if nombreArg != 3:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if arguments[2] == "all":
                    try:
                        cur.execute("SELECT * FROM quote WHERE user ="\
                            " %s", arguments[1])
                        record = cur.fetchall()
                        if not record:
                            serv.privmsg(
                                chan, "n00b "+author+" ! This user "\
                                "doesn't have quotes !")
                        else:
                            try:
                                cur.execute("DELETE FROM quote WHERE "\
                                    "user = %s", arguments[1])
                                db.commit()
                                serv.privmsg(
                                    chan, "nice job "+author+", all"\
                                    " "+arguments[1]+"'s quotes deleted !")
                            except MySQLdb.Error, e:
                                serv.privmsg(chan, "MySql Error : "+str(e))
                    except MySQLdb.Error, e:
                        serv.privmsg(chan, "MySql Error : "+str(e))
                        pass
                    cur.close()
                elif arguments[2].isdigit():
                    try:
                        cur.execute("SELECT * FROM quote WHERE user = %s"\
                            " ORDER BY id ASC LIMIT %s,1",\
                            [arguments[1],int(arguments[2])-1])
                        record = cur.fetchone()
                        if not record:
                            serv.privmsg(
                                chan, "n00b "+author+" ! "\
                                "This quote doesn't exist !")
                        else:
                            try:
                                cur.execute("DELETE FROM quote WHERE user"\
                                    " = %s AND text = %s",\
                                    [arguments[1],record[2]])
                                db.commit()
                                serv.privmsg(
                                    chan, "nice job "+author+\
                                    ", quote deleted !")
                            except MySQLdb.Error, e:
                                serv.privmsg(chan, "MySql Error : "+str(e))
                    except MySQLdb.Error, e:
                        serv.privmsg(chan, "MySql Error : "+str(e))
                        pass
                    cur.close()
                else:
                    error_message()
            else:
                unknow_message()
        elif '!quotedel' == arguments[0] and level <= "8":
            powa_message()

        #---[ BEER ]---#
        if '!beer' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, author+" boit une bière en juif !")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" paye sa tournée de bière !")
            elif (author == arguments[1]):
                n00b_message()
            elif (droit == 1) or (droit == 2):
                serv.privmsg(
                    chan, "Oups "+arguments[1]+" a trop bu de bière "\
                    "today ! "+author+" prend la relève !")
            elif (droit == 3) or (droit == 4):
                serv.privmsg(
                    chan, "Oula "+arguments[1]+" est complètement bourré"\
                    " ! "+author+" se sauve avec le pack !")
            else:
                serv.privmsg(
                    chan, author+" paye une bière à "+arguments[1]+" !")

        #---[ BEDO ]---#
        if '!bedo' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, author+" fume un bédo en juif !")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" paye sa tournée de weed !")
            elif (author == arguments[1]):
                n00b_message()
            elif (droit == 1) or (droit == 2):
                serv.privmsg(
                    chan, "Oups "+arguments[1]+" a trop fumé today"\
                    " ! "+author+" reprend son du !")
            elif (droit == 3) or (droit == 4):
                serv.privmsg(
                    chan, "Oula "+arguments[1]+" est complètement défoncé"\
                    " ! "+author+" se sauve avec la fume !")
            else:
                serv.privmsg(
                    chan, author+" paye un bédo à "+arguments[1]+" !")

        #---[ SEX ]---#
        if '!sex' == arguments[0] and level > "2":
            action = randrange(0,len(sex))
            if nombreArg == 1:
                serv.privmsg(
                    chan, "OMG "+author+" est en manque !"\
                    " Go buy a toy baby, ça ira mieux :p")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" fou le chan AWALP !")
            elif (arguments[1].lower() == bot_owner and bot_owner != author):
                serv.action(
                    chan, "viole subtilement "+author+" !"\
                    " Pas touche à "+bot_owner+" !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, author+" "+sex[action]+arguments[1])

        #---[ SLAP ]---#
        if '!slap' == arguments[0] and level > "2":
            action = randrange(0,len(slap))
            if nombreArg == 1:
                serv.action(chan, "slaps "+author+" "+slap[action])
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" slaps le chan "+slap[action])
            elif (arguments[1].lower() == bot_owner and bot_owner != author):
                serv.action(
                    chan, "slaps "+author+" "+slap[action]+\
                    " ! Pas touche à "+bot_owner+" !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(
                    chan, author+" slaps "+arguments[1]+" "+slap[action])

        #---[ HIT ]---#
        if '!hit' == arguments[0] and level > "2":
            action = randrange(0,len(hit))
            if nombreArg == 1:
                serv.action(chan, hit[action]+author)
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" "+hit[action]+"tout le monde !")
            elif (arguments[1].lower() == bot_owner and bot_owner != author):
                serv.action(
                    chan, hit[action]+author+\
                    " ! Pas touche à "+bot_owner+" !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, author+" "+hit[action]+arguments[1])

        #---[ BIFFLE ]---#
        if '!bif' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.action(chan, " biffle "+author+" !")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" biffle le chan !")
            elif (author == arguments[1]):
                n00b_message()
            elif (arguments[1].lower() == bot_owner and bot_owner != author):
                serv.action(
                    chan, hit[action]+" "+author+\
                    " ! Pas touche à "+bot_owner+" !")
            else:
                serv.privmsg(chan, author+" biffle "+arguments[1])

        #---[ KISS ]---#
        if '!kiss' == arguments[0] and level > "2":
            action = randrange(0,len(kiss))
            if nombreArg == 1:
                serv.action(chan, "w00t... pas de bisous pour "+author)
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" paye sa tournée de bisous !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, author+" "+kiss[action]+arguments[1])

        #---[ CAFE ]---#
        if '!caf' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, "pas de café pour "+author+" !")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" paye sa tournée de kawa !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, author+" paye son café à "+arguments[1])

        #---[ HUG ]---#
        if '!hug' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, "pas de calin pour "+author+" !")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" fait un gros calin au chan !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, author+" caline "+arguments[1])

        #---[ CHAMP ]---#
        if '!champ' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, "pas de champagne pour "+author+" !")
            elif (arguments[1] == "all"):
                serv.privmsg(chan, author+" paye sa tournée de champagne !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(
                    chan, author+" paye le champagne à "+arguments[1])

        #---[ WOMP ]---#
        if '!womp' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, "http://wompwompwomp.com/ "+author+" :p")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(
                    chan, "http://wompwompwomp.com/ "+arguments[1]+" :p")

        #---[ GG ]---#
        if '!gg' == arguments[0] and level > "2":
            if nombreArg == 1:
                error_message()
            elif (arguments[1] == "all"):
                serv.privmsg(chan, "GG tout le monde !")
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, "Bien joué "+arguments[1]+" ! Congrats !")

        #---[ OUT ]---#
        if '!out' == arguments[0] and level > "2":
            if nombreArg == 1:
                serv.privmsg(chan, author+" is out !")
            else:
                error_message()

        #---[ ISOUT ]---#
        if '!isout' == arguments[0] and level > "2":
            if nombreArg == 1:
                error_message()
            elif (author == arguments[1]):
                n00b_message()
            else:
                serv.privmsg(chan, arguments[1]+" is out !")

        #---------------------#
        #---  IRC OPTIONS  ---#
        #---------------------#

        #---[ EXEMPT ]---#
        if '!e' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            else:
                serv.mode(chan, "+e "+arguments[1])
        elif '!e' == arguments[0] and level <= "3":
            powa_message()

        #---[ REMOVE EXEMPT ]---#
        if '!de' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif level >= target:
                serv.mode(chan, "-e "+arguments[1])
            else:
                serv.privmsg(
                    chan, author+" is not allowed to "\
                    "remove "+arguments[1]+" exempt !")
        elif '!de' == arguments[0] and level <= "3":
            powa_message()

        #---[ KICK ]---#
        if '!k' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    if nombreArg == 2:
                        serv.kick(chan_verif[0], arguments[1], author)
                    else:
                        serv.kick(
                            chan_verif[0], arguments[1], message\
                            .replace('!k', '').replace(\
                            arguments[1], '')[2:]+' ('+author+')')
                else:
                    serv.privmsg(
                        chan, author+" is not allowed to"\
                        " kick "+arguments[1]+" !")
            else:
                unknow_message()
        elif '!k' == arguments[0] and level <= "3":
            powa_message()

        #---[ BAN ]---#
        if '!b' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif level >= target:
                serv.mode(chan_verif[0], "+b "+arguments[1])
            else:
                serv.privmsg(
                    chan, author+" is not allowed to "\
                    "ban "+arguments[1]+" !")
        elif '!b' == arguments[0] and level <= "3":
            powa_message()

        #---[ UNBAN ]---#
        if '!db' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif level >= target:
                serv.mode(chan_verif[0], "-b "+arguments[1])
            else:
                serv.privmsg(
                    chan, author+" is not allowed to "\
                    "removes "+arguments[1]+" ban !")
        elif '!db' == arguments[0] and level <= "3":
            powa_message()

        #---[ KICK & BAN ]---#
        if '!kb' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif level >= target:
                if nombreArg == 2:
                    serv.mode(chan_verif[0], "ban "+arguments[1])
                    serv.kick(chan_verif[0], arguments[1], author)
                else:
                    serv.mode(chan_verif[0], "ban "+arguments[1])
                    serv.kick(
                        chan_verif[0], arguments[1], message\
                        .replace('!kb', '').replace(\
                        arguments[1], '')[2:]+' ('+author+')')
            else:
                serv.privmsg(
                    chan, author+" is not allowed to "\
                    "kick&ban "+arguments[1]+" !")
        elif '!kb' == arguments[0] and level <= "3":
            powa_message()

        #---[ VOICE ]---#
        if '!v' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "+v "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!v' == arguments[0] and level <= "3":
            powa_message()

        #---[ REMOVE VOICE ]---#
        if '!dv' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "-v "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!dv' == arguments[0] and level <= "3":
            powa_message()

        #---[ HOP ]---#
        if '!h' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "+h "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!h' == arguments[0] and level <= "3":
            powa_message()

        #---[ REMOVE HOP ]---#
        if '!dh' == arguments[0] and level > "3":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "-h "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!dh' == arguments[0] and level <= "3":
            powa_message()

        #---[ OP ]---#
        if '!op' == arguments[0] and level > "4":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "+o "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!op' == arguments[0] and level <= "4":
            powa_message()

        #---[ REMOVE OP ]---#
        if '!deop' == arguments[0] and level > "4":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "-o "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!deop' == arguments[0] and level <= "4":
            powa_message()

        #---[ ADMIN ]---#
        if '!a' == arguments[0] and level > "5":
            if nombreArg == 1:
                error_message()
            elif level >= target:
                serv.mode(chan_verif[0], "+a "+arguments[1])
            else:
                modif_powa_message()
        elif '!a' == arguments[0] and level <= "5":
            powa_message()

        #---[ REMOVE ADMIN ]---#
        if '!da' == arguments[0] and level > "5":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.mode(chan_verif[0], "-a "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!da' == arguments[0] and level <= "5":
            powa_message()

        #---[ ACCESS ]---#
        if '!ax' == arguments[0] and level > "4":
            if nombreArg <= 2:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.privmsg(
                        "chanserv", "access "+chan_verif[0]+\
                        " add "+arguments[1]+" "+arguments[2])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!ax' == arguments[0] and level <= "4":
            powa_message()

        #---[ REMOVE ACCESS ]---#
        if '!del' == arguments[0] and level > "4":
            if nombreArg == 1:
                error_message()
            elif (chan_verif[1].has_user(arguments[1]))\
                    or (arguments[1] in self.owner)\
                    or (arguments[1] in admin_users):
                if level >= target:
                    serv.privmsg(
                        "chanserv", "access "+chan_verif[0]+\
                        " del "+arguments[1])
                else:
                    modif_powa_message()
            else:
                unknow_message()
        elif '!del' == arguments[0] and level <= "4":
            powa_message()

if __name__ == "__main__":
    bot().start()
