madbot
======
![madbot](http://i.imgur.com/RggugqK.png "madbot")
IRC bot written in python...

    >-------------------------------------------------------------<
    >----------[ FRiPOUiLLEJACK [O_o] IRC BOT COMMANDS ]----------<
    >-------------------------------------------------------------<
                                                                   
    >----------[ SERVICES ]---------------------------------------<
                                                                   
       !srt     + 'search'        => subtitles on sous-titres.eu
       !sub     + 'search'        => subtitles on subsynchro.com
       !imdb    + 'search'        => release on imdb.com
       !tmdb    + 'search'        => movies on themoviedb.org
       !tv      + 'search'        => series on themoviedb.org
       !allo    + 'search'        => movies on allocine.fr
       !add     + 'id imdb'       => add item in Team DATABASE
       !img     + 'search'        => images on google images
       !google  + 'search'        => something on google
       !tub     + 'search'        => video on youtube
       !daily   + 'search'        => video on dailymotion
       !sound   + 'search'        => music on soundcloud
       !meteo   + 'city'          => weather forecast
       !dist    + 'city / city'   => distance between cities
       !ip      + 'ip' or 'ndd'   => ip/ndd location finder
                                                                   
    >----------[ FANTASY ]----------------------------------------<
                                                                   
       !quizz                               => quizz question
       !quote     + 'user' + 'nb' or 'all'  => view quotes
       !quoteadd  + 'user' + 'text'         => add quote
       !quotedel  + 'user' + 'nb' or 'all'  => del quote
       !beer      + 'user' or 'all'         => fantasy action
       !bedo      + 'user' or 'all'         => fantasy action
       !sex       + 'user' or 'all'         => fantasy action
       !slap      + 'user' or 'all'         => fantasy action
       !hit       + 'user' or 'all'         => fantasy action
       !kiss      + 'user' or 'all'         => fantasy action
       !bif       + 'user' or 'all'         => fantasy action
       !caf       + 'user' or 'all'         => fantasy action
       !hug       + 'user' or 'all'         => fantasy action
       !champ     + 'user' or 'all'         => fantasy action
       !womp      + 'user'                  => fantasy action
       !gg        + 'user' or 'all'         => fantasy action
       !out                                 => fantasy action
       !isout     + 'user'                  => fantasy action
                                                                   
    >----------[ IRC OPTIONS ]------------------------------------<
                                                                   
       !e       + 'user'              => exempt user
       !de      + 'user'              => removes user exempt
       !k       + 'user' + (reason)   => kick user
       !b       + 'user' + (reason)   => ban user
       !db      + 'user'              => unban user
       !kb      + 'user' + (reason)   => kick&ban user
       !v       + 'user'              => voice user
       !dv      + 'user'              => removes user voice
       !h       + 'user'              => half-op user
       !dh      + 'user'              => removes user half-op
       !op      + 'user'              => operator user
       !deop    + 'user'              => removes user operator
       !a       + 'user'              => protect user
       !da      + 'user'              => removes user protection
       !ax      + 'user' + 'level'    => add user access list
       !del     + 'user'              => remove user access list
                                                                   
    >-------------------------------------------------------------<

Specifics owner commands (by b0t PV) :

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

Go to the [wiki](https://github.com/grm34/madbot/wiki) for installation instructions!
