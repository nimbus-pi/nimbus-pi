all: install

install:
	pip install -r requirements.txt
	#python setup.py install

test:
	pylint nimbuspi --rcfile=.pylintrc
	pylint nimbuspi/tests/steps/*.py --rcfile=.pylintrc
	behave nimbuspi/tests/

coverage:
	@-coverage run --source='./nimbuspi/' --omit=nimbuspi/__*,nimbuspi/tests/* -m behave -f progress nimbuspi/tests/
	@coverage xml
	@coverage html
	coverage report

clean:
	@-find . -type f -name '*.pyc' -delete ||: > /dev/null 2>&1
	@-rm -rf .coverage coverage.xml htmlcov ||: > /dev/null 2>&1
