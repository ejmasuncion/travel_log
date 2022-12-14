import streamlit as st
import pandas as pd
import geopy
import pickle
from geopy.geocoders import Nominatim
# from sklearn.preprocessing import MinMaxScaler
# from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
# from sklearn.ensemble import GradientBoostingClassifier
# from imblearn.pipeline import Pipeline, make_pipeline
# from imblearn.over_sampling import SMOTE


class Classifier():    
    def get_nationality(x):
        if x == 'Filipino':
            return 0
        else:
            return 1

    def get_occupant(x):
        if x == 'Solo Traveler':
            return 1
        elif x == 'Couple':
            return 2
        elif x == 'Family':
            return 3
        elif x == 'Group':
            return 4

    def get_lat_long(x):
        geolocator = Nominatim(user_agent="http")
        location = geolocator.geocode(x)
        lat = location.latitude
        long = location.longitude
        return lat, long

    def input_features(STA, NAT, PRC, ENT, BDK, OCT, LAT, LON, NON, OTF, BTK, SRK, CWA, DNA, TOP):
        data = {
            'stars': STA,
            'nationality': NAT,
            'price': PRC,
            'ent_amenities': ENT,
            'bedroom_keys': BDK,
            'occupant': OCT,
            'latitude': LAT,
            'longitude': LON,
            'number_nights': NON,
            'other_amenities': OTF,
            'bathroom_keys': BTK,
            'security_keys': SRK,
            'Count_Walkable_Attractions': CWA,
            'Distance_To_Nearest_Airport': DNA,
            'total_price': TOP
        }
        features = pd.DataFrame(data, index=[0])
        return features
    
    def model_fit(input_holdout):
        sav_file = open('data/best_model_gradientboosting1.sav', 'rb')
        model=pickle.load(sav_file)
        sav_file.close()

        prediction = model.predict_proba(input_holdout)[:,1] >= 0.7
        # prediction = model.predict(input_holdout)

        if prediction[0] == 0:
            return ('Negative Experience')
        else:
            return('Positive Experience')
                                                              
