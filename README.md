# WTForms HTML5

[![PyPI Status](https://img.shields.io/pypi/v/wtforms-html5.svg)](https://pypi.org/project/wtforms-html5/)
[![Coverage Status](https://coveralls.io/repos/github/brutus/wtforms-html5/badge.svg?branch=main)](https://coveralls.io/github/brutus/wtforms-html5?branch=main)
[![pre-commit.ci Status](https://results.pre-commit.ci/badge/github/brutus/wtforms-html5/main.svg)](https://results.pre-commit.ci/latest/github/brutus/wtforms-html5/main)
[![Test Status](https://github.com/brutus/wtforms-html5/actions/workflows/test.yml/badge.svg)](https://github.com/brutus/wtforms-html5/actions/workflows/test.yml)

**VERSION**: `0.6.0`

**WTForms HTML5** generates render keywords for HTML5 INPUT widgets used by the
[WTForms][] library.

## Evolution

_Original Function_: This module used to add support for the new HTML5 INPUT
elements to [WTForms][]. Besides supporting the new INPUT _types_, it also set
some of the new _attributes_ automatically, based on widget type and what kind
of validators where set for the field.

_Changes_: [WTForms][] — beginning around version 1.0.4 — started to implement
some of these features. As of late 2016 the development version — that
should become version 3 — has enough support for them IMO, so that to prevent
the duplication of functionality, **WTForms HTML5** dropped all the fields,
widgets and validators — just use vanilla [WTForms][].

_Current Function_: starting with `0.2` versions of **WTForms HTML5** merely
contain one function: `get_html5_kwargs` — it adds the automatically generated
keys to the _render keywords_ of a [WTForms][] field. A slim subclass of the new
default _Meta_ class for forms is also provided: `AutoAttrMeta`. If you use this
class as your forms _Meta_, you get the automatic attributes for all fields in
your form, just like in the original version of **WTForms HTML5**.

## Supported Auto–Attributes

-   **required**

    Is set if the field has the _required_ flag set. This happens i.e. if you use
    the _DataRequired_ or _InputRequired_ validator. The `required` attribute is
    used by browsers to indicate a required field (and most browsers won't
    activate the forms action unless all required fields have content).

-   **invalid**

    If the field got any validation errors, the CSS class _invalid_ is added. The
    `invalid` class is also set by browsers, if they detect errors on a field.
    The validation errors detected by your code, are then by default styled in
    the same way as browser generated errors.

-   **min** / **max** and **minlength** / **maxlength**

    If either _Length_ or _NumberRange_ is used as a validator to set minimal
    and / or maximal values, the corresponding INPUT attribute is
    set (based on which validator is used). This allows for browser based
    validation of the values.

-   **title**

    If no _title_ is provided for a field, the _description_ (if one is set) is
    used for the `title` attribute.

## Example

Declare your form just like in vanilla _WTForms_, but include `AutoAttrMeta`
as your meta class:

```py
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
```

**The only difference is, that you include a `Meta` class, that inherits from
`AutoAttrMeta`.**

This meta class sets the above mentioned attributes automatically for all the
fields of the form:

```py
>>> form.test_field()
'<input id="test_field" maxlength="12" minlength="3" name="test_field" required title="Just a test field." type="text" value="">'
```

The _minlength_ and _maxlength_ attributes are created because the `Length`
validator was used. And the field is marked _required_ because of the
`InputRequired` validator. The field also gets a _title_ taken from the fields
`description`.

If you validate the form and any errors pop up, the field also get `invalid`
added to its class:

```py
>>> form.validate()
False
>>> form.test_field()
'<input class="invalid" id="test_field" maxlength="12" minlength="3" name="test_field" required title="Just a test field." type="text" value="">'
```

## Install

You can install **WTForms HTML5** with _pip_ or from _source_.

[pip][] is _"a tool for installing and managing Python packages"_. If you don't
have it installed, see the [pip install instructions][].

```shell
pip install --user wtforms-html5
```

### Install Requirements

Since **WTForms HTML5** only adds functionality to [WTForms][], you need to
have it installed too. But if you use the installation method described
above, it should have been taken care of.

## Testing and Contribution

**WTForms HTML5** is at home at: https://github.com/brutus/wtforms-html5/

You can run `make setup` after checkout, to setup a development environment.

If you find any bugs, issues or anything, please use the [issue tracker][].

### Testing

You can run the provided **doctest** like this: `make doctest`. If you want to
run the **test cases**, run `make unittest` (or `make coverage`). You can also
run `make all-tests` to run this for all supported versions (this might take
some time though).

If something fails, please get in touch.

[home]: https://github.com/brutus/wtforms-html5/
[issue tracker]: https://github.com/brutus/wtforms-html5/issues
[wtforms]: https://wtforms.readthedocs.io/
[pip]: https://pip.pypa.io/
[pip install instructions]: https://pip.pypa.io/en/stable/installing/
