# WTForms HTML5

[![Build Status](https://travis-ci.org/brutus/wtforms-html5.svg?branch=master)](https://travis-ci.org/brutus/wtforms-html5)
[![Coverage Status](https://coveralls.io/repos/github/brutus/wtforms-html5/badge.svg?branch=master)](https://coveralls.io/github/brutus/wtforms-html5?branch=master)
[![Code Health](https://landscape.io/github/brutus/wtforms-html5/master/landscape.svg?style=flat)](https://landscape.io/github/brutus/wtforms-html5/master)

__WTForms HTML5__ generates render keywords for HTML5 INPUT widgets used by the
[WTForms][] library.

## Evolution

_Original Function_: This module used to add support for the new HTML5 INPUT
elements to [WTForms][]. Besides supporting the new INPUT _types_, it also set
some of the new _attributes_ automatically, based on widget type and what kind
of validators where set for the field.

_Changes_: [WTForms][] — beginning around version 1.0.4 — started to implement
some of these features. The current (late 2016) development version — that
should become version 3 — has enough support for them imo, so that to prevent
the duplication of functionality, __WTForms HTML5__ dropped all the fields,
widgets and validators — just use vanilla [WTForms][].

_Current Function_: recent versions of __WTForms HTML5__ (starting with 0.2)
contain only one function: `get_html5_kwargs` — it adds the automatically
generated keys to the _render keywords_ of a [WTForms][] field. A slim subclass
of the new default _Meta_ class for forms is also provided: `AutoAttrMeta`. If
you use this class as your forms _Meta_, you get the automatic attributes for
all fields in your form, just like in the original version of __WTForms HTML5__.


## Supported Auto–Attributes

- __required__

  Is set if the field has the _required_ flag set. This happens i.e. if you use
  the _DataRequired_ or _InputRequired_ validator. The `required` attribute is
  used by browsers to indicate a required field (and most browsers won't
  activate the forms action unless all required fields have content).

- __invalid__

  If the field got any validation errors, the CSS class _invalid_ is added.
  The `invalid` class is also set by browsers if they detect errors on a field.
  This validation errors detected by your code, are by default styled in the
  same way as browser generated errors.

- __min__ and __max__

  If either _Length_ or _NumberRange_ is used as a validator to set minimal and
  / or maximal values, the corresponding `min` / `max` INPUT attribute is set.
  This allows for browser based validation of the values.

- __title__

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

__The only difference is, that you include a `Meta` class, that inherits from
`AutoAttrMeta`.__

This meta class sets the above mentioned attributes automatically for all the
fields of the form:

```py
>>> form.test_field()
'<input id="test_field" max="12" min="3" name="test_field" required title="Just a test field." type="text" value="">'
```

The _min_ and _max_ attributes are created because the `Length` validator was
used. And the field is marked _required_ because of the `InputRequired`
validator. The field also gets a _title_ taken from the fields `description`.

If you validate the form and any errors pop up, the field also get `invalid`
added to its class:

```py
>>> form.validate()
False
>>> form.test_field()
'<input class="invalid" id="test_field" max="12" min="3" name="test_field" required title="Just a test field." type="text" value="">'
```


## Install

You can install __WTForms HTML5__ with _pip_ or from _source_.

### Install with pip

[pip][] is _"a tool for installing and managing Python packages"_. If you don't
have it installed, see the [pip install instructions][].

`pip install wtforms-html5`

### Install from source

You can fetch the latest [sourceball][] from github and unpack it, or just
clone this repository:

`git clone git://github.com/brutus/wtforms-html5.git`

If you got the source, change into the directory and use _setup.py_:

`python setup.py install`

### Install Requirements

Since __WTForms HTML5__ only adds functionality to [WTForms][], you need to
have it installed too. But if you use the installation methods described
above, it should have been taken care of.


## Testing and Contribution

__WTForms HTML5__ is at home at: https://github.com/brutus/wtforms-html5/

If you find any bugs, issues or anything, please use the [issue tracker][].

### Testing

There are some __doctest__ in the module. You can run them from the _source
directory_ like this: `python -m doctest wtforms_html5.py`. If you want to
run the __test cases__, run `python -m unittest discover`  (also from the
_source directory_).

If something fails, please get in touch.

### Testing Requirements

To run the test cases a few additional requirements need to be fulfilled. You
can install all testing requirements like this: ``pip install -r
requirements/testing.txt``.



[home]: https://github.com/brutus/wtforms-html5/
[sourceball]: https://github.com/brutus/wtforms-html5/zipball/master
[issue tracker]: https://github.com/brutus/wtforms-html5/issues

[WTForms]: http://wtforms.simplecodes.com/
[pip]: http://www.pip-installer.org/en/latest/index.html
[pip install instructions]: http://www.pip-installer.org/en/latest/installing.html
