# -*- coding: utf-8 -*-

from flask.ext.admin import expose

from .models import Person
from .base import BaseMultiView

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


