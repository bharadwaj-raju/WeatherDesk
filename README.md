# WeatherDesk

Change the wallpaper based on the weather and (optionally) the time.

![WeatherDesk](http://i.imgur.com/F2Lml2n.png)

License: [GNU GPL v3](https://www.gnu.org/licenses/gpl.txt)

Thanks to StackOverflow user [Martin Hensen](http://stackoverflow.com/users/2118300/martin-hansen) for the `Desktop.py` module. (The functions modified a bit from the original.)

[![Powered by Yahoo!](https://poweredby.yahoo.com/purple.png)](https://www.yahoo.com/?ilc=401)

# Installation

## Requirements:

- Python 3

## Running

Just run the `WeatherDesk.py` script.

### In background mode (only for OS X and Linux)

Run

```sh
$ python3 WeatherDesk.py &
```

### Note for OS X users

Please disable the auto-reset/change of wallpaper in the  "Desktop and Screen Saver" preferences.

![Disable this](http://i.imgur.com/BFi1GHGm.png)

# Usage

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
      -t [{2,3,4}], --time [{2,3,4}]
                            Use different backgrounds for different times.

                            Variations:
                              2 = day/night
                              3 = day/evening/night [Default]
                              4 = morning/day/evening/night

                            See --naming.
      -n, --naming          Show the image file-naming rules and exit.
      -c name [name ...], --city name [name ...]
                            Specify city for weather. If not given, taken from ipinfo.io.


## Naming of Pictures

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

# Note for KDE users

Since KDE 4 and above does not provide an interface to change the desktop background, KDE 4 and above is not supported.

Any contributions on this welcome.
