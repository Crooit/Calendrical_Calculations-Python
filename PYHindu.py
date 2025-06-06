########################################################################################
# File: PYHindu.py
# Contents: Hindu calendar calculations.
# Version: 1.11
# Python Version: 3.13
# Date: 2025-06-05
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################

#
# Hindu Calendrical Calculations
#

from datetime import datetime, date
import math

# Global Variables

HINDU_EPOCH = -1132959   # January 23, -3101
HINDU_SOLAR_ERA = 3179
HINDU_LUNAR_ERA = 3044
HinduSiderealYear = (365 + 279457 / 1080000)
HinduSiderealMonth = (27 + 4644439 / 14438334)
HinduSynodicMonth = (29 + 7087771 / 13358334)
HinduCreation = (HINDU_EPOCH - 1955880000 * HinduSiderealYear)
HinduAnomalisticYear = (1577917828000 / (4320000000 - 387))
HinduAnomalisticMonth = (1577917828 / (57753336 - 488199))
HinduLocaleLatitude = 23.1793013
HinduLocaleLongitude = 75.7849097             
HinduLocaleElevation = 0
HinduLocaleZone = 5.5
HinduLocaleName = 'Ujjain'

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

KARTIKA = 8    # Eighth month of Hindu lunar year
PHALGUNA = 12  # Twelth month of Hindu lunar year

# Time

ONE_DAY = 86400000   # Milliseconds in a day
ONE_HOUR = 3600000   # Milliseconds in a hour
ONE_MINUTE = 60000   # Milliseconds in a minute
ONE_SECOND = 1000    # Milliseconds in a second

# Astronomical definitions

J2000 = 730120.5   # January 1, 2000 at noon
SUNRISE_SUNSET_TIME = 47
MORNING = True
EVENING = False
NEWMOON = 0
FULLMOON = 180
VisibleHorizon = 0.8413147543981382   # Half diameter of the sun (16 minutes + 34.478885263888294 minutes for refraction)
MeanSynodicMonth = 29.530588861   # Mean time from new moon to new moon
GEOCENTRIC = True
TOPOCENTRIC = False

SolarMonthNames = ['Vaisakha','Jyaistha','Asadha','Shravana','Bhadrapada','Asvina','Kartika','Margasirsa','Pausa','Magha','Phalguna','Chaitra']
LunarMonthNames = ['Chaitra','Vaisakha','Jyaistha','Asadha','Shravana','Bhadrapada','Asvina','Kartika','Margasirsa','Pausa','Magha','Phalguna',]
LunarLeapMonthName = 'Adhik Maas'
LunarStationName = ['Asvini','Bharani','Krttika','Rohini','Mrigasiras','Ardra','Punarvasu','Pusya','Aslesa','Magha','Purva-Phasguni', \
   'Uttara-Phasguni','Hasta','Citra','Svati','Visakka','Anradha','Jyestha','Mula','Purva-Asadha','Uttara-Asadha','Sravana','Dhanistha', \
   'Satataraka','Purva-Bhadrapada','Uttara-Bhadrapada','Revanti']
HinduYogaName = ['Viskambha','Priti','Ayusman','Saubhagya','Sobhana','Atiganda','Sukarman','Dhrti','Sula','Ganda','Vrddhi','Dhruva', \
    'Vyaghata','Harsana','Vajra','Siddhi','Vyatipata','Variyas','Parigha','Siva','Siddha','Sadhya','Subha','Sukla','Brahman', \
    'Indra','Vaidhrti']

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

def cmObliquity (nCenturies: float) -> float:
#
# Obliquity Earth Orbit
#
   return cmAngle(23,26,21.448) - (cmAngle(0,0,46.8150) * nCenturies) - (cmAngle(0,0,0.00059) * nCenturies**2) + (cmAngle(0,0,0.001813) * nCenturies**3)
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

def cmAMod (x: float, y: float) -> float:
#
# Variation of x MOD y for Real Numbers adjusted so that the modulus
# of a multiple of the divisor is the divisor itself rather than zero.
# 
# If x MOD y = 0 then result is adjusted to y
#
   return y + cmMod(x,y * -1)
# End Def

def cmMod3 (x: float, a: float, b: float) -> float:
#
# Force modulus x into the range a..b for Real Numbers
#
   if a == b:
      return x
   else:
      return a + (cmMod(x - a,b - a))
# End Def

def cmRound (x: float) -> int:
#
# Round x up to nearest integer
#
   return cmFloor(x + .5)
# End Def

def cmMomentToSerial (nMoment: float) -> int:
#
# Convert Moment to Serial Date
#
   nDays = cmFloor(nMoment)
   nTime = cmFloor(cmMod(abs(nMoment),1) * ONE_DAY)
   nSerial = (abs(nDays) * ONE_DAY) + nTime
   if nDays < 0:
      nSerial = nSerial * -1
   return nSerial
# End Def

def cmTimeFromSerial (nSerial: int) -> datetime:
#
# Extract time from a serial period
#
   nDays = cmFloor(nSerial / ONE_DAY)
   pyDate = date.fromordinal(nDays)
   nTime = nSerial - (nDays * ONE_DAY)
   #
   # If nTime is < 0 assume it has wrapped back past midnight
   #
   #if nTime < 0:
   #   nTime = cmFloor(cmMod(nTime,ONE_DAY))
   nHour = cmFloor(nTime / ONE_HOUR)
   nTime = nTime - nHour * ONE_HOUR
   nMinute = cmFloor(nTime / ONE_MINUTE)
   nTime = nTime - nMinute * ONE_MINUTE
   nSecond = cmFloor(nTime / ONE_SECOND)
   nMillisecond = nTime - (nSecond * ONE_SECOND)
   return datetime(pyDate.year,pyDate.month,pyDate.day,nHour,nMinute,nSecond,nMillisecond)
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

def cmUniversalFromLocal (nLocal: float, nLongitude: float) -> float:
#
# Convert Local Time to Universal
#
   return nLocal - cmZoneFromLongitude(nLongitude)
# End Def

def cmStandardFromUniversal (nUniversal: float, nZone: float) -> float:
#
# Convert Universal Time to Standard
#
   return nUniversal + nZone / 24
# End Def

def cmStandardFromLocal (nLocal: float, nZone: float, nLongitude: float) -> float:
#
# Convert Local Time to Standard
#
   return cmStandardFromUniversal(cmUniversalFromLocal(nLocal,nLongitude),nZone)
# End Def

def cmLocalFromApparent (nMoment: float, nLongitude: float) -> float:
#
# Convert Apparent time to Local
#
   return nMoment - cmEquationOfTime(cmUniversalFromLocal(nMoment,nLongitude))
# End De

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

def cmEarthRadius (nLatitude: float) -> float:
#
# Earth Radius at a given Latitude
#
# As a safeguard, ensure latitude is in the range of 0-90
#
   nLatitudeRadians = cmDegreesToRadians(cmMod(abs(nLatitude),90))**2
#
# Radius at the equator = 6378136.6 meters
# Radius at the poles = 6356752.314245 meters
#
   return 6356752.314245 * (1 + nLatitudeRadians)**0.5 / ((6356752.314245**2 / 6378136.6**2) + nLatitudeRadians)**.5
# End Def

def cmSolarRefraction (nElevation: float, nLatitude: float) -> float:
#
# Atmosphere General Refraction of Light adjusted for Elevation
#
   nEarthRadius = cmEarthRadius(nLatitude)
   if nElevation > 0:
      nAdjustedElevation = nElevation
      nElevationSQRT = nElevation**.5
   else:
      nAdjustedElevation = 0
      nElevationSQRT = 0
   return VisibleHorizon \
          + cmArcCoSineDegrees(nEarthRadius / (nEarthRadius + nAdjustedElevation)) \
          + cmAngle(0,0,19) * nElevationSQRT
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

def cmDeclination (nMoment: float, nLatitude: float, nLongitude: float) -> float:
#
# Angular distance of a point north or south of the celestial equator
#
   nObliquity = cmObliquity(cmJulianCenturies(nMoment))
   return cmArcSinDegrees(cmSinDegrees(nLatitude) \
          * cmCoSineDegrees(nObliquity) \
          + cmCoSineDegrees(nLatitude) \
          * cmSinDegrees(nObliquity) \
          * cmSinDegrees(nLongitude))
# End Def

def cmSineOffset (nMoment: float, nLatitude: float, nLongitude: float, nDepression: float) -> float:
#
# Angle between where the sun is at (nMoment) and where we want it to be (nDeclination)
#
   nUniversal = cmUniversalFromLocal(nMoment,nLongitude)
   nDeclination = cmDeclination(nUniversal,0,cmSolarLongitude(nMoment))
   return cmTangentDegrees(nLatitude) \
          * cmTangentDegrees(nDeclination) \
          + (cmSinDegrees(nDepression) / (cmCoSineDegrees(nDeclination) * cmCoSineDegrees(nLatitude)))
# End Def

def cmApproxMomentOfDepression (nMoment: float, nLatitude: float, nLongitude: float, nDepression: float, bEarly: bool) -> float:
#
# Approximation for Moment when Sun is at nDepression angle
#
   nApprox = 0    # if return is 0, event did not occur
   nDays = cmFloor(nMoment)
   nTry = cmSineOffset(nMoment,nLatitude,nLongitude,nDepression)
   if nDepression >= 0:
      if bEarly == MORNING:
         nAlt = 1
      else:
         nAlt = nDays + .5
   if abs(nTry) > 1:
      nValue = cmSineOffset(nAlt,nLatitude,nLongitude,nDepression)
   else:
      nValue = nTry
   if abs(nValue) <=1:   # Event Occurs
      nOffset = cmMod3(cmArcSinDegrees(nValue) / 360,-.5,.5)
      if bEarly == MORNING:
         nOffsetAdjust = (.25 - nOffset)
      else:
        nOffsetAdjust = (.75 + nOffset)
      nApprox = cmLocalFromApparent(nDays + nOffsetAdjust,nLongitude)
   return nApprox
# End Def

def cmMomentOfDepression (nApprox: float, nLatitude: float, nLongitude: float, nDepression: float, bEarly: bool) -> float:
#
# Find Moment when the Sun is at nDepression angle
#
   nMoment = cmApproxMomentOfDepression(nApprox,nLatitude,nLongitude,nDepression,bEarly)
   if nMoment != 0:
      if abs(nApprox - nMoment) >= 30 / 3600:   # Within 30 sec?
         nMoment = cmApproxMomentOfDepression(nMoment,nLatitude,nLongitude,nDepression,bEarly)
   return nMoment
# End Def

def cmDawn (nDays: int, nZone: float, nLatitude: float, nLongitude: float, nDepression: float) -> float:
#
# Calculate Dawn
#
   nEvent = cmMomentOfDepression(nDays + .25,nLatitude,nLongitude,nDepression,MORNING)
   return cmStandardFromLocal(nEvent,nZone,nLongitude)
# End Def

def cmDusk (nDays: int, nZone: float, nLatitude: float, nLongitude: float, nDepression: float) -> float:
#
# Calculate Dusk
#
   nEvent = cmMomentOfDepression(nDays + .75,nLatitude,nLongitude,nDepression,EVENING)
   return cmStandardFromLocal(nEvent,nZone,nLongitude)
# End Def

def cmSunRise (nDays: int, nZone: float, nLatitude: float, nLongitude: float, nElevation: float, nDepression: float) -> float: 
#
# Calculate Sunrise in nZone time
#
   return cmDawn(nDays,nZone,nLatitude,nLongitude,nDepression + cmSolarRefraction(nElevation,nLatitude))
# End Def

def cmSunSet (nDays: int, nZone: float, nLatitude: float, nLongitude: float, nElevation: float, nDepression: float) -> float: 
#
# Calculate Sunset in nZone time
#
   return cmDusk(nDays,nZone,nLatitude,nLongitude,nDepression + cmSolarRefraction(nElevation,nLatitude))
# End Def

def cmHinduSunRise (nDays: int) -> float:
#
# Hindu Sunrise
#
# Uses modern computation of sunrise to get better agreement with published Hindu calendars
# instead of following the strict Hindu Surya-Siddhanta calculations which can be off by more
# than 16 minutes
#
   nRise = cmSunRise(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0))
   return ((1/60) / 24) * cmRound(nRise * 1440)
# End Def

def cmHinduSunSet (nDays: int) -> float:
#
# Hindu Sunset
#
# Uses modern computation of sunset to get better agreement with published Hindu calendars
# instead of following the strict Hindu Surya-Siddhanta calculations which can be off by more
# than 16 minutes
#
   nSet = cmSunSet(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0))
   return ((1/60) / 24) * cmRound(nSet * 1440)
# End Def

def cmDayTimeTemporalHour (nDays: int) -> float:
#
# Temporal or Seasonal Hour
#
   return (1 / 12) * (cmSunSet(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)) \
      - cmSunRise(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)))
# End Def

def cmNightTimeTemporalHour (nDays: int) -> float:
#
# Temporal or Seasonal Hour
#
   return (1 / 12) * (cmSunRise(nDays + 1,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)) \
      - cmSunSet(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)))
# End Def

def cmStandardFromSunDial (nMoment: float) -> float:
#
# Convert Sundial time to Standard time
#
   nDate = cmFloor(nMoment)
   nHour = 24 * cmMod(nMoment,1)
   if nHour >= 6 and nHour <= 18:
      return cmSunRise(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)) \
         + (nHour - 6) * cmDayTimeTemporalHour(nDate)
   elif nHour < 6:
      return cmSunSet(nDays - 1,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)) \
         + (nHour + 6) * cmNightTimeTemporalHour(nDate - 1)
   else:
      return cmSunSet(nDays,HinduLocaleZone,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,cmAngle(0,SUNRISE_SUNSET_TIME,0)) \
         + (nHour - 18) * cmNightTimeTemporalHour(nDate)
# End Def 

def cmHinduStandardFromSundial (nMoment: float) -> float:
#
# Hindu Temporal Time
#
   nDate = cmFloor(nMoment)
   nTime = cmMod(nMoment,1)
   nQ = cmFloor(nTime * 4)
   if nQ == 0:
      nA = cmHinduSunSet(nDate - 1)
      nB = cmHinduSunRise(nDate)
      nAdjust = -.25
   elif nQ == 3:
      nA = cmHinduSetSet(nDate)
      nB = cmHinduSunRise(nDate + 1)
      nAdjust = .75
   else:
      nA = cmHinduSunRise(nDate)
      nB = cmHinduSunSet(nDate)
      nAdjust = .25
   return nA + 2 * (nB - nA) * (nTime - nAdjust)
# End Def

def cmHinduMeanPosition (nMoment: float, nPeriod: float) -> float:
#
# Position in degrees at nMoment in uniform circular orbit of nPeriod days
#
   return 360 * cmMod((nMoment - HinduCreation) / nPeriod,1)
# End Def

def cmHinduSineTable (nEntry: int) -> float:
#
# Hindu Sine Table simulation where nEntry is a multiplier of 225 minutes
#
   nExact = 3438 * cmSinDegrees(nEntry * cmAngle(0,225,0))
   nError = 0.215 * cmSignum(nExact) * cmSignum(abs(nExact) - 1716)
   return cmRound(nExact + nError) / 3438.0
# End Def

def cmHinduSine (nDegrees: float) -> float:
#
# Linear interpolation of Hindu Sine Table
#
   nEntry = nDegrees / cmAngle(0,225,0)
   nFraction = cmMod(nEntry,1)
   return nFraction * cmHinduSineTable(cmCeiling(nEntry)) + (1 - nFraction) * cmHinduSineTable(cmFloor(nEntry))
# End Def

def cmHinduArcsin (nAmp: float) -> float:
#
# Inverse of cmHinduSine()
#
   nPosition = 0
   if nAmp < 0:
      bNegative = True
   else:
      bNegative = False
   if bNegative == True:
      nAmpLoop = nAmp * -1
   else:
      nAmpLoop = nAmp
   bLoop = True
   while bLoop == True:
      if nAmpLoop > cmHinduSineTable(nPosition):
         nPosition = nPosition + 1
      else:
         bLoop = False
   nBelow = cmHinduSineTable(nPosition - 1)
   nReturn = cmAngle(0,225,0) * (nPosition - 1 + ((nAmpLoop - nBelow) / (cmHinduSineTable(nPosition) - nBelow)))
   if bNegative == True:
      return nReturn * -1
   else:
      return nReturn
# End Def

def cmHinduMeanPosition (nMoment: float, nPeriod: float) -> float:
#
# Position in degrees at nMoment in uniform circular orbit of nPeriod days
#
   return 360 * cmMod((nMoment - HinduCreation) / nPeriod,1)
# End Def

def cmHinduTruePosition (nMoment: float, nPeriod: float, nSize: float, nAnomalistic: float, nChange: float) -> float:
#
# Longitudinal Solar or Lunar position at nMoment
#
   nLong = cmHinduMeanPosition(nMoment,nPeriod)
   nOffset = cmHinduSine(cmHinduMeanPosition(nMoment,nAnomalistic))
   nContraction = abs(nOffset) * nChange * nSize
   nEquation = cmHinduArcsin(nOffset * (nSize - nContraction))
   return cmCalcDegrees(nLong - nEquation)
# End Def

def cmHinduSolarLongitude (nMoment: float) -> float:
#
# Hindu Solar Longitude
#
   return cmHinduTruePosition(nMoment,HinduSiderealYear,14 / 360,HinduAnomalisticYear,1 / 42)
# End Def

def cmHinduZodiac (nMoment: float) -> int:
#
# Hindu Zodiac Sign
#
   return cmFloor(cmHinduSolarLongitude(nMoment) / 30) + 1
# End Def

def cmHinduCalendarYear (nMoment: float) -> int:
#
# Calculate Hindu Year
#
   return cmRound(((nMoment - HINDU_EPOCH) / HinduSiderealYear) - (cmHinduSolarLongitude(nMoment) / 360))
# End Def

def HinduSolarFromDays (nDays: int):
#
# Given a Days date, return the Hindu Solar date (Saka Era)
#
   nCritical = cmHinduSunRise(nDays + 1)
   nMonth = cmHinduZodiac(nCritical)
   nYear = cmHinduCalendarYear(nCritical) - HINDU_SOLAR_ERA
   nApprox = nDays - 3 - cmMod(cmFloor(cmHinduSolarLongitude(nCritical)),30)
   bLoop = True
   while bLoop == True:
      if cmHinduZodiac(cmHinduSunRise(nApprox + 1)) != nMonth:
         nApprox = nApprox + 1
      else:
         bLoop = False
   nDay = nDays - nApprox + 1
   HinduSolarDate = []
   HinduSolarDate.append(nMonth)
   HinduSolarDate.append(nDay)
   HinduSolarDate.append(nYear)
   return HinduSolarDate
# End Def

def DaysFromHinduSolar (nMonth: int, nDay: int, nYear: int) -> int:
#
# Hindu Solar Date to Days Date
#
   nBegin = cmFloor((nYear + HINDU_SOLAR_ERA + ((nMonth - 1) / 12)) * HinduSiderealYear) + HINDU_EPOCH - 3
   bLoop = True
   while bLoop == True:
      if cmHinduZodiac(cmHinduSunRise(nBegin + 1)) != nMonth:
         nBegin = nBegin + 1
      else:
         bLoop = False
   return nBegin + nDay - 1
# End Def

def cmHinduLunarLongitude (nMoment: float) -> float:
#
# Hindu Lunar Longitude
#
   return cmHinduTruePosition(nMoment,HinduSiderealMonth,32 / 360,HinduAnomalisticMonth,1 / 96)
# End Def

def cmHinduLunarPhase (nMoment: float) -> float:
#
# Hindu Lunar Phase
#
  return cmCalcDegrees(cmHinduLunarLongitude(nMoment) - cmHinduSolarLongitude(nMoment))
# End Def

def cmHinduLunarDayFromMoment (nMoment: float) -> int:
#
# Hindu Phase of the moon (tithi) at nMoment - returns values from 1 to 30
#
   return cmFloor((cmHinduLunarPhase(cmHinduSunRise(nMoment)) / 12) + 1)
# End Def

def cmHinduNewMoonBefore (nMoment: float) -> float:
#
# Hindu New Moon
#
# Given a date/time moment, this routine will calculate the next
# new moon before nMoment.
#
# The basic strategy is to take the moment and search a bisection
# within an interval The search can terminate as soon as it has
# narrowed the position of the new moon down to one zodiacal sign
# and nExact = False. When nExact is True,the exact moment of the
# new moon is calculated.
#
# Calculate bisection interval
#
   nNewMoment = nMoment \
              - (1 / 360) \
              * cmHinduLunarPhase(nMoment) \
              * HinduSynodicMonth
   nStartMoment = nNewMoment - 1
   if nMoment < nNewMoment + 1:
      nEndMoment = nMoment
   else:
      nEndMoment = nNewMoment + 1
   nNewMoment = (nEndMoment + nStartMoment) * .5
   bLoop = True
   while bLoop == True:
      if cmHinduZodiac(nStartMoment) != cmHinduZodiac(nEndMoment) or nEndMoment - nStartMoment < .00001:
         if cmHinduLunarPhase(nNewMoment) < 180:
            nEndMoment = nNewMoment
         else:
            nStartMoment = nNewMoment
         nNewMoment = (nEndMoment + nStartMoment) * .5
      else:
         bLoop = False
   return nNewMoment
# End Def

def cmHinduLunarStation (nDays: int) -> int:
#
# Hindu Lunar Station (naksatra)
#
   return cmFloor(cmHinduLunarLongitude(cmHinduSunRise(nDays)) / cmAngle(0,800,0)) + 1
# End Def

def cmHinduYoga (nDays: int) -> int:
#
# Hindu Yoga number
#
   return cmFloor(cmMod((cmHinduSolarLongitude(nDays) + cmHinduLunarLongitude(nDays)) / cmAngle(0,800,0),27)) + 1
# End Def

def HinduLunarFromDays (nDays: int):
#
# Given a days date, return the Hindu Lunar date
#
   nCritical = cmHinduSunRise(nDays)
   nDay = cmHinduLunarDayFromMoment(nCritical)
#
# Check for Leap Day
#
   if nDay == cmHinduLunarDayFromMoment(cmHinduSunRise(nDays - 1)):
      bLeapDay = True
   else:
      bLeapDay = False
#
# Calculate Last/Next New Moons and Solar Month
#
   nLastNewMoon = cmHinduNewMoonBefore(nCritical)
   nNextNewMoon = cmHinduNewMoonBefore(cmFloor(nLastNewMoon) + 35)
   nSolarMonth = cmHinduZodiac(nLastNewMoon)
   nMonth = cmAMod(nSolarMonth + 1,12)
#
# Check for Leap Month
#
   if nSolarMonth == cmHinduZodiac(nNextNewMoon):
      bLeapMonth = True
   else:
      bLeapMonth = False
   if nMonth <= 2:
      nYear = cmHinduCalendarYear(nDays + 180) - HINDU_LUNAR_ERA
   else:
      nYear = cmHinduCalendarYear(nDays) - HINDU_LUNAR_ERA
   HinduLunarDate = []
   HinduLunarDate.append(nMonth)
   HinduLunarDate.append(bLeapMonth)
   HinduLunarDate.append(nDay)
   HinduLunarDate.append(bLeapDay)
   HinduLunarDate.append(nYear)
   HinduLunarDate.append(cmHinduLunarStation(nDays))
   return HinduLunarDate
# End Def

def cmHinduLunarOnOrBefore (nMonth1: int, bLeapMonth1: bool, nDay1: int, bLeapDay1: bool, nYear1: int, nMonth2: int, bLeapMonth2: bool, nDay2: int, bLeapDay2: bool, nYear2: int) -> bool:
#
# Given two Hindu Lunar dates, determine if the first is on or before the second
#
   if nYear1 > nYear2:
      bReturn = False
   else:
      if nMonth1 > nMonth2:
         bReturn = False
      else:
         bReturn = False
         if (bLeapMonth1 == True and bLeapMonth2 == False) or \
            (bLeapMonth1 == bLeapMonth2 and \
            (nDay1 < nDay2 or (nDay1 == nDay2 and \
            (bLeapDay1 == False or bLeapDay2 == True)))):
            bReturn = True
   return bReturn
# End Def

def DaysFromHinduLunar (nMonth: int, bLeapMonth: bool, nDay: int, bLeapDay: bool, nYear: int) -> int:
#
# Given a Hindu Lunar date, return the Days date
#
# Rough Approximation
#
   nApprox = HINDU_EPOCH + HinduSiderealYear * (nYear + HINDU_LUNAR_ERA + (nMonth - 1) / 12)
#
# Solar based approximation
#
   nSolarApprox = cmFloor(nApprox - (HinduSiderealYear * cmMod3(((cmHinduSolarLongitude(nApprox) / 360) - ((nMonth - 1) / 12)),-.5,.5)))
#
# Lunar Day of Solar Approximation
#
   nLunarDay = cmHinduLunarDayFromMoment(nSolarApprox + .25)
#
# Check for month
#
   if 3 < nLunarDay and nLunarDay < 27:   # Borderline case - New Moon and Solar Month close to same
      nAdjustment = nLunarDay
   else:
#
# Middle of preceding solar month
#
      HinduLunarDate = HinduLunarFromDays(nSolarApprox - 15)
      #
      # Look in preceding month
      #
      if (HinduLunarDate[0] != nMonth) or (HinduLunarDate[1] == True and bLeapMonth == False):
         nAdjustment = cmMod3(nLunarDay,-15,15)
      else:
         #
         # Look in next month
         #
         nAdjustment = cmMod3(nLunarDay,15,45)
#
# Calculate Estimation
#
   nEstimated = nSolarApprox + nDay - nAdjustment
#
# Refine Estimation
#
   nTau = nEstimated - cmMod3(cmHinduLunarDayFromMoment(nEstimated + .25) - nDay,-15,15)
   bLoop = True
   while bLoop == True:
      nLoopDay = cmHinduLunarDayFromMoment(cmHinduSunRise(nTau))
      if nLoopDay == nDay or nLoopDay == cmAMod(nDay + 1,30):
         bLoop = False
      else:
         nTau = nTau - 1
   return nTau
# End Def

def cmHinduSolarLongitudeAtOrAfter (nTargetLongitude: float, nMoment: float) -> float:
#
# Time at or after nMoment when solar longitude will be target
#
   nTau = nMoment + HinduSiderealYear * ( 1 / 360) * (cmCalcDegrees((nTargetLongitude - cmHinduSolarLongitude(nMoment))))
#
# Estimate within 5 days
#
   if nMoment > nTau:
      nStartMoment = nMoment
   else:
      nStartMoment = nTau - 5
   nEndMoment = nTau + 5
   bLoop = True
   while bLoop == True:
      nNewMoment = nStartMoment + ((nEndMoment - nStartMoment) * .5)
      nNewLongitude = cmCalcDegrees(cmHinduSolarLongitude(nNewMoment) - nTargetLongitude)
      if nNewLongitude < 180:
         nEndMoment = nNewMoment
      else:
         nStartMoment = nNewMoment
      if nEndMoment - nStartMoment < .000001:
         bLoop = False
   return nStartMoment + ((nEndMoment - nStartMoment) * .5)
# End Def

def cmHinduLunarDayAtOrAfter (nLunarDay: float, nMoment: float) -> float:
# 
# Moment at which nLunarDay occurred at or after nMoment
#
   return cmStandardFromUniversal(cmLunarPhaseAtOrAfter(nMoment,(nLunarDay - 1) * 12),HinduLocaleZone)
# End Def

def cmHinduLunarNewYear (nGregorianYear: int) -> date:
#
# Hindu Lunar New Year (Chandramana Ugadi)
#
# Lunar New Year is the (sunrise-to-sunrise) day of the last new moon before the sun reaches the fixed First
# Point in Aries
#
   nJan1 = date(nGregorianYear,January,1).toordinal()
   nMina = cmHinduSolarLongitudeAtOrAfter(330,nJan1)
   nNewMoon = cmHinduLunarDayAtOrAfter(1,nMina)
   nDays = cmFloor(nNewMoon)
   nCritical = cmHinduSunRise(nDays)
   if (nNewMoon >= nCritical) or (cmHinduLunarDayFromMoment(cmHinduSunRise(nDays + 1)) != 2):
      nDays = nDays + 1
#
# Check for a leap month where the Hindu Lunar New Year is observed in the following month
#
   HinduLunarDate = HinduLunarFromDays(nDays)
   if HinduLunarDate[1] == True:
      nNewMoon = cmFloor(cmHinduNewMoonBefore(nDays + 35))
      nDays = cmFloor(nNewMoon)
      nCritical = cmHinduSunRise(nDays)
      if (nNewMoon >= nCritical) or (cmHinduLunarDayFromMoment(cmHinduSunRise(nDays + 1)) != 2):
         nDays = nDays + 1
   return date.fromordinal(nDays)
# End Def

def FormatHinduLunarDate (nMonth: int, bLeapMonth: bool, nDay: int, bLeapDay: bool, nYear: int, nStation: int) -> str:
#
# Format Hindu Lunar Date
#
   if bLeapMonth == False:
      sMonth = LunarMonthNames[nMonth - 1]
   else:
      sMonth = LunarLeapMonthName + '.Leap'
   if bLeapDay == False:
      sDay = str(nDay)
   else:
      sDay = str(nDay) + '.Leap'
   return sMonth + ' ' + sDay + ', ' + str(nYear) + ' Lunar Station (naksatra): ' + LunarStationName[nStation - 1]
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

def cmMeanLunarLongitude (nC: float) -> float:
#
# Mean Lunar Longitude
#
   return cmCalcDegrees(218.3164477 + 481267.88123421 * nC - .0015786 * nC**2 + (nC**3 / 538841) - (nC**4 / 65194000))
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

def cmLunarPhaseAtOrBefore (nMoment: float, nTargetLongitude: float) -> float:
#
# Given a date/time moment, this routine will calculate the previous
# lunar event within a longitutinal limitation. Typical lunar events
# are new and full moons.
#
# The basic strategy is to take the moment and number of degrees and
# search for the moment when next the nLongitude of the moon is a multiple of
# the given degrees. The search is a bisection within an interval beginning
# 5 days before our estimate or nMoment whichever is earlier and
# ending long enough past nMoment to insure that the moon passes through
# exactly one multiple of nuTargetLongitude. The process terminates when the
# time is ascertained within one hundred-thousanth of a day (about 0.9 seconds).
# The discontinuity from 360 to 0 degress is taken into account.
#
#  Calculate upper part of bisection interval
#
   nEndMoment = nMoment - ((MeanSynodicMonth / 360) * cmCalcDegrees(((cmLunarPhase(nMoment) - nTargetLongitude))))
   nStartMoment = nEndMoment - 2
   if nMoment > nEndMoment + 2:
      nEndMoment = nEndMoment + 2
   else:
      nEndMoment = nMoment
   nSearch = True
   while nSearch == True:
      nNewMoment = nStartMoment + ((nEndMoment - nStartMoment) * .5)
      nNewLongitude = cmCalcDegrees(cmLunarPhase(nNewMoment) - nTargetLongitude)
      if nNewLongitude < 180:
         nEndMoment = nNewMoment
      else:
         nStartMoment = nNewMoment
      if nEndMoment - nStartMoment < .00001:
         nSearch = False
   return nStartMoment + ((nEndMoment - nStartMoment) * .5)
# End Def

def cmLunarPhaseAtOrAfter (nMoment: float, nTargetLongitude: float) -> float:
#
# Given a date/time moment, this routine will calculate the next
# lunar event within a longitutinal limitation. Typical lunar events
# are new and full moons.
#
# Calculate upper part of bisection interval
#

   nEndMoment = nMoment + (MeanSynodicMonth / 360) * cmCalcDegrees(((nTargetLongitude - cmLunarPhase(nMoment))))
   if nMoment > nEndMoment:
      nStartMoment = nEndMoment - 2
   else:
      nStartMoment = nEndMoment - 2
#   nStartMoment = IIf(nMoment > nEndMoment - 2,nMoment,nEndMoment - 2)
   nEndMoment = nEndMoment + 2
   bLoop = True
   while bLoop == True:
      nNewMoment = nStartMoment + ((nEndMoment - nStartMoment) * .5)
      nNewLongitude = cmCalcDegrees(cmLunarPhase(nNewMoment) - nTargetLongitude)
      if (nEndMoment - nStartMoment) <= .00001:
         bLoop = False
      elif nNewLongitude < 180:
         nEndMoment = nNewMoment
      else:
         nStartMoment = nNewMoment
   return nNewMoment
# End Def

def cmLunarFindPhase (nFromDays: int, nToDays: int, nTargetLongitude: float) -> float:
#
# Lunar Phases
#
# Cycle through the period from end to beginning 28 days at a time
# and check for lunar phase at nTargetLongitude
#
   nTo = nToDays
   bLoop = True
   while bLoop == True:
      nMoon = cmLunarPhaseAtOrBefore(nTo + 1,nTargetLongitude)
      if cmFloor(nMoon) >= nFromDays and cmFloor(nMoon) <= nTo:
         bLoop = False
      else:
         nTo = nTo - 28
         if nFrom > nTo:
            bLoop = False
            nMoon = date(1,1,1).toordinal()
   return nMoon
# End Def

def cmSumDistancePeriods (nE: float, nElongation: float, nSolarAnomaly: float, nLunarAnomaly: float, nMoonFromNode: float, nV: float, nW: float, nX: float, nY: float, nZ: float) -> float:
#
# Distance adjustments of the Moon from Earth
#
   return nV * nE**abs(nX) * cmCoSineDegrees((nW * nElongation) + (nX * nSolarAnomaly) + (nY * nLunarAnomaly) + (nZ * nMoonFromNode))
# End Def

def cmLunarDistance (nMoment: float) -> float:
#
# Return the Distance in meters of the Moon from Earth
#
# Get UTC Moment in nTimeZone
#
   nC = cmJulianCenturies(nMoment)
   nElongation = cmLunarElongation(nC)
   nSolarAnomaly = cmSolarAnomaly(nC)
   nLunarAnomaly = cmLunarAnomaly(nC)
   nMoonFromNode = cmMoonNode(nC)
   nE = 1 - .002516 * nC - .0000074 * nC**2
   nCorrection = cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-20905355,0,0,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2955968,2,0,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,48888,0,1,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,246158,2,0,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-170733,2,0,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-129620,0,1,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,104755,0,1,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-34782,4,0,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-21636,4,0,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,30824,2,1,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-16675,1,1,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-10445,2,0,2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,14403,2,0,-3,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,6322,1,0,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,5751,0,1,2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-4950,2,-2,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2616,2,1,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-2117,0,2,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1423,4,0,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1571,4,-1,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,1165,0,2,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-3699111,2,0,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-569925,0,0,2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-3149,0,0,0,2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-152138,2,-1,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-204586,2,-1,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,108743,1,0,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,10321,2,0,0,-2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,79661,0,0,1,-2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-23210,0,0,3,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,24208,2,1,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-8379,1,0,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-12831,2,-1,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-11650,4,0,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-7003,0,1,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,10056,2,-1,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-9884,2,-2,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,4130,2,0,1,-2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-3958,4,-1,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,3258,3,0,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1897,4,-1,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2354,2,2,-1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1117,0,0,4,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1739,1,0,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-4421,0,0,2,-2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,0,0,1,2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,2,0,-1,2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,0,2,0,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,2,0,0,2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,0,0,2,2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,2,1,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,2,-1,0,-2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,2,1,0,-2) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,1,1,1,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,3,0,-2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,4,0,-3,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,0,2,-1,2,0) \
               + cmSumDistancePeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,8752,2,0,-1,-2)
   return 385000560 + nCorrection
# End Def

def cmEarthRadius (nLatitude: float) -> float:
#
# Earth Radius at a given Latitude
#
# As a safeguard, ensure latitude is in the range of 0-90
#
   nLatitudeRadians = cmDegreesToRadians(cmMod(abs(nLatitude),90))**2
#
# Radius at the equator = 6378136.6 meters
# Radius at the poles = 6356752.314245 meters
#
   return 6356752.314245 * (1 + nLatitudeRadians)**0.5 / ((6356752.314245**2 / 6378136.6**2) + nLatitudeRadians)**.5
# End Def

def cmLunarParallax (nMoment: float, nLunarAltitude: float, nLatitude: float) -> float:
#
# Lunar Parallax
#
   return cmArcSinDegrees((cmEarthRadius(nLatitude) / cmLunarDistance(nMoment)) * cmCoSineDegrees(nLunarAltitude))
# End Def

def cmRightAscension (nMoment: float, nLatitude: float, nLongitude: float) -> float:
#
# Angular distance measured eastward along the celestial equator from the vernal equinox 
#
   nObliquity = cmObliquity(cmJulianCenturies(nMoment))
   return cmArcTanDegrees((cmSinDegrees(nLongitude) * cmCoSineDegrees(nObliquity)) - (cmTangentDegrees(nLatitude) * cmSinDegrees(nObliquity)),cmCoSineDegrees(nLongitude))
# End Def

def cmSiderealFromMoment (nMoment: float) -> float:
#
# Convert Moment Time to Sidereal
#
   nC = (nMoment - J2000) / 36525
   return cmCalcDegrees(280.46061837 + 36525 * 360.98564736629 * nC + .000387933 * nC**2 - (nC**3 / 38710000))
# End Def

def cmGeocentricLunarAltitude (nMoment: float, nLatitude: float, nLongitude: float) -> float:
#
# Geocentric Altitude of the Moon above the horizon at UTC nMoment
#
# Not corrected for parallax or refraction
#
   nLunarLongitude = cmLunarLongitude(nMoment)
   nLunarLatitude = cmLunarLatitude(nMoment)
   nLunarRightAscension = cmRightAscension(nMoment,nLunarLatitude,nLunarLongitude)
   nLunarDeclination = cmDeclination(nMoment,nLunarLatitude,nLunarLongitude)
   nLocalSiderealHourAngle = cmCalcDegrees(cmSiderealFromMoment(nMoment) + nLongitude - nLunarRightAscension)
   nAltitude = cmArcSinDegrees((cmSinDegrees(nLatitude) \
             * cmSinDegrees(nLunarDeclination)) \
             + (cmCoSineDegrees(nLatitude) \
             * cmCoSineDegrees(nLunarDeclination) \
             * cmCoSineDegrees(nLocalSiderealHourAngle)))
   return cmMod3(nAltitude,-180,180)
# End Def

def cmTopocentricLunarAltitude (nMoment: float, nLatitude: float, nLongitude: float, nElevation: float) -> float:
#
# Topocentric Lunar Altitude
#
# Correct geocentric altitude from earth center to surface
# and adjust for parallax and refraction
#
   nLunarAltitude = cmGeocentricLunarAltitude(nMoment,nLatitude,nLongitude)
   return nLunarAltitude - cmLunarParallax(nMoment,nLunarAltitude,nLatitude) + cmSolarRefraction(nElevation,nLatitude)
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

def cmMeanLunarLongitude (nC: float) -> float:
#
# Mean Lunar Longitude
#
   return cmCalcDegrees(218.3164477 + 481267.88123421 * nC - .0015786 * nC**2 + (nC**3 / 538841) - (nC**4 / 65194000))
# End Def

def cmLunarLatitude (nMoment: float) -> float:
#
# Return the Latitude of the Moon
#
   nC = cmJulianCenturies(nMoment)
   nMeanMoon = cmMeanLunarLongitude(nC)
   nElongation = cmLunarElongation(nC)
   nSolarAnomaly = cmSolarAnomaly(nC)
   nLunarAnomaly = cmLunarAnomaly(nC)
   nMoonFromNode = cmMoonNode(nC)
   nE = 1 - .002516 * nC - .0000074 * nC**2
   nVenus = .000175 * (cmSinDegrees(119.75 + (nC * 131.849) + nMoonFromNode) +  cmSinDegrees(119.75 + (nC * 131.849) - nMoonFromNode))
   nFlatEarth = (-.002235 * cmSinDegrees(nMeanMoon)) + (.000127 * cmSinDegrees(nMeanMoon - nLunarAnomaly)) + (-.000115 * cmSinDegrees(nMeanMoon + nLunarAnomaly))
   nExtra = .000382 * cmSinDegrees(313.45 + nC * 481266.484)
   nCorrection = cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,5128122,0,0,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,277693,0,0,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,55413,2,0,-1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,32573,2,0,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,9266,2,0,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,8216,2,-1,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,4200,2,0,1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2463,2,-1,-1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2065,2,-1,-1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,1828,4,0,-1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1749,0,0,0,3) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1491,1,0,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1410,0,1,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1335,1,0,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,1021,4,0,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,777,0,0,1,-3) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,607,2,0,0,-3) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,491,2,-1,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,439,0,0,3,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,421,2,0,-3,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-351,2,1,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,315,2,-1,1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-283,0,0,1,3) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,223,1,1,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-220,0,1,-2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-185,1,0,1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-177,0,1,2,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,166,4,-1,-1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,132,4,0,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,115,4,-1,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,280602,0,0,1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,173237,2,0,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,46271,2,0,-1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,17198,0,0,2,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,8822,0,0,2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,4324,2,0,-2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-3359,2,1,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,2211,2,-1,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1870,0,1,-1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1794,0,1,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1565,0,1,-1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1475,0,1,1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-1344,0,1,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,1107,0,0,3,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,833,4,0,-1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,671,4,0,-2,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,596,2,0,2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-451,2,0,-2,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,422,2,0,2,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-366,2,1,-1,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,331,4,0,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,302,2,-2,0,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-229,2,1,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,223,1,1,0,1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-220,2,1,-1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,181,2,-1,-2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,176,4,0,-2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-164,1,0,1,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,-119,1,0,-2,-1) \
                + cmSumLunarPeriods(nE,nElongation,nSolarAnomaly,nLunarAnomaly,nMoonFromNode,107,2,-2,0,1)
   nCorrection = .000001 * nCorrection
   return cmCalcDegrees(nCorrection + nVenus + nFlatEarth + nExtra)
# End Def

def cmMoonRise (nUniversalDays: int, nLatitude: float, nLongitude: float, nElevation: float, ntimezone: str, nType: bool):
#
# Moonrise Times for one day in ntimezone
#
   MoonRiseList = []
   nOneHour = 1 / 24
   nLower = nDays
   nUpper = nDays + 1
   nLowerStarting = nLower
   nUpperStarting = nUpper
   if nType == GEOCENTRIC:
      nLastAltitude = cmGeocentricLunarAltitude(nLower,nLatitude,nLongitude)
   else:
      nLastAltitude = cmTopocentricLunarAltitude(nLower,nLatitude,nLongitude,nElevation)
   nRise1 = 0
   nRise2 = 0
   nPrecision = ONE_SECOND / ONE_DAY
   bLoop = True
#
# Find hour of rising
#
   while bLoop == True:
      nHour = nLower + nOneHour
      nApprox = nHour
      if nType == GEOCENTRIC:
         nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
      else:
         nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
#
# Have we found the hour of rising?
#
      if (0 > nLastAltitude) and (0 < nCurrentAltitude):
#
# Binary Search within the hour of rising
#
         nUpper = nApprox
         if nType == GEOCENTRIC:
            nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
            nLastAltitude = cmGeocentricLunarAltitude(nLower,nLatitude,nLongitude)
         else:
            nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
            nLastAltitude = cmTopocentricLunarAltitude(nLower,nLatitude,nLongitude,nElevation)
         while (nUpper - nLower) > nPrecision:
            if (0 > nLastAltitude) and (0 < nCurrentAltitude):
#
# Use lower range
#
               nUpper = nApprox
               nApprox = nLower + ((nUpper - nLower) * .5)
               if nType == GEOCENTRIC:
                  nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
               else:
                  nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
            else:
#
# Use upper range
#
               nLower = nApprox
               nLastAltitude = nCurrentAltitude
               nApprox = nLower + ((nUpper - nLower) * .5)
               if nType == GEOCENTRIC:
                  nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
               else:
                  nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
#
# Is rise standard time within the day requested?
#
         if nApprox >= nLowerStarting and nApprox < nUpperStarting:
#
# Rise may occur twice in the same day at latitudes above approximately 61.5 degrees North or South
#
            if nRise1 == 0:
               nRise1 = nApprox
               if nType == GEOCENTRIC:
                 nLastAltitude = cmGeocentricLunarAltitude(nHour + nOneHour * 3,nLatitude,nLongitude)
               else:
                 nLastAltitude = cmTopocentricLunarAltitude(nHour + nOneHour * 3,nLatitude,nLongitude,nElevation)
               nHour = nHour + nOneHour * 4
#
# Second rise found, end search
#
            else:
               nRise2 = nApprox
               bLoop = False
         else:
#
# Event did not occur
#
            bLoop = False
      else:
         nLastAltitude = nCurrentAltitude
         nLower = nApprox
      if bLoop == True and nHour >= nUpper:
         bLoop = False
   if nRise1 != 0:
      MoonRiseList.append(cmStandardFromUniversal(nRise1,ntimezone))
   if nRise2 != 0:
      MoonRiseList.append(cmStandardFromUniversal(nRise2,ntimezone))
   return MoonRiseList
# End Def

def cmMoonSet (nUniversalDays: int, nLatitude: float, nLongitude: float, nElevation: float, ntimezone: str, nType: bool):
#
# Moonset Times for one day in ntimezone
#
   MoonSetList = []
   nOneHour = 1 / 24
   nLower = nDays - 1
   nUpper = nDays
   nLowerStarting = nLower
   nUpperStarting = nUpper
   if nType == GEOCENTRIC:
      nLastAltitude = cmGeocentricLunarAltitude(nLower,nLatitude,nLongitude)
   else:
      nLastAltitude = cmTopocentricLunarAltitude(nLower,nLatitude,nLongitude,nElevation)
   nSet1 = 0
   nSet2 = 0
   nPrecision = ONE_SECOND / ONE_DAY
   bLoop = True
#
# Find hour of setting
#
   while bLoop == True:
      nHour = nLower + nOneHour
      nApprox = nHour
      if nType == GEOCENTRIC:
         nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
      else:
         nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
#
# Have we found the hour of setting?
#
      if (nLastAltitude > 0) and (nCurrentAltitude < 0):
#
# Binary Search within the hour of setting
#
         nUpper = nApprox
         if nType == GEOCENTRIC:
            nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
            nLastAltitude = cmGeocentricLunarAltitude(nLower,nLatitude,nLongitude)
         else:
            nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
            nLastAltitude = cmTopocentricLunarAltitude(nLower,nLatitude,nLongitude,nElevation)
         while (nUpper - nLower) > nPrecision:
            if (nLastAltitude > 0) and (nCurrentAltitude < 0):
#
# Use lower range
#
               nUpper = nApprox
               nApprox = nLower + ((nUpper - nLower) * .5)
               if nType == GEOCENTRIC:
                  nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
               else:
                  nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
            else:
#
# Use upper range
#
               nLower = nApprox
               nLastAltitude = nCurrentAltitude
               nApprox = nLower + ((nUpper - nLower) * .5)
               if nType == GEOCENTRIC:
                  nCurrentAltitude = cmGeocentricLunarAltitude(nApprox,nLatitude,nLongitude)
               else:
                  nCurrentAltitude = cmTopocentricLunarAltitude(nApprox,nLatitude,nLongitude,nElevation)
#
# Is setting time within the day requested?
#
         if nApprox >= nLowerStarting and nApprox < nUpperStarting:
#
# Setting may occur twice in the same day at latitudes above approximately 61.5 degrees North or South
#
            if nSet1 == 0:
               nSet1 = nApprox
               if nType == GEOCENTRIC:
                 nLastAltitude = cmGeocentricLunarAltitude(nHour + nOneHour * 3,nLatitude,nLongitude)
               else:
                 nLastAltitude = cmTopocentricLunarAltitude(nHour + nOneHour * 3,nLatitude,nLongitude,nElevation)
               nHour = nHour + nOneHour * 4
#
# Second rise found, end search
#
            else:
               nSet2 = nApprox
               bLoop = False
         else:
#
# Event did not occur
#
            bLoop = False
      else:
         nLastAltitude = nCurrentAltitude
         nLower = nApprox
      if bLoop == True and nHour >= nUpper:
         bLoop = False
   if nSet1 != 0:
      MoonSetList.append(cmStandardFromUniversal(nSet1,ntimezone))
   if nSet2 != 0:
      MoonSetList.append(cmStandardFromUniversal(nSet2,ntimezone))
   return MoonSetList
# End Def

def cmHinduLunarOnOrBefore (nMonth1: int, nLeapMonth1: bool, nDay1: int, nLeapDay1: bool, nYear1: int, nMonth2: int, nLeapMonth2: bool, nDay2: int, nLeapDay2: bool, nYear2: int) -> bool:
#
# Check for Hindu Lunar holidays in leap months, and, possible expunged days
#
   return (nYear1 < nYear2) or \
      (nYear1 == nYear2 and \
      (nMonth1 < nMonth2 or \
      (nMonth1 == nMonth2 and \
      ((nLeapMonth1 == True and nLeapMonth2 == False) or \
      (nLeapMonth1 == nLeapMonth2 and \
      (nDay1 < nDay2 or \
      (nDay1 == nDay2 and (nLeapDay1 == False or nLeapDay2 == True))))))))
# End Def

def cmHinduDateOccur (nMonth: int, nDay: int, nYear: int) -> int:
#
# Compute day on which an event is observed
#
   nTry = DaysFromHinduLunar(nMonth,False,nDay,False,nYear)
   if nDay > 15:
      MidLunarDate = HinduLunarFromDays(nTry - 5)
   else:
      MidLunarDate = HinduLunarFromDays(nTry)
   bExpunged = nMonth != MidLunarDate[0]
   nOccurDate = nTry
   if bExpunged == True:
      bLoop = True
      while bLoop == True:
        HinduLoopDate = HinduLunarFromDays(nOccurDate)
        if cmHinduLunarOnOrBefore(HinduLoopDate[0],HinduLoopDate[1],HinduLoopDate[2],HinduLoopDate[3],HinduLoopDate[4],MidLunarDate[0],MidLunarDate[1],nDay,False,MidLunarDate[4]) == False:
           nOccurDate = nOccurDate + 1
        else:
           nOccurDate = nOccurDate - 1
           bLoop = False
   else:
      HinduLunarDate = HinduLunarFromDays(nOccurDate)
      if nDay != HinduLunarDate[2]:
         nOccurDate = nOccurDate - 1
   return nOccurDate
# End Def

def cmHinduTithiOccur (nMonth: int, nTithi: float, nTime: float, nYear: int) -> int:
#
# Tithi time of day
#
  nApprox = cmHinduDateOccur(nMonth,cmFloor(nTithi),nYear)
  nLunar = cmHinduLunarDayAtOrAfter (nTithi,nApprox - 2)
  nTry = cmFloor(nLunar)
  nT = cmStandardFromSunDial(nTry + nTime)
  if (nLunar <= nT) or (cmHinduLunarPhase(cmStandardFromSunDial(nTry + 1 + nTime)) > nTithi * 12):
     return nTry
  else:
     return nTry + 1
# End Def

def cmHinduLunarEvent (nMonth: int, nTithi: float, nTime: float, nGregorianYear: int) -> int:
#
# Occurence of Hindu Lunar Event
#
   nJan1 = date(nGregorianYear,January,1).toordinal()
   nDec31 = date(nGregorianYear,December,31).toordinal()
   HinduLunarDate = HinduLunarFromDays(nJan1)
   nDate0 = cmHinduTithiOccur(nMonth,nTithi,nTime,HinduLunarDate[4])
   nDate1 = cmHinduTithiOccur(nMonth,nTithi,nTime,HinduLunarDate[4] + 1)
   if nDate0 >= nJan1 and nDate0 <= nDec31:
      return nDate0
   else:
      return nDate1
# End Def

def cmDiwali (nGregorianYear: int) -> date:
#
# Diwali in nGregorianYear
#
   nDiwali = cmHinduLunarEvent(KARTIKA,1,0,nGregorianYear)
   HinduLunarDate = HinduLunarFromDays(nDiwali)
   if HinduLunarDate[1] == True:
      nNewMoon = cmStandardFromUniversal(cmLunarPhaseAtOrBefore(nDiwali - 15,NEWMOON),HinduLocaleZone)
      nDiwali = cmFloor(nNewMoon - 1)
   else:
      nNewMoon = cmStandardFromUniversal(cmLunarPhaseAtOrBefore(nDiwali + 5,NEWMOON),HinduLocaleZone)
#
# If New Moon is before or equal to 6pm and the month KARTIKA isn't a leap month, Diwali is the prior day
#
   if cmMod(nNewMoon,1) <= .75 and HinduLunarDate[1] == False:
      nDiwali = nDiwali - 1
   elif HinduLunarDate[1] == False:
#
# If Lunar Day (Tithi) starts on after 6pm, Diwali is the prior day
#
      nSunRise = cmHinduSunRise(nDiwali)
      nTithi = cmCalcDegrees((cmHinduLunarLongitude(nSunRise) - cmHinduSolarLongitude(nSunRise))) / 12
      if cmMod(nSunRise - (1 - cmMod(nTithi,1)),1) >= .75:
         nDiwali = nDiwali - 1
   return date.fromordinal(nDiwali)
# End Def

def cmHoli (nGregorianYear: int) -> date:
#
# Holi in nGregorian Year
#
   nMonthEnd = cmHinduLunarEvent(PHALGUNA,29,0,nGregorianYear)
   nFullMoon = cmStandardFromUniversal(cmLunarPhaseAtOrBefore(nMonthEnd,FULLMOON),HinduLocaleZone)
   nDays = cmFloor(nFullMoon)
   nSunSet = cmHinduSunSet(cmFloor(nFullMoon))
   nTithi = cmCalcDegrees(cmHinduLunarLongitude(cmHinduSunSet(cmFloor(nSunSet)) - cmHinduSolarLongitude(cmFloor(nSunSet)))) / 12
   if nFullMoon >= nSunSet:
      nDays = nDays + 1
   elif (cmMod(nTithi,1) >= .75):
      nDays = nDays + 1
   return date.fromordinal(nDays)
# End Def

pyNow = CurrentDate()
#pyNow = date(2026,3,3)
print ("Today: " + str(pyNow))
nDays = pyNow.toordinal()
print ("Today's Ordinal Days: " + str(nDays))
print ("Hindu Location: " + HinduLocaleName)
dtSunRise = cmTimeFromSerial(cmMomentToSerial(cmHinduSunRise(nDays)))
print ("Sunrise: " + f"{dtSunRise.hour:02d}" + ':' + f"{dtSunRise.minute:02d}")
dtSunSet = cmTimeFromSerial(cmMomentToSerial(cmHinduSunSet(nDays)))
print ("Sunset: " + f"{dtSunSet.hour:02d}" + ':' + f"{dtSunSet.minute:02d}") 
MoonRiseList = cmMoonRise(nDays,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,HinduLocaleZone,TOPOCENTRIC)
if len(MoonRiseList) > 0:
   dtMoonRise = cmTimeFromSerial(cmMomentToSerial(MoonRiseList[0]))
   print ("Moonrise: " + f"{dtMoonRise.hour:02d}" + ':' + f"{dtMoonRise.minute:02d}")
else:
   print ("Moonrise: Did not occur")
MoonSetList = cmMoonSet(nDays,HinduLocaleLatitude,HinduLocaleLongitude,HinduLocaleElevation,HinduLocaleZone,TOPOCENTRIC)
if len(MoonSetList) > 0:
   dtMoonSet = cmTimeFromSerial(cmMomentToSerial(MoonSetList[0]))
   print ("Moonset: " + f"{dtMoonSet.hour:02d}" + ':' + f"{dtMoonSet.minute:02d}")
else:
   print ("Moonset: Did not occur")
HinduSolarDate = HinduSolarFromDays(nDays)
print ('Hindu Solar Date: ' + SolarMonthNames[HinduSolarDate[0] - 1] + ' ' + str(HinduSolarDate[1]) + ', ' + str(HinduSolarDate[2]))
print ('Days from Hindu Solar: ' + str(DaysFromHinduSolar(HinduSolarDate[0],HinduSolarDate[1],HinduSolarDate[2])))
HinduLunarDate = HinduLunarFromDays(nDays)
print ('Hindu Yoga: ' + HinduYogaName[cmHinduYoga(nDays) - 1])
print ('Hindu Lunar Date: ' + FormatHinduLunarDate(HinduLunarDate[0],HinduLunarDate[1],HinduLunarDate[2],HinduLunarDate[3],HinduLunarDate[4],HinduLunarDate[5]))
print ('Days from Hindu Lunar: ' + str(DaysFromHinduLunar(HinduLunarDate[0],HinduLunarDate[1],HinduLunarDate[2],HinduLunarDate[3],HinduLunarDate[4])))
print ('')
print ('Hindu Holidays during Gregorian Year ' + str(pyNow.year))
print ('')
print ('Mesha Sankranti (Solar New Year): ' + str(date.fromordinal(cmFloor(cmHinduSolarLongitudeAtOrAfter(0,date(pyNow.year,January,1).toordinal())))))
print ('Chandramana Ugadi (Lunar New Year): ' + str(cmHinduLunarNewYear(pyNow.year)))
print ('Diwali: ' + str(cmDiwali(pyNow.year)))
print ('Holi: ' + str(cmHoli(pyNow.year)))
