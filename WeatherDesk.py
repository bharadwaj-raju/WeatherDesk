#!/usr/bin/env python3

# Copyright (c) 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com> All Rights Reserved.

# Licensed under the GNU General Public License 3: https://www.gnu.org/licenses/gpl.txt

import urllib.request
import os
import time
import datetime
import json
import sys
import argparse
import Desktop

__author__ = 'Bharadwaj Raju <bharadwaj.raju777@gmail.com>'


NAMING_RULES = '''
This is how to name files in the wallpaper directory:\n

       WEATHER           |    FILENAME
_________________________|________________
 Clear, Calm, Fair:      | normal{0}
 Thunderstorm:           | thunder{0}
 Windy, Breeze, Gale:    | wind{0}
 Drizzle, Rain, Showers: | rain{0}
 Snow:                   | snow{0}
 Cloudy:                 | cloudy{0}
 Other:                  | normal{0}

 If using with --time or --time 3, add:
 "day-", "night-" or "evening-" in front of filename.

 If using with --time 4, add:
 "morning-", "day-", "evening-" or "night-"

 If using with --time 2, add:
 "day-" or "night-"
'''


#-- Arguments

arg_parser = argparse.ArgumentParser(
    description='''WeatherDesk - Change the wallpaper based on the weather
    (Uses the Yahoo! Weather API)''', formatter_class=argparse.RawTextHelpFormatter)

arg_parser.add_argument('-d', '--dir', metavar='directory', type=str,
    help='Specify wallpaper directory. Default: %s' % '~/.weatherdesk_walls',
    required=False)

arg_parser.add_argument('-f', '--format', metavar='format', type=str,
    help='Specify image file format. Default: %s' % '.jpg',
    required=False)

arg_parser.add_argument('-w', '--wait', metavar='seconds', type=int,
    help='Specify time (in seconds) to wait before updating. Default: %d' % 600,
    required=False)

arg_parser.add_argument('-t', '--time', nargs='?',
    help='''Use different backgrounds for different times.\n
Variations:
  2 = day/night
  3 = day/evening/night [Default]
  4 = morning/day/evening/night

See --naming.''',
    type=int, choices=[2, 3, 4], const=3, required=False)

arg_parser.add_argument('-n', '--naming', action='store_true',
    help='Show the image file-naming rules and exit.',
    required=False)

arg_parser.add_argument('-c', '--city', metavar='name', type=str,
    help=str('Specify city for weather. If not given, taken from ipinfo.io.'), nargs='+',
    required=False)

args = arg_parser.parse_args()

if args.city:
    city = ' '.join(args.city).replace(' ', '%20')
else:
    try:
        city = json.loads(urllib.request.urlopen('http://ipinfo.io/json').read().decode('utf-8'))
        city = city['city'].replace(' ', '%20')
    except:
        pass


use_time = bool(args.time)

if args.dir:
    # User provided a directory
    walls_dir = os.path.abspath(args.dir)
    if not os.path.isdir(walls_dir):
        sys.stderr.write('Invalid directory %s.' % walls_dir)
        sys.exit(1)
else:
    walls_dir = os.path.join(os.path.expanduser('~'), '.weatherdesk_walls')
    if not os.path.isdir(walls_dir):
        os.mkdir(walls_dir)
        fmt = 'No directory specified. Creating in {}... Put files there or specify directory with --dir'
        sys.stderr.write(fmt.format(walls_dir))
        sys.exit(1)


if args.format:
    if not args.format.startswith('.'):
        args.format = '.' + args.format
    file_format = args.format
else: file_format = '.jpg'

wait_time = args.wait or 600  # ten minutes

if args.naming:
    print(NAMING_RULES.format(file_format))
    sys.exit(0)

#-- -- Functions

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

    # For some weird reason, Python evaluates the following as True:
    # 'some' or 'the other' or 'nope' in 'string_which_doesnt_have_these'

    rain_strs = ('drizzle', 'rain', 'shower')
    wind_strs = ('wind', 'breez', 'gale')  # breez matches both breeze and breezy
    normal_strs = ('calm', 'clear', 'fair', 'sun')

    if any(substr in weather_name for substr in rain_strs):
        weather_file = 'rain' + file_format

    elif 'thunder' in weather_name:
        weather_file = 'thunder' + file_format

    elif 'snow' in weather_name:
        weather_file = 'snow' + file_format

    elif any(substr in weather_name for substr in wind_strs):
        weather_file = 'wind' + file_format

    elif any(substr in weather_name for substr in normal_strs):
        weather_file = 'normal' + file_format

    elif 'cloud' in weather_name:
        weather_file = 'cloudy' + file_format

    else:
        weather_file = 'normal' + file_format

    if time:

        return get_time_of_day(args.time) + '-' + weather_file

    return weather_file


def check_if_all_files_exist(time=False, level=3):

    all_exist = True

    required_files = ['rain', 'snow', 'normal', 'cloudy', 'wind', 'thunder']

    if time:

        if level == 3:

            daytime = ['day', 'evening', 'night']

        elif level == 4:

            daytime = ['morning', 'day', 'evening', 'night']

        else:  # level 2

            daytime = ['day', 'night']

        required_files = [moment + '-' + weather
            for moment in daytime
            for weather in required_files]

    for i in required_files:

        if not os.path.isfile(os.path.join(walls_dir, (i + file_format))):

            all_exist = False

            sys.stderr.write(os.path.join(walls_dir, (i + file_format)) + '\n')

    return all_exist


if not check_if_all_files_exist(time=use_time, level=args.time):

    sys.stderr.write('\nNot all required files were found.\n %s' % NAMING_RULES.format(file_format))

    sys.exit(1)

while True:

    try:

        weather_json_url = r'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22' + city + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'

        weather_json = json.loads(urllib.request.urlopen(weather_json_url).read().decode('utf-8'))

        weather = str(weather_json['query']['results']['channel']['item']['condition']['text']).lower()
        city=str(weather_json['query']['results']['channel']['location']['city'])+str(weather_json['query']['results']['channel']['location']['region'])
        print(weather)
        print(city)


        print(os.path.join(walls_dir, get_file_name(weather, time=use_time)))

        Desktop.set_wallpaper(os.path.join(walls_dir, get_file_name(weather, time=use_time)))

    except:

        pass

    time.sleep(wait_time)
