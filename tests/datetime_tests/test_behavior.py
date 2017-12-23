import pickle
from datetime import datetime, date, time, timedelta
from copy import deepcopy

import pytest

import pendulum
from pendulum.tz.timezone import Timezone
from pendulum import timezone


@pytest.fixture
def p():
    return pendulum.create(2016, 8, 27, 12, 34, 56, 123456, tz='Europe/Paris')


@pytest.fixture
def p1(p):
    return p.in_tz('America/New_York')


@pytest.fixture
def dt(p):
    tz = timezone('Europe/Paris')

    return tz.convert(datetime(2016, 8, 27, 12, 34, 56, 123456))


def test_timetuple(p, dt):
    assert dt.timetuple() == p.timetuple()


def test_utctimetuple(p, dt):
    assert dt.utctimetuple() == p.utctimetuple()


def test_date(p, dt):
    assert p.date() == dt.date()


def test_time(p, dt):
    assert p.time() == dt.time()


def test_timetz(p, dt):
    assert p.timetz() == dt.timetz()


def test_astimezone(p, dt, p1):
    assert p.astimezone(p1.tzinfo) == dt.astimezone(p1.tzinfo)


def test_ctime(p, dt):
    assert p.ctime() == dt.ctime()


def test_isoformat(p, dt):
    assert p.isoformat() == dt.isoformat()


def test_utcoffset(p, dt):
    assert p.utcoffset() == dt.utcoffset()


def test_tzname(p, dt):
    assert p.tzname() == dt.tzname()


def test_dst(p, dt):
    assert p.dst() == dt.dst()


def test_toordinal(p, dt):
    assert p.toordinal() == dt.toordinal()


def test_weekday(p, dt):
    assert p.weekday() == dt.weekday()


def test_isoweekday(p, dt):
    assert p.isoweekday() == dt.isoweekday()


def test_isocalendar(p, dt):
    assert p.isocalendar() == dt.isocalendar()


def test_fromtimestamp():
    p = pendulum.fromtimestamp(0, pendulum.UTC)
    dt = datetime.fromtimestamp(0, pendulum.UTC)

    assert p == dt


def test_utcfromtimestamp():
    p = pendulum.utcfromtimestamp(0)
    dt = datetime.utcfromtimestamp(0)

    assert p == dt


def test_fromordinal():
    assert datetime.fromordinal(730120) == pendulum.fromordinal(730120)


def test_combine():
    p = pendulum.combine(date(2016, 1, 1), time(1, 2, 3, 123456))
    dt = datetime.combine(date(2016, 1, 1), time(1, 2, 3, 123456))

    assert p == dt


def test_hash():
    dt1 = pendulum.create(2016, 8, 27, 12, 34, 56, 123456, tz='Europe/Paris')
    dt2 = pendulum.create(2016, 8, 27, 12, 34, 56, 123456, tz='Europe/Paris')
    dt3 = pendulum.create(2016, 8, 27, 12, 34, 56, 123456, tz='America/Toronto')

    assert hash(dt1) == hash(dt2)
    assert hash(dt1) != hash(dt3)


def test_pickle():
    dt1 = pendulum.create(2016, 8, 27, 12, 34, 56, 123456, tz='Europe/Paris')
    s = pickle.dumps(dt1)
    dt2 = pickle.loads(s)

    assert dt1 == dt2


def test_pickle_with_integer_tzinfo():
    dt1 = pendulum.create(2016, 8, 27, 12, 34, 56, 123456, tz=0)
    s = pickle.dumps(dt1)
    dt2 = pickle.loads(s)

    assert dt1 == dt2


def test_proper_dst():
    dt = pendulum.create(1941, 7, 1, tz='Europe/Amsterdam')

    assert dt.dst() == timedelta(0, 6000)


def test_deepcopy():
    dt = pendulum.create(1941, 7, 1, tz='Europe/Amsterdam')

    assert dt == deepcopy(dt)


def test_pickle_timezone():
    dt1 = pendulum.timezone('Europe/Amsterdam')
    s = pickle.dumps(dt1)
    dt2 = pickle.loads(s)

    assert isinstance(dt2, Timezone)

    dt1 = pendulum.timezone('UTC')
    s = pickle.dumps(dt1)
    dt2 = pickle.loads(s)

    assert isinstance(dt2, Timezone)