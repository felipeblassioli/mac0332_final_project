from . import app
from .models import Person, Vehicle, Order
from random import randint, choice

import datetime

VEHICLE_MODELS = [ 'Fusca', 'Fiat Palio', 'Ferrari', 'Tucson', 'BMW', 'Porsche', 'Fiat UNO', 'Saveiro', 'Clio', 'Renault' ]

# ----------------- Utils ----------------- #

def _random_plate():
	alphabet = [ c for c in 'ABCDEFGHIJKLMNOPQRSTUVXYZ']
	letters = ''.join([ choice(alphabet) for i in range(1,4) ])
	numbers = ''.join([ str(randint(0,9)) for i in range(0,4)])
	return '{}-{}'.format(letters,numbers)

def _random_attendant():
	attendants = [ a for a in Person.select().where(Person.type=='A') ]
	x = choice(attendants)
	print x
	return x

def _random_vehicle(client):
	vehicles = [ v for v in client.vehicles ]
	return choice(vehicles)

def _random_order_datetime():
	year, month, day = randint(2005,2014), randint(1,12), randint(1,28)
	d = datetime.timedelta(days=randint(1,19))

	begin = datetime.date(year, month, day)
	end = begin + d
	remind_at = begin + datetime.timedelta(weeks=2)
	return begin,end,remind_at
	
# ----------------- Mocks ----------------- #

def _mock_managers(total):
	for i in range(0,total):
		params = dict(
			name='manager%003d' % i,
			email='manager%003d@gmail.com.br' % i,
			type='M',
			cpf=str((11111111111 - i)),
			address='Estrada das lagrimas, %d' % i
		)
		Person.create(**params)

def _mock_attendants(total):
	for i in range(0,total):
		params = dict(
			name='attendant%003d' % i,
			email='attendant%003d@gmail.com.br' % i,
			type='A',
			cpf=str((333333333 - i)),
			address='Estrada das lagrimas, %d' % i
		)
		Person.create(**params)

def _mock_clients(total=100, max_vehicles=3, max_orders=10):
	for i in range(0,total):
		params = dict(
			name='client%003d' % i,
			email='client%003d@gmail.com.br' % i,
			type='C',
			cpf=str((99999999911 - i)),
			address='Estrada das lagrimas, %d' % i
		)
		p = Person.create(**params)

		for i in range(0,randint(1,max_vehicles)):
			params = dict(
				owner=p,
				year=randint(1993,2014),
				model=choice(VEHICLE_MODELS),
				plate=_random_plate()
			)
			v = Vehicle.create(**params)

		for i in range(0, randint(0,max_orders)):
			b,e,r = _random_order_datetime()
			params = dict(
				added_by=_random_attendant(),
				client=p,
				vehicle=_random_vehicle(p),
				begin=b,
				end=e,
				remind_at=r,
			)
			o = Order.create(**params)

# ----------------- Public ----------------- #

@app.route('/mock/')
def mock():
	_mock_managers(2)
	_mock_attendants(5)
	_mock_clients(100,3)

	return "Ok"