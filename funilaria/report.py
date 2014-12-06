# -*- coding: utf-8 -*-

from .models import Person, Order
from peewee import fn


class Report(object):
	@staticmethod
	def clientsXOrders():
		query = Person.select(Person.name, Person.cpf, fn.count(Order.id).alias('total_orders')).join(Order, on=(Person.id == Order.client)).group_by(Person.id).order_by(fn.count(Order.id).desc())
		#return [ row for row in query ]
		return query

	@staticmethod
	def attendantsXOrders():
		query = Person.select(Person.name, Person.cpf, fn.count(Order.id).alias('total_orders')).join(Order, on=(Person.id == Order.added_by)).group_by(Person.id).order_by(fn.count(Order.id).desc())
		#return [ row for row in query ]
		return query