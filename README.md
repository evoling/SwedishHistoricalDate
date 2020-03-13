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

```python
In [1] from SwedishHistoricalDate import SwedishHistoricalDate

In [2]: SwedishHistoricalDate(1700,2,28)
Out[2]: <SwedishHistoricalDate(1700, 2, 28, style=Julian)>

In [3]: SwedishHistoricalDate(1700,2,28) + 1
Out[3]: <SwedishHistoricalDate(1700, 3, 1, style=Swedish)>

In [4]: SwedishHistoricalDate(1800, 1,1) - 1
Out[4]: <SwedishHistoricalDate(1799, 12, 31, style=Gregorian)>

In [5]: SwedishHistoricalDate(1700,2,28) + 1 == SwedishHistoricalDate(1700,3,1)
Out[5]: True

In [6]: SwedishHistoricalDate.fromordinal(625000)
Out[6]: <SwedishHistoricalDate(1712, 2, 30, style=Swedish)>
```
