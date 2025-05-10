########################################################################################
# File: PYSamaritan.py
# Contents: Samaritan calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025-05-11
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################
#
# Samaritan Calendrical Calculations (The Samaritan Calendar doesn't have month names)
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

NO_RULES = 0
SIMMUT_OF_PASSOVER = 1
SIMMUT_OF_TABERNACLES = 2
PENTECOST = 3

# Name, Month, Day, Rule
SamaritanHolidaysList = [
   'Simmut of Passover',0,0,SIMMUT_OF_PASSOVER,
   'Passover',1,14,NO_RULES,
   'Feast of Unleavened Bread Begins',1,15,NO_RULES,
   'Feast of Unleavened Bread Ends',1,21,NO_RULES,
   'Festival of Pentecost',0,0,PENTECOST,
   'Simmut of Tabernacles',0,0,SIMMUT_OF_TABERNACLES,
   'Festival of the Seventh Month',7,1,NO_RULES,
   'Day of Atonement',7,10,NO_RULES,
   'Festival of Tabernacles',7,15,NO_RULES,
   'Eighth Day of Sukkot',7,22,NO_RULES
]

# Astronomical definitions

SAMARITAN_EPOCH = -598573   # March 15, -1639 (Julian)
JULIAN_EPOCH = -1   # December 30, 0000
J2000 = 730120.5   # January 1, 2000 at noon
MeanSynodicMonth = 29.530588861   # Mean time from new moon to new moon
SamaritanLocale_Latitude = 32.1994   # Mount Gerizim  
SamaritanLocale_Longitude = 35.2728 
SamaritanLocale_Elevation = 881
SamaritanLocale_Zone = 2

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

def cmRound (x: float) -> int:
#
# Round x up to nearest integer
#
   return cmFloor(x + .5)
# End Def

def cmCeiling (x: float) -> int:
#
# Largest integer greater than x
#
   return int(math.ceil(x))
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

def cmAngle (nDegrees: float, nMinutes: float, nSeconds: float) -> float:
#
# Return decimal degrees
#
   nDecimalDegrees = (abs(nDegrees) + (abs(nMinutes) / 60) + (abs(nSeconds) / 3600))
   if nDegrees < 0:
      nDecimalDegrees = nDegrees * -1
   return nDecimalDegrees
# End Def

def cmObliquity (nCenturies: float) -> float:
#
# Obliquity Earth Orbit
#
   return cmAngle(23,26,21.448) - (cmAngle(0,0,46.8150) * nCenturies) - (cmAngle(0,0,0.00059) * nCenturies**2) + (cmAngle(0,0,0.001813) * nCenturies**3)
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

def cmLocalFromApparent (nMoment: float, nLongitude: float) -> float:
#
# Convert Apparent time to Local
#
   return nMoment - cmEquationOfTime(cmUniversalFromLocal(nMoment,nLongitude))
# End Def

def cmUniversalFromApparent (nMoment: float, nLongitude: float) -> float:
#
# Convert Apparent time to Universal
#
   return cmUniversalFromLocal(cmLocalFromApparent(nMoment,nLongitude),nLongitude)
# End Def

def cmZoneFromLongitude (nLongitude: float) -> float:
#
# Local mean time zone changes every 15 degrees. Convert to a fraction of a day.
#
   return nLongitude / 360
# End Def

def cmUniversalFromLocal (nLocal: float, nLongitude: float) -> float:
#
# Convert Local Time to Universal
#
   return nLocal - cmZoneFromLongitude(nLongitude)
# End Def

def cmLocalFromUniversal (nUniversal: float, nLongitude: float) -> float:
#
# Convert Universal Time to Local
#
   return nUniversal  + cmZoneFromLongitude(nLongitude)
# End Def

def cmApparentFromLocal (nMoment: float, nLongitude: float) -> float:
#
# Convert Local time to Apparent
#
   return nMoment + cmEquationOfTime(cmUniversalFromLocal(nMoment,nLongitude))
# End Def

def cmApparentFromUniversal (nMoment: float, nLongitude: float) -> float:
#
# Convert Universal time to Apparent
#
   return cmApparentFromLocal(cmLocalFromUniversal(nMoment,nLongitude),nLongitude)
# End Def

def cmMidday (nMoment: float, nLongitude: float) -> float:
#
# True middle of a Solar Day
#
   return cmUniversalFromApparent(nMoment + .5,nLongitude)
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

def cmSamaritanNoon (nDays: int) -> float:
#
# Calculate Samaritan solar noon on nDays
#
   return cmMidday(nDays,SamaritanLocale_Longitude)
# End Def

def cmSamaritanNewMoonAfter (nMoment: float) -> float:
#
# Calculate Samaritan date of the first new moon after nMoment
#
   return cmCeiling(cmApparentFromUniversal(cmNewMoonAfter(nMoment),SamaritanLocale_Longitude) - .5)
# End Def

def cmSamaritanNewMoonAtOrBefore (nMoment: float) -> float:
#
# Calculate Samaritan date of the first new moon at or before nMoment
#
   return cmCeiling(cmApparentFromUniversal(cmNewMoonBefore(nMoment),SamaritanLocale_Longitude) - .5)
# End Def

def cmGregorianWeekDay (nDays: int) -> int:
#
# Calculate the Gregorian day of the week handling nDays < 0
#
  return abs(cmFloor(cmMod(nDays,7)))
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

def cmDaysFromJulian (nMonth: int, nDay: int, nYear) -> int:
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

def cmJulianFromDays (nDays: int):
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
   nPriorDays = nDays - cmDaysFromJulian(January,1,nYear)
   if nDays < cmDaysFromJulian(March,1,nYear):
      nCorrection = 0
   elif nLeapYear == True:
      nCorrection = 1
   else:
      nCorrection = 2
   nMonth = cmFloor((1 / 367) * (12 * (nPriorDays + nCorrection) + 373))
   nDay = nDays - cmDaysFromJulian(nMonth,1,nYear) + 1
   JulianDate = []
   JulianDate.append(nMonth)
   JulianDate.append(nDay)
   JulianDate.append(nYear)
   JulianDate.append(nWeekDay)
   JulianDate.append(nLeapYear)
   return JulianDate
# End Def

def cmJulianInGregorian (nMonth: int, nDay: int, nGregorianYear: int):
#
# Return the Julian days dates occuring in a Gregorian Year
#
   nJan1 = date(nGregorianYear,January,1).toordinal()
   JulianDate = cmJulianFromDays(nJan1)
   nJulianMonth = JulianDate[0] 
   nJulianDay = JulianDate[1]
   nJulianYear0 = JulianDate[2]
   if nJulianYear0 == -1:
      nJulianYear1 = 1
   else:
      nJulianYear1 = nJulianYear0 + 1
   nDays0 = cmDaysFromJulian(nMonth,nDay,nJulianYear0)
   nDays1 = cmDaysFromJulian(nMonth,nDay,nJulianYear1)
   JulianInGregorian = []
   JulianInGregorian.append(nDays0)
   JulianInGregorian.append(nDays1)
   return JulianInGregorian
# End Def

def cmSamaritanNewYearOnOrBefore (nDays: int) -> int:
#
# Calculate Samaritan New Year
#
   nGregorianYear = cmGregorianYearFromDays(nDays)
   nJan1 = date(nGregorianYear,January,1).toordinal()
   nDec31 = date(nGregorianYear,December,31).toordinal()
   JulianInGregorian = cmJulianInGregorian(March,11,nGregorianYear)
#
# Find which date is in the Gregorian Year
#
   if JulianInGregorian[0] >= nJan1 and JulianInGregorian[0] <= nDec31:
      nJulianDays = JulianInGregorian[0]
   else:
      nJulianDays = JulianInGregorian[1]
   return cmFloor(cmSamaritanNewMoonAfter(cmSamaritanNoon(nJulianDays)))
# End Def

def SamaritanFromDays (nDays: int):
#
# Calculate Samaritan Date from Days
#
   nMoon = cmFloor(cmSamaritanNewMoonAtOrBefore(cmSamaritanNoon(nDays)))
   nNewYear = cmSamaritanNewYearOnOrBefore(nMoon)
   nMonth = cmRound((nMoon - nNewYear) / 29.5) + 1
   nYear = cmRound(((nNewYear - SAMARITAN_EPOCH) / 365.25) + cmCeiling((nMonth - 5) / 8))
   nDay = nDays - nMoon + 1
   SamaritanDate = []
   SamaritanDate.append(nMonth)
   SamaritanDate.append(nDay)
   SamaritanDate.append(nYear)
   return SamaritanDate
# End Def

def DaysFromSamaritan (nMonth: int, nDay: int, nYear: int) -> int:
#
# Calculate Days from Samaritan Date
#
   nY = cmSamaritanNewYearOnOrBefore(cmFloor(SAMARITAN_EPOCH + 50 + (365.25 * (nYear - cmCeiling((nMonth - 5) / 8)))))
   nM = cmSamaritanNewMoonAtOrBefore(nY + 29.5 * (nMonth - 1) + 15)
   return nM + nDay - 1
# End Def

def cmSamaritanInGregorian (nMonth: int, nDay: int, nGregorianYear: int) -> int: 
#
# Return the Samaritan days date occuring in a Gregorian Year
#
   nSamaritanYear0 = nGregorianYear + 1638
   nSamaritanYear1 = nSamaritanYear0 + 1
   nJan1 = date(nGregorianYear,January,1).toordinal()
   nDec31 = date(nGregorianYear,December,31).toordinal()
   nDays = DaysFromSamaritan(nMonth,nDay,nSamaritanYear0)
   if nDays >= nJan1 and nDays <= nDec31:
      return nDays
   else:
      return DaysFromSamaritan(nMonth,nDay,nSamaritanYear1)
# End Def

def SamaritanDateCalculation (nMonth: int, nDay: int, nGregorianYear: int, nRule: int) -> date:
#
# Return Samaritan dates occurring in a given Gregorian year
#
   if nRule == SIMMUT_OF_PASSOVER:
      nPassover = cmSamaritanInGregorian(1,14,nGregorianYear)      
      nCalcDays = nPassover - 49 - cmGregorianWeekDay(nPassover)
   elif nRule == SIMMUT_OF_TABERNACLES:
      nTabernacles = cmSamaritanInGregorian(7,15,nGregorianYear)
      nCalcDays = nTabernacles - 49 - cmGregorianWeekDay(nTabernacles)
   elif nRule == PENTECOST:
      nPassover = cmSamaritanInGregorian(1,14,nGregorianYear)
      nCalcDays = nPassover + 56
   else:
      nCalcDays = cmSamaritanInGregorian(nMonth,nDay,nGregorianYear)
   return date.fromordinal(nCalcDays)
# End Def

pyNow = CurrentDate()
print ('Today Local: ' + str(pyNow))
nDays = pyNow.toordinal()
print ("Today's Local Ordinal Days: " + str(nDays))
SamaritanDate = SamaritanFromDays(nDays)
print ('Samaritan Date: ' + str(SamaritanDate[0]) + ' ' + str(SamaritanDate[1]) + ', ' + str(SamaritanDate[2]))
print ('Days From Samaritan: ' + str(DaysFromSamaritan(SamaritanDate[0],SamaritanDate[1],SamaritanDate[2])))
print ('')
print ('Samaritan Holidays during Gregorian Year ' + str(pyNow.year))
print ('')
i = 0
while i < len(SamaritanHolidaysList):
   print (SamaritanHolidaysList[i] + ': ' + str(SamaritanDateCalculation(SamaritanHolidaysList[i + 1],SamaritanHolidaysList[i + 2],pyNow.year,SamaritanHolidaysList[i + 3])))      
   i = i + 4
