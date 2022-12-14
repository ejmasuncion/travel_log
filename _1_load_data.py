
from datetime import datetime
import pandas as pd
pd.set_option('display.max_columns', 500)
import matplotlib
import time
from shutil import get_terminal_size
pd.set_option('display.width', get_terminal_size()[0])
import pickle
import numpy as np
import datetime as dt

pd.options.display.float_format = '{:,.0f}'.format


class Load_Data:

    def __init__(self):
        self.raw_hotel_data = pickle.load(open("data/merged_hotel_data_withprice.pkl", "rb"))
        self.raw_hotel_data=self.raw_hotel_data.replace(r'^\s*$', np.nan, regex=True)
        #self.hotel_level_df=pickle.load(open("data/!ml_dataset_hotel_level_v2.pkl", "rb"))
        #self.client = RESTClient(self.API_KEY) # api_key is used
        

    def pp_raw_hotel_data (self):
        df=self.raw_hotel_data
        df["review_score"]=df["review_score"].apply(lambda x: float(x.strip()))
        df["nights_stayed_"]=df["nights_stayed"].apply(lambda x: int(x.strip().split(" ")[0]))

        month_map = {'January':1, 'February':2, 'March':3 , 'April':4, 'May':5, 'June':6,
                    'July':7, 'August':8 , 'September':9, 'October':10, 'November':11, 'December':12}

        df['date_stayed']=df['month_stayed'].apply(lambda x: dt.datetime(int(x.strip().split(" ")[1]),month_map[x.strip().split(" ")[0]],1))
        df['month_name'] = df['month_stayed'].apply(lambda x: x.strip().split(" ")[0])
        df['month'] = df['month_name'].map(month_map)
        df['year'] = df['month_stayed'].apply(lambda x: x.strip().split(" ")[1])


        df['date_reviewed_']=df['date_reviewed'].apply(lambda x: dt.datetime(int(x.strip().split(" ")[1]),month_map[x.strip().split(" ")[0]],1))
        df['month_name_reviewed'] = df['date_reviewed'].apply(lambda x: x.strip().split(" ")[0])
        df['month_reviewed'] = df['month_name_reviewed'].map(month_map)
        df['year_reviewed'] = df['date_reviewed'].apply(lambda x: x.strip().split(" ")[1])

        traveller_cols=['name','occupant_type','from_country',"room_type",'nights_stayed_',
                #'month_stayed',"'date_reviewed',",
                'date_stayed','month','year','month_name',
                'date_reviewed_','month_reviewed','year_reviewed',
                'review_score']

        df_tr=df[traveller_cols]
        df_tr["good_review"]=np.where(df_tr["review_score"]>=7.5,1,0)

        return df_tr


    # def get_hotel_level_df(self):
    #     return self.hotel_level_df





if __name__=='__main__':
    
    dl=Load_Data()
    print(dl.pp_raw_hotel_data())



