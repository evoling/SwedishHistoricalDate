#!/usr/bin/env python3
"""
In November 1699, the Government of Sweden decided that, rather than
adopt the Gregorian calendar outright, it would gradually approach it
over a 40-year period. The plan was to skip all leap days in the period
1700 to 1740. Every fourth year, the gap between the Swedish calendar
and the Gregorian would reduce by one day, until they finally lined up
in 1740. In the meantime, this calendar would not be in line with either
of the major alternative calendars and the differences would change
every four years.

In accordance with the plan, February 29 was omitted in 1700, but the
Great Northern War stopped any further omissions from being made in the
following years.

In January 1711, King Charles XII declared that Sweden would abandon the
calendar, which was not in use by any other nation, in favour of a
return to the older Julian calendar. An extra day was added to February
in the leap year of 1712, thus giving it a unique 30-day length
(February 30).

In 1753, one year later than England and its colonies, Sweden introduced the
Gregorian calendar. The leap of 11 days was accomplished in one step, with
February 17 being followed by March 1.

Source: https://en.wikipedia.org/wiki/Swedish_calendar (2020-03-13)
"""
from datetime import datetime
from math import floor
import unittest

GREGORIAN_START = 639965 # Gregorian 1 March 1753
SWEDISH_STYLE_END = 625000 # Swedish 30 February 1712 / Julian 29 Feb
SWEDISH_STYLE_START = 620617 # Swedish 1 March 1700 / Julian 29 Feb
MONTH_LEN = [None,31,None,31,30,31,30,31,31,30,31,30,31]
class SwedishHistoricalDate:
    
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

        # set *rate die*
        if (year, month, day) >= (1753, 3, 1): # Gregorian
            self.rd = datetime(year, month, day).toordinal()
        elif (year, month, day) > (1712, 2, 30): # Julian
            assert (year, month, day) < (1753, 2, 18) 
            self.rd = julian2rd(year, month, day)
        elif (year, month, day) > (1700, 2, 28): # Swedish
            assert (year, month, day) != (1700, 2, 29) 
            self.rd = swedish2rd(year, month, day)
        else: # Julian
            self.rd = julian2rd(year, month, day)

        # sanity checks
        assert year > 0
        assert 1 <= month <= 12
        if month == 2:
            if self.style == "Swedish" and year == 1712:
                feb_len = 30
            elif self.style == "Gregorian" and _is_gregorian_leapyear(year):
                feb_len = 29
            elif _is_julian_leapyear(year): # Julian or Swedish
                feb_len = 29
            else:
                feb_len = 28
            assert 1 <= day <= feb_len
        else:
            assert 1 <= day <= MONTH_LEN[month]
        return

    def __add__(self, N):
        return SwedishHistoricalDate.fromordinal(self.rd + N)

    def __sub__(self, N):
        return SwedishHistoricalDate.fromordinal(self.rd - N)

    def __eq__(self, other):
        if isinstance(other, SwedishHistoricalDate):
            return self.rd == other.rd
        raise NotImplemented

    @classmethod
    def fromordinal(cls, N):
        style = _get_style_from_rd(N)
        if style == "Julian":
            return cls(*rd2julian(N))
        elif style == "Swedish":
            return cls(*rd2swedish(N))
        else:
            assert style == "Gregorian"
            dateobj = datetime.fromordinal(N)
            return cls(dateobj.year, dateobj.month, dateobj.day)

    def toordinal(self):
        return self.rd

    @property
    def tuple(self):
        return (self.year, self.month, self.day)

    @property
    def proleptic_gregorian_tuple(self):
        dateobj = datetime.fromordinal(self.rd)
        return (dateobj.year, dateobj.month, dateobj.day)

    @property
    def style(self):
        if self.rd >= GREGORIAN_START:
            return "Gregorian"
        elif self.rd > SWEDISH_STYLE_END:
            return "Julian"
        elif self.rd >= SWEDISH_STYLE_START:
            return "Swedish"
        else:
            return "Julian"

    def __repr__(self):
        return "<SwedishHistoricalDate({}, {}, {}, style={})>".format(
                self.year, self.month, self.day, self.style)

# Julian calendar calculations from:
#   Reingold, Edward M. and Nachum Dershowitz. 2018. Calendrical
#   Calculations: The Ultimate Edition. 4th ed. Cambridge University
#   Press. https://doi.org/10.1017/9781107415058.

_julian_epoch = -1

def _is_julian_leapyear(year):
    return year % 4 == 0

def _is_gregorian_leapyear(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

def _get_style_from_rd(rd):
    if rd >= GREGORIAN_START:
        return "Gregorian"
    elif rd > SWEDISH_STYLE_END:
        return "Julian"
    elif rd >= SWEDISH_STYLE_START:
        return "Swedish"
    else:
        return "Julian"

def rd2julian(rd):
    # Year
    approx = floor((4 * (rd - _julian_epoch) + 1464) / 1461)
    if approx <= 0: 
        year = approx - 1
    else:
        year = approx
    # Month
    prior_days = rd - julian2rd(year, 1, 1)
    if rd < julian2rd(year, 3, 1):
        correction = 0
    elif _is_julian_leapyear(year):
        correction = 1
    else:
        correction = 2
    month = floor((12 * (prior_days + correction) + 373) / 367)
    # Day
    day = rd - julian2rd(year, month, 1) + 1
    return year, month, day

def rd2swedish(rd):
    if rd == SWEDISH_STYLE_END:
        return (1712, 2, 30)
    else:
        return rd2julian(rd + 1)

def julian2rd(year, month, day):
    if month <= 2:
        leap_year_correction = 0
    elif _is_julian_leapyear(year):
        leap_year_correction = -1
    else:
        leap_year_correction = -2
    rd = (_julian_epoch - 1 +        # year zero
            365 * (year - 1) +       # 365 * the number of complete years
            floor((year -1 ) / 4) +  # an extra day for every leap year
            floor((367 * month - 362) / 12) +
            leap_year_correction + day)
    return rd

def swedish2rd(year, month, day):
    assert (year, month, day) >= (1700, 3, 1)
    assert (year, month, day) <= (1712, 2, 30)
    if (year, month, day) == (1712, 2, 30):
        return SWEDISH_STYLE_END
    else:
        return julian2rd(year, month, day) - 1

class ReingoldDershowitzData:
            
    dates = [# rd gyear gmonth gday jyear jmonth jday
            (524156, 1436, 2, 3,  1436, 1, 25),
            (544676, 1492, 4, 9,  1492, 3, 31),
            (567118, 1553, 9, 19, 1553, 9, 9),
            (569477, 1560, 3, 5,  1560, 2, 24),
            (601716, 1648, 6, 10, 1648, 5, 31),
            (613424, 1680, 6, 30, 1680, 6, 20),
            (626596, 1716, 7, 24, 1716, 7, 13),
            (645554, 1768, 6, 19, 1768, 6, 8),
            (664224, 1819, 8, 2,  1819, 7, 21)]

class TestUtilityFunctions(unittest.TestCase,ReingoldDershowitzData):
    
    def test_julian2rd(self):
        for rd, gy, gm, gd, jy, jm, jd in self.dates:
            self.assertEqual(rd, julian2rd(jy, jm, jd)) 

    def test_rd2julian(self):
        for rd, gy, gm, gd, jy, jm, jd in self.dates:
            self.assertEqual((jy, jm, jd), rd2julian(rd)) 

    def test_swedish_style_start(self):
        self.assertEqual(julian2rd(1700, 2, 29), SWEDISH_STYLE_START)

    def test_swedish_style_end(self):
        self.assertEqual(julian2rd(1712, 2, 29), SWEDISH_STYLE_END)

class TestSwedishHistoricalDateClass(unittest.TestCase,ReingoldDershowitzData):

    def test_date_from_rd(self):
        for rd, gy, gm, gd, jy, jm, jd in self.dates:
            date = SwedishHistoricalDate.fromordinal(rd)
            if date.style == "Gregorian":
                self.assertEqual(date.tuple, (gy, gm, gd))
            elif date.style == "Julian":
                self.assertEqual(date.tuple,
                        (jy, jm, jd))
            else:
                self.assertEqual(date.style, "Swedish")

    def test_julian_to_swedish_transition(self):
        self.assertEqual(
                julian2rd(1700, 2, 29),
                SwedishHistoricalDate(1700, 3, 1).toordinal())

    def test_julian_to_swedish_sequence(self):
        self.assertEqual(
                SwedishHistoricalDate(1700, 2, 28) + 1,
                SwedishHistoricalDate(1700, 3, 1))


    def test_swedish_to_julian_transition(self):
        self.assertEqual(
                julian2rd(1712, 2, 29),
                SwedishHistoricalDate(1712, 2, 30).toordinal())

    def test_swedish_to_julian_sequence(self):
        self.assertEqual(
                SwedishHistoricalDate(1712, 2, 29) + 2,
                SwedishHistoricalDate(1712, 2, 30) + 1,
                SwedishHistoricalDate(1712, 3, 1))

    def test_julian_to_gregorian_seq(self):
        self.assertEqual(
                SwedishHistoricalDate(1753, 2, 17) + 1,
                SwedishHistoricalDate(1753, 3, 1))

    def test_nonexistant_days(self):
        for day in [(1700, 2, 29), (1753, 2, 18), (1753, 2, 28)]:
            with self.assertRaises(AssertionError):
                SwedishHistoricalDate(*day)


__all__ = ["SwedishHistoricalDate"]

if __name__ == "__main__":
    unittest.main()
