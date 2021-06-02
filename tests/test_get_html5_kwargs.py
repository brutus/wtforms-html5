# pylama:ignore=C0111
"""
Tests for the :func:`wtforms_html5.get_html5_kwargs` function.

"""
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

from unittest import TestCase

from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Length

from wtforms_html5 import get_html5_kwargs
from wtforms_html5 import MINMAX_VALIDATORS
from wtforms_html5 import MINMAXLENGTH_VALIDATORS

from . import get_form
from . import SkipIfNoSubtests


class TestGetHtml5Kwargs(TestCase):

    # BASICS

    def test_unbound_field(self):
        field = StringField("unbound test field")
        with self.assertRaises(ValueError):
            get_html5_kwargs(field)

    def test_copy_kwargs(self):
        org_kwargs = {}
        form = get_form()
        new_kwargs = get_html5_kwargs(form.test_field, org_kwargs)
        self.assertIsNot(org_kwargs, new_kwargs)

    def test_unchanged(self):
        form = get_form()
        res = get_html5_kwargs(
            form.test_field,
            {
                "foo": 1,
                "bar": [2, 3],
                "x": "y",
            },
        )
        exp = {
            "foo": 1,
            "bar": [2, 3],
            "x": "y",
        }
        self.assertEqual(res, exp)

    def test_unchanged_empty(self):
        form = get_form()
        res = get_html5_kwargs(form.test_field)
        exp = {}
        self.assertEqual(res, exp)

    # TITLE

    def test_auto_title(self):
        form = get_form(description="Test description.")
        res = get_html5_kwargs(form.test_field)
        exp = {
            "title": "Test description.",
        }
        self.assertEqual(res, exp)

    def test_auto_title_no_overwrite(self):
        form = get_form(description="Test description.")
        render_kw = {"title": "Test title."}
        res = get_html5_kwargs(form.test_field, render_kw)
        exp = {
            "title": "Test title.",
        }
        self.assertEqual(res, exp)

    # REQUIRED

    def test_auto_required(self):
        form = get_form(flags=["required"])
        res = get_html5_kwargs(form.test_field)
        exp = {
            "required": True,
        }
        self.assertEqual(res, exp)

    def test_auto_required_by_validator(self):
        # InputRequired
        form = get_form(
            validators=[
                InputRequired(),
            ]
        )
        res = get_html5_kwargs(form.test_field)
        exp = {
            "required": True,
        }
        self.assertEqual(res, exp)
        # DataRequired
        form = get_form(
            validators=[
                DataRequired(),
            ]
        )
        res = get_html5_kwargs(form.test_field)
        exp = {
            "required": True,
        }
        self.assertEqual(res, exp)
        # Length
        form = get_form(
            validators=[
                Length(max=5),
            ]
        )
        res = get_html5_kwargs(form.test_field)
        self.assertNotIn("required", res)

    def test_auto_required_no_overwrite(self):
        form = get_form(flags=["required"])
        render_kw = {"required": False}
        res = get_html5_kwargs(form.test_field, render_kw)
        exp = {
            "required": False,
        }
        self.assertEqual(res, exp)

    # INVALID

    def test_auto_invalid(self):
        # nothing
        form = get_form()
        self.assertTrue(form.validate())
        res = get_html5_kwargs(form.test_field)
        exp = {}
        self.assertEqual(res, exp)
        # nothing invalid
        form_data = {"test_field": "x" * 5}
        form = get_form(
            form_data=form_data,
            validators=[
                Length(min=5),
            ],
        )
        self.assertTrue(form.validate())
        res = get_html5_kwargs(form.test_field)
        exp = {
            "minlength": 5,
        }
        self.assertEqual(res, exp)
        # invalid input
        form_data = {"test_field": "x" * 2}
        form = get_form(
            form_data=form_data,
            validators=[
                Length(min=5),
            ],
        )
        self.assertFalse(form.validate())
        res = get_html5_kwargs(form.test_field)
        exp = {
            "class": "invalid",
            "minlength": 5,
        }
        self.assertEqual(res, exp)

    def test_auto_invalid_no_overwrite(self):
        # add to class
        form_data = {"test_field": "x" * 2}
        form = get_form(
            form_data=form_data,
            validators=[
                Length(min=5),
            ],
        )
        self.assertFalse(form.validate())
        res = get_html5_kwargs(form.test_field, {"class": "test"})
        exp = {
            "class": "invalid test",
            "minlength": 5,
        }
        self.assertEqual(res, exp)
        # add to class_
        form_data = {"test_field": "x" * 2}
        form = get_form(
            form_data=form_data,
            validators=[
                Length(min=5),
            ],
        )
        self.assertFalse(form.validate())
        res = get_html5_kwargs(form.test_field, {"class_": "test zwo"})
        exp = {
            "class": "invalid test zwo",
            "minlength": 5,
        }
        self.assertEqual(res, exp)

    # MIN / MAX

    @SkipIfNoSubtests
    def test_auto_minmax(self):
        for Validator in MINMAX_VALIDATORS:
            with self.subTest(Validator=Validator):
                # min
                form = get_form(validators=[Validator(min=5)])
                res = get_html5_kwargs(form.test_field)
                exp = {
                    "min": 5,
                }
                self.assertEqual(res, exp)
                # max
                form = get_form(validators=[Validator(max=5)])
                res = get_html5_kwargs(form.test_field)
                exp = {
                    "max": 5,
                }
                self.assertEqual(res, exp)
                # min + max
                form = get_form(validators=[Validator(max=5, min=2)])
                res = get_html5_kwargs(form.test_field)
                exp = {
                    "min": 2,
                    "max": 5,
                }
                self.assertEqual(res, exp)

    @SkipIfNoSubtests
    def test_auto_minmax_no_overwrite(self):
        render_kw = {
            "min": 10,
            "max": 20,
        }
        exp = render_kw.copy()
        for Validator in MINMAX_VALIDATORS:
            with self.subTest(Validator=Validator):
                # min
                form = get_form(validators=[Validator(min=5)])
                res = get_html5_kwargs(form.test_field, render_kw)
                self.assertEqual(res, exp)
                # max
                form = get_form(validators=[Validator(max=5)])
                res = get_html5_kwargs(form.test_field, render_kw)
                self.assertEqual(res, exp)
                # min + max
                form = get_form(validators=[Validator(max=5, min=2)])
                res = get_html5_kwargs(form.test_field, render_kw)
                self.assertEqual(res, exp)

    @SkipIfNoSubtests
    def test_auto_minmaxlength(self):
        for Validator in MINMAXLENGTH_VALIDATORS:
            with self.subTest(Validator=Validator):
                # minlength
                form = get_form(validators=[Validator(min=5)])
                res = get_html5_kwargs(form.test_field)
                exp = {
                    "minlength": 5,
                }
                self.assertEqual(res, exp)
                # maxlength
                form = get_form(validators=[Validator(max=5)])
                res = get_html5_kwargs(form.test_field)
                exp = {
                    "maxlength": 5,
                }
                self.assertEqual(res, exp)
                # minlength + maxlength
                form = get_form(validators=[Validator(max=5, min=2)])
                res = get_html5_kwargs(form.test_field)
                exp = {
                    "minlength": 2,
                    "maxlength": 5,
                }
                self.assertEqual(res, exp)

    @SkipIfNoSubtests
    def test_auto_minmaxlength_no_overwrite(self):
        render_kw = {
            "minlength": 10,
            "maxlength": 20,
        }
        exp = render_kw.copy()
        for Validator in MINMAXLENGTH_VALIDATORS:
            with self.subTest(Validator=Validator):
                # minlength
                form = get_form(validators=[Validator(min=5)])
                res = get_html5_kwargs(form.test_field, render_kw)
                self.assertEqual(res, exp)
                # maxlength
                form = get_form(validators=[Validator(max=5)])
                res = get_html5_kwargs(form.test_field, render_kw)
                self.assertEqual(res, exp)
                # minlength + maxlength
                form = get_form(validators=[Validator(max=5, min=2)])
                res = get_html5_kwargs(form.test_field, render_kw)
                self.assertEqual(res, exp)
