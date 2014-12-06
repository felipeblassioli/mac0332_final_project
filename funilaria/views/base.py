# -*- coding: utf-8 -*-

from flask.ext.admin import BaseView
from flask.ext.admin.contrib.peewee import ModelView
from flask.ext.admin.model.helpers import prettify_name


from jinja2 import contextfunction
from peewee import ForeignKeyField, PrimaryKeyField

class MyBaseModelView(ModelView):
	form_excluded_columns = ('created_at', 'updated_at')

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