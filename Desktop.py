#!/usr/bin/env python3
# coding: utf-8

# Copyright © 2016 Bharadwaj Raju <bharadwaj.raju777@gmail.com>
# All Rights Reserved.

# Original code taken from the following answers by StackOverflow user
# Martin Hansen (http://stackoverflow.com/users/2118300/martin-hansen):
# - http://stackoverflow.com/a/21213358/5413945
# - http://stackoverflow.com/a/21213504/5413945

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

import os
import sys
import subprocess
import re
import tempfile
import shutil
import configparser
from textwrap import dedent

# Library to set wallpaper and find desktop - Cross-platform

def get_desktop_environment():

	if sys.platform in ['win32', 'cygwin']:

		return 'windows'

	elif sys.platform == 'darwin':

		return 'mac'

	else:

		desktop_session = os.environ.get('XDG_CURRENT_DESKTOP') or os.environ.get('DESKTOP_SESSION')

		if desktop_session is not None:

			desktop_session = desktop_session.lower()

			# Fix for X-Cinnamon etc

			if desktop_session.startswith('x-'):

				desktop_session = desktop_session.replace('x-', '')

			if desktop_session in ['gnome','unity', 'cinnamon', 'mate',
									'xfce4', 'lxde', 'fluxbox',
								   'blackbox', 'openbox', 'icewm', 'jwm',
								   'afterstep','trinity', 'kde', 'pantheon',
								   'i3', 'lxqt', 'awesome']:

				return desktop_session

			#-- Special cases --#

			# Canonical sets $DESKTOP_SESSION to Lubuntu rather than LXDE if using LXDE.
			# There is no guarantee that they will not do the same with the other desktop environments.
			# In Ubuntu 17.04, $DESKTOP_SESSION is set to 'Unity:Unity7' instead of 'Unity' when using Unity

			elif 'xfce' in desktop_session or desktop_session.startswith('xubuntu'): return 'xfce4'

			elif desktop_session.startswith('ubuntu') or desktop_session.startswith('unity'): return 'unity'

			elif desktop_session.startswith('lubuntu'): return 'lxde'

			elif desktop_session.startswith('kubuntu'):  return 'kde'

			elif desktop_session.startswith('razor'): return 'razor-qt'

			elif desktop_session.startswith('wmaker'): return 'windowmaker'

		if os.environ.get('KDE_FULL_SESSION') == 'true':

			return 'kde'

		elif os.environ.get('GNOME_DESKTOP_SESSION_ID'):

			if not 'deprecated' in os.environ.get('GNOME_DESKTOP_SESSION_ID'):

				return 'gnome2'

		elif is_running('xfce-mcs-manage'): return 'xfce4'
		elif is_running('ksmserver'): return 'kde'

	return 'unknown'

def is_running(process):

	try:  # Linux/Unix

		s = subprocess.Popen(['ps', 'axw'],stdout=subprocess.PIPE)

	except:  # Windows

		s = subprocess.Popen(['tasklist', '/v'],stdout=subprocess.PIPE)

	process_list, err = s.communicate()

	return process in str(process_list)


def set_wallpaper(image):

	desktop_env = get_desktop_environment()


	if desktop_env in ['gnome', 'unity', 'cinnamon', 'pantheon']:

		uri = 'file://%s' % image

		try:

			SCHEMA = 'org.gnome.desktop.background'
			KEY = 'picture-uri'
			gsettings = Gio.Settings.new(SCHEMA)

			gsettings.set_string(KEY, uri)

		except:

			args = ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', uri]
			subprocess.Popen(args)

	elif desktop_env == 'mate':

		try: # MATE >= 1.6

			args = ['gsettings', 'set', 'org.mate.background', 'picture-filename', '%s' % image]
			subprocess.Popen(args)

		except: # MATE < 1.6

			args = ['mateconftool-2','-t','string','--set','/desktop/mate/background/picture_filename','%s' % image]
			subprocess.Popen(args)

	elif desktop_env == 'gnome2':

		args = ['gconftool-2','-t','string','--set','/desktop/gnome/background/picture_filename', '%s' % image]
		subprocess.Popen(args)

	elif desktop_env == 'kde':

		kde_script = dedent(
		'''\
		var Desktops = desktops();
		for (i=0;i<Desktops.length;i++) {
			d = Desktops[i];
			d.wallpaperPlugin = "org.kde.image";
			d.currentConfigGroup = Array("Wallpaper",
										"org.kde.image",
										"General");
			d.writeConfig("Image", "file://%s")
		}
		''') % image

		print(kde_script)

		subprocess.Popen(
				['dbus-send',
				'--session',
				'--dest=org.kde.plasmashell',
				'--type=method_call',
				'/PlasmaShell',
				'org.kde.PlasmaShell.evaluateScript',
				'string:{}'.format(kde_script)]
		)


	elif desktop_env in ['kde3', 'trinity']:

		args = 'dcop kdesktop KBackgroundIface setWallpaper 0 "%s" 6' % image
		subprocess.Popen(args,shell=True)

	elif desktop_env=='xfce4':

		# XFCE4's image property is not image-path but last-image (What?)
		# Only GNOME seems to have a sane wallpaper interface

		# Update: the monitor id thing seems to be changed in
		# XFCE 4.12 to just monitor0 instead of monitorVGA1 or something
		# So now we need to do both.

		list_of_properties_cmd = subprocess.Popen(['bash -c "xfconf-query -R -l -c xfce4-desktop -p /backdrop"'], shell=True, stdout=subprocess.PIPE)

		list_of_properties, list_of_properties_err = list_of_properties_cmd.communicate()

		list_of_properties = list_of_properties.decode('utf-8')

		for i in list_of_properties.split('\n'):

			if i.endswith('last-image'):

				# The property given is a background property
				subprocess.Popen(
					['xfconf-query -c xfce4-desktop -p %s -s "%s"' % (i, image)],
					shell=True)

				subprocess.Popen(['xfdesktop --reload'], shell=True)

	elif desktop_env=='razor-qt':

		desktop_conf = configparser.ConfigParser()
		# Development version

		desktop_conf_file = os.path.join(get_config_dir('razor'),'desktop.conf')

		if os.path.isfile(desktop_conf_file):

			config_option = r'screens\1\desktops\1\wallpaper'

		else:

			desktop_conf_file = os.path.join(os.path.expanduser('~'),'.razor/desktop.conf')
			config_option = r'desktops\1\wallpaper'

		desktop_conf.read(os.path.join(desktop_conf_file))

		try:

			if desktop_conf.has_option('razor',config_option):  # only replacing a value

				desktop_conf.set('razor',config_option,image)

				with codecs.open(desktop_conf_file, 'w', encoding='utf-8', errors='replace') as f:

					desktop_conf.write(f)

		except: pass


	elif desktop_env in ['fluxbox','jwm','openbox','afterstep', 'i3']:

		try:

			args = ['feh','--bg-scale', image]
			subprocess.Popen(args)

		except:

			sys.stderr.write('Error: Failed to set wallpaper with feh!')
			sys.stderr.write('Please make sre that You have feh installed.')

	elif desktop_env == 'icewm':

		args = ['icewmbg', image]
		subprocess.Popen(args)

	elif desktop_env == 'blackbox':

		args = ['bsetbg', '-full', image]
		subprocess.Popen(args)

	elif desktop_env == 'lxde':

		args = 'pcmanfm --set-wallpaper %s --wallpaper-mode=scaled' % image
		subprocess.Popen(args, shell=True)

	elif desktop_env == 'lxqt':

		args = 'pcmanfm-qt --set-wallpaper %s --wallpaper-mode=scaled' % image
		subprocess.Popen(args, shell=True)

	elif desktop_env == 'windowmaker':

		args = 'wmsetbg -s -u %s' % image
		subprocess.Popen(args, shell=True)

	elif desktop_env == 'enlightenment':

		args = 'enlightenment_remote -desktop-bg-add 0 0 0 0 %s' % image
		subprocess.Popen(args, shell=True)

	elif desktop_env == 'awesome':

		with subprocess.Popen("awesome-client", stdin=subprocess.PIPE) as awesome_client:

			command = 'local gears = require("gears"); for s = 1, screen.count() do gears.wallpaper.maximized("%s", s, true); end;' % image
			awesome_client.communicate(input=bytes(command, 'UTF-8'));

	elif desktop_env == 'windows':

			WIN_SCRIPT = '''reg add "HKEY_CURRENT_USER\Control Panel\Desktop" /v Wallpaper /t REG_SZ /d  %s /f

rundll32.exe user32.dll,UpdatePerUserSystemParameters
''' % image

			win_script_file = open(os.path.abspath(os.path.expanduser('~/.weatherdesk_script.bat')), 'w')

			win_script_file.write(WIN_SCRIPT)

			win_script_file.close()

			subprocess.Popen([os.path.abspath(os.path.expanduser('~/.weatherdesk_script.bat'))], shell=True)

	elif desktop_env == 'mac':

		try:

			from appscript import app, mactypes

			app('Finder').desktop_picture.set(mactypes.File(image))

		except ImportError:

			OSX_SCRIPT = '''tell application "System Events"
								  set desktopCount to count of desktops
									repeat with desktopNumber from 1 to desktopCount
									  tell desktop desktopNumber
										set picture to POSIX file "%s"
									  end tell
									end repeat
								end tell
			''' % image

			osx_script_file = open(os.path.expanduser('~/.weatherdesk_script.AppleScript'), 'w')

			osx_script_file.truncate()

			osx_script_file = open(os.path.expanduser('~/.weatherdesk_script.AppleScript'), 'w')

			osx_script_file.truncate()

			osx_script_file.write(OSX_SCRIPT)

			osx_script_file.close()

			subprocess.Popen(['/usr/bin/osascript', os.path.abspath(os.path.expanduser('~/.weatherdesk_script.AppleScript'))])
	else:

		sys.stderr.write('Error: Failed to set wallpaper. (Desktop not supported)')

		return False

	return True


def get_config_dir(app_name):

		if 'XDG_CONFIG_HOME' in os.environ:

			confighome = os.environ['XDG_CONFIG_HOME']

		elif 'APPDATA' in os.environ:  # On Windows

			confighome = os.environ['APPDATA']

		else:

			try:

				from xdg import BaseDirectory
				confighome =  BaseDirectory.xdg_config_home

			except ImportError:  # Most likely a Linux/Unix system anyway

				confighome =  os.path.join(os.path.expanduser('~'),'.config')

		configdir = os.path.join(confighome,app_name)

		return configdir
