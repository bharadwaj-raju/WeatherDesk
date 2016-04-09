#!/usr/bin/env python3

from urllib.request import urlopen
from os import system, path, mkdir, walk
import time
import json
from sys import exit, platform, stderr
import argparse
import Desktop

TIME_WAIT = 3600  # seconds

DEFAULT_WALLS_DIR = path.expanduser('~') + '/.weatherdesk_walls/'

FILE_FORMAT = '.jpg'

city = urlopen('http://ipinfo.io/'
    + urlopen('http://ip.42.pl/short').read().decode('utf-8')
    + '/city').read().decode('utf-8').rstrip()

arg_parser = argparse.ArgumentParser(
    description='''WeatherDesk - Change the wallpaper based on the weather
    (Uses the Yahoo! Weather API)''')

arg_parser.add_argument('-d', '--dir', metavar='directory', type=str,
    help=str('Specify wallpaper directory. Current: %s' % DEFAULT_WALLS_DIR),
    required=False)

arg_parser.add_argument('-f', '--format', metavar='format', type=str,
    help=str('Specify image file format. Current: %s' % FILE_FORMAT),
    required=False)

arg_parser.add_argument('-w', '--wait', metavar='seconds', type=int,
    help=str('Specify time (in seconds) to wait before updating. Current: %d' % TIME_WAIT),
    required=False)

arg_parser.add_argument('-n', '--naming', action='store_true',
    help='Show the image file-naming rules and exit.',
    required=False)

# TODO: Implement day/night variation.
# arg_parser.add_argument('--time', action='store_true',
# help='Also include day/night variation in wallpapers. To support, add "day-" or "night-" in front of file name.')

args = arg_parser.parse_args()

NAMING_RULES = '''
This is how to name files in the wallpaper directory:\n

       WEATHER        |    FILENAME
______________________|________________
 Clear, Calm, Fair:   | normal{0}
 Thunderstorm:        | thunder{0}
 Windy, Breeze, Gale: | wind{0}
 Drizzle, Rain:       | rain{0}
 Snow:                | snow{0}
 Cloudy:              | cloudy{0}
 Other:               | normal{0}
'''


def get_file_name(weather_name):

    if 'drizzle' or 'rain' in weather_name: weather_file = 'rain' + FILE_FORMAT

    if 'thunder' in weather_name: weather_file = 'thunder' + FILE_FORMAT

    if 'snow' in weather_name: weather_file = 'snow' + FILE_FORMAT

    if 'windy' or 'breeze' or 'gale' in weather_name: weather_file = 'wind' + FILE_FORMAT

    if 'haze' or 'mist' or 'dust' in weather_name: weather_file = 'mist' + FILE_FORMAT

    if 'calm' or 'clear' or 'fair' in weather_name: weather_file = 'normal' + FILE_FORMAT

    if 'cloud' in weather_name: weather_file = 'cloudy' + FILE_FORMAT

    else: weather_file = 'normal' + FILE_FORMAT

    return weather_file

if args.dir is not None:

    # User provided a directory

    walls_dir = args.dir

    if not path.isdir(walls_dir):

        stderr.write('Invalid directory %s.' % walls_dir)

        exit(1)

else:

    if not path.isdir(DEFAULT_WALLS_DIR):

        mkdir(DEFAULT_WALLS_DIR)

    walls_dir = DEFAULT_WALLS_DIR

for dirpath, dirnames, files in walk(walls_dir):

    if not files:

        stderr.write('No image files in %s.' % walls_dir)

        exit(1)

if args.format is not None:

    if not args.format.startswith('.'): args.format = ''.join(('.', args.format))

    FILE_FORMAT = args.format

if args.wait is not None:

    TIME_WAIT = args.wait

if args.naming: print(NAMING_RULES.format(FILE_FORMAT)); exit(0)

while True:

    weather_json_url = 'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22' + city + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'
    weather_json = json.loads(urlopen(weather_json_url).read().decode('utf-8'))

    weather = str(weather_json['query']['results']['channel']['item']['condition']['text']).lower()

    Desktop.set_wallpaper(path.join(walls_dir, get_file_name(weather)), FILE_FORMAT)

    time.sleep(TIME_WAIT)
