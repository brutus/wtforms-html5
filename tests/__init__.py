import pytest
from wtforms import Form
from wtforms import StringField

from wtforms_html5 import AutoAttrMeta

try:
    from werkzeug.datastructures import MultiDict
except ImportError:
    MultiDict = None

try:
    from bs4 import BeautifulSoup
except ImportError:
    BeautifulSoup = None


def get_form(form_data=None, flags=None, use_meta=False, **kwargs):
    """
    Returns a WTForms :cls:`Form`.

    The form has one :cls:`StringField` named `test_field` and the *kwargs*
    are used as arguments for the field instance. If *flags* is set, the given
    flags are set for the field too.

    If *form_data* is set, it is cast to a :cls:`Werkzeug.MultiDict` and
    used to fill the form using the :meth:`Form.process` method.

    """
    form_data = form_data or {}
    flags = flags or []
    meta_class = AutoAttrMeta if use_meta else object

    class TestForm(Form):
        class Meta(meta_class):
            pass

        test_field = StringField("Testfield", **kwargs)

    # create instance
    form = TestForm()

    # flags
    for flag in flags:
        setattr(form.test_field.flags, flag, True)

    # process data
    if form_data:
        if MultiDict is None:
            pytest.skip("This test requires `MultiDict` from `Werkzeug`.")
        form.process(MultiDict(form_data))

    return form


def get_field(form, fieldname="test_field"):
    """
    Returns *fieldname* from *form* as an BeautifulSoup object.

    """
    if BeautifulSoup is None:
        pytest.skip("This test requires `BeautifulSoup`.")
    field = getattr(form, fieldname)
    return BeautifulSoup(field(), "html.parser").input
