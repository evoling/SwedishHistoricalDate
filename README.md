# SwedishHistoricalDate

A module for handling the vagaries of the Swedish calendar before 1753

From https://en.wikipedia.org/wiki/Swedish_calendar:

> In November 1699, the Government of Sweden decided that, rather than adopt the Gregorian calendar outright, it would gradually approach it over a 40-year period. The plan was to skip all leap days in the period 1700 to 1740. Every fourth year, the gap between the Swedish calendar and the Gregorian would reduce by one day, until they finally lined up in 1740. In the meantime, this calendar would not be in line with either of the major alternative calendars and the differences would change every four years.
> 
> In accordance with the plan, February 29 was omitted in 1700, but the Great Northern War stopped any further omissions from being made in the following years.
> 
> In January 1711, King Charles XII declared that Sweden would abandon the calendar, which was not in use by any other nation, in favour of a return to the older Julian calendar. An extra day was added to February in the leap year of 1712, thus giving it a unique 30-day length (February 30).
>
> In 1753, one year later than England and its colonies, Sweden introduced the Gregorian calendar. The leap of 11 days was accomplished in one step, with February 17 being followed by March 1.

The package exports a single class, `SwedishHistoricalDate`. This can be initialised with year-month-day sequences; the object will determine which calendar style was in force at that date
```python
In [1]: from SwedishHistoricalDate import SwedishHistoricalDate

In [2]: SwedishHistoricalDate(1700, 2, 28)
Out[2]: <SwedishHistoricalDate(1700, 2, 28, style=Julian)>
```

These date objects allow simple arithmetic and equality operations.
```python
In [3]: SwedishHistoricalDate(1712, 2, 29) + 1
Out[3]: <SwedishHistoricalDate(1712, 2, 30, style=Swedish)>

In [4]: s = SwedishHistoricalDate(1753, 3, 1)

In [5]: s
Out[5]: <SwedishHistoricalDate(1753, 3, 1, style=Gregorian)>

In [6]: s - 1
Out[6]: <SwedishHistoricalDate(1753, 2, 17, style=Julian)>

In [7]: SwedishHistoricalDate(1700, 2, 28) + 1 == SwedishHistoricalDate(1700,3,1)
Out[7]: True
```

Subtracting one date from another returns an integer indicating the number of days difference: 

```python
In [8]: SwedishHistoricalDate(1753, 3, 1) - SwedishHistoricalDate(1753, 2, 1)
Out[8]: 17
```

Other mathematical operations with two SwedishHistoricalDate objects are not supported. The package doesn't currently implement <, >, <=, >=.

The `.toordinal()` and `.fromordinal()` methods use the same *rate die* (‘fixed dates’—elapsed days since the onset of Monday, 1 January in the Gregorian year 1) that the `datetime` package uses:
```python
In [9]: SwedishHistoricalDate.fromordinal(625000)
Out[9]: <SwedishHistoricalDate(1712, 2, 30, style=Swedish)>
```
