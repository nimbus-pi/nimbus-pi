all: dependencies

dependencies:
	pip install -r requirements.txt

test:
	pylint nimbus_pi --rcfile=.pylintrc
	behave -f progress --junit tests/
