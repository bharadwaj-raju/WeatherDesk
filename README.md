# WeatherDesk
Change the wallpaper based on the weather

<a href="https://www.yahoo.com/?ilc=401" target="_blank"> <img src="https://poweredby.yahoo.com/purple.png" width="134" height="29"></img></a>

# Installation

## Requirements:

- Python 3

## Running

Just run the `WeatherDesk.py` script.

# Usage

## Options

```sh
$ python3 WeatherDesk.py --help
usage: WeatherDesk.py [-h] [-d directory] [-f format] [-w seconds] [-n]

WeatherDesk - Change the wallpaper based on the weather (Uses the Yahoo!
Weather API)

optional arguments:
  -h, --help            show this help message and exit
  -d directory, --dir directory
                        Specify wallpaper directory. Current:
                        ~/.weatherdesk_walls/
  -f format, --format format
                        Specify image file format. Current: .jpg
  -w seconds, --wait seconds
                        Specify time (in seconds) to wait before updating.
                        Current: 3600
  -n, --naming          Show the image file-naming rules and exit.
```

## Naming of Pictures

```sh
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

```

# Note for KDE users

Since KDE 4 and above does not provide an interface to change the desktop background, KDE 4 and above is not supported.

Any contributions on this welcome.
