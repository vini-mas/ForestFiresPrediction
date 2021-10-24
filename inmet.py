class Inmet():
    def __init__(self, day, hour, city):
        self.day = day
        self.hour = hour
        self.city = city

    def __str__(self):
        return ("Day: "+ self.day + " \nHour: " + self.hour + " \nCity: " + self.city)