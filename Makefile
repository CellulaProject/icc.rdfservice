.PHONY: env dev install test edit

LPYTHON=python3
V=$(PWD)/../$(LPYTHON)
PYTHON=$(V)/bin/$(LPYTHON)
ROOT=$(PWD)
INI=icc.rdfservice

env:
	[ -d $(V) ] || virtualenv  $(V)

dev:	env
	$(V)/bin/pip install rdflib
	$(PYTHON) setup.py develop

install: env
	$(PYTHON) setup.py install

edit:
	cd src && emacs

test:
	ip a | grep 2001
	ip a | grep 172.
	. $(V)/bin/activate
	$(V)/bin/pserve $(INI).ini --reload
	#cd src && $(PYTHON) app.py
