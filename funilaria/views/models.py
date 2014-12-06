# -*- coding: utf-8 -*-

from flask.ext.admin.contrib.peewee import ModelView
from flask.ext.admin import BaseView
from wtforms import SelectField
from wtforms.validators import Email

from ..models import Person, Order, Vehicle
from .base import MyBaseModelView

class PersonView(MyBaseModelView):
	#column_labels
	column_list = ('name', 'email', 'address', 'cpf','type')
	column_choices = dict(type=[('A', 'Atendente'), ('M', 'Gerente'), ('C', 'Cliente')])
	column_searchable_list = ('name', 'email', 'cpf')
	can_delete = False
	#column_filters = ('name', 'email')
	
	page_size = 6

	# Form overrides
	list_template = 'client_list.html'

	form_overrides = dict(type=SelectField)
	form_args = dict(
		# Pass the choices to the `SelectField`
		type=dict(label=u'Tipo', choices=[('A', 'Atendente'), ('M', 'Gerente'), ('C', 'Cliente')]),
		name=dict(label=u'Nome'),
		address=dict(label=u'Endereço'),
		email=dict(validators=[Email()]),
		cpf=dict(label='CPF')
	)

	def __init__(self, **kwargs):
		super(PersonView, self).__init__(Person, **kwargs)

class OrderView(MyBaseModelView):
	column_list = ('client', 'vehicle', 'remind_at', 'created_at')

	create_template = 'create_order.html'

	def __init__(self, **kwargs):
		super(OrderView, self).__init__(Order, **kwargs)

class VehicleView(MyBaseModelView):
	def __init__(self, **kwargs):
		super(VehicleView, self).__init__(Vehicle, **kwargs)