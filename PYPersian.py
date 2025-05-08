########################################################################################
# File: PYPersian.py
# Contents: Persian calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025-05-08
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################
#
# Persian Calendrical Calculations
#

import math
from datetime import date

#
# Global variables
#

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

FARVARDIN = 1
ORDIBEHESHT = 2
XORDAD = 3
TIR = 4
MORDAD = 5
SHAHRIVAR = 6
MEHR = 7
ABAN = 8
AZAR = 9
DEY = 10
BAHMAN = 11
ESFAND = 12

# Astronomical definitions

PERSIAN_EPOCH = 226896   # March 22, 622
J2000 = 730120.5   # January 1, 2000 at noon
SPRING = 0
TehranLocale_Latitude = 35.69439  
TehranLocale_Longitude = 51.42151 
TehranLocale_Elevation = 1178
TehranLocale_Zone = 3.5

PersianMonthNames = ['Farvardin','Ordibehesht','Xordad','Tir','Mordad','Shahrivar','Mehr','Aban','Azar','Dey','Bahman','Esfand']
#
# Name, Persian Month, Persian Day
#
PersianHolidaysList = [
   'Nowruz',FARVARDIN,1,
   'Islamic Republic Day',FARVARDIN,12,
   'Sizdah Bedar',FARVARDIN,13,
]

def CurrentDate () -> date:
#
# Retrieve the current date
#
   return date.today()
# End Def

def cmGregorianDateDifference (nStartMonth: int, nStartDay: int, nStartYear: int, nEndMonth: int, nEndDay: int, nEndYear: int) -> int:
#
# Calculate the difference in days between two Gregorian dates
#
   return date(nEndYear, nEndMonth, nEndDay).toordinal() - date(nStartYear, nStartMonth, nStartDay).toordinal()
# End Def

def cmGregorianYearFromDays (nDays: int) -> int:
#
# Given a Days date, return the gregorian year
#
   pyDate = date.fromordinal(nDays)
   return pyDate.year
# End Def

def cmAngle (nDegrees: float, nMinutes: float, nSeconds: float) -> float:
#
# Return decimal degrees
#
   nDecimalDegrees = (abs(nDegrees) + (abs(nMinutes) / 60) + (abs(nSeconds) / 3600))
   if nDegrees < 0:
      nDecimalDegrees = nDegrees * -1
   return nDecimalDegrees
# End Def

def cmFloor (x: float) -> int:
#
# Largest integer less than or equal to x
#
   return int(math.floor(x))
# End Def

def cmCeiling (x: float) -> int:
#
# Largest integer greater than x
#
   return int(math.ceil(x))
# End Def

def cmMod (x: float, y: float) -> float:
#
# x MOD y for Real Numbers, y<>0
#
   return x % y
# End Def

def cmSignum (nAny: float) -> int:
#
# Return the sign of nAny
#
   if nAny < 0:
      return -1
   elif nAny > 0:
      return 1
   else:
      return 0
# End Def

def cmRound (x: float) -> int:
#
# Round x up to nearest integer
#
   return cmFloor(x + .5)
# End Def

def cmCalcDegrees (nDegrees: float) -> float:
#
# Normalize degress within 0-360
#
   return cmMod(nDegrees,360)
# End Def

def cmDegreesToRadians (nDegrees: float) -> float:
#
# Convert Degrees to Radians
#
   return math.radians(nDegrees)
# End Def

def cmRadiansToDegrees (nRadians: float) -> float:
#
# Convert Radians to Degrees
#
   return math.degrees(nRadians)
# End Def

def cmSinDegrees (nTheta: float) -> float:
#
# Sine Degrees converted to Radians
#
   return math.sin(cmDegreesToRadians(nTheta))
# End Def

def cmCoSineDegrees (nTheta: float) -> float:
#
# Cosine Degrees converted to Radians
#
   return math.cos(cmDegreesToRadians(nTheta))
# End Def

def cmArcCoSineDegrees (nTheta: float) -> float:
#
# Arc Cosine converted to degrees
#
   return cmRadiansToDegrees(math.acos(nTheta))
# End Def

def cmArcSinDegrees (nTheta: float) -> float:
#
# Arc Sine converted to Degrees
#
   return cmRadiansToDegrees(math.asin(nTheta))
# End Def
 
def cmTangentDegrees (nTheta: float) -> float:
#
# Tangent degrees converted to Radians
#
   return math.tan(cmDegreesToRadians(nTheta))
# End Def

def cmArcTanDegrees (nY: float, nX: float) -> float:
#
# Arc Tangent converted to -180 to 180 degrees range
#
 return cmCalcDegrees(cmRadiansToDegrees(math.atan2(nY,nX)))
# End Def

def cmEphemerisCorrection (nMoment: float) -> float:
#
# General adjustment for the slowly decreasing rotation of the earth
#
   nYear = cmGregorianYearFromDays(cmFloor(nMoment))
   nC = cmGregorianDateDifference(January,1,1900,July,1,nYear) / 36525.0
   if nYear >= 2051 and nYear <= 2150:
      nCorrection = (-20 + 32 * ((nYear - 1820) / 100)**2 + 0.5628 * (2150 - nYear)) / 86400.0
   elif nYear >= 2006 and nYear <= 2050:
      nY = nYear - 2000
      nCorrection = (62.92 + 0.32217 * nY + 0.005589 * nY**2) / 86400.0
   elif nYear >= 1987 and nYear <= 2005:
      nY = nYear - 2000
      nCorrection = (63.86 + 0.3345 * nY - 0.060374 * nY**2 + 0.0017275 * nY**3 + 0.000651814 * nY**4 + 0.00002373599 * nY**5) / 86400.0
   elif nYear >= 1900 and nYear <= 1986:
      nCorrection = -0.00002 + 0.000297 * nC + 0.025184 * nC**2 - 0.181133 * nC**3 + 0.553040 * nC**4 - 0.861938 * nC**5 + 0.677066 * nC**6 - 0.212591 * nC**7
   elif nYear >= 1800 and nYear <= 1899:
      nCorrection = -0.000009 + 0.003844 * nC + 0.083563 * nC**2 + 0.865736 * nC**3 + 4.867575 * nC**4 + 15.845535 * nC**5 + 31.332267 * nC**6 + 38.291999 * nC**7 + 28.316289 * nC**8 + 11.636204 * nC**9 + 2.043794 * nC**10
   elif nYear >= 1700 and nYear <= 1799:
      nY = nYear - 1700
      nCorrection = (8.118780842 - 0.005092142 * nY + 0.003336121 * nY**2 - 0.0000266484 * nY**3) / 86400.0
   elif nYear >= 1600 and nYear <= 1699:
      nY = nYear - 1600
      nCorrection = (120 - 0.9808 * nY - 0.01532 * nY**2 + 0.000140272128 * nY**3) / 86400.0
   elif nYear >= 500 and nYear <= 1599:
      nY = (nYear - 1000) / 100
      nCorrection = (1574.2 - 556.01 * nY + 71.23472 * nY**2 + 0.319781 * nY**3 - 0.8503463 * nY**4 - 0.005050998 * nY**5 + 0.0083572073 * nY**6) / 86400.0
   elif nYear >= -499 and nYear <= 499:
      nY = nYear / 100
      nCorrection = (10583.6 - 1014.41 * nY + 33.78311 * nY**2 - 5.952053 * nY**3 - 0.1798452 * nY**4 + 0.022174192 * nY**5 + 0.0090316521 * nY**6) / 86400.0
   else:
      nY = (nYear - 1820) / 100
      nCorrection = (-20 + 32 * nY**2) / 86400.0
   return nCorrection
# End Def

def cmMeanTropicalYear (nC: float) -> float:
#
# Mean Interval between Vernal Equinoxes
#
   return 365.2421896698 - (.00000615359 * nC)- (.000000000729 * nC**2) + (.000000000264 * nC**3)
# End Def

def cmEquationOfTime (nMoment: float) -> float:
#
# Equation of Time
#
   nC = cmJulianCenturies(nMoment)
   nLongitude = 280.46645 + 36000.76983 * nC + .0003032 * nC**2
   nAnomaly = 357.52910 + 35999.05030 * nC - 0.0001559 * nC**2 - 0.00000048 * nC**3
   nEccentricity = 0.016708617 - 0.000042037 * nC - 0.0000001236 * nC**2
   nY = cmTangentDegrees(cmObliquity(nC) / 2)**2
   nEquation = 1 / (2 * math.pi) \
             * ((nY * cmSinDegrees(nLongitude * 2)) \
             - (2 * nEccentricity * cmSinDegrees(nAnomaly)) \
             + (4 * nEccentricity * nY * cmSinDegrees(nAnomaly) * cmCoSineDegrees(nLongitude * 2)) \
             - (.5 * nY**2 * cmSinDegrees(nLongitude * 4)) \
             - (1.25 * nEccentricity**2 * cmSinDegrees(nAnomaly * 2)))
   nEquationAdjust = abs(nEquation) if abs(nEquation) < .5 else .5 
   return cmSignum(nEquation) * nEquationAdjust
# End Def

def cmApparentFromLocal (nMoment: float) -> float:
#
# Convert Local time to Apparent
#
   return nMoment + cmEquationOfTime(cmUniversalFromLocal(nMoment,nLongitude))
# End Def

def cmLocalFromApparent (nMoment: float, nLongitude: float) -> float:
#
# Convert Apparent time to Local
#
   return nMoment - cmEquationOfTime(cmUniversalFromLocal(nMoment,nLongitude))
# End Def

def cmZoneFromLongitude (nLongitude: float) -> float:
#
# Local mean time zone changes every 15 degrees. Convert to a fraction of a day.
#
   return nLongitude / 360
# End Def

def cmLocalFromUniversal (nUniversal: float, nLongitude: float) -> float:
#
# Convert Universal Time to Local
#
   return nUniversal  + cmZoneFromLongitude(nLongitude)
# End Def

def cmUniversalFromLocal (nLocal: float, nLongitude: float) -> float:
#
# Convert Local Time to Universal
#
   return nLocal - cmZoneFromLongitude(nLongitude)
# End Def

def cmUniversalFromApparent (nMoment: float, nLongitude: float) -> float:
#
# Convert Apparent time to Universal
#
   return cmUniversalFromLocal(cmLocalFromApparent(nMoment,nLongitude),nLongitude)
# End Def

def cmDynamicalFromUniversal (nUniversal: float) -> float:
#
# Convert Universal Time to Dynamical
#
   return nUniversal + cmEphemerisCorrection(nUniversal)
# End Def

def cmJulianCenturies (nMoment: float) -> float:
#
# Julian Centuries since 2000
#
   return (cmDynamicalFromUniversal(nMoment) - J2000) / 36525
#End Def

def cmMidday (nMoment: float, nLongitude: float) -> float:
#
# True middle of a Solar Day
#
   return cmUniversalFromApparent(nMoment + .5,nLongitude)
# End Def

def cmMiddayInTehran (nDays: int) -> float:
#
# Midday or solar noon in Tehran
#
   return cmMidday(nDays,TehranLocale_Longitude)
# End Def

def cmAberration (nC: float) -> float:
#
# Abberration = Effect of the sun's apparent motion of moving about 20.47 seconds of arc
#               while its light is traveling towards Earth
#
   return (.0000974 * cmCoSineDegrees(177.63 + 35999.01848 * nC)) - .005575
# End Def

def cmNutation (nC: float) -> float:
#
# Nutation = Wobble of the Earth
#
   nC2 = nC**2
   nA = 124.90 - 1934.134 * nC + .002063 * nC2
   nB = 201.11 + 72001.5377 * nC + .00057 * nC2

   return (-.004778 * cmSinDegrees(nA)) - (.0003667 * cmSinDegrees(nB))
# End Def

def cmSumSolarLongitudePeriods (dtC: float, dwX: float, dtY: float, dtZ: float) -> float:
#
# Support for adjustment of solar longitude calculation
#
   return dwX * cmSinDegrees(dtY + (dtZ * dtC))
# End def

def cmSolarLongitude (dtMoment: float) -> float:
#
# Solar Longitude
#
   dtC = cmJulianCenturies(dtMoment)
   dtLongitude = 282.7771834 + 36000.76953744 * dtC \
               + (.000005729577951308232 \
               * (cmSumSolarLongitudePeriods(dtC,403406,270.54861,.9287892) \
               + cmSumSolarLongitudePeriods(dtC,195207,340.19128,35999.1376958) \
               + cmSumSolarLongitudePeriods(dtC,119433,63.91854,35999.4089666) \
               + cmSumSolarLongitudePeriods(dtC,112392,331.2622,35998.7287385) \
               + cmSumSolarLongitudePeriods(dtC,3891,317.843,71998.20261) \
               + cmSumSolarLongitudePeriods(dtC,2819,86.631,71998.4403) \
               + cmSumSolarLongitudePeriods(dtC,1721,240.052,36000.35726) \
               + cmSumSolarLongitudePeriods(dtC,660,310.26,71997.4812) \
               + cmSumSolarLongitudePeriods(dtC,350,247.23,32964.4678) \
               + cmSumSolarLongitudePeriods(dtC,334,260.87,-19.4410) \
               + cmSumSolarLongitudePeriods(dtC,314,297.82,445267.1117) \
               + cmSumSolarLongitudePeriods(dtC,268,343.14,45036.884) \
               + cmSumSolarLongitudePeriods(dtC,242,166.79,3.1008) \
               + cmSumSolarLongitudePeriods(dtC,234,81.53,22518.4434) \
               + cmSumSolarLongitudePeriods(dtC,158,3.5,-19.9739) \
               + cmSumSolarLongitudePeriods(dtC,132,132.75,65928.9345) \
               + cmSumSolarLongitudePeriods(dtC,129,182.95,9038.0293) \
               + cmSumSolarLongitudePeriods(dtC,114,162.03,3034.7684) \
               + cmSumSolarLongitudePeriods(dtC,99,29.8,33718.148) \
               + cmSumSolarLongitudePeriods(dtC,93,266.4,3034.448) \
               + cmSumSolarLongitudePeriods(dtC,86,249.2,-2280.773) \
               + cmSumSolarLongitudePeriods(dtC,78,157.6,29929.992) \
               + cmSumSolarLongitudePeriods(dtC,72,257.8,31556.493) \
               + cmSumSolarLongitudePeriods(dtC,68,185.1,149.588) \
               + cmSumSolarLongitudePeriods(dtC,64,69.9,9037.75) \
               + cmSumSolarLongitudePeriods(dtC,46,8,107997.405) \
               + cmSumSolarLongitudePeriods(dtC,38,197.1,-4444.176) \
               + cmSumSolarLongitudePeriods(dtC,37,250.4,151.771) \
               + cmSumSolarLongitudePeriods(dtC,32,65.3,67555.316) \
               + cmSumSolarLongitudePeriods(dtC,29,162.7,31556.08) \
               + cmSumSolarLongitudePeriods(dtC,28,341.5,-4561.54) \
               + cmSumSolarLongitudePeriods(dtC,27,98.5,1221.655) \
               + cmSumSolarLongitudePeriods(dtC,27,291.6,107996.706) \
               + cmSumSolarLongitudePeriods(dtC,25,146.7,62894.167) \
               + cmSumSolarLongitudePeriods(dtC,24,110,31437.369) \
               + cmSumSolarLongitudePeriods(dtC,21,342.6,-31931.757) \
               + cmSumSolarLongitudePeriods(dtC,21,5.2,14578.298) \
               + cmSumSolarLongitudePeriods(dtC,20,230.9,34777.243) \
               + cmSumSolarLongitudePeriods(dtC,18,256.1,1221.999) \
               + cmSumSolarLongitudePeriods(dtC,17,45.3,62894.511) \
               + cmSumSolarLongitudePeriods(dtC,14,242.9,-4442.039) \
               + cmSumSolarLongitudePeriods(dtC,13,151.8,119.066) \
               + cmSumSolarLongitudePeriods(dtC,13,115.2,107997.909) \
               + cmSumSolarLongitudePeriods(dtC,13,285.3,16859.071) \
               + cmSumSolarLongitudePeriods(dtC,12,53.3,-4.578) \
               + cmSumSolarLongitudePeriods(dtC,10,205.7,-39.127) \
               + cmSumSolarLongitudePeriods(dtC,10,126.6,26895.292) \
               + cmSumSolarLongitudePeriods(dtC,10,85.9,12297.536) \
               + cmSumSolarLongitudePeriods(dtC,10,146.1,90073.778)))
   return cmCalcDegrees(dtLongitude + cmAberration(dtC) + cmNutation(dtC))
# End Def

def cmObliquity (nCenturies: float) -> float:
#
# Obliquity Earth Orbit
#
   return cmAngle(23,26,21.448) - (cmAngle(0,0,46.8150) * nCenturies) - (cmAngle(0,0,0.00059) * nCenturies**2) + (cmAngle(0,0,0.001813) * nCenturies**3)
# End Def

def cmEstimatePriorSolarLongitude (nMoment: float, nLongitude: float) -> float:
#
# Estimation of when solar longitude reaches nLongitude
#
   nRate = cmMeanTropicalYear(cmJulianCenturies(nMoment)) / 360
   nEstimate = nMoment - nRate * cmCalcDegrees((cmSolarLongitude(nMoment) - nLongitude))
   nError = cmCalcDegrees((cmSolarLongitude(nEstimate) - nLongitude + 180)) - 180
   nEstimate = nEstimate - nRate * nError
   if nMoment < nEstimate:
      return nMoment
   else:
      return nEstimate
# End Def

def cmPersianNewYearOnOrBefore (nDays: int) -> int:
#
# Search for Persian New Year on vernal equinox (Around March 21)
#
   nApprox = cmFloor(cmEstimatePriorSolarLongitude(cmMiddayInTehran(nDays),SPRING))
   while cmSolarLongitude(cmMiddayInTehran(nApprox)) > SPRING + 2:
      nApprox = nApprox + 1
   return nApprox
# End Def

def DaysFromPersian (nMonth: int, nDay: int, nYear: int) -> int:
#
# Given a Persian Date, return Days Date
#
   if 0 < nYear:
      nYearAdjusted = nYear - 1
   else:
    nYearAdjusted = nYear
   nDays = cmPersianNewYearOnOrBefore(PERSIAN_EPOCH + 180 + cmFloor(cmMeanTropicalYear(0) * nYearAdjusted))
   if nMonth <= MEHR:
      nDayAdjusted = 31
      nExtraDays = 0
   else:
      nDayAdjusted = 30
      nExtraDays = 6
   return nDays - 1 + (nDayAdjusted * (nMonth - 1)) + nExtraDays + nDay
# End Def

def PersianFromDays (nDays: int):
#
# Given a Days date, return Persian Date
#
   nNewYear = cmPersianNewYearOnOrBefore(nDays)
   nYear = cmRound((nNewYear - PERSIAN_EPOCH) / (cmMeanTropicalYear(0)) + 1)
   if 0 > nYear:
      nYear = nYear + 1
   nDayOfYear = nDays - DaysFromPersian(FARVARDIN,1,nYear) + 1
   if nDayOfYear <= 186:
      nMonth = cmCeiling(nDayOfYear / 31)
   else:
      nMonth = cmCeiling((nDayOfYear - 6) / 30)
   nDay = nDays - DaysFromPersian(nMonth,1,nYear) + 1
   PersianDate = []
   PersianDate.append(nMonth)
   PersianDate.append(nDay)
   PersianDate.append(nYear)
   return PersianDate
# End Def

def cmPersianYear (nGregorianYear: int) -> int:
#
# Given a Gregorian year, return the Persian year equivalent
#
   nPersianYear = nGregorianYear - 621
#
# Compensate for the lack of year 0 on the Persian calendar
# We can still be off a year if Persian Month is >= 10
   if nPersianYear <= 0:
      return nPersianYear - 1
   else:
      return nPersianYear
# End Def

def PersianDateCalculation (nMonth: int, nDay: int, nGregorianYear: int) -> date:
#
# Return Persian dates occurring in a given Gregorian year
#
   nPersianYear = cmPersianYear(nGregorianYear)
   nJan1 = date(nGregorianYear,January,1).toordinal()
   nDec31 = date(nGregorianYear,December,31).toordinal()
#
# Calculate the Persian Date
#
   nCalcDays = DaysFromPersian(nMonth,nDay,nPersianYear)
   if nCalcDays < nJan1:
      nCalcDays = DaysFromPersian(nMonth,nDay,nPersianYear + 1)
   else:
      if nCalcDays > nDec31:
         nCalcDays = DaysFromPersian(nMonth,nDay,nPersianYear - 1)
   return date.fromordinal(nCalcDays)
# End Def

pyNow = CurrentDate()
#pyNow = date(2025,10,31)
print ('Today Local: ' + str(pyNow))
nDays = pyNow.toordinal()
print ("Today's Local Ordinal Days: " + str(nDays))
PersianDate = PersianFromDays(nDays)
print ('Persian Date: ' + PersianMonthNames[PersianDate[0] - 1] + ' ' + str(PersianDate[1]) + ', ' + str(PersianDate[2]))
print ('Days from Persian: ' + str(DaysFromPersian(PersianDate[0],PersianDate[1],PersianDate[2])))
print ('')
print ('Persian Holidays during Gregorian Year ' + str(pyNow.year))
print ('')
i = 0
while i < len(PersianHolidaysList):
   print (PersianHolidaysList[i] + ': ' + str(PersianDateCalculation(PersianHolidaysList[i + 1],PersianHolidaysList[i + 2],pyNow.year)))      
   i = i + 3


