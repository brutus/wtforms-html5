# pylama:ignore=C0111
"""
Tests for the :func:`wtforms_html5.get_html5_kwargs` function.

"""

import pytest
from wtforms import StringField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired
from wtforms.validators import Length

from wtforms_html5 import get_html5_kwargs

from . import get_form

# FIELD


def test_unbound_field_raises_value_error():
    field = StringField("unbound test field")
    with pytest.raises(ValueError, match=r"\bneeds a bound field\b"):
        get_html5_kwargs(field)


# KWARG HANDLING


def test_kwargs_are_copied():
    org_kwargs = {}
    form = get_form()
    new_kwargs = get_html5_kwargs(form.test_field, org_kwargs)
    assert org_kwargs is not new_kwargs


def test_kwargs_unchanged_when_no_action():
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
    assert res == exp


def test_kwargs_empty_return_empty():
    form = get_form()
    res = get_html5_kwargs(form.test_field)
    exp = {}
    assert res == exp


# SET TITLE


def test_title_from_desription():
    form = get_form(description="Test description.")
    res = get_html5_kwargs(form.test_field)
    exp = {
        "title": "Test description.",
    }
    assert res == exp


def test_title_no_overwrite():
    form = get_form(description="Test description.")
    render_kw = {"title": "Test title."}
    res = get_html5_kwargs(form.test_field, render_kw)
    exp = {
        "title": "Test title.",
    }
    assert res == exp


# REQUIRED


def test_required_by_flag():
    form = get_form(flags=["required"])
    res = get_html5_kwargs(form.test_field)
    exp = {
        "required": True,
    }
    assert res == exp


def test_required_by_validator():
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
    assert res == exp
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
    assert res == exp
    # Length
    form = get_form(
        validators=[
            Length(max=5),
        ]
    )
    res = get_html5_kwargs(form.test_field)
    assert "required" not in res


def test_required_no_overwrite():
    form = get_form(flags=["required"])
    render_kw = {"required": False}
    res = get_html5_kwargs(form.test_field, render_kw)
    exp = {
        "required": False,
    }
    assert res == exp


# INVALID


def test_invalid():
    # nothing
    form = get_form()
    assert form.validate() is True
    res = get_html5_kwargs(form.test_field)
    exp = {}
    assert res == exp
    # nothing invalid
    form_data = {"test_field": "x" * 5}
    form = get_form(
        form_data=form_data,
        validators=[
            Length(min=5),
        ],
    )
    assert form.validate() is True
    res = get_html5_kwargs(form.test_field)
    exp = {
        "minlength": 5,
    }
    assert res == exp
    # invalid input
    form_data = {"test_field": "x" * 2}
    form = get_form(
        form_data=form_data,
        validators=[
            Length(min=5),
        ],
    )
    assert form.validate() is False
    res = get_html5_kwargs(form.test_field)
    exp = {
        "class": "invalid",
        "minlength": 5,
    }
    assert res == exp


def test_invalid_append():
    # add to class
    form_data = {"test_field": "x" * 2}
    form = get_form(
        form_data=form_data,
        validators=[
            Length(min=5),
        ],
    )
    assert form.validate() is False
    res = get_html5_kwargs(form.test_field, {"class": "test"})
    exp = {
        "class": "invalid test",
        "minlength": 5,
    }
    assert res == exp
    # add to class_
    form_data = {"test_field": "x" * 2}
    form = get_form(
        form_data=form_data,
        validators=[
            Length(min=5),
        ],
    )
    assert form.validate() is False
    res = get_html5_kwargs(form.test_field, {"class_": "test zwo"})
    exp = {
        "class": "invalid test zwo",
        "minlength": 5,
    }
    assert res == exp


# MIN / MAX


@pytest.mark.parametrize(
    "kwargs,exp",
    [
        ({"min": 5}, {"min": 5}),  # min only
        ({"max": 5}, {"max": 5}),  # max only
        ({"max": 5, "min": 2}, {"min": 2, "max": 5}),  # min and max
    ],
)
def test_minmax_validator(minmax_validator, kwargs, exp):
    # no render keywords
    form = get_form(validators=[minmax_validator(**kwargs)])
    res = get_html5_kwargs(form.test_field)
    assert res == exp
    # with render keywords - no overwrite
    render_kw = {
        "min": 10,
        "max": 20,
    }
    exp_render_kw = render_kw.copy()
    form = get_form(validators=[minmax_validator(**kwargs)])
    res = get_html5_kwargs(form.test_field, render_kw)
    assert res == exp_render_kw


@pytest.mark.parametrize(
    "kwargs,exp",
    [
        ({"min": 5}, {"minlength": 5}),  # min only
        ({"max": 5}, {"maxlength": 5}),  # max only
        ({"max": 5, "min": 2}, {"minlength": 2, "maxlength": 5}),  # min and max
    ],
)
def test_minmaxlength_validator(minmaxlength_validator, kwargs, exp):
    # no render keywords
    form = get_form(validators=[minmaxlength_validator(**kwargs)])
    res = get_html5_kwargs(form.test_field)
    assert res == exp
    # with render keywords - no overwrite
    render_kw = {
        "minlength": 10,
        "maxlength": 20,
    }
    exp_render_kw = render_kw.copy()
    form = get_form(validators=[minmaxlength_validator(**kwargs)])
    res = get_html5_kwargs(form.test_field, render_kw)
    assert res == exp_render_kw
