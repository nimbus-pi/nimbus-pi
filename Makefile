all: dependencies

dependencies:
	pip install -r requirements.txt
	#python setup.py install

test:
	pylint nimbus_pi --rcfile=.pylintrc
	#behave -f progress --junit tests/
