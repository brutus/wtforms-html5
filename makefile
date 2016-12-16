default: styletests clean

test: styletests doctests unittests clean

styletests:
	pyflakes wtforms_html5.py
	pylama wtforms_html5.py

doctests:
	python -m doctest wtforms_html5.py

unittests:
	python -m unittest discover

cover:
	coverage run --append --source wtforms_html5 -m unittest discover
	coverage report -m

clean:
	find -not \( -path './.git/*' -o -path './.tox/*' \) -a \( -name '__pycache__' -o -name '*.pyc' -o -name '*.egg-info' -o -path '*.egg-info/*' \) > /dev/null
