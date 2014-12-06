# -*- coding: utf-8 -*-
from wtforms import SelectField
from wtforms.validators import Email

from ..models import Person, Order, Vehicle
from .base import MyBaseModelView

class PersonView(MyBaseModelView):
	#column_labels
	column_list = ('name', 'email', 'address', 'cpf')
	column_choices = dict(type=[('A', 'Atendente'), ('M', 'Gerente'), ('C', 'Cliente')])
	column_searchable_list = ('name', 'email', 'cpf')
	can_delete = False
	#column_filters = ('name', 'email')
	column_labels = dict(
		name='Nome', 
		address=u'Endereço',
	)

	
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

	def get_query(self):
		return self.model.select().where(Person.type=='C')

class OrderView(MyBaseModelView):
	column_list = ('client', 'added_by', 'vehicle', 'remind_at', 'created_at')
	column_labels = dict(
		client='Cliente', 
		vehicle='Veiculo',
		remind_at='Data Validade',
		added_by='Criada por',
		created_at='Criada em',
	)

	create_template = 'create_order.html'

	def __init__(self, **kwargs):
		super(OrderView, self).__init__(Order, **kwargs)

class VehicleView(MyBaseModelView):
	column_list = ('owner', 'year', 'model', 'plate')
	column_searchable_list = ('plate',)
	column_labels = dict(
		owner='Dono', 
		plate='Placa',
		year='Ano',
		model='Modelo'
	)

	def __init__(self, **kwargs):
		super(VehicleView, self).__init__(Vehicle, **kwargs)