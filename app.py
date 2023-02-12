import pandas as pd
import numpy as np
from flask import Flask, request
import pickle
from datetime import datetime
import json
### files:
import Temp
rf_normal = pd.read_csv('./datasets/district wise rainfall normal.csv')
agri_data = pd.read_csv('./datasets/agri data.csv')
###

app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

months = ['lol', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'sep', 'oct', 'nov', 'dec']

soil_type = dict({
    'rice': ['alluvial', 'kharif', 6],
    'maize': ['alluvial', 'kharif', 6.4],
    'chickpea': ['alluvial', 'rabi', 6.25],
    'kidneybeans': ['loamy', 'rabi', 6.5],
    'pigeonpeas': ['black', 'kharif', 7.75],
    'mothbeans': ['sandy', 'kharif', 6.66],
    'mungbean': ['loamy black', 'rabi kharif', 6.5],
    'blackgram': ['loamy black', 'rabi kharif', 7.15],
    'lentil': ['loamy', 'rabi', 7.0],
    'pomegranate': ['loamy', 'zaid', 7.5],
    'banana': ['alluvial', 'rabi', 7.0],
    'mango': ['laterite alluvial sandy loam', 'rabi', 6.5],
    'grapes': ['alluvial sandy red', 'rabi', 7.0],
    'watermelon': ['sandy loam', 'kharif', 7.0],
    'muskmelon': ['sandy loam', 'zaid', 7.0],
    'apple': ['loamy', 'kharif', 6.0],
    'orange': ['loamy', 'kharif', 7.0],
    'papaya': ['sandy loam', 'kharif', 6.75],
    'coconut': ['laterite alluvial sandy loam', 'kharif', 6.6],
    'cotton': ['laterite', 'kharif', 6.9],
    'jute': ['loamy', 'kharif', 5.3],
    'coffee': ['volcanic red sandy loam', 'kharif', 6.65]
})

translate = dict({
    'rice': ['Broken Rice'],
    'maize': ['Maize'],
    'chickpea': ['NONE'],
    'kidneybeans': ['NONE'],
    'pigeonpeas': ['Pegeon Pea (Arhar Fali)'],
    'mothbeans': ['NONE'],
    'mungbean': ['Green Gram (Moong)(Whole)'],
    'blackgram': ['Black Gram (Urd Beans)(Whole)'],
    'lentil': ['Lentil (Masur)(Whole)'],
    'pomegranate': ['Pomegranate'],
    'banana': ['Banana', 'Banana - Green'],
    'mango': ['Mango', 'Mango (Raw-Ripe)'],
    'grapes': ['Grapes'],
    'watermelon': ['Water Melon'],
    'muskmelon': ['Karbuja(Musk Melon)'],
    'apple': ['Apple'],
    'orange': ['Orange'],
    'papaya': ['Papaya (Raw)', 'Papaya'],
    'coconut': ['Coconut', 'Tender Coconut'],
    'cotton': ['Cotton'],
    'jute': ['Jute'],
    'coffee': ['NONE']
})

strings = "Andaman and Nicobar', 'Andhra Pradesh', 'Assam', 'Chattisgarh', 'Goa', 'Gujarat', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Karnataka', 'Kerala', 'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya', 'Nagaland', 'Odisha', 'Pondicherry', 'Punjab', 'Rajasthan', 'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh', 'Uttrakhand', 'West Bengal"

strings_dist = "'South Andaman', 'Chittor', 'Kurnool', 'West Godavari', 'Cachar', 'Darrang', 'Dhubri', 'Jorhat', 'Kamrup', 'Sonitpur', 'Bastar', 'Kanker', 'Surajpur', 'North Goa', 'Amreli', 'Anand', 'Bharuch', 'Kachchh', 'Kheda', 'Panchmahals', 'Surat', 'Vadodara(Baroda)', 'Valsad', 'Ambala', 'Faridabad', 'Gurgaon', 'Kurukshetra', 'Mewat', 'Panipat', 'Kangra', 'Kullu', 'Badgam', 'Bangalore', 'Kolar', 'Tumkur', 'Alappuzha', 'Ernakulam', 'Kannur', 'Kasargod', 'Kollam', 'Kottayam', 'Malappuram', 'Thirssur', 'Thiruvananthapuram', 'Anupur', 'Badwani', 'Dhar', 'Dindori', 'Jhabua', 'Khandwa', 'Narsinghpur', 'Sheopur', 'Ahmednagar', 'Buldhana', 'Jalgaon', 'Kolhapur', 'Nagpur', 'Nanded', 'Nashik', 'Pune', 'Satara', 'Sholapur', 'Bishnupur', 'Chandel', 'Imphal East', 'Imphal West', 'Thoubal', 'East Khasi Hills', 'Mokokchung', 'Angul', 'Balasore', 'Bargarh', 'Dhenkanal', 'Gajapati', 'Ganjam', 'Jharsuguda', 'Mayurbhanja', 'Nowarangpur', 'Sundergarh', 'Karaikal', 'Amritsar', 'Barnala', 'Bhatinda', 'Gurdaspur', 'Hoshiarpur', 'Jalandhar', 'Ludhiana', 'Mansa', 'Muktsar', 'Patiala', 'Ropar (Rupnagar)', 'Tarntaran', 'Baran', 'Barmer', 'Bikaner', 'Chittorgarh', 'Jalore', 'Jhalawar', 'Kota', 'Sikar', 'Tonk', 'Coimbatore', 'Cuddalore', 'Dharmapuri', 'Dindigul', 'Erode', 'Kancheepuram', 'Krishnagiri', 'Madurai', 'Nagercoil (Kannyiakumari)', 'Namakkal', 'Ramanathapuram', 'Salem', 'Sivaganga', 'Thanjavur', 'Thiruvannamalai', 'Vellore', 'Villupuram', 'Virudhunagar', 'Hyderabad', 'Karimnagar', 'Khammam', 'Nalgonda', 'Nizamabad', 'Ranga Reddy', 'North Tripura', 'Sepahijala', 'South District', 'Agra', 'Aligarh', 'Allahabad', 'Baghpat', 'Bahraich', 'Ballia', 'Bhadohi(Sant Ravi Nagar)', 'Bulandshahar', 'Chitrakut', 'Etah', 'Etawah', 'Farukhabad', 'Fatehpur', 'Gautam Budh Nagar', 'Ghaziabad', 'Jalaun (Orai)', 'Jhansi', 'Kannuj', 'Kanpur', 'Khiri (Lakhimpur)', 'Lakhimpur', 'Mahoba', 'Mau(Maunathbhanjan)', 'Mirzapur', 'Muradabad', 'Muzaffarnagar', 'Raebarelli', 'Rampur', 'Saharanpur', 'Shahjahanpur', 'Sitapur', 'Sonbhadra', 'Dehradoon', 'UdhamSinghNagar', 'Bankura', 'Burdwan', 'Hooghly', 'Jalpaiguri', 'Malda', 'Medinipur(W)', 'Murshidabad', 'Nadia', 'North 24 Parganas', 'Puruliya', 'Sounth 24 Parganas', 'Uttar Dinajpur'"

los = strings.replace(',', " ").replace("'", '').split("  ")
los2 = strings_dist.replace(',', " ").replace("'", '').split("  ")

state_dict = dict()
for st in los:
    state_dict[st.lower().replace(" ", '')] = st

dist_dict = dict()
for dt in los2:
    dist_dict[dt.lower().replace(" ", '')] = dt

state_rainfall = rf_normal['STATE_UT_NAME'].unique()
state_rf = dict()
for dist in state_rainfall:
    state_rf[dist.lower().replace(" ", "").replace("&", "and")] = dist

dist_rainfall = rf_normal['DISTRICT'].unique()
dist_rf = dict()
for dist in dist_rainfall:
    dist_rf[dist.lower().replace(" ", "")] = dist


def rainfall_pred(state, district, month):
    state = state_rf[state]; district = dist_rf[district]
    rainfall_data = rf_normal[rf_normal['STATE_UT_NAME'] == state][rf_normal['DISTRICT'] == district]
    month = month.lower()
    if month in ['jan', 'feb']:
        return float(rainfall_data['Jan-Feb'].to_numpy()[0])
    elif month in ['mar', 'apr', 'may']:
        return float(rainfall_data['Mar-May'].to_numpy()[0])
    elif month in ['jun', 'jul', 'sep']:
        return float(rainfall_data['Jun-Sep'].to_numpy()[0])
    elif month in ['oct', 'nov', 'dec']:
        return float(rainfall_data['Oct-Dec'].to_numpy()[0])


def predict(n, p, k, t, hu, ph, rainfall):  # n, p, k, temperature, humidity, ph, rainfall
    features = [n, p, k, t, hu, ph, rainfall]
    features = np.array(features)
    prediction = model.predict([features])
    return prediction[0]


def best_market(crop):
    # crop_list = translate[crop]
    price_list = dict()
    for crops in crop:
        mindf = agri_data[agri_data['commodity'] == crops]
        fin = pd.DataFrame()
        fin['market'] = mindf['market']
        fin['state'] = mindf['state']
        fin['district'] = mindf['district']
        fin['modal_price'] = mindf['modal_price']
        fin = fin.sort_values(by='modal_price', ascending=False)
        price_list = {
            'state': fin['state'].iloc[:3].to_list(),
            'district': fin['district'].iloc[:3].to_list(),
            'market': fin['market'].iloc[:3].to_list(),
            'modal_price': fin['modal_price'].iloc[:3].to_list()
        }
    return price_list


def best_market_2(crop):
    price_list = dict()
    list = dict()
    fin = pd.DataFrame()
    fin['market'] = agri_data['market']
    fin['state'] = agri_data['state']
    fin['district'] = agri_data['district']
    fin['modal_price'] = agri_data['modal_price']
    fin = fin.sort_values(by='modal_price', ascending=False)
    price_list= {
        'state': fin['state'].iloc[:3].to_list(),
        'district': fin['district'].iloc[:3].to_list(),
        'market': fin['market'].iloc[:3].to_list(),
        'modal_price': fin['modal_price'].iloc[:3].to_list()
    }
    return price_list


@app.route('/', methods=['GET'])
def output():
    #### data in:
    data = request.args.to_dict()
    state = str(data['state']).replace(" ", "").lower()
    district = str(data['district']).replace(" ", "").lower()
    n = float(data['n'])
    p = float(data['p'])
    k = float(data['k'])
    ph = float(data['ph'])
    ####

    #### get rainfall data
    rainfall = rainfall_pred(state, district, months[datetime.now().month])
    if (type(rainfall) == None): rainfall = 103.46365541576817
    print(rainfall)
    ####

    ### temp and hu
    temp_hu = dict()
    temp_hu = Temp.getparams(district)
    if (type(temp_hu) == None): temp_hu = {'avg_temp': 25.616243851779544, 'avg_humid': 71.48177921778637}
    temp = temp_hu['avg_temp']
    hu = temp_hu['avg_humid']
    print(temp, hu)
    ###

    #### get the prediction
    print(n, p, k, temp, hu, ph, rainfall)
    crop = predict(n, p, k, temp, hu, ph, rainfall)  # n, p, k, temperature, humidity, ph, rainfall
    print(crop)
    crop_list = translate[crop]
    print(crop_list)
    lis = []
    soil_det = soil_type[crop]
    for crops in crop_list:
        out = dict()
        name = crops
        dict1 = dict()
        if crops == "NONE":
            name = crop
            ### from the biggest market 2
            dict1 = best_market_2(crop)
            ###
        else:
            dict1 = best_market(crops)
        state = dict1['state']
        district = dict1['district']
        market = dict1['market']
        modal_price = dict1['modal_price']
        out = {
            'Name': name,
            'Soil': soil_det[0],
            'Harvest Kind': soil_det[1],
            'pH': soil_det[2],
            'State': state,
            'District': district,
            'Market': market,
            'Modal_Price': modal_price
        }
        lis.append(out)
    test = predict(90, 43, 42, 20.87974371, 82.00274423, 6.502985292000001, 202.9355362)
    print(test)
    return json.dumps(lis, indent=2)

if __name__ == '__main__':
    app.run(debug = True)