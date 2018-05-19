#!/usr/bin/env python3
# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.
# This file is part of WeatherDesk.
#
# WeatherDesk is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WeatherDesk is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WeatherDesk (in the LICENSE file).
# If not, see <http://www.gnu.org/licenses/>.

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
import traceback
import urllib.error
import urllib.parse

from itertools import product
from urllib.request import urlopen

import Desktop

NAMING_RULES = '''
This is how to name files in the wallpaper directory:\n

       WEATHER		     |	FILENAME
_________________________|________________
 Clear, Calm, Fair:	     | normal{0}
 Thunderstorm:		     | thunder{0}
 Windy, Breeze, Gale:	 | wind{0}
 Drizzle, Rain, Showers: | rain{0}
 Snow:				     | snow{0}
 Cloudy:				 | cloudy{0}
 Other:				     | normal{0}

 If using with --time or --time 3, add:
 "day-", "night-" or "evening-" in front of filename.

 If using with --time 4, add:
 "morning-", "day-", "evening-" or "night-"

 If using with --time 2, add:
 "day-" or "night-"
 
 If you use --no-weather, the files have to be named simply after the time of day depending of your time schema.
 E.g.: "day.jpg", "night.jpg"
'''


def get_args():
    arg_parser = argparse.ArgumentParser(
        description='''WeatherDesk - Change the wallpaper based on the weather
        (Uses the Yahoo! Weather API)''',
        formatter_class=argparse.RawTextHelpFormatter)

    arg_parser.add_argument(
        '-d', '--dir', metavar='directory', type=str,
        help='Specify wallpaper directory. Default: %s' % '~/.weatherdesk_walls',
        required=False)

    arg_parser.add_argument(
        '-f', '--format', metavar='format', type=str,
        help='Specify image file format. Default: %s' % '.jpg',
        default='.jpg',
        required=False)

    arg_parser.add_argument(
        '-w', '--wait', metavar='seconds', type=int,
        help='Specify time (in seconds) to wait before updating. Default: 600',
        default=600,
        required=False)

    arg_parser.add_argument(
        '-t', '--time', nargs='?',
        help='''Use different backgrounds for different times.\n
    Variations:
      2 = day/night
      3 = day/evening/night [Default]
      4 = morning/day/evening/night
    
    See --naming.''',
        type=int, choices=[2, 3, 4], default=3, required=False)

    arg_parser.add_argument(
        '-n', '--naming', action='store_true',
        help='Show the image file-naming rules and exit.',
        required=False)

    arg_parser.add_argument(
        '--no-weather', action='store_true',
        help='Disable the weather functionality of the script. Wallpapers will only be changed based on the time of day.'
             'With this option, no internet connection is required.',
        required=False)

    arg_parser.add_argument(
        '-c', '--city', metavar='name', type=str,
        help=str('Specify city for weather. If not given, taken from ipinfo.io.'),
        nargs='+', required=False)

    arg_parser.add_argument(
        '-o', '--one-time-run', action='store_true',
        help='Run once, then exit.',
        required=False)

    return vars(arg_parser.parse_args())


def validate_args(args):
    parsed_args = dict(args).copy()

    if not parsed_args['no_weather']:
        try:
            parsed_args['city'] = get_city(args['city'])
        except (urllib.error.URLError, ValueError):
            sys.stderr.write(
                'Finding city from IP failed! Specify city manually with --city.')
            sys.exit(1)

    try:
        parsed_args['walls_dir'] = get_config_dir(args['dir'])
    except ValueError as e:
        sys.stderr.write(e)
        sys.exit(1)

    parsed_args['file_format'] = get_file_format(args['format'])

    parsed_args['wait_time'] = args['wait']  # ten minutes

    missing_files = get_missing_files(
        time_level=parsed_args['time'],
        no_weather=parsed_args['no_weather'],
        file_format=parsed_args['file_format'],
        walls_dir=parsed_args['walls_dir'],
    )
    if missing_files:
        sys.stderr.write('\nNot all required files were found!\n The following files were expected, but are missing:\n')
        for file in missing_files:
            sys.stderr.write(file + '\n')
        sys.exit(1)

    return parsed_args


def get_time_of_day(level=3, hour=None):
    """
    For detail level 2:
    06 to 20: day
    20 to 06: night

    For detail level 3:
    06 to 17: day
    17 to 20: evening
    20 to 06: night

    For detail level 4:
    06 to 08: morning
    08 to 17: day
    17 to 20: evening
    20 to 06: night
    """
    if hour is None:
        current_hour = datetime.datetime.now().hour
    else:
        current_hour = hour

    if level == 2:
        labels = ['day', 'night']
        thres = [5, 19]
    elif level == 3:
        labels = ['day', 'evening', 'night']
        thres = [5, 16, 19]
    elif level == 4:
        labels = ['morning', 'day', 'evening', 'night']
        thres = [5, 7, 16, 19]
    else:
        raise ValueError('Invalid time level.')

    thres.append(current_hour)
    thres.sort()
    day_index = thres.index(current_hour)
    return labels[day_index - 1]


def get_weather_summary(weather_name):
    summaries = {'rain': ['drizzle', 'rain', 'shower'],
                 'wind': ['breez', 'gale', 'wind'],  # breez matches both breeze and breezy
                 'thunder': ['thunder'],
                 'snow': ['snow'],
                 'cloudy': ['cloud']}

    for summary, options in summaries.items():
        if weather_name in options:
            return summary
    return 'normal'


def get_config_dir(config_dir_arg):
    if config_dir_arg:
        # User provided a directory
        walls_dir = os.path.abspath(config_dir_arg)

        if not os.path.isdir(walls_dir):
            raise ValueError('Invalid directory %s.' % walls_dir)
    else:
        walls_dir = os.path.join(os.path.expanduser('~'), '.weatherdesk_walls')

        if not os.path.isdir(walls_dir):
            os.mkdir(walls_dir)
            fmt = '''No directory specified.
    Creating in {}... Put files there or specify directory with --dir'''
            raise ValueError(fmt.format(walls_dir))
    return walls_dir


def get_file_format(file_format_arg):
    if not file_format_arg.startswith('.'):
        file_format_arg = '.' + file_format_arg

    return file_format_arg


def get_file_name(weather, daytime, walls_dir, file_format):
    if weather and daytime:
        name = '{}-{}'.format(daytime, weather)
    elif weather:
        name = weather
    elif daytime:
        name = daytime
    else:
        raise ValueError('Either a correct weather or a correct time is required.')

    return os.path.join(walls_dir, name + file_format)


def get_missing_files(time_level, no_weather, file_format, walls_dir):
    missing_files = []

    if no_weather:
        weathers = [None]
    else:
        weathers = ['rain', 'snow', 'normal', 'cloudy', 'wind', 'thunder']

    if time_level == 2:
        daytimes = ['day', 'night']
    elif time_level == 3:  # level 2
        daytimes = ['day', 'evening', 'night']
    elif time_level == 4:
        daytimes = ['morning', 'day', 'evening', 'night']
    else:
        daytimes = [None]

    required_files = (get_file_name(weather, daytime, walls_dir, file_format) for weather, daytime in
                      product(weathers, daytimes))

    for file in required_files:
        if not os.path.isfile(file):
            missing_files.append(file)

    return missing_files


def get_city(city_arg):
    if city_arg:
        city = ' '.join(city_arg).replace(' ', '%20')
    else:
        city_json_url = 'http://ipinfo.io/json'

        city_json = urlopen(city_json_url).read().decode('utf-8')

        city = json.loads(city_json)
        city = city['city'].replace(' ', '%20')
    return city


def get_current_weather(city):
    weather_json_url = r'https://query.yahooapis.com/v1/public/yql?q=select%20*%20from%20weather.forecast%20where%20woeid%20in%20(select%20woeid%20from%20geo.places(1)%20where%20text%3D%22' + urllib.parse.quote(
        city) + '%22)&format=json&env=store%3A%2F%2Fdatatables.org%2Falltableswithkeys'

    weather_json = json.loads(urlopen(weather_json_url).read().decode('utf-8'))['query']['results']['channel']

    weather = str(weather_json['item']['condition']['text']).lower()

    city_with_area = str(weather_json['location']['city']) + str(weather_json['location']['region'])

    return weather, city_with_area


def set_conditional_wallpaper(city, time_level, no_weather, walls_dir, file_format):
    if not no_weather:
        weather, actual_city = get_current_weather(city)
        weather_code = get_weather_summary(weather)
        print('The retrieved weather for {} is {}'.format(actual_city, weather))
    else:
        weather_code = None

    time_of_day = get_time_of_day(time_level)
    print('The current time of the day is {}'.format(time_of_day))

    file_name = get_file_name(weather_code, time_of_day, walls_dir, file_format)
    print('Changing wallpaper to {}'.format(file_name))

    desktop_env = Desktop.get_desktop_environment()

    Desktop.set_wallpaper(file_name, desktop_env)


def restart_program():
    # Restarts the current program, with file objects and descriptors cleanup

    new_weatherdesk_cmd = ''

    for i in sys.argv:
        new_weatherdesk_cmd = ' ' + i

    subprocess.Popen([new_weatherdesk_cmd], shell=True)

    sys.exit(0)


if __name__ == '__main__':

    args = get_args()
    parsed_args = validate_args(args)

    if parsed_args['naming']:
        print(NAMING_RULES.format(parsed_args['file_format']))
        sys.exit(0)

    if parsed_args['one_time_run']:
        set_conditional_wallpaper(parsed_args['city'],
                                  parsed_args['time'],
                                  parsed_args['no_weather'],
                                  parsed_args['walls_dir'],
                                  parsed_args['file_format'])
        sys.exit(0)

    trace_main_loop = None

    while True:
        try:
            set_conditional_wallpaper(parsed_args['city'],
                                      parsed_args['time'],
                                      parsed_args['no_weather'],
                                      parsed_args['walls_dir'],
                                      parsed_args['file_format'])

        except urllib.error.URLError:
            # Don't shut off on temporary network problems
            trace_main_loop = '[Main loop] \n' + traceback.format_exc()

            if sys.platform.startswith('linux'):
                # HACK: glibc on Linux only loads /etc/resolv.conf once
                # This breaks our network communications after suspend/resume
                # So we force it to reload using the res_init() function

                # But sometimes res_init() mysteriously crashes the program
                # and it's too low-level for any try-except to catch.

                # So we restart the whole thing!

                restart_program()

        except ValueError:
            # Sometimes JSON returns a null value for no reason

            trace_main_loop = '[Main loop] \n' + traceback.format_exc()

        except:
            # All other errors (except KeyboardInterrupt ^C)
            # We'll still have a full stack trace

            trace_main_loop = '[Main loop] \n' + traceback.format_exc()

        else:
            trace_main_loop = '[Main loop] No error.'

        finally:
            if trace_main_loop:
                print(trace_main_loop)

        time.sleep(parsed_args['wait_time'])
