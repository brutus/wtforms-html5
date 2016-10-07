full: stylechecks doctests unittests clean

unittests:
	python -m unittest discover

doctests:
	python -m doctest wtforms_html5.py

stylechecks:
	flake8 wtforms_html5.py
	pylint --errors-only wtforms_html5.py

clean:
	find -not -path .git -type f -name '*.pyc' -delete
	find -not -path .git -type d -name '__pycache__' -delete
	find -not -path .git -type d -name '*.egg-info' -delete
