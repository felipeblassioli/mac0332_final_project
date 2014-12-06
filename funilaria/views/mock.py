from . import app
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