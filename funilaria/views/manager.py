from ..models import Person
from ..report import Report
from .base import MyBaseModelView

class BaseReportView(MyBaseModelView):
	can_create = False
	can_edit = False
	can_delete = False

	def __init__(self, **kwargs):
		super(BaseReportView, self).__init__(Person, **kwargs)

	def scaffold_list_columns(self):
		return ['name','cpf','total_orders']


class ReportClientsXOrdersView(BaseReportView):
	def get_query(self):
		return Report.clientsXOrders()

class ReportAttendantsXOrdersView(BaseReportView):
	def get_query(self):
		return Report.attendantsXOrders()

