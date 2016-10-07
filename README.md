# WTForms HTML5

![Build Status][badge-travis] ![Code Status][badge-landscape] ![Coverage Status][badge-coveralls]

Generates render keywords for [WTForms][] HTML5 field's widgets.

_Original Function_: This module used to add HTML5 support to _WTForms_.

It supported the new INPUT __types__ for fields and had also set some of the new
INPUT __attributes__ automatically for the generated HTML Input elements (based
on widget type and what kind of validator was set for the field).

_Changes_: _WTForms_ version 1.0.4 started to implement some of these features
and the current (late 2016) development version — that should become version 3 —
has enough support for all that features, that to prevent the duplication of
functionality, current versions of __WTForms HTML5__ dropped all the fields,
widgets and validators — just use vanilla _WTForms_.

_Current Function_: recent versions (starting with 0.2) contain only one
function: `get_html5_kwargs` — it adds the automatically generated keys to the
_render keywords_ of a _WTForms_ field.

A slim subclass of the new default _Meta_ class for forms is also provided:
`AutoAttrMeta`. If you use this class as your forms _Meta_, you get the
automatic attributes for all fields in your form, just like in the original
version of __WTForms HTML5__.


## Supported Auto–Attributes

- __required__

  Is set if the field has the ``required`` flag set.

  This happens if you use the _DataRequired_ or _InputRequired_ validator.

- __invalid__

  If the field got any validation errors, the CSS class _invalid_ is added.

- __min__ and __max__

  If either _Length_ or _NumberRange_ is used as a validator and sets a minimal
  or maximal value, the corresponding INPUT attribute is set.

- __title__

  If no _title_ attribute is provided for a field, but a _description_, the
  _description_ is used for the _title_.


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

Now you get some attributes created automatically for your fields:

```py
>>> form.test_field()
'<input id="test_field" max="12" min="3" name="test_field" required title="Just a test field." type="text" value="">'
```

The _min_ and _max_ attributes are created because you used the `Length`
validator. And the field is marked _required_ because of the `InputRequired` validator. The field also gets a _title_ taken from the fields `description`.

If you validate the form and any errors pop up, the field would also get an
_invalid_ attribute:

```py
>>> form.validate()
False
>>> form.test_field()
'<input class="invalid" id="test_field" max="12" min="3" name="test_field" required title="Just a test field." type="text" value="">'
```


## Install

You can install __WTForms HTML5__ with [pip][] or from source.

### Install with pip

[pip][] is _"a tool for installing and managing Python packages"_. If you don't
have it installed, see the [pip install instructions][].

`pip install wtforms-html5`

### Install from source

You can fetch the latest [sourceball][] from github and unpack it, or just
clone this repository: `git clone git://github.com/brutus/wtforms-html5.git`.
If you got the source, change into the directory and use _setup.py_:

`python setup.py install`

### Install Requirements

Since __WTForms HTML5__ only adds functionality to [WTForms][], you need to
have it installed too. But if you use the installation methods described
above, it should have been taken care of. Otherwise see the `requirements.txt`
file for a list.


## Testing and Contribution

__WTForms HTML5__ is at home at: https://github.com/brutus/wtforms-html5/

If you find any bugs, issues or anything, please use the [issue tracker][].

### Testing

There are some __doctest__ in the module. You can run them from the _source
directory_ like this: `python -m doctest wtforms_html5.py`. If you want to
run the __test cases__, run `python -m unittest discover`  (also from the
_source directory_).

If something fails, please get in touch.

### Additional Requirements

To run the test cases a few additional requirements need to be fulfilled. You
can install all testing requirements like this: ``pip install -r
requirements/testing.txt``.



[home]: https://github.com/brutus/wtforms-html5/
[sourceball]: https://github.com/brutus/wtforms-html5/zipball/master
[issue tracker]: https://github.com/brutus/wtforms-html5/issues

[WTForms]: http://wtforms.simplecodes.com/
[pip]: http://www.pip-installer.org/en/latest/index.html
[pip install instructions]: http://www.pip-installer.org/en/latest/installing.html

[badge-travis]: https://api.travis-ci.org/brutus/wtforms-html5.svg?branch=master
[badge-landscape]: https://landscape.io/github/brutus/wtforms-html5/master/landscape.svg?style=flat
[badge-coveralls]: https://coveralls.io/repos/github/brutus/wtforms-html5/badge.svg?branch=master
