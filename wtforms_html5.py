# -*- coding: UTF-8 -*-

"""
Generates render keywords for widgets of WTForms HTML5 fields.

The :func:`get_html5_kwargs` generates rendering keywords for a field.

The :cls:`AutoAttrMeta` can be included as a base class for the `Meta` class
in your forms to handle this automatically for each field of the form.


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
:cls:`AutoAttrMeta`. Now you get some attributes created automatically for
your fields:

>>> form.test_field()
'<input id="test_field" max="12" min="3" name="test_field" required \
title="Just a test field." type="text" value="">'

As you can see, the *min* and *max* attributes are created because you used
the `Length` validator. The field also gets a *title* taken from the fields
`description`. And the field is marked *required* because of the
`InputRequired` validator.

If you validate the form and any errors pop up, the field would also get an
*invalid* attribute::

>>> form.validate()
False
>>> form.test_field()
'<input class="invalid" id="test_field" max="12" min="3" name="test_field" \
required title="Just a test field." type="text" value="">'

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from wtforms.fields.core import UnboundField
from wtforms.meta import DefaultMeta
from wtforms.validators import (
    Length,
    NumberRange,
)


__version__ = '0.2.2'
__author__ = 'Brutus [DMC] <brutus.dmc@googlemail.com>'
__license__ = 'GNU General Public License v3 or above - '\
              'http://www.opensource.org/licenses/gpl-3.0.html'


MINMAX_VALIDATORS = (
    Length,
    NumberRange,
)


def get_html5_kwargs(field, render_kw=None):
    """
    Returns a copy of *render_kw*  with keys added for a bound *field*.

    If some *render_kw* are given, the new keys are added to a copy of them,
    which is then returned. If none are given, a dictionary containing only
    the automatically generated keys is returned.

    .. important::

        This might add keys but never changes any values. If a key already is
        in *render_kw* it is left untouched.

    Raises:

        ValueError: if *field* is an :cls:`UnboundField`.

    The following keys are set automatically:

    :required:
        Sets the *required* key if the `required` flag is set for the
        field (mostly the case if it is set by validators). This is
        used by browsers to indicate a required field.

    :invalid:
        Set (or appends) 'invalid' to the fields CSS class(es), if the *field*
        got any errors. 'invalid' is also set by browsers if they detect
        errors on a field.

    :min / max:
        Sets *min* and / or *max* keys if the `Length` or `NumberRange`
        validator is using them.

    :title:
        If the field got a *description* but no *title* key is set, the
        *title* is set to *description*.

    """
    if isinstance(field, UnboundField):
        msg = 'This function needs a bound field not: {}'
        raise ValueError(msg.format(field))

    kwargs = render_kw.copy() if render_kw else {}

    # is field required?
    if 'required' not in kwargs and field.flags.required:
        kwargs['required'] = True

    # is field invalid?
    if field.errors:
        cls = kwargs.get('class') or kwargs.pop('class_', '')
        if cls:
            kwargs['class'] = 'invalid {}'.format(cls)
        else:
            kwargs['class'] = 'invalid'

    # check validators for min/max
    for validator in field.validators:
        if isinstance(validator, MINMAX_VALIDATORS):
            if 'min' not in kwargs:
                v_min = getattr(validator, 'min', -1)
                if v_min not in (-1, None):
                    kwargs['min'] = v_min
            if 'max' not in kwargs:
                v_max = getattr(validator, 'max', -1)
                if v_max not in (-1, None):
                    kwargs['max'] = v_max

    # missing tile?
    if 'title' not in kwargs and getattr(field, 'description'):
        kwargs['title'] = '{}'.format(field.description)

    return kwargs


class AutoAttrMeta(DefaultMeta):
    """
    Meta class for WTForms :cls:`Form` classes.

    It uses :func:`get_html5_kwargs` to automatically add some render
    keywords for each field's widget when it gets rendered.

    """

    def render_field(self, field, render_kw):
        """
        Returns the rendered field after adding auto–attributes.

        Calls the field`s widget with the following kwargs:

        1. the *render_kw* set on the field are used as based
        2. and are updated with the *render_kw* arguments from the render call
        3. this is used as an argument for a call to `get_html5_kwargs`
        4. the return value of the call is used as final *render_kw*

        """
        field_kw = getattr(field, 'render_kw', None)
        if field_kw is not None:
            render_kw = dict(field_kw, **render_kw)
        render_kw = get_html5_kwargs(field, render_kw)
        return field.widget(field, **render_kw)
