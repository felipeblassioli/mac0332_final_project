class Configuration(object):
	#: Application's root directory.
	DIR_ROOT = '/var/www/funilaria'
	UPLOADED_DEFAULT_DEST = DIR_ROOT + '/uploads'
	#: Log file for the application
	LOG_FILENAME = DIR_ROOT + '/funilaria.log'
	DATABASE = {
		'name': 'funilaria',
		'engine': 'peewee.MySQLDatabase',
		'user': 'root',
		'passwd': ''
	}
	DEBUG = True
	SECRET_KEY = 'shhhh'
	#: enable MockView
	MOCK = True