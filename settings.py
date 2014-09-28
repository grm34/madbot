#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#--------------------  [O_o]  ---------------------#
#     Made with love by grm34 (FRIPOUILLEJACK)     #
#     ........fripouillejack@gmail.com .......     #
#--------------------------------------------------#
"""

Specifics bot commands (by b0t PV) :

    !say #chan message  :  say something
    !act #chan message  :  do an action
    !j #chan            :  join a channel
    !p #chan (message)  :  leave a channel
    !exit (message)     :  disconnect from server

API Keys required (free) :

    meteo_api_key   :  http://www.wunderground.com/weather/api/
    geoips_api_key  :  http://www.geoips.com/fr/developer/api-guide
    google_api_key  :  https://code.google.com (Directions API Service)

Quote usage requires MYSQL Database with table configured like this :

    CREATE TABLE quote (
    id INT not null AUTO_INCREMENT,
    user TINYTEXT not null,
    text TINYTEXT not null,
    author TINYTEXT not null,
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    ON UPDATE CURRENT_TIMESTAMP not null,
    PRIMARY KEY (id));

"""

def settings():

    bot_owner = ""
    bot_name = "madbot"
    bot_description = ""
    server_irc = ""
    server_port = 6667
    channels = "#test"
    nickserv_pass = ""
    mysql_host = ""
    mysql_user = ""
    mysql_pass = ""
    mysql_db = ""
    meteo_api_key = ""
    geoips_api_key = ""
    google_api_key = ""
    admin_users = ["", "", "",""]
    database_user = ""
    database_pass = ""
    database_url = ""

    team_users = [
        "", "", "", "", "", "", ""
    ]

    bad = [
        " b0ts ", " pute ", " connasse ", " connard ", " batard ",
        " salope ", " enculé ", " enfoiré ", " T411 "
    ]

    slap = [
        "around a bit with a large trout", "with an enormous pike, with "\
        "equally enormous teeth", "with the broad side of their sword",
        "with a very large fern", "till it's all green and mushy",
        "with the end of a 1200V power cable", "with a very slimy vine",
        "with a humongous duck feather","with a bungee cord", "silly",
        "with a perma-ban", "with a Windows 7 install DVD", "with a MacBook",
        "with glass of water, spilling water everywhere", "with a traffic "\
        "cone", "to hard and gets sued", "with a lawsuit", "with a pancake "\
        "causing a butter stain", "with an extremely large paperclip",
        "with a coke bottle causing it to explode"
    ]

    hit = [
        "donne un coup de fouet à ", "tord le cou de ", "gifle violemment ",
        "casse les côtes de ", "fout un coup de tête à ", "agresse et "\
        "séquestre ", "fracasse la gueule de ", "cogne sur ",
        "se défoule sur " , "arrache le bras de "
    ]

    sex = [
        "agresse sexuellement ", "déshabille ", "fait une proposition "\
        "indécente à ", "licks ", "gives a favor to ", "déglingue ",
        "mange subtilement ", "prête son doigt à ", "donne la fessée à ",
        "tripote ", "viole sauvagement ", "descend à la cave avec ",
        "défouraille ", "démonte ", "craque le jean de ",
        "ponce les genoux de "
    ]

    kiss = [
        "fait un gros bisou à ", "embrasse tendrement ", "roule une pelle à ",
        "fait des bisous à ", "bisouille ", "embrasse sauvagement ",
        "just gives one kiss to ", "fait un bisou, contraint forcé à "
    ]

    options = [
        "!help", "!srt", "!sub", "!imdb", "!tmdb", "!tv", "!allo", "!rls",
        "!img", "!google", "!tub", "!daily", "!sound", "!meteo", "!dist",
        "!ip", "!quizz", "!quote", "!quoteadd", "!beer", "!bedo", "!sex",
        "!slap", "!hit", "!kiss", "!bif", "!caf", "!hug", "!champ",
        "!womp", "!gg", "!out", "!isout"
    ]

    utils = [
        "!srt", "!sub", "!imdb", "!tmdb", "!tv", "!allo", "!img",
        "!google", "!tub", "!daily", "!sound", "!meteo", "!dist","!ip"
    ]

    help = [
        ">-------------------------------------------------------------<",
        ">----------[ FRiPOUiLLEJACK [O_o] IRC BOT COMMANDS ]----------<",
        ">-------------------------------------------------------------<",
        "                                                               ",
        ">----------[ SERVICES ]---------------------------------------<",
        "                                                               ",
        "   !srt     + 'search'        => subtitles on sous-titres.eu",
        "   !sub     + 'search'        => subtitles on subsynchro.com",
        "   !imdb    + 'search'        => release on imdb.com",
        "   !tmdb    + 'search'        => movies on themoviedb.org",
        "   !tv      + 'search'        => series on themoviedb.org",
        "   !allo    + 'search'        => movies on allocine.fr",
        "   !add     + 'id imdb'       => add item in Team DATABASE",
        "   !img     + 'search'        => images on google images",
        "   !google  + 'search'        => something on google",
        "   !tub     + 'search'        => video on youtube",
        "   !daily   + 'search'        => video on dailymotion",
        "   !sound   + 'search'        => music on soundcloud",
        "   !meteo   + 'city'          => weather forecast",
        "   !dist    + 'city / city'   => distance between cities",
        "   !ip      + 'ip' or+ 'ndd'  => ip/ndd location finder",
        "   !uptime                    => seen bot uptime",
        "                                                               ",
        ">----------[ FANTASY ]----------------------------------------<",
        "                                                               ",
        "   !quizz                               => quizz question",
        "   !quote     + 'user' + 'nb' or 'all'  => view quotes",
        "   !quoteadd  + 'user' + 'text'         => add quote",
        "   !quotedel  + 'user' + 'nb' or 'all'  => del quote",
        "   !beer      + 'user' or 'all'         => fantasy action",
        "   !bedo      + 'user' or 'all'         => fantasy action",
        "   !sex       + 'user' or 'all'         => fantasy action",
        "   !slap      + 'user' or 'all'         => fantasy action",
        "   !hit       + 'user' or 'all'         => fantasy action",
        "   !kiss      + 'user' or 'all'         => fantasy action",
        "   !bif       + 'user' or 'all'         => fantasy action",
        "   !caf       + 'user' or 'all'         => fantasy action",
        "   !hug       + 'user' or 'all'         => fantasy action",
        "   !champ     + 'user' or 'all'         => fantasy action",
        "   !womp      + 'user'                  => fantasy action",
        "   !gg        + 'user' or 'all'         => fantasy action",
        "   !out                                 => fantasy action",
        "   !isout     + 'user'                  => fantasy action",
        "                                                               ",
        ">----------[ IRC OPTIONS ]------------------------------------<",
        "                                                               ",
        "   !e       + 'user'              => exempt user",
        "   !de      + 'user'              => removes user exempt",
        "   !k       + 'user' + (reason)   => kick user",
        "   !b       + 'user' + (reason)   => ban user",
        "   !db      + 'user'              => unban user",
        "   !kb      + 'user' + (reason)   => kick&ban user",
        "   !v       + 'user'              => voice user",
        "   !dv      + 'user'              => removes user voice",
        "   !h       + 'user'              => half-op user",
        "   !dh      + 'user'              => removes user half-op",
        "   !op      + 'user'              => operator user",
        "   !deop    + 'user'              => removes user operator",
        "   !a       + 'user'              => protect user",
        "   !da      + 'user'              => removes user protection",
        "   !ax      + 'user' + 'level'    => add user access list",
        "   !del     + 'user'              => remove user access list",
        "                                                               ",
        ">-------------------------------------------------------------<",
        ">---[ MADE WiTH LOVE BY grm34 -- fripouillejack@gmail.com ]---<",
        ">-------------------------------------------------------------<"
    ]

    infos = (
        bot_owner, bot_name, bot_description, server_irc, server_port,
        channels, nickserv_pass, mysql_host, mysql_user, mysql_pass,
        mysql_db, meteo_api_key, geoips_api_key, google_api_key,
        admin_users, database_user, database_pass, database_url,
        team_users, bad, slap, hit, sex, kiss, options, utils, help
    )

    return infos
