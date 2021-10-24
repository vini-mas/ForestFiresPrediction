import inmet

def format_hour(hour):
    return hour[0] + hour[1] + "00"

class Fire:
    def __init__(self, day, hour, city, bioma, days_without_rain, precipitation, fire_risk, latitude, longitude, frp, inmet):
        #add the rest of the data
        self.day = day
        self.hour = hour
        self.city = city
        self.bioma = bioma
        self.days_without_rain = days_without_rain
        self.precipitation = precipitation
        self.fire_risk = fire_risk
        self.latitude = latitude
        self.longitude = longitude
        self.frp = frp
        self.inmet = inmet

    @staticmethod
    def init(row):
        list_day_hour = row[0].split(" ")
        day = list_day_hour[0]
        hour = format_hour(list_day_hour[1])
        state = row[3].upper()
        city = row[4].upper()
        bioma = row[5].upper()
        days_without_rain = row[6]
        precipitation = row[7]
        fire_risk = row[8]
        latitude = row[9]
        longitude = row[10]
        frp = row[11]
        fire = Fire(day, hour, city, bioma, days_without_rain, precipitation, fire_risk, latitude, longitude, frp, None)
        return fire

    def __str__(self):
        return ("Day: "+ self.day + " \nHour: " + self.hour + " \nCity: " + self.city +
                " \nBioma: " + self.bioma + " \nDays Without Rain: " + self.days_without_rain + 
                " \nPrecipitation: " + self.precipitation + " \nFire Risk: " + self.fire_risk +
                " \nLatitude: " + self.latitude + " \nLongitude: " + self.longitude +
                " \nfrp: " + self.frp)