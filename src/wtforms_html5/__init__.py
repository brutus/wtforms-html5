"""
Generates render keywords for `WTForms`_ HTML5 field's widgets.

The :func:`get_html5_kwargs` adds the automatically generated keys to the
*render keywords* of a `WTForms`_ field.

The :cls:`AutoAttrMeta` can be included as a base class for the `Meta` class
in your forms, to handle this automatically for each field of the form.


Supported Auto–Attributes
-------------------------

- *required*

  Is set if the field has the _required_ flag set. This happens i.e. if you
  use the _DataRequired_ or _InputRequired_ validator. The `required`
  attribute is used by browsers to indicate a required field (and most
  browsers won't activate the forms action unless all required fields have
  content).

- *invalid*

  If the field got any validation errors, the CSS class _invalid_ is added.
  The `invalid` class is also set by browsers if they detect errors on a
  field. This validation errors detected by your code, are by default styled
  in the same way as browser generated errors.

- *min* / *max* and *minlength* / *maxlength*

  If either _Length_ or _NumberRange_ is used as a validator to set minimal
  and / or maximal values, the corresponding INPUT attribute is
  set (based on which validator is used). This allows for browser based
  validation of the values.

- *title*

  If no _title_ is provided for a field, the _description_ (if one is set) is
  used for the `title` attribute.


An Example
----------

Declare your form just like in vanilla *WTForms*, but include `AutoAttrMeta`
as your meta class:

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

**The only difference is, that you include a `Meta` class, that inherits from
`AutoAttrMeta`.**

This meta class sets the above mentioned attributes automatically for all the
fields of the form:

>>> f = form.test_field()
>>> exp = (
...  '<input id="test_field" maxlength="12" minlength="3" name="test_field" '
...  'required title="Just a test field." type="text" value="">'
... )
>>> assert f == exp

The _min_ and _max_ attributes are created because the `Length` validator was
used. And the field is marked _required_ because of the `InputRequired`
validator. The field also gets a _title_ taken from the fields `description`.

If you validate the form and any errors pop up, the field also get `invalid`
added to its class:

>>> form.validate()
False
>>> exp = (
... '<input class="invalid" id="test_field" maxlength="12" minlength="3" '
... 'name="test_field" required title="Just a test field." type="text" '
... 'value="">'
... )
>>> f = form.test_field()
>>> assert f == exp


.. _WTForms: https://wtforms.readthedocs.io/

"""

from wtforms.fields.core import UnboundField
from wtforms.meta import DefaultMeta
from wtforms.validators import Length
from wtforms.validators import NumberRange

__version__ = "0.6.1"
__author__ = "Brutus [DMC] <brutus.dmc@googlemail.com>"
__license__ = (
    "GNU General Public License v3 or above - "
    "http://www.opensource.org/licenses/gpl-3.0.html"
)


MINMAX_VALIDATORS = (NumberRange,)

MINMAXLENGTH_VALIDATORS = (Length,)


def set_required(field, render_kw=None, force=False):
    """
    Returns *render_kw* with *required* set if the field is required.

    Sets the *required* key if the `required` flag is set for the field (this
    is mostly the case if it is set by validators). The `required` attribute
    is used by browsers to indicate a required field.

    ..note::

        This won't change keys already present unless *force* is used.

    """
    if render_kw is None:
        render_kw = {}
    if "required" in render_kw and not force:
        return render_kw
    if field.flags.required:
        render_kw["required"] = True
    return render_kw


def set_invalid(field, render_kw=None):
    """
    Returns *render_kw* with `invalid` added to *class* on validation errors.

    Set (or appends) 'invalid' to the fields CSS class(es), if the *field* got
    any errors. 'invalid' is also set by browsers if they detect errors on a
    field.

    """
    if render_kw is None:
        render_kw = {}
    if field.errors:
        classes = render_kw.get("class") or render_kw.pop("class_", "")
        if classes:
            render_kw["class"] = f"invalid {classes}"
        else:
            render_kw["class"] = "invalid"
    return render_kw


def set_minmax(field, render_kw=None, force=False):
    """
    Returns *render_kw* with *min* and *max* set if validators use them.

    Sets *min* and / or *max* keys if one of the validators from
    `MINMAX_VALIDATORS` is using them.

    ..note::

        This won't change keys already present unless *force* is used.

    """
    if render_kw is None:
        render_kw = {}
    for validator in field.validators:
        if isinstance(validator, MINMAX_VALIDATORS):
            if "min" not in render_kw or force:
                v_min = getattr(validator, "min", -1)
                if v_min not in (-1, None):
                    render_kw["min"] = v_min
            if "max" not in render_kw or force:
                v_max = getattr(validator, "max", -1)
                if v_max not in (-1, None):
                    render_kw["max"] = v_max
    return render_kw


def set_minmaxlength(field, render_kw=None, force=False):
    """
    Returns *render_kw* with *minlength* and *maxlength* set if validators use
    them.

    Sets *minlength* and / or *maxlength* keys if one of the validators from
    `MINMAXLENGTH_VALIDATORS` is present and the corresponding parameters (i.e.
    `min` or `max`) are set.

    ..note::

        This won't change keys already present unless *force* is used.

    """
    if render_kw is None:
        render_kw = {}
    for validator in field.validators:
        if isinstance(validator, MINMAXLENGTH_VALIDATORS):
            if "minlength" not in render_kw or force:
                v_min = getattr(validator, "min", -1)
                if v_min not in (-1, None):
                    render_kw["minlength"] = v_min
            if "maxlength" not in render_kw or force:
                v_max = getattr(validator, "max", -1)
                if v_max not in (-1, None):
                    render_kw["maxlength"] = v_max
            # Inconsistency: Length validator uses min and max for specifying
            #                length limits while HTML5 uses minlength and
            #                maxlength (attributes of input element) for the
            #                same purpose.
    return render_kw


def set_title(field, render_kw=None):
    """
    Returns *render_kw* with missing *title* set to *description*.

    If the field got a *description* but no *title* key is set, the *title* is
    set to *description*.

    """
    if render_kw is None:
        render_kw = {}
    if "title" not in render_kw and field.description:
        render_kw["title"] = f"{field.description}"
    return render_kw


def get_html5_kwargs(field, render_kw=None, force=False):
    """
    Returns a copy of *render_kw*  with keys added for a bound *field*.

    If some *render_kw* are given, the new keys are added to a copy of them,
    which is then returned. If none are given, a dictionary containing only
    the automatically generated keys is returned.

    .. important::

        This might add new keys but won't changes any values if a key is
        already in *render_kw*,  unless *force* is used.

    Raises:

        ValueError: if *field* is an :cls:`UnboundField`.

    The following keys are set automatically:

    :required:
        Sets the *required* key if the `required` flag is set for the
        field (this is mostly the case if it is set by validators). The
        `required` attribute is used by browsers to indicate a required field.

    :invalid:
        Set (or appends) 'invalid' to the fields CSS class(es), if the *field*
        got any errors. 'invalid' is also set by browsers if they detect
        errors on a field.

    :min / max and minlength / maxlength:
        Sets those keys if a  or `NumberRange` or `Length` validator is using
        them.

    :title:
        If the field got a *description* but no *title* key is set, the
        *title* is set to *description*.

    """
    if isinstance(field, UnboundField):
        msg = f"This function needs a bound field, not: '{field}'"
        raise ValueError(msg)
    kwargs = render_kw.copy() if render_kw else {}
    kwargs = set_required(field, kwargs, force)
    kwargs = set_invalid(field, kwargs)
    kwargs = set_minmax(field, kwargs, force)
    kwargs = set_minmaxlength(field, kwargs, force)
    kwargs = set_title(field, kwargs)
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
        field_kw = getattr(field, "render_kw", None)
        if field_kw is not None:
            render_kw = dict(field_kw, **render_kw)
        render_kw = get_html5_kwargs(field, render_kw)
        return field.widget(field, **render_kw)
