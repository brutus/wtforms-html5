# -*- coding: UTF-8 -*-

from datetime import date

from nose.tools import (
  assert_equal, assert_in, assert_not_in
)
from nose.plugins.skip import SkipTest

BeautifulSoup = None
MultiDict = None
try:
  from bs4 import BeautifulSoup
  from werkzeug.utils import MultiDict
except ImportError:
  pass

from wtforms import Form

from wtforms.validators import (
  DataRequired, InputRequired,
  Length, NumberRange
)

from wtforms_html5 import (
  TextField, SearchField, URLField, EmailField, TelField,
  IntegerField, IntegerRangeField, DecimalField, DecimalRangeField,
  FloatField, FloatRangeField,
  DateField
)

from wtforms_html5 import Required, DataNotNone, DateRange


# TEST DATA

field_types = (
  (TextField, 'text'),
  (SearchField, 'search'),
  (URLField, 'url'),
  (EmailField, 'email'),
  (TelField, 'tel'),
  (IntegerField, 'number'),
  (IntegerRangeField, 'range'),
  (DecimalField, 'number'),
  (DecimalRangeField, 'range'),
  (FloatField, 'number'),
  (FloatRangeField, 'range'),
  (DateField, 'date')
)

fields_with_step_any = (
  DecimalField, DecimalRangeField,
  FloatField, FloatRangeField
)

validators_with_required_flag = (
  DataRequired, InputRequired, Required, DataNotNone
)

validators_with_limits = (
  # validator class, min example, max example
  (Length, 5, 25),
  (NumberRange, 1000, 9999),
  (DateRange, date(2000, 4, 20), date(2012, 5, 23))
)

data_daterange = (
  {
    'min': date(2000, 4, 20), 'max': None,
    'good': (date(2012, 5, 23),),
    'bad': (date(1995, 4, 20),)
  },
  {
    'min': None, 'max': date(2012, 5, 23),
    'good': (date(2000, 4, 20),),
    'bad': (date(2014, 4, 20),)
  },
  {
    'min': date(2000, 4, 20), 'max': date(2012, 5, 23),
    'good': (date(2000, 4, 20), date(2012, 5, 23)),
    'bad': (date(1995, 4, 20), date(2014, 5, 23))
  }
)


def get_widget_output(
  FieldClass, validators=list(), description='',
  check=False, process=False, **kwargs
):
  """
  Return widget output as **BeautifulSoup** parser.

  Build a form, add an instance of *FieldClass* with the given *validators*
  and return a BeautifulSoup representation of the widgets output.

  If *process* is set (needs to be a ``Dict``), call ``process`` with it.
  If *check* is set, the form gets validated. Finally *kwargs* are
  passed to the call to the widget.

  """
  class TestForm(Form):
    test = FieldClass('Testfield', description=description, validators=validators)
  if not BeautifulSoup:
    raise SkipTest('This test requires `BeautifulSoup`.')
  f = TestForm()
  if process:
    if not MultiDict:
      raise SkipTest('This test requires `Werkzeug`.')
    f.process(MultiDict(process))
  if check:
    f.validate()
  return BeautifulSoup(f.test(**kwargs), 'html.parser').input


def test_field_type():
  """Test if `type` gets set correct."""
  err = "'{}' has unexpected ``type``: '{}' instead of '{}'."
  for FieldClass, ftype in field_types:
    # type set correct?
    tag = get_widget_output(FieldClass)
    assert_equal(tag['type'], ftype, err.format(
      FieldClass, tag['type'], ftype
    ))
    # type gets overwritten?
    tag = get_widget_output(FieldClass, type='myTest')
    assert_equal(tag['type'], 'myTest', err.format(
      FieldClass, tag['type'], ftype
    ))


def test_step_size():
  """Test auto-set `step` to ``any`` for fields with decimal points."""
  err = "'{}' has an unexpected ``step``: '{}' instead of '{}'."
  for FieldClass in fields_with_step_any:
    # step gets set?
    tag = get_widget_output(FieldClass)
    assert_equal(tag['step'], 'any', err.format(
      FieldClass, tag['step'], 'any'
    ))
    # step gets overwritten?
    tag = get_widget_output(FieldClass, step='0.5')
    assert_equal(tag['step'], '0.5', err.format(
      FieldClass, tag['step'], '0.5'
    ))


def test_title():
  """Test auto-set ``title``."""
  err = "'{}' set ``title`` but it shoudn't be set."
  err_set = "'{}' failed to set ``title``."
  err_overwrite = "'{}' failed to override ``title``."
  for FieldClass, ftype in field_types:
    # not set by default?
    tag = get_widget_output(FieldClass)
    assert_not_in('title', tag.attrs, err.format(FieldClass))
    # set on keyword?
    tag = get_widget_output(FieldClass, title='Test')
    assert_in('title', tag.attrs, err_set.format(FieldClass))
    # auto-set from description?
    tag = get_widget_output(FieldClass, description='Test')
    assert_in('title', tag.attrs, err_set.format(FieldClass))
    # overwrite auto?
    tag = get_widget_output(FieldClass, description='Test', title='OTest')
    assert_equal(tag['title'], 'OTest', err_overwrite.format(FieldClass))


def test_required():
  """Test auto-set ``required``."""
  err = "'{}' set ``required`` but it shoudn't be set."
  err_set = "'{}' failed to set ``required``."
  err_overwrite = "'{}' failed to override ``required``."
  # not set by by default?
  for FieldClass, ftype in field_types:
    tag = get_widget_output(FieldClass)
    assert_not_in('required', tag.attrs, err.format(FieldClass))
  # auto-set on validators with the ``required`` flag?
  for FieldClass, ftype in field_types:
    for Validator in validators_with_required_flag:
      tag = get_widget_output(FieldClass, validators=[Validator()])
      assert_equal(tag['required'], 'required', err_set.format(FieldClass))
  # overwrite auto?
  for FieldClass, ftype in field_types:
    for Validator in validators_with_required_flag:
      tag = get_widget_output(FieldClass, validators=[Validator()], required='test')
      assert_equal(tag['required'], 'test', err_overwrite.format(FieldClass))


def test_limits():
  """Test auto-set ``min`` and ``max``."""
  err = "'{}' set ``{}`` but it shoudn't be set: {}."
  err_set = "'{}' failed to set ``{}`` to '{}' on validator {}, '{}' ({}) instead."
  err_overwrite = "'{}' failed to override ``min`` or ``max``."
  # not set by by default?
  for FieldClass, ftype in field_types:
    tag = get_widget_output(FieldClass)
    assert_not_in('min', tag.attrs, err.format(FieldClass, 'min', tag))
    assert_not_in('max', tag.attrs, err.format(FieldClass, 'max', tag))
  # auto-set if set by validator?
  for FieldClass, ftype in field_types:
    for validator, min, max in validators_with_limits:
      # min only
      tag = get_widget_output(FieldClass, validators=[validator(min=min)])
      assert_equal(tag.attrs['min'], str(min), err_set.format(
        FieldClass, 'min', min, validator, tag.attrs['min'], type(tag.attrs['min'])
      ))
      assert_not_in('max', tag.attrs, err.format(FieldClass, 'max', tag))
      # max only
      tag = get_widget_output(FieldClass, validators=[validator(max=max)])
      assert_equal(tag.attrs['max'], str(max), err_set.format(
        FieldClass, 'max', max, validator, tag.attrs['max'], type(tag.attrs['max'])
      ))
      assert_not_in('min', tag.attrs, err.format(FieldClass, 'min', tag))
      # min and max
      tag = get_widget_output(FieldClass, validators=[validator(min=min, max=max)])
      assert_equal(tag.attrs['min'], str(min), err_set.format(
        FieldClass, 'min', min, validator, tag.attrs['min'], type(tag.attrs['min'])
      ))
      assert_equal(tag.attrs['max'], str(max), err_set.format(
        FieldClass, 'max', max, validator, tag.attrs['max'], type(tag.attrs['max'])
      ))
  # overwrite?
  for FieldClass, ftype in field_types:
    for validator, min, max in validators_with_limits:
      tag = get_widget_output(
        FieldClass, validators=[validator(min=min)],
        min=1213, max=6174
      )
      assert_equal(tag.attrs['min'], str(1213), err_overwrite.format(FieldClass))
      assert_equal(tag.attrs['max'], str(6174), err_overwrite.format(FieldClass))


def test_invalid():
  """Test that ``invalid`` is added to class on field errors."""
  err = "{} set ``invalid`` but it shoudn't be set: {}."
  err_removed = "{} removed '{}' but it shoud be there: {}."
  err_set = "{} not set ``invalid`` but it shoud be there: {}."
  # not set by default?
  for FieldClass, ftype in field_types:
    tag = get_widget_output(FieldClass)
    cls = tag.get('class', [])
    assert_not_in('invalid', cls, err.format(FieldClass, tag))
  # not set with extra styles?
  for FieldClass, ftype in field_types:
    tag = get_widget_output(FieldClass, class_='add some_css')
    cls = tag.get('class', '')
    assert_not_in('invalid', cls, err.format(FieldClass, tag))
    assert_in('add', cls, err_removed.format(FieldClass, 'add', tag))
    assert_in('some_css', cls, err_removed.format(FieldClass, 'some_css', tag))
  # set correct on error?
  for FieldClass, ftype in field_types:
    tag = get_widget_output(
      FieldClass,
      validators=[DataRequired()],
      check=True
    )
    cls = tag.get('class', '')
    assert_in('invalid', cls, err_set.format(FieldClass, tag))
  # set correct on error (with extra styles)?
  for FieldClass, ftype in field_types:
    tag = get_widget_output(
      FieldClass,
      validators=[DataRequired()],
      check=True,
      class_='add some_css'
    )
    cls = tag.get('class', '')
    assert_in('invalid', cls, err_set.format(FieldClass, tag))
    assert_in('add', cls, err_removed.format(FieldClass, 'add', tag))
    assert_in('some_css', cls, err_removed.format(FieldClass, 'some_css', tag))


def test_datanotnone():
  """Test ``DataNotNone`` validator."""
  err = "``DataNotNone`` not catches invalid data with '{}': {}."
  err_false = "``DataNotNone`` error raised on valid data '{}': {}."
  # check with correct data
  tag = get_widget_output(
    TextField,
    validators=[DataNotNone()],
    check=True,
    process={'test': 'test data'}
  )
  cls = tag.get('class', '')
  assert_not_in('invalid', cls, err_false.format('test data', tag))
  # check with correct data (but "false" values)
  for fval in (0, False):  # BTW list seem not to work, but dicts do
    tag = get_widget_output(
      TextField,
      validators=[DataNotNone()],
      check=True,
      process={'test': fval}
    )
    cls = tag.get('class', '')
    assert_not_in('invalid', cls, err_false.format(fval, tag))
  # check with invalid data (no data)
  tag = get_widget_output(
    TextField,
    validators=[DataNotNone()],
    check=True,
  )
  cls = tag.get('class', '')
  assert_in('invalid', cls, err.format('no data', tag))


def test_daterange():
  """Test ``DateRange`` validator."""
  err = "``DateRange`` not catches invalid data with '{}': {}."
  err_false = "``DateRange`` error raised on valid data '{}': {}."
  for case in data_daterange:
    min = case['min']
    max = case['max']
    # don't set ``invalid`` on good values
    for test_value in case['good']:
      tag = get_widget_output(
        TextField,
        validators=[DateRange(min=min, max=max)],
        check=True,
        process={'test': test_value}
      )
      cls = tag.get('class', '')
      assert_not_in('invalid', cls, err_false.format(test_value, tag))
    # set ``invalid`` on bad values
    for test_value in case['bad']:
      tag = get_widget_output(
        TextField,
        validators=[DateRange(min=min, max=max)],
        check=True,
        process={'test': test_value}
      )
      cls = tag.get('class', '')
      assert_in('invalid', cls, err.format(test_value, tag))
