########################################################################################
# File: PYJulian.py
# Contents: Julian calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025-05-04
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################

#
# Julian Calendrical Calculations
#

import math
from collections import namedtuple
from datetime import date

# Global Variables

Sunday = 0
Monday = 1
Tuesday = 2
Wednesday = 3
Thursday = 4
Friday = 5
Saturday = 6

January = 1
February = 2
March = 3
April = 4
May = 5
June = 6
July = 7
August = 8
September = 9
October = 10
November = 11
December = 12

JULIAN_EPOCH = -1   # December 30, 0000

MonthNames = ['January','February','March','April','May','June','July','August','September','October','November','December']
WeekDayNames = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def CurrentDate () -> date:
#
# Retrieve the current date
#
   return date.today()
# End Def

def cmFloor (x: float) -> int:
#
# Largest integer less than or equal to x
#
   return int(math.floor(x))
# End Def

def cmMod (x: float, y: float) -> float:
#
# x MOD y for Real Numbers, y<>0
#
   return x % y
# End Def

def cmJulianLeapYear (nYear: int):
#
# Determine if nYear is a Julian leap year
#
   nLeapYear = False
   if nYear > 0 and cmFloor(cmMod(nYear,4)) == 0:
      nLeapYear = True
   elif nYear == 0:
      nLeapYear = True
   elif cmFloor(cmMod(nYear,4)) == 3:
     nLeapYear = True
   return nLeapYear
# End Def

def cmGregorianWeekDay (nDays: int) -> int:
#
# Calculate the Gregorian day of the week handling nDays < 0
#
  return abs(cmFloor(cmMod(nDays,7)))
# End Def

def WeekdayOnOrBefore (nGregorianDays: int, weekday: int) -> int:
#
# Description: Calculate weekday on or before
# Weekday = 0=Sun....6=Sat
   return nGregorianDays - ((nGregorianDays - weekday) % 7)
# End Def

def WeekDayAfter (nGregorianDays: int, weekday: int) -> int:
#
# Description: Calculate weekday after
# Weekday = 0=Sun....6=Sat
#
   return WeekdayOnOrBefore(nGregorianDays + 7, weekday)
# End Def

def DaysFromJulian (nMonth: int, nDay: int, nYear) -> int:
#
# Calculate days date from Julian date
#
   if nMonth <= 2:
      nMonthAdjust = 0
   else:
      if cmJulianLeapYear(nYear):
         nMonthAdjust = -1
      else:
         nMonthAdjust = -2
   # 
   # Year has to be adjusted since year zero is not valid
   #
   if nYear < 1:
      nYearAdjust = nYear + 1
   else:
      nYearAdjust = nYear
   return (JULIAN_EPOCH - 1 + 365 * (nYearAdjust - 1)) + cmFloor((nYearAdjust - 1) / 4) + cmFloor((nMonth * 367 - 362) / 12) + nMonthAdjust + nDay
# End Def

def JulianFromDays (nDays: int):
#
# Return the Julian date from a days date
#
   nWeekDay = cmGregorianWeekDay(nDays)
   nApprox = cmFloor((1 / 1461) * (4 * (nDays - JULIAN_EPOCH) + 1464))   # 1461 represents the last day of a 4 year cycle
   if nApprox <= 0:
      nYear = nApprox - 1
   else:
      nYear = nApprox
   nLeapYear = cmJulianLeapYear(nYear)
   nPriorDays = nDays - DaysFromJulian(January,1,nYear)
   if nDays < DaysFromJulian(March,1,nYear):
      nCorrection = 0
   elif nLeapYear == True:
      nCorrection = 1
   else:
      nCorrection = 2
   nMonth = cmFloor((1 / 367) * (12 * (nPriorDays + nCorrection) + 373))
   nDay = nDays - DaysFromJulian(nMonth,1,nYear) + 1
   JulianDate = []
   JulianDate.append(nMonth)
   JulianDate.append(nDay)
   JulianDate.append(nYear)
   JulianDate.append(nWeekDay)
   JulianDate.append(nLeapYear)
   return JulianDate
# End Def

def OrthodoxEasterDate (nYear: int) -> date:
#
# Calculate Easter for Orthodox churches
#
   nNicaeanRule = cmFloor(cmMod(nYear,19))
   nShiftedEpact = cmFloor(cmMod(14 + 11 * nNicaeanRule,30))
   # 
   # Year has to be adjusted since year zero is not valid
   #
   if nYear > 0:
      nYearAdjust = nYear
   else:
      nYearAdjust = nYear - 1
   nEasterDays = WeekDayAfter (DaysFromJulian(April,19,nYearAdjust) - nShiftedEpact,Sunday)
   return date.fromordinal (nEasterDays)
# End Def

def FormatJulianDate (JulianDate) -> str:
#
# Using the JulianDate list return a formatted string
#
   if JulianDate[4] == False:
      sLeapYear = ''
   else:
      sLeapYear = '.Leap'
   return  WeekDayNames[JulianDate[3]] + ', ' + MonthNames[JulianDate[0] - 1] + ' ' + str(JulianDate[1]) + ', ' + str(JulianDate[2]) + sLeapYear
# End Def 

pyNow = CurrentDate()
print ("Today: " + str(pyNow))
print ("Today's Ordinal Days: " + str(pyNow.toordinal()))
JulianDate = JulianFromDays(pyNow.toordinal())
print ('Julian Date: ' + FormatJulianDate(JulianDate))
print ("DaysFromJulian: " + str(DaysFromJulian(JulianDate[0],JulianDate[1],JulianDate[2])))
print ("Orthodox Easter: " + str(OrthodoxEasterDate(pyNow.year)))
