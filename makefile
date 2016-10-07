default: stylechecks

test: stylechecks doctests unittests clean

stylechecks:
	flake8 wtforms_html5.py
	pylint --errors-only wtforms_html5.py

doctests:
	python -m doctest wtforms_html5.py

unittests:
	python -m unittest discover

cover:
	coverage run --append --source wtforms_html5 -m unittest discover
	coverage report -m

clean:
	find -not -path .git -type f -name '*.pyc' -delete
	find -not -path .git -type d -name '__pycache__' -delete
	find -not -path .git -type f -path '*.egg-info/*' -delete
	find -not -path .git -type d -name '*.egg-info' -delete
