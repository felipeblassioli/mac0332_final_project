# -*- coding: utf-8 -*-
from flask import Flask
from flask_peewee.db import Database
import logging

app = Flask(__name__)
app.config.from_object('funilaria.config.Configuration')
app.config.from_envvar('FUNILARIA_SETTINGS', silent=True)
db = Database(app)

from logging import Formatter
from logging.handlers import TimedRotatingFileHandler

if 'LOG_FILENAME' in app.config:
	try: 
		file_handler = TimedRotatingFileHandler(app.config['LOG_FILENAME'], when='D', interval=1, utc=True)
		file_handler.setLevel(logging.DEBUG)
		file_handler.setFormatter(Formatter(
			'%(asctime)s %(levelname)s: %(message)s '
			'[in %(pathname)s:%(lineno)d]'
		))
		app.logger.addHandler(file_handler)
	except Exception as err:
		app.logger.error("Cannot log to file=[{}]. Err=[{}]".format(app.config['LOG_FILENAME'],str(err)))

if app.debug:
	peewee_logger = logging.getLogger('peewee')
	peewee_logger.setLevel(logging.DEBUG)
	peewee_logger.addHandler(logging.StreamHandler())

# ----------- Init Extensions ----------- #


from flask.ext import admin

class MyAdmin(admin.Admin):
	def add_view(self, view, show_in_menu=True):
		self._views.append(view)

		# If app was provided in constructor, register view with Flask app
		if self.app is not None:
			self.app.register_blueprint(view.create_blueprint(self))

		if show_in_menu:
			self._add_view_to_menu(view)

admin = MyAdmin(app, name='Funilaria')

from views import *