########################################################################################
# File: PYCoptic.py
# Contents: Coptic calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025-05-09
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################
#
# Coptic Calendrical Calculations (Used in Egypt)
#
# Copts are a Christian group native to Northeast Africa and follow the Orthodox Church in Alexandria.
#
# A subset of Julian date calculations are included for the calculation of Easter

import math
from datetime import date

#
# Global variables
#

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

THOOUT = 1
PAOP = 2
ATHOR = 3
KOIAK = 4
TOBE = 5
MESHIR = 6
PAREMOTEP = 7
PARMOUTE = 8
PASHONS = 9
PAONE = 10
EPEP = 11
MESORE = 12
EPAGOMENE = 13

NO_RULES = 0
EASTER_RULES = 1

# Astronomical definitions

COPTIC_EPOCH = 103605   # August 29, 0284
JULIAN_EPOCH = -1   # December 30, 0000

CopticMonthNames = ['Tout','Paopi','Hathor','Koiak','Tobi','Meshir','Paremhat','Parmouti','Pashons','Paoni','Epip','Mesori','Pi Kogi Enavot']

# Name, Month, Day, Rule
CopticHolidaysList = [
   'Nayrouz',THOOUT,1,NO_RULES,
   'The Annunciation',PAREMOTEP,29,NO_RULES,
   'The Nativity of Christ',KOIAK,29,NO_RULES,
   'The Epiphany',TOBE,11,NO_RULES,
   'The Apostles Feast',EPEP,5,NO_RULES,
   'The Two Feasts of the Cross (first)',THOOUT,17,NO_RULES,
   'The Two Feasts of the Cross (second)',PAREMOTEP,10,NO_RULES,
   'Palm Sunday',0,-7,EASTER_RULES,
   'Good Friday',0,-2,EASTER_RULES,
   'Easter',0,0,EASTER_RULES,
   'Ascension',0,39,EASTER_RULES
]

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

def cmOrthodoxEasterDate (nYear: int) -> int:
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
   return nEasterDays
# End Def

def DaysFromCoptic (nMonth: int, nDay: int, nYear: int) -> int:
#
# Given a Coptic Date, return Days Date
#
   return cmFloor(COPTIC_EPOCH - 1 + 365 * (nYear - 1) + (cmFloor(nYear / 4)) + 30 * (nMonth - 1) + nDay)
# End Def

def CopticFromDays (nDays: int):
#
# Given a Days Date, return Coptic Date
#
   nYear = cmFloor((4 * (nDays - COPTIC_EPOCH) + 1463) / 1461)
   nMonth = cmFloor((nDays - DaysFromCoptic(1,1,nYear)) / 30) + 1
   nDay = nDays + 1 - DaysFromCoptic(nMonth,1,nYear)
   CopticDate = []
   CopticDate.append(nMonth)
   CopticDate.append(nDay)
   CopticDate.append(nYear)
   return CopticDate
# End Def

def CopticDateCalculation (nMonth: int, nDay: int, nGregorianYear: int, nRule: int) -> date:
#
# Return Coptic dates occurring in a given Gregorian year
#
   if nRule == NO_RULES:
      nJan1 = date(nGregorianYear,January,1).toordinal()
      CopticDate = CopticFromDays(nJan1)
#
# Calculate the Coptic Date
#
      nCalcDays = DaysFromCoptic(nMonth,nDay,CopticDate[2])
      if nCalcDays < nJan1:
         nCalcDays = DaysFromCoptic(nMonth,nDay,CopticDate[2] + 1)
   else:
#
# Easter based dates, nDay is the number of +- days offset from Easter
#
      nCalcDays = cmOrthodoxEasterDate(nGregorianYear) + nDay
   return date.fromordinal(nCalcDays)
# End Def

pyNow = CurrentDate()
print ('Today Local: ' + str(pyNow))
nDays = pyNow.toordinal()
print ("Today's Local Ordinal Days: " + str(nDays))
CopticDate = CopticFromDays(nDays)
print ('Coptic Date: ' + CopticMonthNames[CopticDate[0] - 1] + ' ' + str(CopticDate[1]) + ', ' + str(CopticDate[2]))
print ('Days from Coptic: ' + str(DaysFromCoptic(CopticDate[0],CopticDate[1],CopticDate[2])))
print ('')
print ('Coptic Holidays during Gregorian Year ' + str(pyNow.year))
print ('')
i = 0
while i < len(CopticHolidaysList):
   print (CopticHolidaysList[i] + ': ' + str(CopticDateCalculation(CopticHolidaysList[i + 1],CopticHolidaysList[i + 2],pyNow.year,CopticHolidaysList[i + 3])))      
   i = i + 4










