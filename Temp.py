import requests, json
base_url = "http://api.weatherapi.com/v1/future.json?"

def getparams(CITY):
    CITY = "jaipur"
    average_temp =0
    average_humd = 0
    count=0
    from datetime import date
    from dateutil.relativedelta import relativedelta

    for i in range(15 , 105):
        six_months = date.today() + relativedelta(days=i)
        URL = base_url + "q=" + CITY + "&dt=" + str(six_months) + "&key=" + "7d6b546322884fce8c0134601231102"
        respons = requests.get(URL)
        response = respons.json()
        listi = response["forecast"]["forecastday"][0]
        average_temp = average_temp + listi["day"]["avgtemp_c"]
        average_humd += listi["day"]["avghumidity"]
        count=count+1
    return {"avg_temp":(average_temp/count),"avg_humid":(average_humd/count)}