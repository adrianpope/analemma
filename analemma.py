import pysolar.solar as PS
import datetime as DT
import numpy as N

class Analemma:
    def __init__(self, latitude=41.1190631, longitude=-83.2225659, offsetHoursUTC=-5.0, year=2021):
        # defaults to EST in Tiffin, OH, USA for 2021
        self.lat = latitude
        self.lon = longitude
        hour = DT.timedelta(hours=1.0)
        self.td = offsetHoursUTC*hour
        self.dayZero = DT.datetime(year, 1, 1, tzinfo=DT.timezone.utc)
        
    def getTimeFromLocal(self, dayOfYear, localStandardTimeHours24):
        # generate UTC datetime object from local day and time
        # day is meant to be integer, should check that
        # local time is floating point
        day = DT.timedelta(days=1)
        hour = DT.timedelta(hours=1)
        time = self.dayZero + int(dayOfYear)*day + localStandardTimeHours24*hour - self.td
        return time
    
    def getAltAz(self, dayOfYear, localStandardTimeHours24):
        # (alt, az) tuple from scalar local day and time
        time = self.getTimeFromLocal(dayOfYear, localStandardTimeHours24)
        alt = PS.get_altitude(self.lat, self.lon, time)
        az = PS.get_azimuth(self.lat, self.lon, time)
        return (alt, az)
    
    def fixedTime(self, localTime, dayList):
        # fixed local time of day
        # iterable days
        # returns list of datetime objects
        return list(map(lambda x: self.getTimeFromLocal(x, localTime), dayList))
    
    def fixedDay(self, day, localTimeList):
        # fixed day of year
        # iterable local times
        # returns list of datetime objects
        return list(map(lambda x: self.getTimeFromLocal(day, x), localTimeList))
    
    def getAltitudes(self, times):
        # input: list of datetime objects
        # output: numpy array of altitudes
        return N.array(list(map(lambda x: PS.get_altitude(self.lat, self.lon, x), times)))
    
    def getAzimuths(self, times):
        # input: list of datetime objects
        # output: numpy array of azimuths
        # azimuths measured clockwise from North
        return N.array(list(map(lambda x: PS.get_azimuth(self.lat, self.lon, x), times)))
    
    def shadowGroundEastNorth(self, alt, az, h=1.0):
        degree = N.pi/180.0
        length = 1.0/N.tan(alt*degree)
        east = -1.0*length*N.sin(az*degree)
        north = -1.0*length*N.cos(az*degree)
        return h*east, h*north
    
    def shadowWallRightUp(self, altSun, azSun, azWall):
        degree = N.pi/180.0
        azDiff = azSun - azWall
        right = -1.0*N.cos(azDiff*degree)/N.sin(azDiff*degree)
        up = -1.0*N.tan(altSun*degree)/N.sin(azDiff*degree)
        return right, up
    
