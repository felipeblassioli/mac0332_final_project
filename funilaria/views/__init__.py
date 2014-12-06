# -*- coding: utf-8 -*-

from .. import app, admin
from flask import redirect

@app.route('/')
def hello():
	return redirect('/admin')

from ..models import create_tables
@app.route('/setup/')
def setup():
	create_tables()
	return "Ok"

import mock

from .models import PersonView, OrderView, VehicleView
from .client import ClientView
from .manager import ReportClientsXOrdersView, ReportAttendantsXOrdersView

admin.add_view(PersonView(name='Clientes'))
admin.add_view(OrderView(name='Ordens'))
admin.add_view(VehicleView(name='Veiculos'))
admin.add_view(ClientView(name='Detalhes'), show_in_menu=False)

admin.add_view(ReportClientsXOrdersView(name='Ordens X Clientes', endpoint='relatorio1', category=u'Relatórios'))
admin.add_view(ReportAttendantsXOrdersView(name='Ordens X Atendentes', endpoint='relatorio2', category=u'Relatórios'))