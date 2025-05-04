########################################################################################
# File: PYHebrew.py
# Contents: Hebrew calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025-05-04
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################

#
# Hebrew Calendrical Calculations
#

import math
from collections import namedtuple
from datetime import date

# Global Variables

HEBREW_EPOCH = -1373427 # October 7, -3761 (Julian)

Nisan = 1
Iyyar = 2
Sivan = 3
Tammuz = 4
Av = 5
Elul = 6
Tishri = 7
Marheshvan = 8
Kislev = 9
Tevet = 10
Shevat = 11
Adar = 12
AdarII = 13

January = 1
December = 12

Sunday = 0
Monday = 1
Tuesday = 2
Wednesday = 3
Thursday = 4
Friday = 5
Saturday = 6

NO_RULE = 0
THURSDAY_OBSERVED_ON_WEDNESDAY = 1
FRIDAY_OBSERVED_ON_THURSDAY = 2
FRIDAY_OBSERVED_ON_WEDNESDAY = 3
SATURDAY_OBSERVED_ON_FRIDAY = 4
SATURDAY_OBSERVED_ON_MONDAY = 5
SATURDAY_OBSERVED_ON_SUNDAY = 6
SATURDAY_OBSERVED_ON_THURSDAY = 7
SUNDAY_OBSERVED_ON_MONDAY = 8
MONDAY_OBSERVED_ON_TUESDAY = 9
HEBREW_HESHVAN30 = 10
HEBREW_KISLEV30 = 11
WEEKDAY_RULES = 12
AFTER_RULE = 13
NO_WEEK_DAY = 14


# Holiday Name, Month, Day, Thursday Rule, Friday Rule, Saturday Rule, Sunday Rule, Monday Rule, Marheshvan Rule, KisLev Rule, Weekday Rule, After Rule, Week Day
HebrewHolidaysList = [
   "Rosh HaShana",Tishri,1,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Shabbat Shuva",Tishri,1,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,AFTER_RULE,Saturday,
   "Yom Kippur",Tishri,10,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Sukkot",Tishri,15,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Sh'mini Atzeret",Tishri,22,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Rosh Chodesh Kislev",Kislev,1,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,HEBREW_HESHVAN30,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Hanukkah",Kislev,25,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Rosh Chodesh Tevet",Tevet,1,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,HEBREW_KISLEV30,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Purim",Adar,14,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Passover",Nisan,15,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Yom HaShoah",Nisan,27,NO_RULE,FRIDAY_OBSERVED_ON_THURSDAY,NO_RULE,SUNDAY_OBSERVED_ON_MONDAY,NO_RULE,NO_RULE,NO_RULE,WEEKDAY_RULES,NO_RULE,NO_WEEK_DAY,
   "Yom HaZikaron",Iyyar,4,THURSDAY_OBSERVED_ON_WEDNESDAY,FRIDAY_OBSERVED_ON_WEDNESDAY,NO_RULE,SUNDAY_OBSERVED_ON_MONDAY,NO_RULE,NO_RULE,NO_RULE,WEEKDAY_RULES,NO_RULE,NO_WEEK_DAY,
   "Yom HaAtzmaut",Iyyar,5,THURSDAY_OBSERVED_ON_WEDNESDAY,FRIDAY_OBSERVED_ON_THURSDAY,SATURDAY_OBSERVED_ON_THURSDAY,NO_RULE,MONDAY_OBSERVED_ON_TUESDAY,NO_RULE,NO_RULE,WEEKDAY_RULES,NO_RULE,NO_WEEK_DAY,
   "Pesach Sheni",Iyyar,14,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Yom Yerushalayim",Iyyar,28,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Shavout",Sivan,6,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_RULE,NO_WEEK_DAY,NO_RULE,NO_WEEK_DAY,
   "Tish'ah B'av",Av,9,NO_RULE,NO_RULE,SATURDAY_OBSERVED_ON_SUNDAY,NO_RULE,NO_RULE,NO_RULE,NO_RULE,WEEKDAY_RULES,NO_RULE,NO_WEEK_DAY
]


ShortHebrewMonths = [Iyyar,Tammuz,Elul,Tevet,AdarII]
MonthNames = ['Nisan','Iyyar','Sivan','Tammuz','Av','Elul','Tishri','Marheshvan','Kislev','Tevet','Shevat','Adar','AdarII']
HebrewHoliday = namedtuple('HebrewHoliday', ['Name', 'DateFound', 'Date', 'DateObserved'])

Nisan = 1
Iyyar = 2
Sivan = 3
Tammuz = 4
Av = 5
Elul = 6
Tishri = 7
Marheshvan = 8
Kislev = 9
Tevet = 10
Shevat = 11
Adar = 12
AdarII = 13


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

def cmHebrewLeapYear (nYear: int) -> bool:
#
# Check for a Hebrew Leap Year
#
   return cmMod((nYear * 7) + 1,19) < 7
# End Def

def cmLastMonthOfHebrewYear (nYear: int) -> int:
#
# Last month of Hebrew Year
#
   if cmHebrewLeapYear (nYear) == True:
      return AdarII
   else:
      return Adar
# End Def

def cmMolad (nMonth: int, nYear: int) -> float:
#
# Fixed moment of mean conjunction for Hebrew month and year
#
   if nMonth < Tishri:
      nYearAdjust = nYear + 1
   else:
      nYearAdjust = nYear
   nMonthsElasped = nMonth - Tishri + cmFloor(((235 * nYearAdjust) - 234) / 19)
   return HEBREW_EPOCH - (876 / 25920) + (nMonthsElasped * (29.5 + (793 / 25920)))
# End Def

def cmHebrewCalendarElapsedDays (nYear: int) -> int: 
#
# Hebrew Elasped Days
#
   nDays = cmFloor(cmMolad(Tishri,nYear) - HEBREW_EPOCH + .5)
   if cmMod(3 * (nDays + 1),7) < 3:
      nDays = nDays + 1
   return nDays
# End Def

def cmHebrewYearLengthCorrection (nYear: int) -> int:
#
# Add correction to length of Hebrew Year
#
   nElaspedDays = cmHebrewCalendarElapsedDays(nYear)
   if nElaspedDays - cmHebrewCalendarElapsedDays(nYear - 1) == 382:
      nDays = 1
   elif cmHebrewCalendarElapsedDays(nYear + 1) - nElaspedDays == 356:
      nDays = 2
   else:
      nDays = 0
   return nDays
# End Def

def cmHebrewNewYear (nYear: int) -> int:
#
# Hebrew New Year (Begins on evening before and we return the next day)
#
   return HEBREW_EPOCH + cmHebrewCalendarElapsedDays(nYear) + cmHebrewYearLengthCorrection(nYear)
# End Def

def cmDaysInHebrewYear (nYear: int) -> int: 
#
# Days in Hebrew Year
#
   return cmHebrewNewYear(nYear + 1) - cmHebrewNewYear(nYear)
# End Def

def cmShortKislev (nYear: int):
#
# Kislev Month Length
#
   nDays = cmDaysInHebrewYear(nYear)
   return nDays in [353,383]
# End Def

def cmLongMarheshvan (nYear: int):
#
# Marheshvan Month Length
#
   nDays = cmDaysInHebrewYear(nYear)
   return nDays in [355,385]
# End Def

def cmLastDayOfHebrewMonth (nMonth: int, nYear: int) -> int:
#
# Last Day of Hebrew Month
#
   isLeapYear = cmHebrewLeapYear (nYear)
   isLongMarheshvan = cmLongMarheshvan (nYear)
   isShortKislev = cmShortKislev (nYear)
   #
   #  Look for 29 day months
   #
   if nMonth in ShortHebrewMonths:
      nMonthLength = 29
   elif nMonth == Adar and isLeapYear == False:
      nMonthLength = 29
   elif nMonth == Marheshvan and isLongMarheshvan == False:
      nMonthLength = 29
   elif nMonth == Kislev and isShortKislev == True:
      nMonthLength = 29
   else:
      nMonthLength = 30
   return nMonthLength
#End Def

def cmHebrewSabbaticalYear (nYear: int):
#
# Check for a Hebrew Sabbatical Year
# Biblically mandated in Exodus 23:10-11
#
   return cmMod(nYear,7) == 0
# End Def

def DaysFromHebrew (nMonth: int, nDay: int, nYear: int) -> int:
#
# Calculate Days from Hebrew Date
#
# Get start of the year plus days so far this month
   nDays = cmHebrewNewYear (nYear) + nDay - 1
   #
   # Add in elasped days in the given month and the length of each elasped month.
   # Since Hebrew years begin on the seventh month (Tishri), we have to check
   # for months before and after Tishri
   #
   nMonthsInYear = cmLastMonthOfHebrewYear (nYear)
   if nMonth < Tishri:
      for nLastMonth in range (Tishri,nMonthsInYear + 1):
         nDays = nDays + cmLastDayOfHebrewMonth (nLastMonth,nYear)
      if nMonth > Nisan:
         for nLastMonth in range (Nisan,nMonth):
            nDays = nDays + cmLastDayOfHebrewMonth (nLastMonth,nYear)
   elif nMonth > Tishri:
      for nLastMonth in range (Tishri,nMonth):
        nDays = nDays + cmLastDayOfHebrewMonth (nLastMonth,nYear)
   if nYear < 0:
      nDays = nDays - 1
   return nDays
#End Def

def cmGregorianNewYear (nYear: int) -> int:
#
# Return the first day of a gregorian year in days format
#
   return date(nYear,January,1).toordinal()
# End Def

def cmGregorianYearEnd (nYear: int) -> int:
#
# Return the last day of a gregorian year in days format
#
   return date(nYear,December,31).toordinal()
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

def HebrewFromDays (nDays: int):
#
# Calculate Hebrew Date from Days
#
   nYear = cmFloor((98496 / 35975351) * (nDays - HEBREW_EPOCH))  # Year can be off by +-1
   while cmHebrewNewYear(nYear) <= nDays:
      nYear = nYear + 1
   nYear = nYear - 1
   #
   # Starting Month for search
   #
   if nDays < DaysFromHebrew(Nisan,1,nYear):
      nMonth = Tishri
   else:
      nMonth = Nisan
   #
   # Look for Month that contains nDays
   #
   while nDays > DaysFromHebrew(nMonth,cmLastDayOfHebrewMonth(nMonth,nYear),nYear):
      nMonth = nMonth + 1
   nDay = nDays - DaysFromHebrew(nMonth,1,nYear) + 1
   HebrewDate = []
   HebrewDate.append(nMonth)
   HebrewDate.append(nDay)
   HebrewDate.append(nYear)
   HebrewDate.append(cmHebrewSabbaticalYear(nYear))
   HebrewDate.append(cmHebrewLeapYear(nYear))
   return HebrewDate
# End Def

def HebrewDateCalculation (holidayName: str, nMonth: int, nDay: int, nGregorianYear: int, ThursdayRule: int, FridayRule: int, SaturdayRule: int, SundayRule: int, MondayRule: int, MarheshvanRule: int, KisLevRule: int, WeekRule: int, AfterRule: int, Weekday: int):
#
# Calculate a Hebrew date based on rules
#
   nHebrewYear = nGregorianYear + 3760
   nJan1 = cmGregorianNewYear (nGregorianYear)
   nDec31 = cmGregorianYearEnd (nGregorianYear)
   #
   # Calculate the Hebrew Year
   #
   nCalcDays = DaysFromHebrew(nMonth,nDay,nHebrewYear)
   #
   # Check if Hebrew date occurs during nGregorianYear
   #
   if nCalcDays not in range(nJan1,nDec31):
      nHebrewYear = nHebrewYear + 1
      nCalcDays = DaysFromHebrew(nMonth,nDay,nHebrewYear)
   HebrewLeapYear = cmHebrewLeapYear(nHebrewYear)
   #
   # Check if Hebrew date occurs during nGregorianYear
   #
   if nCalcDays not in range(nJan1,nDec31):
      gregorianDate = date.fromordinal (nCalcDays)
      observedDate = gregorianDate
      HEBREWHolidayCalc = HebrewHoliday(holidayName,False,str(gregorianDate),str(observedDate))
      return HEBREWHolidayCalc
   #
   # If month is Adar and we have a leap year, change month to AdarII
   # Examples where this is applicable include Purim and Ta'anit Esther
   #
   if nMonth == Adar and HebrewLeapYear == True:
      nCalcDays = cmDaysFromHebrew(AdarII,nDay,nHebrewYear)	
   gregorianDate = date.fromordinal (nCalcDays)
   #
   # Check for rules
   #
   if MarheshvanRule == HEBREW_HESHVAN30 and cmLastDayOfHebrewMonth(Marheshvan,nHebrewYear) == 30:  # Examples using this rule: Rosh Chodesh Kislev
      nCalcDays = nCalcDays - 1
   if KisLevRule == HEBREW_KISLEV30 and cmLastDayOfHebrewMonth(Kislev,nHebrewYear) == 30:  # Examples using this rule: Rosh Chodesh Tevet
      nCalcDays = nCalcDays - 1
   if AfterRule == AFTER_RULE:   # Examples using this rule: Shabbat Shuva - Saturday after New Year
      nCalcDays = WeekDayAfter (nCalcDays, Weekday)  
   if WeekRule == WEEKDAY_RULES:
      nWeekDay = nCalcDays % 7
      if nWeekDay == Monday and MondayRule == MONDAY_OBSERVED_ON_TUESDAY:
         nCalcDays = nCalcDays + 1
      elif nWeekDay == Thursday and ThursdayRule == THURSDAY_OBSERVED_ON_WEDNESDAY:
         nCalcDays = nCalcDays - 1
      elif nWeekDay == Friday and FridayRule == FRIDAY_OBSERVED_ON_THURSDAY:
         nCalcDays = nCalcDays - 1
      elif nWeekDay == Friday and FridayRule == FRIDAY_OBSERVED_ON_WEDNESDAY:
         nCalcDays = nCalcDays - 2
      elif nWeekDay == Saturday and SaturdayRule == SATURDAY_OBSERVED_ON_FRIDAY:
         nCalcDays = nCalcDays - 1
      elif nWeekDay == Saturday and SaturdayRule == SATURDAY_OBSERVED_ON_MONDAY:
         nCalcDays = nCalcDays + 2
      elif nWeekDay == Saturday and SaturdayRule == SATURDAY_OBSERVED_ON_SUNDAY:
         nCalcDays = nCalcDays + 1
      elif nWeekDay == Saturday and SaturdayRule == SATURDAY_OBSERVED_ON_THURSDAY:
        nCalcDays = nCalcDays - 2
      elif nWeekDay == Sunday and SundayRule == SUNDAY_OBSERVED_ON_MONDAY:
         nCalcDays = nCalcDays + 1
   observedDate = date.fromordinal (nCalcDays) 
   HEBREWHolidayCalc = HebrewHoliday(holidayName,True,str(gregorianDate),str(observedDate))
   return HEBREWHolidayCalc
# End Def

def FormatHebrewDate (HebrewDate) -> str:
#
# Using the HebrewDate list return a formatted string
#
   if HebrewDate[4] == False:
      sLeapYear = ''
   else:
      sLeapYear = '.Leap'
   if HebrewDate[3] == False:
      sSabbaticalYear = ''
   else:
      sSabbaticalYear = ' (Sabbatical Year)'
   return  MonthNames[HebrewDate[0] - 1] + ' ' + str(HebrewDate[1]) + ', ' + str(HebrewDate[2]) + sLeapYear + sSabbaticalYear
# End Def

pyNow = CurrentDate()
print ("Today: " + str(pyNow))
print ("Today's Ordinal Days: " + str(pyNow.toordinal()))
HebrewDate = HebrewFromDays (pyNow.toordinal())
print ('Hebrew Date: ' + FormatHebrewDate(HebrewDate))
print ("DaysFromHebrew: " + str(DaysFromHebrew(HebrewDate[0],HebrewDate[1],HebrewDate[2])))
print ('')
print ('Hebrew Holidays during Gregorian Year ' + str(pyNow.year))
print ('')
i = 0
while i < len(HebrewHolidaysList):
   HEBREWHoliday = HebrewDateCalculation (HebrewHolidaysList[i],HebrewHolidaysList[i + 1],HebrewHolidaysList[i + 2],pyNow.year,HebrewHolidaysList[i + 3],HebrewHolidaysList[i + 4],HebrewHolidaysList[i + 5],HebrewHolidaysList[i + 6],HebrewHolidaysList[i + 7],HebrewHolidaysList[i + 8],HebrewHolidaysList[i + 9],HebrewHolidaysList[i + 10],HebrewHolidaysList[i + 11],HebrewHolidaysList[i + 12])
   print (HEBREWHoliday)
   i = i + 13
