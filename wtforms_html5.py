# -*- coding: UTF-8 -*-

"""
WTForms HTML5 Widgets
~~~~~~~~~~~~~~~~~~~~~

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

"""

from wtforms import TextField as _TextField
from wtforms import IntegerField as _IntegerField
from wtforms import DecimalField as _DecimalField
from wtforms import FloatField as _FloatField
from wtforms import DateField as _DateField

from wtforms.widgets import Input as _Input

from wtforms.validators import Length, NumberRange, StopValidation

from wtforms.compat import string_types


__all__ = (
  # WIDGETS
  'Input',
  'TextInput',
  'DateInput',
  'URLInput',
  'EmailInput',
  'SearchInput',
  'TelInput',
  'NumberInput',
  'RangeInput',
  'DecimalInput',
  'DecimalRangeInput',
  # FIELDS
  'TextField',
  'SearchField',
  'URLField',
  'EmailField',
  'TelField',
  'IntegerField',
  'DateField',
  'DecimalField',
  'FloatField',
  'IntegerRangeField',
  'DecimalRangeField',
  'FloatRangeField',
  # VALIDATORS
  'Required',
  'DataNotNone',
  'DateRange'
)


# CUSTOM LOGIC

def get_html5_kwargs(field, kwargs):
  """
  Return new *kwargs* for *field*.

  If the field got a *description* but no *title* is set, the *title*
  is set to *description*.

  Generate *kwargs* for the new HTML5 INPUT attributes (`required`, `min` and
  `max`) based on the validators set for *field*.

  Also set (or append) 'invalid' to the fields class(es), if the *field* got
  errors. 'invalid' is also set by browsers if they detect errors on a field.

  If a key is already in *kwargs* it is left untouched.

  """
  # got description?
  if not 'title' in kwargs and getattr(field, 'description'):
    kwargs['title'] = u'{}'.format(field.description)
  # is field required?
  if not 'required' in kwargs and field.flags.required:
    kwargs['required'] = u'required'
  # check validators Length, NumberRange or DateRange
  for vali in field.validators:
    if (
      isinstance(vali, Length) or
      isinstance(vali, NumberRange) or
      isinstance(vali, DateRange)
    ):
      if not 'min' in kwargs and hasattr(vali, 'min'):
        if vali.min and vali.min != -1:
          kwargs[u'min'] = vali.min
      if not 'max' in kwargs and hasattr(vali, 'max'):
        if vali.max and vali.max != -1:
          kwargs[u'max'] = vali.max
  # check for errors
  if field.errors:
    cls = kwargs.get('class', kwargs.pop('class_', ''))
    if cls:
      kwargs[u'class'] = u'invalid {}'.format(cls)
    else:
      kwargs[u'class'] = u'invalid'
  return kwargs


# WIDGETS

class Input(_Input):
  """Base INPUT class. Subclass this."""

  def __call__(self, field, **kwargs):
    kwargs = get_html5_kwargs(field, kwargs)
    return _Input.__call__(self, field, **kwargs)


class TextInput(Input):
  """Creates `<input type=text>` widget with custom *kwargs* parsing."""
  input_type = "text"


class NumberInput(Input):
  """Creates `<input type=number>` widget with custom *kwargs* parsing."""
  input_type = "number"


class DateInput(Input):
  """Creates `<input type=date>` widget with custom *kwargs* parsing."""
  input_type = "date"


class RangeInput(NumberInput):
  """Creates `<input type=range>` widget with custom *kwargs* parsing."""
  input_type = "range"


class URLInput(Input):
  """Creates `<input type=url>` widget with custom *kwargs* parsing."""
  input_type = "url"


class EmailInput(Input):
  """Creates `<input type=email>` widget with custom *kwargs* parsing."""
  input_type = "email"


class SearchInput(Input):
  """Creates `<input type=search>` widget with custom *kwargs* parsing."""
  input_type = "search"


class TelInput(Input):
  """Creates `<input type=tel>` widget with custom *kwargs* parsing."""
  input_type = "tel"


class DecimalInput(NumberInput):

  """Creates `<input type=number>` widget with custom *kwargs* parsing.

  Also adds a *step size* of ``any`` to the field, if not other step
  size is set.

  """

  def __call__(self, field, **kwargs):
    if not u'step' in kwargs:
      kwargs[u'step'] = u'any'
    return NumberInput.__call__(self, field, **kwargs)


class DecimalRangeInput(DecimalInput):

  """Creates `<input type=range>` widget with custom *kwargs* parsing.

  Also inherits *step size* from ``DecimalInput``.

  """

  input_type = "range"


# FIELDS

class TextField(_TextField):
  """**TextField** using **TextInput** by default """
  widget = TextInput()


class SearchField(TextField):
  """**TextField** using **SearchInput** by default """
  widget = SearchInput()


class URLField(TextField):
  """**TextField** using **URLInput** by default """
  widget = URLInput()


class EmailField(TextField):
  """**TextField** using **EmailInput** by default """
  widget = EmailInput()


class TelField(TextField):
  """**TextField** using **TelInput** by default """
  widget = TelInput()


class IntegerField(_IntegerField):
  """**IntegerField** using **NumberInput** by default """
  widget = NumberInput()


class DateField(_DateField):
  """**DateField** using **DateInput** by default """
  widget = DateInput()


class DecimalField(_DecimalField):
  """**DecimalField** using **DecimalInput** by default """
  widget = DecimalInput()


class FloatField(_FloatField):
  """**DecimalField** using **DecimalInput** by default """
  widget = DecimalInput()


class IntegerRangeField(_IntegerField):
  """**IntegerField** using **RangeInput** by default """
  widget = RangeInput()


class DecimalRangeField(_DecimalField):
  """**DecimalField** using **DecimalRangeInput** by default """
  widget = DecimalRangeInput()


class FloatRangeField(_FloatField):
  """**DecimalField** using **DecimalRangeInput** by default """
  widget = DecimalRangeInput()


# VALIDATORS


class Required(object):

  """
  No validation, just set the *required* flag.

  Setting the *required* flag along with ``get_html5_kwargs`` prevents
  browsers from sending empty fields.

  """

  field_flags = ('required', )

  def __call__(self, form, field):
    pass


class DataNotNone(object):

  """
  Validates that the field contains data that is not ``None``.

  This validator will stop the validation chain on error.

  If the data is not ``None``, it also removes prior errors (such as
  processing errors) from the field.

  :param message:
      Error message to raise in case of a validation error.

  """

  field_flags = ('required', )

  def __init__(self, message=None):
      self.message = message

  def __call__(self, form, field):
    if field.data is None or (
      isinstance(field.data, string_types)
      and not field.data.strip()
    ):
      if self.message is None:
        self.message = field.gettext('This field is required.')
      field.errors[:] = []
      raise StopValidation(self.message)


class DateRange(object):

  """
  Validate that a date is in the *min* and *max* range.

  :param message:
    Error message to raise in case of a validation error.
    *message* should be a tuple if you want two different error messages.

  """

  def __init__(self, min=None, max=None, message=None):
    try:
      self.err_min, self.err_max = message
    except TypeError:
      self.err_min = self.err_max = message
    self.min = min
    self.max = max

  def __call__(self, form, field):
    if self.min and field.data < self.min:
      if not self.err_min:
        self.err_min = field.gettext("Date must be >= {}.").format(self.min)
      field.errors.append(self.err_min)
    if self.max and field.data > self.max:
      if not self.err_max:
        self.err_max = field.gettext("Date must be >= {}.").format(self.max)
      field.errors.append(self.err_max)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
