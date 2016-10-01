=============
WTForms HTML5
=============

**Original Function**: This module used to add HTML5 support to WTForms_.

It supported the new INPUT **types** for fields and also sets some of the new
INPUT **attributes** automatically (based on widget type and what kind of
validators are set for the field).

**Changes**: WTForms_ version 1.0.4 started to implement some of these
features and the current development version (that should become version 3)
has enough support for all features, so that to prevent the duplication of
functionality, current versions of *WTForms HTML5* dropped all the fields,
widgets and validators — just use vanilla WTForms_.

**Current Function**: recent versions (starting with 0.2) contain only a
function that adds the automatically generated keys to the *render_kw* of a
field. Also a slim subclass of the new `DefaultMeta` class for forms. If you
use this class as your forms meta, you get the automatic attributes just like
in the original version of *WTForms HTML5*.


Supported Auto–Attributes
=========================

- **required**

  Is set if the field has the ``required`` flag set.

  This happens if you use the *DataRequired* or *InputRequired* validator.

- **invalid**

  If the field got any validation errors, the CSS class *invalid* gets set.

- **min** and **max**

  If either *Length* or *NumberRange* or *DateRange* is used as a validator
  and sets a minimal or maximal value, the corresponding INPUT attribute is
  set.

- **title**

  If no *title* attribute is provided for a field, but a *description*, the
  *description* is used for the *title*.



Example
=======

Declare your form just like vanilla WTForms but include :cls:`AutoAttrMeta`
as your meta class::

>>> from wtforms import Form, StringField
>>> from wtforms.validators import InputRequired, Length
>>> from wtforms_html5 import AutoAttrMeta
>>> class MyForm(Form):
...   class Meta(AutoAttrMeta):
...     pass
...   test_field = StringField(
...     'Testfield',
...      validators=[InputRequired(), Length(min=3, max=12)],
...      description='Just a test field.',
...   )
>>> form = MyForm()

The only difference is, that you include a `Meta` class that inherits from
:cls:`AutoAttrMeta`. Now you get some attributes created automatically for your fields:

>>> form.test_field()
'<input id="test_field" max="12" min="3" name="test_field" required title="Just a test field." type="text" value="">'

As you can see, the *min* and *max* attributes are created because you used
the `Length` validator. The field also gets a *title* taken from the fields
`description`. And the field is marked *required* because of the
`InputRequired` validator.

If you validate the form and any errors pop up, the field would also get an
*invalid* attribute::

>>> form.validate()
False
>>> form.test_field()
'<input class="invalid" id="test_field" max="12" min="3" name="test_field" required title="Just a test field." type="text" value="">'



Install
=======

You can install **WTForms HTML5 Widgets** with pip_ or from source.

Install with pip
----------------

pip_ is *"a tool for installing and managing Python packages"*. If you don't
have it installed, see the `pip install instructions`_.

  ``pip install wtforms-html5``

Install from source
-------------------

You can fetch the latest sourceball_ from github and unpack it, or just clone
this repository: ``git clone git://github.com/brutus/wtforms-html5.git``.
If you got the source, change into the directory and use ``setup.py``:

  ``python setup.py install``

Requirements
------------

Since **WTForms HTML5** only adds functionality to WTForms_, you need to have
WTForms_ installed too. But if you use the installation methods described
above, it should have been taken care of.



Testing and Contribution
========================

**WTForms HTML5 Widgets** is at home at: https://github.com/brutus/wtforms-html5/

If you find any bugs, issues or anything, please use the `issue tracker`_.

Testing
-------

There are some **doctest** in the module. You can run them from the *source
directory* like this: ``python -m doctest wtforms_html5.py``. If you want to
run the **test cases**, run ``python -m unittest``, also  from the *source
directory*.

If something fails, please get in touch.

Additional Requirements
-----------------------

To run the test cases a few additional requirements need to be fulfilled: see
the `requirements/testing.txt` file for a list. You can install all testing
requirements like this: ``pip install -r requirements/testing.txt``.



.. _home: https://github.com/brutus/wtforms-html5/
.. _sourceball: https://github.com/brutus/wtforms-html5/zipball/master
.. _`issue tracker`: https://github.com/brutus/wtforms-html5/issues
.. _WTForms: http://wtforms.simplecodes.com/
.. _pip: http://www.pip-installer.org/en/latest/index.html
.. _`pip install instructions`: http://www.pip-installer.org/en/latest/installing.html
