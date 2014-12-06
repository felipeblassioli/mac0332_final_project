# -*- coding: utf-8 -*-

from . import app, admin
from flask import redirect

@app.route('/')
def hello():
	return redirect('/admin')

from .models import create_tables
@app.route('/setup/')
def setup():
	create_tables()
	return "Ok"

from .models import Person
@app.route('/mock/')
def mock():
	for i in range(1,100):
		params = dict(
			name='client%003d' % i,
			email='client%003d@gmail.com.br' % i,
			type='C',
			cpf=str((99999999911 - i)),
			address='Estrada das lagrimas, %d' % i
		)
		Person.create(**params)
	for i in range(1,2):
		params = dict(
			name='manager%003d' % i,
			email='manager%003d@gmail.com.br' % i,
			type='M',
			cpf=str((11111111111 - i)),
			address='Estrada das lagrimas, %d' % i
		)
		Person.create(**params)
	for i in range(1,5):
		params = dict(
			name='attendant%003d' % i,
			email='attendant%003d@gmail.com.br' % i,
			type='A',
			cpf=str((333333333 - i)),
			address='Estrada das lagrimas, %d' % i
		)
		Person.create(**params)
	return "Ok"

# ------------ Register AdminViews ------------ #

from flask.ext.admin.contrib.peewee import ModelView
from flask.ext.admin import BaseView, expose
from .models import Person, Order, Vehicle
from wtforms import SelectField
from wtforms.validators import Email

class MyBaseModelView(ModelView):
	form_excluded_columns = ('created_at', 'updated_at')


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

# {% for c, name in list_columns %}
# <td>{{ get_value(row, c) }}</td>
# {% endfor %}

class TesteView(MyBaseModelView):
	list_template = 'client_list.html'
	page_size=5
	can_create = False
	can_edit = False
	can_delete = False
	column_list = ('name', 'email', 'address', 'cpf','type')

	def _handle_vehicle(self, v,c,m):
		print v,c,m
		return 'hello'

	column_formatters = dict(cpf=_handle_vehicle)

	def get_list(self, page, sort_column, sort_desc, search, filters,execute=True):
		p = Person.get(Person.name=='Felipe')
		v = Vehicle.get(Vehicle.owner == p)
		print '-------->', p, v
		return 1, [p, v,v,v,p]

	def __init__(self, **kwargs):
		print self.list_template
		super(TesteView, self).__init__(Person, endpoint='bla', **kwargs)

from flask.ext.admin.model.helpers import prettify_name
from jinja2 import contextfunction
from peewee import ForeignKeyField, PrimaryKeyField

class BaseMultiView(BaseView):
	column_list = None
	column_exclude_list = None
	column_labels = None
	column_formatters = None

	column_display_pk = False

	def _prettify_name(self, name):
		return prettify_name(name)


	def get_column_name(self, field):
		if self.column_labels and field in self.column_labels:
			return self.column_labels[field]
		else:
			return self._prettify_name(field)

	def scaffold_list_columns(self, model):
		columns = []

		for n, f in model._meta.get_sorted_fields():
			# Verify type
			field_class = type(f)

			if field_class == ForeignKeyField:
				columns.append(n)
			elif self.column_display_pk or field_class != PrimaryKeyField:
				columns.append(n)

		return [(c, self.get_column_name(c)) for c in columns]

	def get_list_columns(self):
		return dict(
			orders=self.scaffold_list_columns(Order),
			vehicles=self.scaffold_list_columns(Vehicle)
		)

	def _get_field_value(self, model, name):
		if hasattr(model, name):
			return getattr(model, name)
		else:
			return ''

	@contextfunction
	def get_list_value(self, context, model, name):
		value = self._get_field_value(model, name)
		return value

	def get_empty_list_message(self):
		return 'There are no items in the table.'


class ClientView(BaseMultiView):
	# def is_accessible(self):
	# 	return False

	@expose('/<id>')
	@expose('/')
	def index(self,id=None):
		if id is None: id = 1
		p = Person.get(Person.id==id)
		print list(p.orders.execute())
		print list(p.vehicles.execute())
		print '-------xxxxxxxxxxxxxxxxxxx-----'
		return self.render(
			'index.html', 
			client = p,
			num_pages=1, 
			get_value=self.get_list_value,
			list_columns=self.get_list_columns()
		)

#admin.add_view(ModelView(Vehicle,name='Vehicle'))
admin.add_view(PersonView(name='Clientes'))
admin.add_view(OrderView(name='Ordens'))
admin.add_view(ClientView(name='Detalhes'), show_in_menu=False)

for name, model_field in Person._meta.get_sorted_fields():
	print name, model_field