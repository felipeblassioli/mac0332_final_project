# -*- coding: utf-8 -*-
from peewee import *
from . import db

import datetime

class BaseModel(db.Model):
	created_at = DateTimeField(default=datetime.datetime.now)
	updated_at = DateTimeField(default=None, null=True)

	@property
	def data(self):
		return self.__dict__['_data']

	def to_json(self):
		_data = self.data
		for f in ['created_at','updated_at', 'id']:
			_data.pop(f,None)
		return _data

	def save(self, *args, **kwargs):
		self.updated_at = datetime.datetime.now()
		return super(BaseModel, self).save(*args, **kwargs)

# ---------------------- Models ------------------- #

class Person(BaseModel):
	name = TextField()
	email = TextField()
	cpf = TextField()
	address = TextField()
	# A: Attendant, M: Manager, C: Client
	type = CharField(max_length=1)

	@property
	def phones(self):
		return [ p for p in Phone.select().where(PersonPhone.person == self) ]

	def __str__(self):
		return '{} ({})'.format(self.name, self.cpf)

class Phone(BaseModel):
	# 'M': Mobile, 'W': Work
	type = CharField(max_length=1)
	number = TextField()

	@property
	def is_mobile(self):
		return self.type == 'M'

class Vehicle(BaseModel):
	owner = ForeignKeyField(Person, related_name='vehicles')
	year = IntegerField()
	model = CharField(max_length=32)
	plate = CharField(max_length=32)

	def __str__(self):
		return '%s - %d placa: %s' % (self.model,self.year,self.plate)
class Order(BaseModel):
	client = ForeignKeyField(Person, related_name='orders')
	vehicle = ForeignKeyField(Vehicle)
	remind_at = DateTimeField(null=True)


class Photo(BaseModel):
	order = ForeignKeyField(Order)
	filename = CharField(max_length=255)
	# 'B': Before , 'A': after
	type = CharField(max_length=1)

# ---------------- Rels ---------------- #

class PersonPhone(db.Model):
	person = ForeignKeyField(Person)
	phone = ForeignKeyField(Phone)

# ---------------- Utils ---------------- #

MODELS = [Person, Phone, Vehicle, Order, Photo, PersonPhone]
def create_tables():
	for m in MODELS:
		m.create_table(fail_silently=True)