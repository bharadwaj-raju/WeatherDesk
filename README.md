# WeatherDesk has moved!
# Now at [GitLab](https://gitlab.com/bharadwaj-raju/WeatherDesk)!

# WeatherDesk

Change the wallpaper based on the weather and (optionally) the time.

![WeatherDesk](http://i.imgur.com/F2Lml2n.png)

Thanks to [Martin Hansen](http://stackoverflow.com/users/2118300/martin-hansen) for the original `Desktop.py` module.

[![Powered by Yahoo!](https://poweredby.yahoo.com/purple.png)](https://www.yahoo.com/?ilc=401)

# Installation

Just download the repository, get some wallpapers (see [the Wallpapers section](#wallpapers)) and run the `WeatherDesk.py` script.

**NOTE:** If you use OS X, see [the note for OS X users](#note-for-os-x-users).

## Options

    $ python3 WeatherDesk.py --help
    usage: WeatherDesk.py [-h] [-d directory] [-f format] [-w seconds]
                          [-t [{2,3,4}]] [-n] [--no-weather] [-c name [name ...]]
                          [-o]

    WeatherDesk - Change the wallpaper based on the weather
            (Uses the Yahoo! Weather API)

    optional arguments:
      -h, --help            show this help message and exit
      -d directory, --dir directory
                            Specify wallpaper directory. Default: ~/.weatherdesk_walls
      -f format, --format format
                            Specify image file format. Default: .jpg
      -w seconds, --wait seconds
                            Specify time (in seconds) to wait before updating. Default: 600
      -t [{2,3,4}], --time [{2,3,4}]
                            Use different backgrounds for different times.

                                Variations:
                                  2 = day/night
                                  3 = day/evening/night [Default]
                                  4 = morning/day/evening/night

                                See --naming.
      -n, --naming          Show the image file-naming rules and exit.
      --no-weather          Disable the weather functionality of the script. Wallpapers will only be changed based on the time of day.With this option, no internet connection is required.
      -c name [name ...], --city name [name ...]
                            Specify city for weather. If not given, taken from ipinfo.io.
      -o, --one-time-run    Run once, then exit.


## Wallpapers

**You can choose your own custom set**, conforming to the [naming rules](#naming-of-pictures).
Either put them in the default `~/.weatherdesk_walls/` directory or specify a directory with the `--dir` option.

### Ready-to-Go wallpaper set

**Don't want to go hunting for wallpapers?** I recommend [this beautiful set (called FireWatch, named after a game)](http://imgur.com/a/snB5O) (download the set using the ZIP file link given below) made by redditor JuniorNeves.

**A zip download of the FireWatch set, named according to the rules:** [ZIP download](https://github.com/bharadwaj-raju/FireWatch-WeatherDesk-Pack/archive/master.zip). Just extract it into `~/.weatherdesk_walls` (or into any directory and pass its path with `--dir`)


### Naming of Pictures

    $ python3 WeatherDesk.py --naming
    This is how to name files in the wallpaper directory:


           WEATHER           |    FILENAME
    _________________________|________________
     Clear, Calm, Fair:      | normal.jpg
     Thunderstorm:           | thunder.jpg
     Windy, Breeze, Gale:    | wind.jpg
     Drizzle, Rain, Showers: | rain.jpg
     Snow:                   | snow.jpg
     Cloudy:                 | cloudy.jpg
     Other:                  | normal.jpg

     If using with --time or --time 3, add:
     "day-", "night-" or "evening-" in front of filename.

     If using with --time 4, add:
     "morning-", "day-", "evening-" or "night-"

     If using with --time 2, add:
     "day-" or "night-"

     If you use --no-weather, the files have to be named simply after the time of day depending of your time schema.
     E.g.: "day.jpg", "night.jpg"


## Supported Platforms

- Linux

  - AfterStep
  - Awesome WM
  - Blackbox
  - Cinnamon
  - Enlightenment
  - Fluxbox
  - Gnome 2
  - Gnome 3
  - i3
  - IceWM
  - JWM
  - KDE
  - LXDE
  - LXQt
  - Mate
  - Openbox
  - Pantheon
  - Razor-Qt
  - Trinity
  - Unity
  - Windowmaker
  - XFCE

- Windows

- OS X

## In background mode (only for OS X and Linux)

Run

```sh
$ nohup python3 WeatherDesk.py > /dev/null &
```

## Note for OS X users

Please disable the auto-reset/change of wallpaper in the  "Desktop and Screen Saver" preferences.

[![Disable this](http://i.imgur.com/BFi1GHGm.png)](http://i.imgur.com/BFi1GHG.png)
