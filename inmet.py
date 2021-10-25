import json

def format_hour(hour):
    return hour[0] + hour[1] + "00"

class Inmet():
    def __init__(self, day, hour, city, temp, umidade, vento):
        self.day = day
        self.hour = hour
        self.city = city
        self.temperatura = temp
        self.vento = vento
        self.umidade_ar = umidade

    @staticmethod
    def init(row, city):
        day = row[0]
        hour = format_hour(row[1])
        temperatura_max = row[9]
        umidade_ar = row[15]
        vento = row[18]

        inmet = Inmet(day, hour, city, temperatura_max, umidade_ar, vento)
        return inmet

    def to_csv_header(self):
        return ['temperatura', 'vento', 'umidade_ar']

    def to_csv(self):
        b = [self.__dict__[attr] for attr in self.to_csv_header()]
        return b

    def __str__(self):
        return json.dumps(self.__dict__, indent=True)
        # return ("Day: "+ self.day + " \nHour: " + self.hour + " \nCity: " + self.city)