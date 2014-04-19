MAKEFLAGS = --no-print-directory --always-make --silent
MAKE = make $(MAKEFLAGS)

VENV_NAME = blog
VENV_PATH = ~/.virtualenvs/$(VENV_NAME)
VENV_ACTIVATE = . $(VENV_PATH)/bin/activate
TEST_POST_DIR = $(PWD)/src/test/posts

clean:
	find . -name "*.pyc" -print -delete
	find . \( -name "*.min.js" -o -name "*.min.css" \) -print -delete
	rm -rfv $(VENV_PATH) && \
	$(MAKE) empty-test-posts

empty-test-posts:
	find src/test -name 'posts' -print -delete && \
	mkdir $(TEST_POST_DIR)

check:
	$(MAKE) virtualenv
	$(MAKE) pylint pep8 nosetests

virtualenv:
	test -d $(VENV_PATH) || virtualenv $(VENV_PATH)
	$(VENV_ACTIVATE) && python setup.py --quiet develop

pep8:
	@echo "Running pep8..."
	$(VENV_ACTIVATE) && pep8 src/web

pylint:
	@echo "Running pylint..."
	$(VENV_ACTIVATE) && \
    pylint src/data && \
    pylint src/commands && \
    pylint src/web && \
    pylint src/test && \
	PYTHONPATH=src pylint src/*.py

nosetests:
	@echo "Running nosetests..."
	$(VENV_ACTIVATE) && BLOG_ENV=test nosetests
