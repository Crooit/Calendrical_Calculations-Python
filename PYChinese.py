########################################################################################
# File: PYChinese.py
# Contents: Chinese calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025--05-02
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################

#
# Chinese Calendrical Calculations
#

import math
from datetime import date, datetime, timezone
import pytz

# Global Variables

CHINESE_EPOCH = -963099   # Feb 15 -2636
#
# Country to base calculations on
#
CHINESE = 0
VIETNAMESE = 1
KOREAN = 2
JAPANESE = 3

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
CHINESE_WIDOW_YEAR = 0
CHINESE_BLIND_YEAR = 1
CHINESE_BRIGHT_YEAR = 2
CHINESE_DOUBLE_BRIGHT_YEAR = 3
CHINESE_MONTH_NAME_EPOCH = 57
NO_RULES = 0
CHINESE_WINTERSOLSTICE = 1
CHINESE_QINGMING = 2


# Astronomical definitions

SPRING = 0
SUMMER = 90
AUTUMN = 180
WINTER = 270
J2000 = 730120.5   # January 1, 2000 at noon
MeanSynodicMonth = 29.530588861   # Mean time from new moon to new moon

# Description Lists

ChineseCountry = ['China','Vietnam','Korea','Japan']
YearAnimal = ['Rat','Ox','Tiger','Rabbit','Dragon','Snake','Horse','Goat','Monkey','Rooster','Dog','Pig']
#
# Chinese Leap Months do not have names
#
MonthNames = ['Zi Rat','Chou Ox','Yin Tiger','Mao Rabbit','Chen Dragon','Si Snake','Wu Horse','Wei Sheep','Shen Monkey','You Rooster','Xu Dog','Hai Pig']
YearAugury = ['Widow Year','Blind Year','Bright Year','Double Bright Year']
#
# Name, Chinese Month, Chinese Day, Rule to use
#
ChineseHolidaysList = [
   'Chinese New Year',1,1,NO_RULES,
   'Lantern Festival',1,15,NO_RULES,
   'Blue Dragon Festival',2,2,NO_RULES,
   'Ching Ming Festival',0,0,CHINESE_QINGMING,
   'Shangsi Festival',3,3,NO_RULES,
   'Qixi Festival',7,7,NO_RULES,
   'Ghost Festival',7,15,NO_RULES,
   'Mid Autumn Festival',8,15,NO_RULES,
   'Double Nine Festival',9,9,NO_RULES,
   'Spirit Festival',10,15,NO_RULES,
   'Winter Solstice',0,0,CHINESE_WINTERSOLSTICE,
   'Laba Festival',12,8,NO_RULES,
]

def CurrentDate () -> date:
#
# Retrieve the current date
#
   return date.today()
# End Def

def cmGregorianYearFromDays (nDays: int) -> int:
#
# Given a Days date, return the gregorian year
#
   pyDate = date.fromordinal(nDays)
   return pyDate.year
# End Def

def cmGregorianDateDifference (nStartMonth: int, nStartDay: int, nStartYear: int, nEndMonth: int, nEndDay: int, nEndYear: int) -> int:
#
# Calculate the difference in days between two Gregorian dates
#
   return date(nEndYear, nEndMonth, nEndDay).toordinal() - date(nStartYear, nStartMonth, nStartDay).toordinal()
# End Def

def cmTimeZoneOffset (ntimezone: str) -> float:
#
# Get ntimezone offset in hours
#
   utcNow = datetime.now(timezone.utc)
   utcTime = datetime(utcNow.year,utcNow.month,utcNow.day,utcNow.hour,utcNow.minute,0)
   tz = pytz.timezone(str(ntimezone))
#
# Localising the datetime object to the timezone
#
   zoneAware = tz.localize(utcTime)
   nOffset = zoneAware.utcoffset()
   nOffsetSeconds = nOffset.total_seconds()
   return nOffsetSeconds / 3600
# End Def

def cmChineseLocation (nMoment: float, nCountry: int) -> float:
#
# Determine zone hours based on country option
#
   nDays = cmFloor(nMoment) 
   nYear = cmGregorianYearFromDays(nDays)
   if nCountry == VIETNAMESE:
      if nDays < date(1968,January,1).toordinal():
         return 8
      else:
         return cmTimeZoneOffset('Asia/Saigon')
   elif nCountry == KOREAN:
      if nDays < date(1908,April,1).toordinal():
         return 8.4644444444
      elif nDays < date(1912,January,12).toordinal():
         return 8.5
      elif nDays < date(1954,March,21).toordinal():
         return 9
      elif nDays < date(1961,August,10).toordinal():
         return 8.5
      else:
         return cmTimeZoneOffset('Asia/Seoul')
   elif nCountry == JAPANESE:
      if nYear < 1888:
         return 9.3177777778
      else:
         return cmTimeZoneOffset('Asia/Tokyo')
#
# Default is CHINESE
#
   else:
      if nYear < 1929:
         return 1397 / 180
      else:
         return cmTimeZoneOffset('Asia/Shanghai')
# End Def

def cmMeanTropicalYear (nC: float) -> float:
#
# Mean Interval between Vernal Equinoxes
#
   return 365.2421896698 - (.00000615359 * nC)- (.000000000729 * nC**2) + (.000000000264 * nC**3)
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

def cmDynamicalFromUniversal (nUniversal: float) -> float:
#
# Convert Universal Time to Dynamical
#
   return nUniversal + cmEphemerisCorrection(nUniversal)
# End Def

def cmUniversalFromDynamical (nDynamical: float) -> float:
#
# Convert Dynamical Time to Universal
#
   return nDynamical - cmEphemerisCorrection(nDynamical)
# End Def

def cmUniversalFromStandard (nStandard: float, nZone: float) -> float:
#
# Convert Standard Time to Universal
#
   return nStandard - nZone / 24
# End Def

def cmStandardFromUniversal (nUniversal: float, nZone: float) -> float:
#
# Convert Universal Time to Standard
#
   return nUniversal + nZone / 24
# End Def

def cmJulianCenturies (nMoment: float) -> float:
#
# Julian Centuries since 2000
#
   return (cmDynamicalFromUniversal(nMoment) - J2000) / 36525
#End Def

def cmMod (x: float, y: float) -> float:
#
# x MOD y for Real Numbers, y<>0
#
   return x % y
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

def cmAMod (x: float, y: float) -> float:
#
# Variation of x MOD y for Real Numbers adjusted so that the modulus
# of a multiple of the divisor is the divisor itself rather than zero.
# 
# If x MOD y = 0 then result is adjusted to y
#
   return x - y * (cmCeiling(x / y) - 1)
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

def cmMeanLunarLongitude (nC: float) -> float:
#
# Mean Lunar Longitude
#
   return cmCalcDegrees(218.3164477 + 481267.88123421 * nC - .0015786 * nC**2 + (nC**3 / 538841) - (nC**4 / 65194000))
# End Def

def cmSolarAnomaly (nC: float) -> float:
#
# Solar Anomaly
#
   return cmCalcDegrees(357.5291092 + 35999.0502909 * nC - .0001536 * nC**2 + (nC**3 / 24490000))
# End Def

def cmLunarAnomaly (nC: float) -> float:
#
# Lunar Anomaly
#
   return cmCalcDegrees(134.9633964 + 477198.8675055 * nC + .0087414 * nC**2 + (nC**3 / 69699) - (nC**4 / 14712000))
# End Def

def cmMoonNode (nC: float) -> float:
#
# Moon Node
#
   return cmCalcDegrees(93.2720950 + 483202.0175233 * nC - .0036539 * nC**2 - (nC**3 / 3526000) + (nC**4 / 863310000))
# End Def

def cmLunarElongation (nC: float) -> float:
#
# Lunar Elongation
#
   return cmCalcDegrees(297.8501921 + 445267.1114034 * nC - .0018819 * nC**2 + (nC**3 / 545868) - (nC**4 / 113065000))
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

def cmSumLunarPeriods (nE: float, nElongation: float, nSolarAnomaly: float, nLunarAnomaly: float, nMoonFromNode: float, nV: float, nW: float, nX: float, nY: float, nZ: float) -> float:
#
# Adjustments for Longitude of the Moon
#
   return nV * nE**abs(nX) * cmSinDegrees((nW * nElongation) + (nX * nSolarAnomaly) + (nY * nLunarAnomaly) + (nZ * nMoonFromNode))
# End Def

def cmLunarLongitude (nMoment: float) -> float:
#
# Return the Longitude of the Moon
#
   nC = cmJulianCenturies(nMoment)
   nMeanMoon = cmMeanLunarLongitude(nC)
   nElongation = cmLunarElongation(nC)
   nSolarAnomaly = cmSolarAnomaly(nC)
   nLunarAnomaly = cmLunarAnomaly(nC)
   nMoonFromNode = cmMoonNode(nC)
   nE = 1 - .002516 * nC - .0000074 * nC**2
   nVenus = .003958  * cmSinDegrees(119.75 + (nC * 131.849))
   nJupiter = .000318 * cmSinDegrees(53.09 + (nC * 479264.29))
   nFlatEarth = .001962 * cmSinDegrees(nMeanMoon - nMoonFromNode)
   nCorrection = cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,6288774,0,0,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,658314,2,0,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-185116,0,1,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,58793,2,0,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,53322,2,0,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-40923,0,1,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-30383,0,1,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-12528,0,0,1,2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,10675,4,0,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,8548,4,0,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-6766,2,1,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,4987,1,1,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,3994,2,0,2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,3665,2,0,-3,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2602,2,0,-1,2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2348,1,0,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2120,0,1,2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2048,2,-2,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1595,2,0,0,2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1110,0,0,2,2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-810,2,1,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-713,0,2,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,691,2,1,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,549,4,0,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,520,4,-1,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-399,2,1,0,-2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,351,1,1,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,330,4,0,-3,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-323,0,2,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,294,2,0,3,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,1274027,2,0,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,213618,0,0,2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-114332,0,0,0,2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,57066,2,-1,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,45758,2,-1,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-34720,1,0,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,15327,2,0,0,-2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,10980,0,0,1,-2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,10034,0,0,3,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-7888,2,1,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-5163,1,0,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,4036,2,-1,1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,3861,4,0,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2689,0,1,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2390,2,-1,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2236,2,-2,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2069,0,2,0,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1773,2,0,1,-2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,1215,4,-1,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-892,3,0,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,759,4,-1,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-700,2,2,-1,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,596,2,-1,0,-2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,537,0,0,4,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-487,1,0,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-381,0,0,2,-2) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-340,3,0,-2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,327,2,-1,2,0) \
               + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,299,1,1,-1,0)
   nCorrection = .000001 * nCorrection
   return cmCalcDegrees(nMeanMoon + nCorrection + nVenus + nJupiter + nFlatEarth + cmNutation(nC))
# End Def

def cmMidnightInChina (nMoment: float, nCountry: int) -> float:
#
# Chinese Midnight in Universal Time
#
   return cmUniversalFromStandard(nMoment,cmChineseLocation(nMoment,nCountry))
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

def cmChineseWinterSolsticeOnOrBefore (nDays: int, nCountry: int) -> int:
#
# Date of Winter Solstice on or before nMoment
#
   nSolstice = cmEstimatePriorSolarLongitude(nDays,WINTER)
   nLoop = True
   while nLoop == True:
      if WINTER > cmSolarLongitude(cmMidnightInChina(cmFloor(nSolstice) + 1,nCountry)):
         nSolstice = nSolstice + 1
      else:
         nLoop = False
   return cmFloor(nSolstice)
# End Def
def cmCorrectionAdjustments (dtE: float, dtSolarAnomaly: float, dtLunarAnomaly: float, dtMoonArgument: float, dtV: float, dtW: float, dtX: float, dtY: float, dtZ: float) -> float:
#
# nth New Moon Adjustments
#
   return dtV * dtE**dtW * cmSinDegrees((dtX * dtSolarAnomaly) + (dtY * dtLunarAnomaly) + (dtZ * dtMoonArgument))
# End Def

def cmAdditionalAdjustments (stK: float, stI: float, stJ: float, stL: float) -> float:
#
# nth New Moon Additional Adjustments
#
   return stL * cmSinDegrees(stI + stJ * stK)
# End Def

def cmNthNewMoon (nNthMoon: int) -> float:
#
# Moment (at Greenwich) of nth new moon after (or before if nNthMoon is negative)
# the new moon of January 11, 1.
#
   nK = nNthMoon - 24724
   nC = nK / 1236.85
   nC2 = nC**2
   nC3 = nC**3
   nC4 = nC**4
   nApprox = J2000 + 5.09766 + MeanSynodicMonth * 1236.85 * nC + .00015437 * nC2 - .000000150 * nC3 + .00000000073 * nC4
   nE = 1.0 - .002516 * nC - .0000074 * nC2
   nSolarAnomaly = 2.5534 + 29.10535670 * 1236.85 * nC - .0000014 * nC2 - .00000011 * nC3
   nLunarAnomaly = 201.5643 + 385.81693528 * 1236.85 * nC + .0107582 * nC2 + .00001238 * nC3 - .000000058 * nC4
   nMoonArgument = 160.7108 + 390.67050284 * 1236.85 * nC - .0016118 * nC2 - .00000227 * nC3 + .000000011 * nC4
   nOmega = 124.7746 + (-1.56375588 * 1236.85 * nC) + .0020672 * nC2 + .00000215 * nC3
   nCorrection = -.00017 * cmSinDegrees(nOmega) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.40720,0,0,1,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.01608,0,0,2,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00739,1,-1,1,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00208,2,2,0,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00057,0,0,1,2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00042,0,0,3,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00038,1,1,0,-2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00007,0,2,1,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00004,0,3,0,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00003,0,0,2,2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00003,0,-1,1,2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00002,0,1,3,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.17241,1,1,0,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.01039,0,0,0,2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00514,1,1,1,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00111,0,0,1,-2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00056,1,1,2,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00042,1,1,0,2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00024,1,-1,2,0) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00004,0,0,2,-2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00003,0,1,1,-2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00003,0,1,1,2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,-.00002,0,-1,1,-2) \
               + cmCorrectionAdjustments(nE,nSolarAnomaly,nLunarAnomaly,nMoonArgument,.00002,0,0,4,0)
   nExtra = .000325 * cmSinDegrees(299.77 + 132.8475848 * nC - .009173 * nC2)
   nAdditional = cmAdditionalAdjustments(nK,251.88,.016321,.000165) \
               + cmAdditionalAdjustments(nK,349.42,36.412478,.000126) \
               + cmAdditionalAdjustments(nK,141.74,53.303771,.000062) \
               + cmAdditionalAdjustments(nK,154.84,7.30686,.000056) \
               + cmAdditionalAdjustments(nK,207.19,.121824,.000042) \
               + cmAdditionalAdjustments(nK,161.72,24.198154,.000037) \
               + cmAdditionalAdjustments(nK,331.55,3.592518,.000023) \
               + cmAdditionalAdjustments(nK,251.83,26.651886,.000164) \
               + cmAdditionalAdjustments(nK,84.66,18.206239,.00011) \
               + cmAdditionalAdjustments(nK,207.14,2.453732,.00006) \
               + cmAdditionalAdjustments(nK,34.52,27.261239,.000047) \
               + cmAdditionalAdjustments(nK,291.34,1.844379,.000040) \
               + cmAdditionalAdjustments(nK,239.56,25.513099,.000035)
   return cmUniversalFromDynamical(nApprox + nCorrection + nExtra + nAdditional)
# End Def

def cmLunarPhase (nMoment: float) -> float:
#
# Lunar Phase
#
# Includes check if the phase obtained by the difference between
# lunar and solar longitudes conflicts with the time of the new
# moon as calculated by the more precise cmNthNewMoon function.
#
# If it does, then an approximation based on cmNthNewMoon is
# preferred.
#
   nLongitudeDifference = cmCalcDegrees(cmLunarLongitude(nMoment) - cmSolarLongitude(nMoment))
   nNthNewMoon = cmNthNewMoon(0)
   nMeanSynodic = cmFloor(cmRound((nMoment - nNthNewMoon) / MeanSynodicMonth))
   nPreferred = cmMod((nMoment - cmNthNewMoon(nMeanSynodic)) / MeanSynodicMonth,1) * 360
   if abs(nLongitudeDifference - nPreferred) > 180:
      return nPreferred
   else:
      return nLongitudeDifference
# End Def

def cmNewMoonAfter (nMoment: float) -> float:
#
# Return New Moon following nMoment
#
# There are slight differences between the approximations
# used by cmNthNewMoon and cmLunarPhase (which in turn uses
# cmSolarLongitude and cmLunarLongitude) which lead to rare
# occasions (i.e. year 2481) when nMoment is very close to
# the time of a new moon which are addressed.
#
   nN0 = cmNthNewMoon(0)
   nLunarPhase = cmLunarPhase(nMoment)
#
# To ensure independence of the phase at the R.D. epoch,
# also subtract from nMoment the moment nN0 of the first
# new moon after R.D. 0.
#
   nNthMoon = cmFloor(cmRound(((nMoment - nN0) / MeanSynodicMonth) - (nLunarPhase / 360)))
   if nLunarPhase < 2 and cmNthNewMoon(nNthMoon) > nMoment:
      nNewMoon = cmNthNewMoon(nNthMoon)
   else:
      if nLunarPhase > 358 and cmNthNewMoon(nNthMoon + 1) <= nMoment:
         nNewMoon = cmNthNewMoon(nNthMoon + 2)
      else:
         nNewMoon = cmNthNewMoon(nNthMoon + 1)
   return nNewMoon
# End Def

def cmChineseNewMoonOnOrAfter (nMoment: float, nCountry: int) -> int:
#
# Date of the first new moon on or after nMoment
#
   nNewMoon = cmNewMoonAfter(cmMidnightInChina(nMoment,nCountry))
   return cmFloor(cmStandardFromUniversal(nNewMoon,cmChineseLocation(nNewMoon,nCountry)))
# End Def

def cmNewMoonBefore (nMoment: float) -> float:
#
# Return New Moon preceding nMoment
#
# There are slight differences between the approximations
# used by cmNthNewMoon and cmLunarPhase (which in turn uses
# cmSolarLongitude and cmLunarLongitude) which lead to rare
# occasions (i.e. year 2481) when nMoment is very close to
# the time of a new moon which are addressed.
#
   nN0 = cmNthNewMoon(0)
   nLunarPhase = cmLunarPhase(nMoment)
#
# To ensure independence of the phase at the R.D. epoch,
# also subtract from nMoment the moment nN0 of the first
# new moon after R.D. 0.
#
   nNthMoon = cmRound(((nMoment - nN0) / MeanSynodicMonth) - (nLunarPhase / 360))
   if nLunarPhase < 2 and cmNthNewMoon(nNthMoon) > nMoment:
      nNewMoon = cmNthNewMoon(nNthMoon - 1)
   else:
      if nLunarPhase > 358 and cmNthNewMoon(nNthMoon + 1) <= nMoment:
         nNewMoon = cmNthNewMoon(nNthMoon + 1)
      else:
         nNewMoon = cmNthNewMoon(nNthMoon)
   return nNewMoon
# End Def

def cmChineseNewMoonBefore (nMoment: float, nCountry: int) -> int: 
#
# Date of the first new moon before nMoment
#
   nNewMoon = cmNewMoonBefore(cmMidnightInChina(nMoment,nCountry))
   return cmFloor(cmStandardFromUniversal(nNewMoon,cmChineseLocation(nNewMoon,nCountry)))
# End Def

def cmCurrentMajorSolarTerm (nMoment: float, nCountry: int) -> int:
#
# Last Chinese major solar term (zhongqi) index before nMoment
#
   nLongitude = cmSolarLongitude(cmUniversalFromStandard(nMoment,cmChineseLocation(nMoment,nCountry)))
   return cmAMod(2 + cmFloor(nLongitude / 30),12)
# End Def

def cmChineseNoMajorSolarTerm (nDays: int, nCountry: int) -> bool:
#
# Returns TRUE if Chinese lunar month starting on nDays
# has no major solar term FALSE otherwise
#
   if cmCurrentMajorSolarTerm(nDays,nCountry) == cmCurrentMajorSolarTerm(cmChineseNewMoonOnOrAfter(nDays + 1,nCountry),nCountry):
      return True
   else:
      return False
# End Def

def cmCurrentMinorSolarTerm (nMoment: float, nCountry: int) -> int:
#
# Last Chinese minor solar term (jieqi) index before nMoment
#
   nLongitude = cmSolarLongitude(cmUniversalFromStandard(nMoment,cmChineseLocation(nMoment,nCountry)))
   return cmAMod(3 + cmFloor((nLongitude - 15) / 30),12)
# End Def

def cmChineseNewYearInSui (nDays: int, nCountry: int) -> int:
#
# Return first day of Chinese year for the sui containing nDays
#
   nS1 = cmChineseWinterSolsticeOnOrBefore(nDays,nCountry)
   nS2 = cmChineseWinterSolsticeOnOrBefore(nS1 + 370,nCountry)
   nM12 = cmChineseNewMoonOnOrAfter(nS1 + 1,nCountry)
   nM13 = cmChineseNewMoonOnOrAfter(nM12 + 1,nCountry)
   nNextM11 = cmChineseNewMoonBefore(nS2 + 1,nCountry)
   nNewYear = cmChineseNewMoonOnOrAfter(nM13 + 1,nCountry)
   if cmRound((nNextM11 - nM12) / MeanSynodicMonth) == 12:
      if cmChineseNoMajorSolarTerm(nM12,nCountry) == True or cmChineseNoMajorSolarTerm(nM13,nCountry) == True:
         nNewYear = cmChineseNewMoonOnOrAfter(nM13 + 1,nCountry)
      else: 
         nNewYear = nM13
   else:
      nNewYear = nM13
   return nNewYear
# End Def

def cmChineseNewYearOnOrBefore (nDays: int, nCountry: int) -> int: 
#
# Find Chinese new year on or before nDays
#
   nNewYear = cmChineseNewYearInSui(nDays,nCountry)
   if nDays < nNewYear:
      nNewYear = cmChineseNewYearInSui(nDays - 180,nCountry)
   return nNewYear
# End Def

def cmChinesePriorLeapMonth (nMPrime: int, nM: int, nCountry: int) -> bool:
#
# Returns True if there is a Chinese leap month at or after lunar
# month nMPrime and at or before lunar month nM
#
   nMLoop = nM
   nReturn = False
   if nMLoop >= nMPrime:
      bLoop = True
      while bLoop == True:
         nReturn = cmChineseNoMajorSolarTerm(nMLoop,nCountry)
         if nReturn == True:
            bLoop = False
         else:
            nMLoop = cmChineseNewMoonBefore(nMLoop,nCountry)
            if nMLoop < nMPrime:
               bLoop = False
   return nReturn
# End Def

def cmChineseFromDays (nDays: int,nCountry):
#
# Given days date nDays, return the Chinese equivalent
#
   ChineseDate = []
   nS1 = cmChineseWinterSolsticeOnOrBefore(nDays,nCountry)
   nM12 = cmChineseNewMoonOnOrAfter(nS1 + 1,nCountry)
   nM = cmChineseNewMoonBefore(nDays + 1,nCountry)
   nS2 = cmChineseWinterSolsticeOnOrBefore(nS1 + 370,nCountry)
   nNextM11 = cmChineseNewMoonBefore(nS2 + 1,nCountry)
   if cmRound((nNextM11 - nM12) / MeanSynodicMonth) == 12:
      bLeapYear = True
   else:
      bLeapYear = False
   nMonth = cmRound((nM - nM12) / MeanSynodicMonth)
   if bLeapYear == True and cmChinesePriorLeapMonth(nM12,nM,nCountry) == True:
      nMonth = nMonth - 1
   nMonth = cmAMod(nMonth,12)
   if bLeapYear == True and cmChineseNoMajorSolarTerm(nM,nCountry) == True and cmChinesePriorLeapMonth(nM12,cmChineseNewMoonBefore(nM,nCountry),nCountry) == False:
      bLeapMonth = True
   else:
      bLeapMonth = False
   nElaspedYears = cmFloor(1.5 - (nMonth / 12) + ((nDays - CHINESE_EPOCH) / 365.242189))
   nCycle = cmFloor((nElaspedYears - 1) / 60) + 1
   nYear = cmAMod(nElaspedYears,60)
   nDay = nDays - nM + 1
   ChineseDate.append(nCycle)
   ChineseDate.append(nYear)
   ChineseDate.append(bLeapYear)
   ChineseDate.append(nMonth)
   ChineseDate.append(bLeapMonth)
   ChineseDate.append(nDay)
   ChineseDate.append(nCountry)
   return ChineseDate
# End Def

def cmDaysFromChinese (nCycle: int, nYear: int, nMonth: int, bLeapMonth: bool, nDay: int, nCountry: int) -> int:
#
# Given Chinese date, return the days equivalent
#
   nMidYear = cmFloor(CHINESE_EPOCH + ((nCycle - 1) * 60 + nYear - 1 + .5) * 365.242189)
   nNewYear = cmChineseNewYearOnOrBefore(nMidYear,nCountry)
   nNextNewMoon = cmChineseNewMoonOnOrAfter(nNewYear + ((nMonth - 1) * 29),nCountry)
   ChineseDate = cmChineseFromDays(nNextNewMoon,nCountry)
   if ChineseDate[3] == nMonth and ChineseDate[4] == bLeapMonth:
      nPriorNewMoon = nNextNewMoon
   else:
      nPriorNewMoon = cmChineseNewMoonOnOrAfter(nNextNewMoon + 1,nCountry)
   return nPriorNewMoon + nDay - 1
# End Def

def cmChineseYearMarriageAuguries (nCycle: int, nYear: int, nCountry: int) -> int:
#
# Chinese Marriage Auguries
#
# Chinese years that do not contain the minor term Beginning of Spring (Lichun) are widow years
# Chinese years that contain Beginning of Spring at both the beginning and the end
#    of the year are double bright years
# Chinese years missing the first Beginning of Spring but contain it at the end
#    of the year are blind years
# Chinese years that contain the first Beginning of Spring but do not have it at the end
#    of the year are bright years
#
# Chinese tradition deems it unlucky to be married in a widow year
#

   nNewYear = cmDaysFromChinese(nCycle,nYear,1,False,1,nCountry)
   if nYear != 60:
      nNextCycle = nCycle
      nNextYear = nYear + 1
   else:
      nNextCycle = nCycle + 1
      nNextYear = nYear 
   nNextNewYear = cmDaysFromChinese(nNextCycle,nNextYear,1,False,1,nCountry)
   nFirstTerm = cmCurrentMinorSolarTerm(nNewYear,nCountry)
   nNextTerm = cmCurrentMinorSolarTerm(nNextNewYear,nCountry)
   if nFirstTerm == 1:
      if nNextTerm == 12:
         nAugury = CHINESE_WIDOW_YEAR
      else:
         nAugury = CHINESE_BLIND_YEAR
   else:
      if nNextTerm == 12:
         nAugury = CHINESE_BRIGHT_YEAR
      else:
         nAugury = CHINESE_DOUBLE_BRIGHT_YEAR
   return nAugury
# End Def

def cmChineseSexagesimalName (nYear: int) -> int:
#
# Find the nth name of the sexagenary cycle of year and month names
#
  return cmAMod(cmAMod(nYear,12),10)
# End Def

def cmChineseYearName (nYear: int) -> int:
#
# Chinese Year Name
#
   return cmChineseSexagesimalName(nYear)
# End Def

def cmChineseMonthName (nMonth: int, nYear: int) -> int:
#
# Chinese Month Name
#
   return cmChineseSexagesimalName((12 * (nYear - 1) + nMonth - 1) - CHINESE_MONTH_NAME_EPOCH)
# End Def

def FormatChineseDate (ChineseDate) -> str:
#
# Using the ChineseDate list return a formatted string
#
   sCountry = ChineseCountry[ChineseDate[6]]
   sAHYear = str((ChineseDate[0] * 60) + ChineseDate[1]) + ' AH'
   sYearName = YearAnimal[cmChineseYearName(ChineseDate[1]) -1]
   if ChineseDate[4] == False:
      sMonthName = '(' + MonthNames[cmChineseMonthName(ChineseDate[3],ChineseDate[1]) -1] + ')'
   else:
      sMonthName = ''
   sYear = str(ChineseDate[1])
   if ChineseDate[2] == True:
      sYear = sYear + ".Leap "
   sMonth = str(ChineseDate[3])
   if ChineseDate[4] == True:
      sMonth = sMonth + ".Leap "
   sYear = sYear + '(' + YearAnimal[cmChineseYearName(ChineseDate[1]) -1] + ',' + YearAugury[cmChineseYearMarriageAuguries(ChineseDate[0],ChineseDate[1],ChineseDate[6])]
   return sCountry + ': ' + sAHYear + ' Cycle ' + str(ChineseDate[0]) + ' Year ' + sYear + ') Month ' + sMonth + ' (' + MonthNames[cmChineseMonthName(ChineseDate[3],ChineseDate[1]) -1] + ') Day ' + str(ChineseDate[5])
# End Def

def cmSolarLongitudeAfter (nMoment: float, nTargetLongitude: float) -> float:
#
# Solar Longitude after a given moment
#
# Given date/time moment, this routine will calculate the next
# solar event within a longitutinal limitation. Typical solar events
# are the equinoxes and solstices.
#
# Vernal (spring) equinox 0 solar longitude on or about March 21
# Summer solstice 90 solar longitude on or about June 21
# Autumnal (fall) equinox 180 solar longitude on or about September 23
# Winter solstice 270 solar longitude on or about December 22.
#
# The basic strategy is to take the moment and number of degrees and
# search for the moment when next the longitude of the sun is a multiple of
# the given degrees. The search is a bisection within an interval beginning
# 5 days before our estimate or nMoment whichever is earlier and
# ending long enough past nMoment to insure that the sun passes through
# exactly one multiple of nTargetLongitude. The process terminates when the
# time is ascertained within one hundred-thousandth of a day (about 0.9 seconds).
# The discontinuity from 360 to 0 degress is taken into account.
#
# Calculate upper part of bisection interval
#
   nEndMoment = nMoment \
              + (cmMeanTropicalYear(cmJulianCenturies(nMoment)) / 360) \
              * cmCalcDegrees(((nTargetLongitude - cmSolarLongitude(nMoment))))
   if nMoment > nEndMoment - 5:
      nStartMoment = nEndMoment
   else:
      nStartMoment = nMoment
   nEndMoment = nEndMoment + 5
   nSearch =  True
   while nSearch == True:
      nNewMoment = nStartMoment + ((nEndMoment - nStartMoment) * .5)
      nNewLongitude = cmCalcDegrees(cmSolarLongitude(nNewMoment) - nTargetLongitude)
      if nNewLongitude < 180:
         nEndMoment = nNewMoment
      else:
         nStartMoment = nNewMoment
      if (nEndMoment - nStartMoment) < .00001:
         nSearch = False
   return nStartMoment + ((nEndMoment - nStartMoment) * .5)
# End Def

def cmChineseSolarLongitudeOnOrAfter (nMoment: float, nSolarTerm: int, nCountry: int) -> float: 
#
#  Moment of the first date on or after nMoment when the solar longitude is a multiple of
#  nSolarTerm degrees
#
   nZone = cmChineseLocation(nMoment,nCountry)
   nLongitude = cmSolarLongitudeAfter(cmUniversalFromStandard(nMoment,nZone),nSolarTerm)
   return cmStandardFromUniversal(nLongitude,nZone)
# End Def

def cmMinorSolarTermOnOrAfter (nMoment: float, nCountry: int) -> float: 
#
# Date Chinese minor solar term (jieqi) on or after nMoment
#
   nSolarTerm = cmCalcDegrees(30 * cmCeiling((cmSolarLongitude(cmMidnightInChina(nMoment,nCountry)) - 15) / 30) + 15)
   return cmChineseSolarLongitudeOnOrAfter(nMoment,nSolarTerm,nCountry)
# End Def

def cmChineseDateCalculation (nMonth: int, nDay: int, nGregorianYear: int, nRule, nCountry: int) -> int: 
#
# Return Chinese dates occurring in a given Gregorian year
# Chinese holidays never occur in a leap month so we can default FALSE
#
# If we have a special rule, we can guarantee finding it within a gregorian year
#
# If Chinese holiday doesn't occur in gregorian year, return 0
#
   if nRule == CHINESE_WINTERSOLSTICE:
      return cmChineseWinterSolsticeOnOrBefore(date(nGregorianYear,December,30).toordinal(),nCountry)
   if nRule == CHINESE_QINGMING:
      return cmFloor(cmMinorSolarTermOnOrAfter(date(nGregorianYear,March,30).toordinal(),nCountry))
   nElaspedYears = nGregorianYear + 2637
   nCycle = cmFloor((1 / 60) * (nElaspedYears - 1)) + 1
   nChineseYear = cmAMod(nElaspedYears,60)
   nJan1 = date(nGregorianYear,January,1).toordinal()
   nDec31 = date(nGregorianYear,December,31).toordinal()
   nCalcDays = cmDaysFromChinese(nCycle,nChineseYear,nMonth,False,nDay,nCountry)
#
# Check if Chinese date occurs during nGregorianYear
#
   if nCalcDays < nJan1 or nCalcDays > nDec31:
      nElaspedYears = nGregorianYear + 2637 - 1
      nCycle = cmFloor((1 / 60) * (nElaspedYears - 1)) + 1
      nChineseYear = cmAMod(nElaspedYears,60)
      nCalcDays = cmDaysFromChinese(nCycle,nChineseYear,nMonth,False,nDay,nCountry)
      if nCalcDays < nJan1 or nCalcDays > nDec31:
         nCalcDays = 0
   return nCalcDays
# End Def

def ChineseHolidayCalculation (nMonth: int, nDay: int, nGregorianYear: int, nRule: int, nCountry: int):
#
# Calculate a Chinese Holiday occurring in nGregorianYear
#
   ChineseHoliday = []
   nDays = cmChineseDateCalculation (nMonth,nDay,nGregorianYear,nRule,nCountry)
#
# Return empty list is holiday did not occur in nGregorianYear
#
   if nDays != 0:
      ChineseHoliday.append(date.fromordinal(nDays))
   return ChineseHoliday
# End Def

#
# Chinese Date List
#
#   Cycle
#   Year
#   Leap Year (True/False)
#   Month
#   Leap Month (True/False)
#   Day
#   Country China=0,Vietnam=1,Korea=2,Japan=3
#

pyNow = CurrentDate()
print ('Today: ' + str(pyNow))
nDays = pyNow.toordinal()
print ("Today's Ordinal Days: " + str(nDays))
ChineseDate = cmChineseFromDays(nDays,CHINESE)
print ('Chinese date in ' + FormatChineseDate(ChineseDate))
print ('Days from Chinese in ' + ChineseCountry[ChineseDate[6]] + ': ' + str(cmDaysFromChinese(ChineseDate[0],ChineseDate[1],ChineseDate[3],ChineseDate[4],ChineseDate[5],ChineseDate[6])))
ChineseDate = cmChineseFromDays(nDays,VIETNAMESE)
print ('Chinese date in ' + FormatChineseDate(ChineseDate))
print ('Days from Chinese in ' + ChineseCountry[ChineseDate[6]] + ': ' + str(cmDaysFromChinese(ChineseDate[0],ChineseDate[1],ChineseDate[3],ChineseDate[4],ChineseDate[5],ChineseDate[6])))
ChineseDate = cmChineseFromDays(nDays,KOREAN)
print ('Chinese date in ' + FormatChineseDate(ChineseDate))
print ('Days from Chinese in ' + ChineseCountry[ChineseDate[6]] + ': ' + str(cmDaysFromChinese(ChineseDate[0],ChineseDate[1],ChineseDate[3],ChineseDate[4],ChineseDate[5],ChineseDate[6])))
ChineseDate = cmChineseFromDays(nDays,JAPANESE)
print ('Chinese date in ' + FormatChineseDate(ChineseDate))
print ('Days from Chinese in ' + ChineseCountry[ChineseDate[6]] + ': ' + str(cmDaysFromChinese(ChineseDate[0],ChineseDate[1],ChineseDate[3],ChineseDate[4],ChineseDate[5],ChineseDate[6])))
print ('')
print ('Chinese Holidays during Gregorian Year ' + str(pyNow.year))
print ('')
i = 0
while i < len(ChineseHolidaysList):
   ChineseHoliday = ChineseHolidayCalculation (ChineseHolidaysList[i+1],ChineseHolidaysList[i+2],pyNow.year,ChineseHolidaysList[i+3],CHINESE)
   if len(ChineseHoliday) != 0:
      print (ChineseHolidaysList[i] + ': ' + str(ChineseHoliday[0]))
   else:
      print (ChineseHolidaysList[i] + ': did not occur')      
   i = i + 4



