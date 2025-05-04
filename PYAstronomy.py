########################################################################################
# File: PYAstronomy.py
# Contents: Astronomical Solar, Lunar Calculations
# Version: 1.11
# Python Version: 3.13
# Date: 2025-05-04
# By: Rick Kelly
# Email: rk55911@outlook.com
# ########################################################################################

#
# A moment is a double precision value representing the days since January 1, 1
# with the fractional part representing a portion of one day.

# Calculations involving astronomical events use algorithms that are fairly precise
# within +- 2000 years or so. Outside that range, errata increase the farther from
# that range. Rise and Set times are +- 10 min or so from published values

from datetime import datetime, date, timezone, timedelta
from dateutil.relativedelta import relativedelta
from zoneinfo import ZoneInfo
from tzlocal import get_localzone
import pytz
import math

# Global Variables

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

# Time

ONE_DAY = 86400000   # Milliseconds in a day
ONE_HOUR = 3600000   # Milliseconds in a hour
ONE_MINUTE = 60000   # Milliseconds in a minute
ONE_SECOND = 1000    # Milliseconds in a second

# Astronomical definitions

SPRING = 0
SUMMER = 90
AUTUMN = 180
WINTER = 270
J2000 = 730120.5   # January 1, 2000 at noon
SUNRISE_SUNSET_TIME = 0
CIVIL_TWILIGHT_TIME = 6 
NAUTICAL_TWILIGHT_TIME = 12
ASTRONOMICAL_TWILIGHT_TIME = 18
MORNING = True
EVENING = False
SUNRISE_SUNSET_TIME = 0
CIVIL_TWILIGHT_TIME = 6 
NAUTICAL_TWILIGHT_TIME = 12
ASTRONOMICAL_TWILIGHT_TIME = 18
NEWMOON = 0
FIRSTQUARTERMOON = 90
FULLMOON = 180
LASTQUARTERMOON = 270
GEOCENTRIC = True
TOPOCENTRIC = False

VisibleHorizon = 0.8413147543981382   # Half diameter of the sun (16 minutes + 34.478885263888294 minutes for refraction)
MeanSynodicMonth = 29.530588861   # Mean time from new moon to new moon

def CurrentDate () -> datetime:
#
# Retrieve the current datetime
#
   return datetime.today()
# End Def

def DateTimeToMoment (dt: datetime) -> float:
#
# Convert Python datetime to moment
#
  return dt.toordinal() + (((dt.hour * 3600) + (dt.minute * 60) + (dt.second) + (dt.microsecond / 1000)) / 86400)
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

def cmMeanTropicalYear (nC: float) -> float:
#
# Mean Interval between Vernal Equinoxes
#
   return 365.2421896698 - (.00000615359 * nC)- (.000000000729 * nC**2) + (.000000000264 * nC**3)
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

def cmLocalTimeZoneOffset () -> float:
   return cmTimeZoneOffset(LocalTimeZoneName())
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

def LocalTimeZoneName () -> str:
#
# Return the local time zone name
#
  return get_localzone()
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

def cmUniversalFromStandard (nStandard: float, nZone: float) -> float:
#
# Convert Standard Time to Universal
#
   return nStandard - nZone / 24
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

def cmUniversalFromApparent (nMoment: float, nLongitude: float) -> float:
#
# Convert Apparent time to Universal
#
   return cmUniversalFromLocal(cmLocalFromApparent(nMoment,nLongitude),nLongitude)
# End Def

def cmMidday (nMoment: float, nLongitude: float) -> float:
#
# True middle of a Solar Day
#
   return cmUniversalFromApparent(nMoment + .5,nLongitude)
# End Def

def SunTransitAware (nDays: int, nLongitude: float, nTimezone: str) -> datetime:
#
# Calculate Transit of the Sun at location Locale. 
#
   return cmLocalAwareFromUniversal(cmMidday(nDays,nLongitude),nTimezone)
# End Def

def cmLocalAwareFromUniversal (nUniversal: float, nTimezone: str) -> datetime:
#
# Covert Universal time to Local zone aware time
#
   nSerial = cmMomentToSerial(nUniversal)
   dtLocalNaive = cmTimeFromSerial(nSerial)
   utc_tz = pytz.utc
   dtUtcAware = utc_tz.localize(dtLocalNaive)
   dtLocalAware = dtUtcAware.astimezone(pytz.timezone(str(nTimezone)))
   return dtLocalAware
# End Def

def cmUniversalAwareFromLocal (nLocal: datetime, nTimezone: str) -> datetime:
#
# Covert Local Naive time to Universal zone aware time
#
   dtLocalNaive = datetime(nLocal.year,nLocal.month,nLocal.day,nLocal.hour,nLocal.minute,nLocal.second,nLocal.microsecond)
   utc_tz = pytz.utc
   dtLocalAware = utc_tz.localize(dtLocalNaive)
   dtUtcAware = dtLocalAware.astimezone(pytz.timezone(str(nTimezone)))
   return dtUtcAware
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

def cmJulianCenturies (nMoment: float) -> float:
#
# Julian Centuries since 2000
#
   return (cmDynamicalFromUniversal(nMoment) - J2000) / 36525
#End Def

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

#    nEarthRadius = cmEarthRadius(nLatitude)
#    Function = cCalendarClass.VisibleHorizon _
#             + cmArcCoSineDegrees(nEarthRadius / (nEarthRadius + IIf(nElevation > 0,nElevation,0))) _
#             + cmAngle(0,0,19) * IIf(nElevation > 0,Sqr(nElevation),0)

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

def SeasonalEquinox (nYear: int, nEquinox: int) -> datetime:
#
# Get one of the seasonal equinoxes as a UTC Moment Type
#
   if nEquinox == SPRING:
      nTargetMonth = March
   elif nEquinox == SUMMER:
      nTargetMonth = June
   elif nEquinox == AUTUMN:
      nTargetMonth = September
   else:
      nTargetMonth = December
   nDays = date.toordinal(date(nYear,nTargetMonth,15))
   nMoment = cmSolarLongitudeAfter(nDays,nEquinox)
   return cmLocalAwareFromUniversal(nMoment,LocalTimeZoneName())
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
   nMeanTropicalYear = cmMeanTropicalYear(cmJulianCenturies(nMoment)) / 360
   nEndMoment = nMoment + nMeanTropicalYear * cmCalcDegrees(((nTargetLongitude - cmSolarLongitude(nMoment))))
#
# Calculate lower part of bisection interval
#
   if nMoment > nEndMoment - 5:
      nStartMoment = nEndMoment - 5
   else:
      nStartMoment = nMoment
   nEndMoment = nEndMoment + 5
   nSearch = True
   while nSearch == True:
      nNewMoment = nStartMoment + ((nEndMoment - nStartMoment) * .5)
      nNewLongitude = cmCalcDegrees(cmSolarLongitude(nNewMoment) - nTargetLongitude)
      if nNewLongitude < 180:
         nEndMoment = nNewMoment
      else:
         nStartMoment = nNewMoment
      if nEndMoment - nStartMoment < .00001:
         nSearch = False
   return nStartMoment + ((nEndMoment - nStartMoment) * .5)
# End Def

def cmSolarMeanAnomaly (nC: float) -> float:
#
# Geometric Mean Anomaly of the Sun
#
   return 357.52911 + nC * (35999.05029 - .0001537 * nC)
# End Def

def cmSolarEquationOfCenter (nC: float) -> float:
#
# Equation of Center for the Sun
#
   nMeanAnomaly = (math.pi * cmSolarMeanAnomaly(nC)) / 180
   nSinM = math.sin(nMeanAnomaly)
   nSin2M = math.sin(nMeanAnomaly + nMeanAnomaly)
   nSin3M = math.sin(nMeanAnomaly + nMeanAnomaly + nMeanAnomaly)
   return nSinM * (1.914602 - nC * (.004817 + .000014 * nC)) + nSin2M * (.019993 - .000101 * nC) + nSin3M * .000289
# End Def

def cmEccentricityEarthOrbit (nCenturies: float) -> float:
#
# Eccentricity of Earth's orbit
#
   return .016708634 - nCenturies * (.000042037 + .0000001267 * nCenturies)
# End Def

def cmSolarDistance (nMoment: float) -> float:
#
# Distance between the centers of the Earth and Sun in Astronomical Units
# 1 AU = 149,597,870.691 kilometers or 92,955,807.267433 miles
#
   nC = cmJulianCenturies(nMoment)
   nEccentricity = cmEccentricityEarthOrbit(nC)
   nSolarAnomaly = cmCalcDegrees(357.5291092 + 35999.0502909 * nC - .0001537 * nC**2) + cmSolarEquationOfCenter(nC)
   return (1.000001018 * (1 - nEccentricity**2)) / (1 + nEccentricity * cmCoSineDegrees(nSolarAnomaly))
# End Def

def SolarDistance (nLocal: datetime, nTimezone: str) -> float:
#
# Solar Distance in Kilometers
#
   nUniversal = DateTimeToMoment(cmUniversalAwareFromLocal(nLocal,nTimezone))
   return cmSolarDistance(nUniversal) * 149597870.7
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
      nValue = cmSineOffset(nAlt,nLatitude,nDepression)
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

def SunRiseTimeZone (nDays: int, nTimeZone: str, nLatitude: float, nLongitude: float, nElevation: float, nDepression: float):
#
# Calculate Sunrise at location and timezone aware
#
   Sunrise = []
   nMoment = cmSunRise(nDays,0,nLatitude,nLongitude,nElevation,nDepression)
   if nMoment != 0:
      Sunrise.append(cmLocalAwareFromUniversal(nMoment,nTimeZone))
   return Sunrise
# End Def

def SunSetTimeZone (nDays: int, nTimeZone: str, nLatitude: float, nLongitude: float, nElevation: float, nDepression: float):
#
# Calculate Sunset at location and timezone aware
#
   Sunset = []
   nMoment = cmSunSet(nDays,0,nLatitude,nLongitude,nElevation,nDepression)
   if nMoment != 0:
      Sunset.append(cmLocalAwareFromUniversal(nMoment,nTimeZone))
   return Sunset
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

def LunarDistance (nLocal: datetime, nTimezone: str) -> float:
#
# Lunar Distance in Kilometers
#
  nUniversal = DateTimeToMoment(cmUniversalAwareFromLocal(nLocal,nTimezone))
  return cmLunarDistance(nUniversal) / 1000
# End Def

def LunarIllumination (nLocal: datetime, nTimezone: str) -> float:
#
# Lunar Illumination
#
   nUniversal = DateTimeToMoment(cmUniversalAwareFromLocal(nLocal,nTimezone))
   nMoment = cmDynamicalFromUniversal(cmUniversalFromStandard(nUniversal,cmLocalTimeZoneOffset()))
   nSolarDistance = cmSolarDistance(nMoment) * 149597870.691
   nLunarDistance = cmLunarDistance(nMoment) / 1000
   nLunarLatitude = cmLunarLatitude(nMoment)
   nLunarLongitude = cmLunarLongitude(nMoment)
   nSolarLongitude = cmSolarLongitude(nMoment)
   nLunarPhase = cmCoSineDegrees(nLunarLatitude) * cmCoSineDegrees(nLunarLongitude - nSolarLongitude)
   nLunarPhase = cmArcCoSineDegrees(nLunarPhase)
   nLunarPhase = (nSolarDistance * cmSinDegrees(nLunarPhase)) / (nLunarDistance - (nSolarDistance * cmCoSineDegrees(nLunarPhase)))
   nLunarPhase = math.atan(nLunarPhase)
   nLunarPhase = cmRadiansToDegrees(nLunarPhase)
#
# Normalize to maximum lunar visible half circle
#
   nLunarPhase = cmMod3(nLunarPhase,0,180)
   return (1 + cmCoSineDegrees(nLunarPhase)) / 2
# End Def

def LunarCrescent (nLocal: datetime, nTimezone: str) -> bool:
#
# Check if moon is in a cresent status
#
   nToday = LunarIllumination(nLocal,nTimezone)
   dtTommorrow = nLocal + timedelta (days=1)
   nTommorrow = LunarIllumination(dtTommorrow,nTimezone)
#
# Use next day illumination to determine cresent
#
   if nToday <=5:
      return True
   else:
      return False
# End Def

def LunarWaxing (nLocal: datetime, nTimezone: str) -> bool:
#
# Check if moon is in a waxing status
#
   nToday = LunarIllumination(nLocal,nTimezone)
   dtYesterday = nLocal + timedelta (days=-1)
   nYesterday = LunarIllumination(dtYesterday,nTimezone)
#
# Use yesterday illumination to determine waxing
#
   if nToday > nYesterday:
      return True
   else:
      return False
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

def LunarNewMoonAware (nYear: int, nMonth: int, ntimezone: str) -> datetime:
#
# New Moon in ntimezone
#
   dtFrom = date(nYear,nMonth,1)
   dtTo = dtFrom + relativedelta(months=1)
   doTo = dtTo - timedelta(days=-1)
   nFromDays = dtFrom.toordinal()
   nToDays = dtTo.toordinal()
   nPhase = cmLunarFindPhase (nFromDays,nToDays,NEWMOON)
   if nPhase != 1:
      return cmLocalAwareFromUniversal(nPhase,ntimezone)
   else:
      return datetime.fromordinal(nPhase)
# End Def

def LunarFirstQuarterMoonAware (nYear: int, nMonth: int, ntimezone: str) -> datetime:
#
# First Quarter Moon in ntimezone
#
   dtFrom = date(nYear,nMonth,1)
   dtTo = dtFrom + relativedelta(months=1)
   doTo = dtTo - timedelta(days=-1)
   nFromDays = dtFrom.toordinal()
   nToDays = dtTo.toordinal()
   nPhase = cmLunarFindPhase (nFromDays,nToDays,FIRSTQUARTERMOON)
   if nPhase != 1:
      return cmLocalAwareFromUniversal(nPhase,ntimezone)
   else:
      return datetime.fromordinal(nPhase)
# End Def

def LunarFullMoonAware (nYear: int, nMonth: int, ntimezone: str) -> datetime:
#
# Full Moon in ntimezone
#
   dtFrom = date(nYear,nMonth,1)
   dtTo = dtFrom + relativedelta(months=1)
   doTo = dtTo - timedelta(days=-1)
   nFromDays = dtFrom.toordinal()
   nToDays = dtTo.toordinal()
   nPhase = cmLunarFindPhase (nFromDays,nToDays,FULLMOON)
   if nPhase != 1:
      return cmLocalAwareFromUniversal(nPhase,ntimezone)
   else:
      return datetime.fromordinal(nPhase)
# End Def

def LunarLastQuarterMoonAware (nYear: int, nMonth: int, ntimezone: str) -> datetime:
#
# Last Quarter Moon in ntimezone
#
   dtFrom = date(nYear,nMonth,1)
   dtTo = dtFrom + relativedelta(months=1)
   doTo = dtTo - timedelta(days=-1)
   nFromDays = dtFrom.toordinal()
   nToDays = dtTo.toordinal()
   nPhase = cmLunarFindPhase (nFromDays,nToDays,LASTQUARTERMOON)
   if nPhase != 1:
      return cmLocalAwareFromUniversal(nPhase,ntimezone)
   else:
      return datetime.fromordinal(nPhase)
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

def MoonRiseAware (nUniversalDays: int, nLatitude: float, nLongitude: float, nElevation: float, ntimezone: str, nType: bool):
#
# Moonrise Times for one day in ntimezone
#
   nZoneOffset = cmTimeZoneOffset(ntimezone)
   MoonRiseList = []
   nOneHour = 1 / 24
   nLower = cmUniversalFromStandard(nUniversalDays,nZoneOffset)
   nUpper = cmUniversalFromStandard(nUniversalDays + 1,nZoneOffset)
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
      MoonRiseList.append(cmLocalAwareFromUniversal(nRise1,ntimezone))
   if nRise2 != 0:
      MoonRiseList.append(cmLocalAwareFromUniversal(nRise2,ntimezone))
   return MoonRiseList
# End Def

def MoonSetAware (nUniversalDays: int, nLatitude: float, nLongitude: float, nElevation: float, ntimezone: str, nType: bool):
#
# Moonset Times for one day in ntimezone
#
   nZoneOffset = cmTimeZoneOffset(ntimezone)
   MoonSetList = []
   nOneHour = 1 / 24
   nLower = cmUniversalFromStandard(nUniversalDays,nZoneOffset)
   nUpper = cmUniversalFromStandard(nUniversalDays + 1,nZoneOffset)
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
      MoonSetList.append(cmLocalAwareFromUniversal(nSet1,ntimezone))
   if nSet2 != 0:
      MoonSetList.append(cmLocalAwareFromUniversal(nSet2,ntimezone))
   return MoonSetList
# End Def

pyNow = CurrentDate()
print ("Today: " + str(pyNow))
print ("Local Time Zone: " + str(LocalTimeZoneName()) + " Current UTC offset hours: " + str(cmLocalTimeZoneOffset()))
print ("Solar Distance today: " + str(SolarDistance(pyNow,LocalTimeZoneName())) + " kilometers")
print ("Lunar Distance today: " + str(LunarDistance(pyNow,LocalTimeZoneName())) + " kilometers")
print ("Lunar Illumination today: " + str(LunarIllumination(pyNow,LocalTimeZoneName())))
print ("Lunar Crescent today: " + str(LunarCrescent(pyNow,LocalTimeZoneName())))
print ("Lunar Waxing today: " + str(LunarWaxing(pyNow,LocalTimeZoneName())))
print ("New Moon at: " + str(LunarNewMoonAware(pyNow.year,pyNow.month,LocalTimeZoneName())))
print ("First Quarter Moon at: " + str(LunarFirstQuarterMoonAware(pyNow.year,pyNow.month,LocalTimeZoneName())))
print ("Full Moon at: " + str(LunarFullMoonAware(pyNow.year,pyNow.month,LocalTimeZoneName())))
print ("Last Quarter Moon at: " + str(LunarLastQuarterMoonAware(pyNow.year,pyNow.month,LocalTimeZoneName())))
print ("Spring Equinox: " + str(SeasonalEquinox (pyNow.year,SPRING)))
print ("Summer Equinox: " + str(SeasonalEquinox (pyNow.year,SUMMER)))
print ("Autumn Equinox: " + str(SeasonalEquinox (pyNow.year,AUTUMN)))
print ("Winter Equinox: " + str(SeasonalEquinox (pyNow.year,WINTER)))
#
# For Sunrise/Sunset/Moonrise/Moonset a location profile is needed
#
nLocationName = 'Los Angles International Airport'
nLocationLatitude = 33.942496     # North
nLocationLongitude = -118.408049  # West
nLocationTimezone = 'America/Los_Angeles'
nLocationElevation = 38.95344  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Salt Lake City International Airport'
nLocationTimezone = 'America/Denver'
nLocationLatitude = 40.788393     # North
nLocationLongitude = -111.977773  # West
nLocationElevation = 1289.6  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Des Moines International Airport'
nLocationLatitude = 41.500639     # North
nLocationLongitude = -93.663072  # West
nLocationTimezone = 'America/Chicago'
nLocationElevation = 292  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Newport, Washington'
nLocationLatitude = 48.188056     # North
nLocationLongitude = -117.056944  # West
nLocationTimezone = 'America/Los_Angeles'
nLocationElevation = 691.896  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Miami International Airport'
nLocationLatitude = 25.784167     # North
nLocationLongitude = -80.290116  # West
nLocationTimezone = 'America/New_York'
nLocationElevation = 2.8  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Sydney Kingsford Smith Airport'
nLocationLatitude = -33.94609833 # South
nLocationLongitude = 151.177002  # East
nLocationTimezone = 'Australia/Brisbane'
nLocationElevation = 6.4008  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Minister Pistarini International Airport'
nLocationLatitude = -34.8222 # South
nLocationLongitude = -58.5358  # West
nLocationTimezone = 'America/Buenos_Aires'
nLocationElevation = 20.4216  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'London Heathrow International Airport'
nLocationLatitude = 51.47060012817383 # North
nLocationLongitude = -0.46194100379944  # West
nLocationTimezone = 'Europe/London'
nLocationElevation = 25.2984  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Henri Coanda International Airport'
nLocationLatitude = 44.572161 # North
nLocationLongitude = 26.102178  # East
nLocationTimezone = 'Europe/Bucharest'
nLocationElevation = 96  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Indira Gandhi International Airport'
nLocationLatitude = 28.550421 # North
nLocationLongitude = 77.121765  # East
nLocationTimezone = 'Asia/Calcutta'
nLocationElevation = 220  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Haneda International Airport'
nLocationLatitude = 35.55333 # North
nLocationLongitude = 139.78111  # East
nLocationTimezone = 'Asia/Tokyo'
nLocationElevation = 6  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')
nLocationName = 'Fairbanks International Airport'
nLocationLatitude = 64.815356 # North
nLocationLongitude = -147.856667  # West
nLocationTimezone = 'America/Anchorage'
nLocationElevation = 131.1  # Meters
Sunrise = SunRiseTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunrise) != 0:
   for i in range(len(Sunrise)):
      print ("Sunrise for " + nLocationName + ': ' + str(Sunrise[i]))
else:
   print ("Sunrise for " + nLocationName + ':  did not occur')
print ("Solar Transit: " + str(SunTransitAware(pyNow.toordinal(),nLocationLongitude,nLocationTimezone)))
Sunset = SunSetTimeZone(pyNow.toordinal(),nLocationTimezone,nLocationLatitude,nLocationLongitude,nLocationElevation,SUNRISE_SUNSET_TIME)
if len(Sunset) != 0:
   for i in range(len(Sunset)):
      print ("Sunset for " + nLocationName + ': ' + str(Sunset[i]))
else:
   print ("Sunset for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Geocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Geocentric Moonrise for " + nLocationName + ':  did not occur')
MoonRise = MoonRiseAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonRise) != 0:
   for i in range(len(MoonRise)):
      print ("Topocentric Moonrise for " + nLocationName + ': ' + str(MoonRise[i]))
else:
   print ("Topocentric Moonrise for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,GEOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Geocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Geocentric Moonset for " + nLocationName + ':  did not occur')
MoonSet = MoonSetAware(pyNow.toordinal(),nLocationLatitude,nLocationLongitude,nLocationElevation,nLocationTimezone,TOPOCENTRIC)
if len(MoonSet) != 0:
   for i in range(len(MoonSet)):
      print ("Topocentric Moonset for " + nLocationName + ': ' + str(MoonSet[i]))
else:
   print ("Topocentric Moonset for " + nLocationName + ':  did not occur')




















