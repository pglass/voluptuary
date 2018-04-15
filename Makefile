.PHONY: clean test

VENV=.venv
VENV_ACTIVATE=. $(VENV)/bin/activate
BUMPTYPE=patch

$(VENV):
	virtualenv $(VENV)
	$(VENV_ACTIVATE); pip install tox bumpversion

test: $(VENV)
	$(VENV_ACTIVATE); tox

release: test
	python setup.py sdist upload -r pypi

bump: $(VENV)
	$(VENV_ACTIVATE); bumpversion $(BUMPTYPE)
	git show -q
	@echo
	@echo "SUCCESS: Version was bumped and committed. Now push the commit:"
	@echo
	@echo " 	git push origin master && git push --tags"

clean:
	rm -rf $(VENV)
