# pylama:ignore=C0111
"""
Tests for the :cls:`wtforms_html5.AutoAttrMeta` class.

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from unittest import TestCase

from wtforms.validators import InputRequired
from wtforms.validators import Length
from wtforms.validators import NumberRange

from . import get_field
from . import get_form


class TestMeta(TestCase):
    def test_standard_field(self):
        form1 = get_form()
        form2 = get_form(use_meta=True)
        self.assertEqual(form1.test_field(), form2.test_field())

    def test_required(self):
        form = get_form(
            validators=[
                InputRequired(),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertIn("required", field.attrs)

    def test_invalid(self):
        form = get_form(
            validators=[
                InputRequired(),
            ],
            use_meta=True,
        )
        self.assertFalse(form.validate())
        field = get_field(form)
        self.assertIn("invalid", field.attrs["class"])

    def test_minmax(self):
        # min
        form = get_form(
            validators=[
                NumberRange(min=3),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertEqual(field.attrs["min"], "3")
        self.assertNotIn("max", field.attrs)
        # max
        form = get_form(
            validators=[
                NumberRange(max=8),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertEqual(field.attrs["max"], "8")
        self.assertNotIn("min", field.attrs)
        # min + max
        form = get_form(
            validators=[
                NumberRange(min=3, max=8),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertEqual(field.attrs["min"], "3")
        self.assertEqual(field.attrs["max"], "8")

    def test_minmaxlength(self):
        # min
        form = get_form(
            validators=[
                Length(min=3),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertEqual(field.attrs["minlength"], "3")
        self.assertNotIn("maxlength", field.attrs)
        # max
        form = get_form(
            validators=[
                Length(max=8),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertEqual(field.attrs["maxlength"], "8")
        self.assertNotIn("minlength", field.attrs)
        # min + max
        form = get_form(
            validators=[
                Length(min=3, max=8),
            ],
            use_meta=True,
        )
        field = get_field(form)
        self.assertEqual(field.attrs["minlength"], "3")
        self.assertEqual(field.attrs["maxlength"], "8")

    def test_title(self):
        form = get_form(description="Some help text", use_meta=True)
        field = get_field(form)
        self.assertEqual(field.attrs["title"], "Some help text")

    def test_field_renderkw(self):
        render_kw = {
            "class": "imspecial too",
        }
        form = get_form(render_kw=render_kw, use_meta=True)
        field = get_field(form)
        self.assertIn("imspecial", field.attrs["class"])
        self.assertIn("too", field.attrs["class"])
