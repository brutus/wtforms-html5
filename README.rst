=====================
WTForms HTML5 Widgets
=====================

This modul adds HTML5 widgets to WTForms_.

It supports the new INPUT **types** for fields and also sets some of the
new INPUT **attributes** automatically (based on widget type and what kind of
validators are set for the field).


Examples
========

>>> # 1st import the needed stuff...
>>> from wtforms import Form
>>> from wtforms.validators import Length, NumberRange, Required
>>> from wtforms_html5 import TextField, IntegerField, DateField
>>> from wtforms_html5 import DateRange
>>> from datetime import date
>>> # the next one is just to test the forms below, it's nomally not needed
>>> from werkzeug.utils import MultiDict
>>> # now the main part: declare your form
>>> class TestForm(Form):
...  name = TextField('Name', validators=[Required(), Length(5, 25)])
...  number = IntegerField('Number', validators=[NumberRange(1000, 9999)], description='Some stuff...')
...  date = DateField('Date:', validators=[DateRange(date(2000,1,1), date(2012,4,20))])
...
>>> # lets see how the generated input fields look like...
>>> # the ``min``, ``max`, ``required` and ``title`` attributes where auto-
>>> # generated from the declaration
>>> f = TestForm()
>>> f.name()
u'<input id="name" max="25" min="5" name="name" required="required" type="text" value="">'
>>> f.number()
u'<input id="number" max="9999" min="1000" name="number" title="Some stuff..." type="number" value="">'
>>> f.date()
u'<input id="date" max="2012-04-20" min="2000-01-01" name="date" type="date" value="">'
>>> # and finally test ``DateRange`` and the setting of the ``invalid`` class on error
>>> d = MultiDict({'name':'Testor', 'date':'1995-05-01'})
>>> f.process(d)  # enter the data to the form
>>> f.validate()  # and check for errors...
False
>>> f.errors
{'date': ['Date must be >= 2000-01-01.'], 'number': [u'Number must be between 1000 and 9999.']}


Install
=======

You can install **WTForms HTML5 Widgets** with pip_ or from source.

Install with pip
----------------

pip_ is "*a tool for installing and managing Python packages*". If you don't
have it installed, see the `pip install instructions`_.

  ``pip install boozelib``

Install from source
-------------------

You can fetch the latest sourceball_ from github and unpack it, or just clone
this repository: ``git clone git://github.com/brutus/boozelib.git``. If you
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
  *InputRequired*. You can set just the flag without any validator logic with
  the *Required* validator from this modul.

* **min** and **max**

  If either **Length**, **NumberRange** or **DateRange** is used as a
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

  Works like the original **DataRequired** but only raises Errors if the
  data is ``None``, so that ``Flase`` or ``0`` are accepted values.

* **DateRange**

  Allows the use of *min* and *max* limits for date fields.


Testing and Contribution
========================

**WTForms HTML5 Widgets** is at home at:

  https://github.com/brutus/wtforms-html5/

If you find any bugs, issues or anything, please use the `issue tracker`_.


.. _home: https://github.com/brutus/wtforms-html5/
.. _sourceball: https://github.com/brutus/wtforms-html5/zipball/master
.. _`issue tracker`: https://github.com/brutus/wtforms-html5/issues
.. _WTForms: http://wtforms.simplecodes.com/
.. _pip: http://www.pip-installer.org/en/latest/index.html
-- _`pip install instructions`: http://www.pip-installer.org/en/latest/installing.html
