=====================
WTForms HTML5 Widgets
=====================

This modul adds HTML5 widgets to WTForms_.

It supports the new INPUT **types** for fields and also sets some of the
new INPUT **attributes** automatically (based on widget type and what kind of
validators are set for the field).

There are **widgets** for all the new INPUT types, that you can use in your
own fields and also **field** classes ready to use. Along with some
**validators** that take advantage of the new attributes.

Use it just like WTForms_. The only difference is, that you import the
**fields** from ``wtforms_html5`` instead.


Examples
========

First import the needed modules...

>>> from wtforms import Form
>>> from wtforms.validators import Length, NumberRange, DataRequired
>>> from wtforms_html5 import TextField, IntegerField, DateField
>>> from wtforms_html5 import DateRange

And some extra stuff for our examples  (nomally not needed)

>>> from datetime import date
>>> from werkzeug.utils import MultiDict

Then comes the main part: declare your form. This works just like vanilla
WTForms, just use the **fields** you imported from ``wtforms_html5``
instead...

>>> class TestForm(Form):
...  name = TextField('Name', validators=[DataRequired(), Length(5, 25)])
...  number = IntegerField('Number', validators=[NumberRange(1000, 9999)], description='Some stuff...')
...  date = DateField('Date:', validators=[DateRange(date(2000,1,1), date(2012,4,20))])
...

Now let's see, how the generated input fields look like... the ``min``,
``max``, ``required`` and ``title`` attributes where auto-generated from the
declaration.

>>> f = TestForm()
>>> f.name()
u'<input id="name" max="25" min="5" name="name" required="required" type="text" value="">'
>>> f.number()
u'<input id="number" max="9999" min="1000" name="number" title="Some stuff..." type="number" value="">'
>>> f.date()
u'<input id="date" max="2012-04-20" min="2000-01-01" name="date" type="date" value="">'

And finally some quick tests for ``DateRange`` and the setting of the
``invalid`` class on error...

>>> d = MultiDict({'name':'Testor', 'date':'1995-05-01'})
>>> f.process(d)  # enter the data to the form
>>> f.validate()  # and check for errors...
False
>>> f.errors
{'date': ['Date must be >= 2000-01-01.'], 'number': [u'Number must be between 1000 and 9999.']}
>>> f.number()
u'<input class="invalid" id="number" max="9999" min="1000" name="number" title="Some stuff..." type="number" value="">'


Install
=======

You can install **WTForms HTML5 Widgets** with pip_ or from source.

Install with pip
----------------

pip_ is "*a tool for installing and managing Python packages*". If you don't
have it installed, see the `pip install instructions`_.

  ``pip install wtforms-html5``

Install from source
-------------------

You can fetch the latest sourceball_ from github and unpack it, or just clone
this repository: ``git clone git://github.com/brutus/wtforms-html5.git``. If you
got the source, change into the directory and use ``setup.py``:

  ``python setup.py install``

Since **WTForms HTML5 Widgets** only adds functionallity to WTForms_, you need
to have WTForms_ installed too. But if you use the installation methods
described above, it should have been taken care of.


Details
=======

Supported INPUT types
---------------------

* TextField
* SearchField
* URLField
* EmailField
* TelField
* IntegerField
* IntegerRangeField
* DecimalField
* DecimalRangeField
* FloatField
* FloatRangeField
* DateField


Supported auto-attributes
-------------------------

* **title**

  If no *title* attribute is provided for a field, but a *description*,
  the description is used for the *title*.

* **required**

  Is set if the field has the ``required`` flag set.

  This happens if you use one of these validators: *DataRequired* or
  *InputRequired*. Or *DataNotNone* from this modul. You can set just the flag
  without any validator logic with the *Required* validator from this modul.

* **min** and **max**

  If either *Length*, *NumberRange* or *DateRange* is used as a
  validator and sets a minimal or maximal value, the corresponding INPUT
  attribute is set.

* **invalid**

  If the field got any validation errors, the css class *invalid* gets set.


New validators
--------------

* **Required**

  The *Required* validator from wtforms is an old alias for *DataRequired*.
  It is deprecated and will be removed in 1.2. The *Required* validator from
  this modul just sets the ``required`` flag, without any validator logic.

* **DataNotNone**

  Works like the original *DataRequired* but only raises an Error if the
  data is ``None``, so that ``False`` or ``0`` are accepted values.

* **DateRange**

  Allows the use of *min* and *max* limits for date fields.


Testing and Contribution
========================

**WTForms HTML5 Widgets** is at home at: https://github.com/brutus/wtforms-html5/

If you find any bugs, issues or anything, please use the `issue tracker`_.

Testing
-------

There are some **doctest** in the module. You can either run them from the
*source directory* like this ``python wtforms_html5.py -v`` or, if you got
this modul already installed, like this ``python -m doctest -v
wtforms_html5``.

If you want to run the **test cases**, see that you got nose_ installed. You
can install it like this: ``pip install nose``. Now either run ``nosetests``
from the *source directory* or, if you got this modul already installed, run
them like this: ``nosetest test_wtforms_html5``.

If something fails, please get in touch.


.. _home: https://github.com/brutus/wtforms-html5/
.. _sourceball: https://github.com/brutus/wtforms-html5/zipball/master
.. _`issue tracker`: https://github.com/brutus/wtforms-html5/issues
.. _WTForms: http://wtforms.simplecodes.com/
.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _`pip install instructions`: http://www.pip-installer.org/en/latest/installing.html
.. _nose: http://readthedocs.org/docs/nose/en/latest/testing.html
