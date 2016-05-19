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
                          [-t [{2,3,4}]] [-n] [-c name [name ...]]

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

      -t {2,3,4}, --time {2,3,4}
                            Use different backgrounds for different times.

                            Variations:
                              2 = day/night
                              3 = day/evening/night [Default]
                              4 = morning/day/evening/night

                            See --naming.

      -n, --naming          Show the image file-naming rules and exit.

      -c name, --city name
                            Specify city for weather. If not given, taken from ipinfo.io.

## Wallpapers

**You can choose your own custom set**, conforming to the [naming rules](#naming-of-pictures).
Either put them in the default `~/.weatherdesk_walls/` directory or specify a directory with the `--dir` option.

### Ready-to-Go wallpaper set

**Don't want to go hunting for wallpapers?** I recommend [this beautiful set (called FireWatch, named after a game)](http://imgur.com/a/snB5O) (download the set using the ZIP file link given below) made by redditor JuniorNeves.

**A zip download of the FireWatch set, named according to the rules:** [ZIP download](https://github.com/bharadwaj-raju/FireWatch-WeatherDesk-Pack/archive/master.zip). Just extract it into `~/.weatherdesk_walls` (or into any directory and pass its path with `--dir`)


### Naming of Pictures

    $ python3 WeatherDesk.py --naming
    This is how to name files in the wallpaper directory:


           WEATHER        |    FILENAME
    ______________________|________________
     Clear, Calm, Fair:   | normal.jpg
     Thunderstorm:        | thunder.jpg
     Windy, Breeze, Gale: | wind.jpg
     Drizzle, Rain:       | rain.jpg
     Snow:                | snow.jpg
     Cloudy:              | cloudy.jpg
     Other:               | normal.jpg

     If using with --time or --time 3, add:
     "day-", "night-" or "evening-" in front of filename.

     If using with --time 4, add:
     "morning-", "day-", "evening-" or "night-"

     If using with --time 2, add:
     "day-" or "night-"


## Supported Platforms

- Linux

  - Gnome 3
  - Pantheon
  - Unity
  - Gnome 2
  - Mate
  - Cinnamon
  - Openbox
  - i3
  - XFCE
  - KDE **3**
  - Trinity
  - Fluxbox
  - Razor-Qt
  - JWM
  - AfterStep
  - IceWM
  - Blackbox
  - Windowmaker
  - Enlightenment
  - LXDE

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

## Note for KDE users

Since KDE 4 and above does not provide an interface to change the desktop background, KDE 4 and above is not supported.

Any contributions on this welcome.
