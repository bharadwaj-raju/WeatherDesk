#!/usr/bin/env python3

# Copyright (c) 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com> All Rights Reserved.

# Licensed under the GNU General Public License 3: https://www.gnu.org/licenses/gpl.txt

from urllib.request import urlopen
from os import system, path, mkdir, walk
import time
import datetime
import json
from sys import exit, stderr
import argparse
import Desktop

__author__ = 'Bharadwaj Raju <bharadwaj.raju777@gmail.com>'

#-- Defaults

TIME_WAIT = 600  # seconds

DEFAULT_WALLS_DIR = path.join(path.expanduser('~') + '/.weatherdesk_walls/')

FILE_FORMAT = '.jpg'

#-- -- Defaults

#-- Arguments

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

arg_parser.add_argument('-t', '--time', nargs='?',
    help='Use different backgrounds for different times. See --naming.',
    type=int, choices=[2, 3, 4], const=3, required=False)

arg_parser.add_argument('-n', '--naming', action='store_true',
    help='Show the image file-naming rules and exit.',
    required=False)

arg_parser.add_argument('-c', '--city', metavar='city name', type=str,
    help=str('Specify city for weather. If not give, taken from GeoIP.'), nargs='+',
    required=False)

args = arg_parser.parse_args()

if args.city is not None:

    city = ' '.join(args.city).replace(' ', '%20')

else:

    city = json.loads(urlopen('http://ipinfo.io/json').read().decode('utf-8'))

    city = city['city'].replace(' ', '%20')

if args.time is not None: use_time = True

if args.dir is not None:

    # User provided a directory

    walls_dir = args.dir

    if not path.isdir(walls_dir):

        stderr.write('Invalid directory %s.' % walls_dir)

        exit(1)

else:

    if not path.isdir(DEFAULT_WALLS_DIR):

        mkdir(DEFAULT_WALLS_DIR)

        stderr.write('No directory specified. Creating in ' +
        path.expanduser('~/.weatherdesk_walls') + '... Put files there or specify directory with --dir')

        exit(1)

    walls_dir = DEFAULT_WALLS_DIR

if args.format is not None:

    if not args.format.startswith('.'): args.format = ''.join(('.', args.format))

    FILE_FORMAT = args.format

if args.wait is not None:

    TIME_WAIT = args.wait

if args.naming: print(NAMING_RULES.format(FILE_FORMAT)); exit(0)

#-- -- Arguments

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

 If using with --time or --time 3, add:
 "day-", "night-" or "evening-" in front of filename.

 If using with --time 4, add:
 "morning-", "day-", "evening-" or "night-"

 If using with --time 2, add:
 "day-" or "night-"
'''

def get_time_of_day(level=3):

    '''
    For detail level 2:
    06 to 20: day
    20 to 06: night
    '''

    '''
    For detail level 3:
    06 to 17: day
    17 to 20: evening
    20 to 06: night
    '''

    '''
    For detail level 4:
    06 to 08: morning
    08 to 17: day
    17 to 20: evening
    20 to 06: night
    '''

    current_time = datetime.datetime.now()

    if level == 3:

        if current_time.hour in range(6, 17):

            return 'day'

        elif current_time.hour in range(17, 20):

            return 'evening'

        else:

            return 'night'

    elif level == 4:

        if current_time.hour in range(6, 8):

            return 'morning'

        elif current_time.hour in range(8, 17):

            return 'day'

        elif current_time.hour in range(17, 20):

            return 'evening'

        else:

            return 'night'

    else:

        if current_time.hour in range(6, 20):

            return 'day'

        else:

            return 'night'

def get_file_name(weather_name, time=False):

    if 'drizzle' or 'rain' in weather_name: weather_file = 'rain' + FILE_FORMAT

    if 'thunder' in weather_name: weather_file = 'thunder' + FILE_FORMAT

    if 'snow' in weather_name: weather_file = 'snow' + FILE_FORMAT

    if 'windy' or 'breeze' or 'gale' in weather_name: weather_file = 'wind' + FILE_FORMAT

    if 'haze' or 'mist' or 'dust' in weather_name: weather_file = 'mist' + FILE_FORMAT

    if 'calm' or 'clear' or 'fair' in weather_name: weather_file = 'normal' + FILE_FORMAT

    if 'cloud' in weather_name: weather_file = 'cloudy' + FILE_FORMAT

    else: weather_file = 'normal' + FILE_FORMAT

    if time:

        return get_time_of_day(args.time) + '-' + weather_file

    return weather_file


def check_if_all_files_exist(time=False, level=3):

    all_exist = True

    if time:

        if args.time == 3:

            required_files = ['evening-normal', 'day-normal', 'night-normal',
            'evening-rain', 'day-rain', 'night-rain',
            'evening-snow', 'day-snow', 'night-snow',
            'evening-thunder', 'day-thunder', 'night-thunder',
            'evening-wind', 'day-wind', 'night-wind',
            'evening-cloudy', 'day-cloudy', 'night-cloudy']

        elif args.time == 4:

            required_files = ['morning-normal', 'day-normal','evening-normal' , 'night-normal',
            'morning-rain', 'evening-rain', 'day-rain', 'night-rain',
            'morning-snow', 'evening-snow', 'day-snow', 'night-snow',
            'morning-thunder', 'evening-thunder', 'day-thunder', 'night-thunder',
            'morning-wind', 'evening-wind', 'day-wind', 'night-wind',
            'morning-cloudy', 'evening-cloudy', 'day-cloudy', 'night-cloudy']

        else:  # level 2

            required_files = ['day-normal', 'night-normal',
            'day-rain', 'night-wind',
            'day-snow', 'night-snow',
            'day-thunder', 'night-thunder',
            'day-wind', 'night-wind',
            'day-cloudy', 'night-cloudy']

    else:

        required_files = ['rain', 'snow', 'normal', 'cloudy', 'wind', 'thunder']

    for i in required_files:

        if not path.isfile(path.join(walls_dir, (i + FILE_FORMAT))):

            all_exist = False

            stderr.write(path.join(walls_dir, (i + FILE_FORMAT)) + '\n')

    return all_exist


while True:

    weather_json_url = r'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22' + city + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'

    weather_json = json.loads(urlopen(weather_json_url).read().decode('utf-8'))

    weather = str(weather_json['query']['results']['channel']['item']['condition']['text']).lower()

    if not check_if_all_files_exist(time=True, level=args.time):

        stderr.write('\nNot all required files were found.\n %s' % NAMING_RULES.format(FILE_FORMAT))

        exit(1)

    if use_time:

        Desktop.set_wallpaper(path.join(walls_dir, get_file_name(weather, time=True)))

    else:

        Desktop.set_wallpaper(path.join(walls_dir, get_file_name(weather, time=False)))

    time.sleep(TIME_WAIT)
