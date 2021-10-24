import inmet

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

    def __str__(self):
        return ("Day: "+ self.day + " \nHour: " + self.hour + " \nCity: " + self.city +
                " \nBioma: " + self.bioma + " \nDays Without Rain: " + self.days_without_rain + 
                " \nPrecipitation: " + self.precipitation + " \nFire Risk: " + self.fire_risk +
                " \nLatitude: " + self.latitude + " \nLongitude: " + self.longitude +
                " \nfrp: " + self.frp)