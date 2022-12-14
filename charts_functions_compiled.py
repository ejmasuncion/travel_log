import numpy as np 
import pandas as pd 
import streamlit as st

import seaborn as sns
import matplotlib.pyplot as plt
import datetime as dt
import plotly as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from PIL import Image
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

### ---------------------------------------
import warnings
warnings.filterwarnings('ignore')
import pickle
from _1_load_data import Load_Data
from _2_visuals import Graphs
from _2_chart_functions import Chart_Functions

### ---------------------------------------
dl=Load_Data()
cf=Chart_Functions()
g=Graphs()

df_og=dl.pp_raw_hotel_data()
### ---------------------------------------





#Setup
dl=Load_Data()
cf=Chart_Functions()
g=Graphs()

df_og=dl.pp_raw_hotel_data()


        
# facilities
df_faci = pickle.load(open("data/hotel_level_features.pkl", "rb"))
faci_cols=df_faci.columns.tolist()[15:]
df_faci=df_faci[['hotel_name_'] + faci_cols]

df_faci=df_faci.loc[:,~df_faci.columns.str.contains('_y', case=False)] 

#Drop duplicate values
df_faci.drop(["facilities_count","non-smoking rooms","upper floors accessible by elevator"], axis=1,inplace=True)

df_hotel_level=pickle.load(open("data/hotel_info_final.pkl", "rb"))
df_hotel_level=df_hotel_level[["hotel_name_","review_rating"]]
df_hotel_level

df1=pd.merge(df_faci,df_hotel_level, on="hotel_name_", how="left")
df1['review_rating']=df1['review_rating'].astype(float)
df1['good_review']=np.where(df1["review_rating"]>=7.5,1,0)

def get_long_format_proportions (df_faci):
    df_to_melt=df_faci.drop(["review_rating","good_review"], axis=1)
    long_df = pd.melt(
        df_to_melt,
        id_vars=['hotel_name_'],
        #value_vars=['inc_q', 'age']
    )

    


    grouped=long_df.groupby(["variable"]).agg(
        sum_=('value', 'sum'),
        count_=('hotel_name_', 'count')).sort_values(by="sum_", ascending=False).reset_index()

    grouped["Proportion"]=grouped["sum_"]/grouped["count_"]*100
    return grouped

green=get_long_format_proportions (df1[df1.good_review==1])[["variable","Proportion"]]
red=get_long_format_proportions (df1[df1.good_review==0])[["variable","Proportion"]]

merged=pd.merge(green,red,on="variable", how="outer")
merged.columns=["Variable", "Green_prop","Red_prop"]

merged.set_index("Variable",inplace=True)
min=merged.min(axis=1)
merged=merged.sub(merged.min(axis=1).values, axis='rows')
merged["Min"]=min


data1=merged[[merged.columns[0]]]
data2=merged[[merged.columns[1]]]
data3=merged[["Min"]]
#Return custom Orders
order=data3.sort_values(by="Min",ascending=False).index
order_green=data1.sort_values(by=merged.columns[0],ascending=False).index
order_red=data2.sort_values(by=merged.columns[1],ascending=False).index

class charts:

    def time_series_initial():
        g.plot_reviews_timeseries()
    
    def local_vs_foreign():
        mapping_dict={1:"Good Review",0: "Bad Review"}
        countries_to_include = ["Philippines"]
        
        
        
        list_for_data=cf.categorical_eda_plots_plotly(df_og,"from_country",
                                            target_mapping=mapping_dict,
                                            column_mapping_list=countries_to_include,others_name="Foreign",
                                            hue="good_review", 
                                            time_series=False,  
                                            #ax=ax1,
                                             )
        
        
        data1,data2,data3,order,order_green, order_red=list_for_data
        
        fig = px.subplots.make_subplots(rows=1, cols=1,
        #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        fig.add_trace(go.Bar(x=data3.index, y=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,),row=1, col=1)
        fig.add_trace(go.Bar(x=data1.index, y=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green"),row=1, col=1)
        fig.add_trace(go.Bar(x=data2.index, y=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red"),row=1, col=1)
        
        
        cf.layout_v1(fig,"Local vs Foreign",500,500,order)
        st.plotly_chart(fig, use_container_width=False)

    def room_types():
        mapping_dict={1:"Good Review",0: "Bad Review"}
        #countries_to_include = ["Philippines"]
        
        df_dropna=df_og[df_og.room_type.isna()==False]
        
        list_for_data=cf.categorical_eda_plots_plotly(df_dropna,"room_type",
                                            target_mapping=mapping_dict,
                                            #column_mapping_list=countries_to_include,
                                            hue="good_review", 
                                            time_series=False,  
                                            )
        
        data1,data2,data3,order,order_green, order_red=list_for_data
        fig = make_subplots(rows=1, cols=1,
        #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        
        
        
        fig.add_trace(go.Bar(x=data3.index, y=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,),row=1, col=1)
        fig.add_trace(go.Bar(x=data1.index, y=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green"),row=1, col=1)
        fig.add_trace(go.Bar(x=data2.index, y=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red"),row=1, col=1)
        
        
        cf.layout_v1(fig,"Room Types",500,1000,order_green)
        
        st.plotly_chart(fig, use_container_width=False)
        
    def occupant_types():
        # Stacked Histplot (Compare Proportions)
        mapping_dict={1:"Good Review",0: "Bad Review"}
        countries_to_include = ["Philippines"]
        
        
        
        list_for_data=cf.categorical_eda_plots_plotly(df_og,"occupant_type",
                                            target_mapping=mapping_dict,
                                            #column_mapping_list=countries_to_include,
                                            hue="good_review", 
                                            time_series=False,  
                                                )
        
        data1,data2,data3,order,order_green, order_red=list_for_data
        fig = make_subplots(rows=1, cols=1,
        #vertical_spacing = 0.04,
        subplot_titles=("",""))
    
        fig.add_trace(go.Bar(x=data3.index, y=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,),row=1, col=1)
        fig.add_trace(go.Bar(x=data1.index, y=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green"),row=1, col=1)
        fig.add_trace(go.Bar(x=data2.index, y=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red"),row=1, col=1)
        
        
        cf.layout_v1(fig,"Occupant Types",500,700,order)
        
        st.plotly_chart(fig, use_container_width=False)
                
                
    def nights_stayed():
        df_ns=df_og.copy()
        df_ns["nights_stayed"]=df_ns["nights_stayed_"].apply(lambda x: str(x))
        
        mapping_dict={1:"Good Review",0: "Bad Review"}
        values_to_include = ["1","2","3"]
        
        
        
        list_for_data=cf.categorical_eda_plots_plotly(df_ns,"nights_stayed",
                                            target_mapping=mapping_dict,
                                            column_mapping_list=values_to_include,others_name="4+",
                                            hue="good_review", 
                                            time_series=False,  
                                            )
        
        data1,data2,data3,order,order_green, order_red=list_for_data
        fig = make_subplots(rows=1, cols=1,
        #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        fig.add_trace(go.Bar(x=data3.index, y=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,),row=1, col=1)
        fig.add_trace(go.Bar(x=data1.index, y=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green"),row=1, col=1)
        fig.add_trace(go.Bar(x=data2.index, y=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red"),row=1, col=1)
        
        cf.layout_v1(fig,"Nights Stayed in Hotels",500,500,order,"ascending")
        st.plotly_chart(fig, use_container_width=False)
    
    def time_series_month():
        mapping_dict={1:"Good Review",0: "Bad Review"}
        values_to_include = ["1","2","3"]
        
        
        
        list_for_data=cf.categorical_eda_plots_plotly(df_og,"month_name",
                                            target_mapping=mapping_dict,
                                            #column_mapping_list=values_to_include,others_name="4+",
                                            hue="good_review", 
                                            time_series=True,month_data=True,  long_dates=True,
                                            )
        
        data1,data2,data3,order,order_green, order_red=list_for_data
        fig = make_subplots(rows=1, cols=1,
                    #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        
        fig.add_trace(go.Bar(x=data3.index, y=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,),row=1, col=1)
        fig.add_trace(go.Bar(x=data1.index, y=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green"),row=1, col=1)
        fig.add_trace(go.Bar(x=data2.index, y=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red"),row=1, col=1)
        
        cf.layout_v1(fig,"Reviews Per Month",490,1000,order)
        st.plotly_chart(fig, use_container_width=False)
        
    def time_series_year():
        mapping_dict={1:"Good Review",0: "Bad Review"}
        values_to_include = ["1","2","3"]
        
        
        
        list_for_data=cf.categorical_eda_plots_plotly(df_og,"year",
                                            target_mapping=mapping_dict,
                                            #column_mapping_list=values_to_include,others_name="4+",
                                            hue="good_review", 
                                            time_series=True,
                                            )
        
        data1,data2,data3,order,order_green, order_red=list_for_data
        fig = make_subplots(rows=1, cols=1,
                    #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        
        
        
        fig.add_trace(go.Bar(x=data3.index, y=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,),row=1, col=1)
        fig.add_trace(go.Bar(x=data1.index, y=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green"),row=1, col=1)
        fig.add_trace(go.Bar(x=data2.index, y=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red"),row=1, col=1)
        
        
        cf.layout_v1(fig,"Reviews Per Year",500,700,order)
        st.plotly_chart(fig, use_container_width=False)
        
    
    def tester():
        st.write("testing if this line works")
    
    def wordcloud():
        print("testing if this part works")
        reviews_uni = pickle.load(open('../deployment/data/reviews_unigram.pkl', "rb"))
        mask=np.array(Image.open('msgbox.png'))
        #https://matplotlib.org/stable/tutorials/colors/colormaps.html
        colors = ImageColorGenerator(mask)
        
        # Create a word cloud image
        wc = WordCloud(scale=3,
                        background_color="white", 
                         max_words=100, mask=mask,
                         collocations=False,
                       #stopwords=stopwords, 
                       contour_width=10, 
                       contour_color='black',
                       colormap="tab20c",
                       #colormap='Accent',
                       #color_func="black",
                       width=500, height=500
                       )
        
        # Generate a wordcloud
        wc.generate(" ".join(tweet for tweet in reviews_uni.word))
        # show
        g = plt.figure(figsize=[15,8],dpi=100)
        #plt.imshow(wc, interpolation='bilinear')
        plt.imshow(wc, interpolation='bilinear',cmap=plt.cm.gray)
        plt.axis("off")
        st.pyplot(g)
        
    def quality_and_stars():
        
        columns=['stars','review_rating','total_reviews','facilities_count','cheapest_price']
        df_hotel_level=pickle.load(open("../data/hotel_info_final.pkl", "rb"))
        df_hotel_level.shape
        
        df_hotel_level[columns].info()
        
        df_hotel_level['review_rating']=df_hotel_level['review_rating'].astype(float)
        df_hotel_level['facilities_count']=df_hotel_level['facilities_count'].astype(float)
        df_hotel_level['total_reviews']=df_hotel_level['total_reviews'].apply(lambda x: float(x.replace(",","")))
        #sns.color_palette("hls", 8)
        #g=sns.pairplot(df_hotel_level[columns], hue="stars",palette="Paired",corner=True)
        #g.fig.set_size_inches(12,7)
        
        sns.set(rc={"figure.dpi":150, 'savefig.dpi':150})
        #sns.set(rc={'axes.facecolor':'lightblue', 'figure.facecolor':'lightgreen'})
        
        sns.set(style="ticks")
        
        g=sns.pairplot(df_hotel_level[columns], 
                    hue="stars",
                    palette="Paired",
                    corner=True,
                    )
                    
        g.fig.set_size_inches(12,7)
        st.pyplot(g)
        
        


        
    def facilities_positive():
        fig = make_subplots(rows=1, cols=1,
                            #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        
        #fig.add_trace(go.Bar(y=data3.index, x=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,orientation='h',width=0.5),row=1, col=1)
        fig.add_trace(go.Bar(y=data1.index, x=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green",orientation='h'),row=1, col=1)
        #fig.add_trace(go.Bar(y=data2.index, x=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red",orientation='h'),row=1, col=2)
        
        #fig.add_trace(go.Bar(y=data1.index, x=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green",width=100),row=1, col=1)
        
        cf.layout_v2(fig,"Facilities Most Likely to <br>Contribute to a Positive Review",500,600,order_green)
        st.plotly_chart(fig)
        
    def facilities_negative():
        sns.set_theme(style="ticks")
        fig = make_subplots(rows=1, cols=1,
                    #vertical_spacing = 0.04,
        subplot_titles=("",""))
        
        
        #fig.add_trace(go.Bar(y=data3.index, x=data3[data3.columns[0]].values.tolist(),name="", opacity=0.6, marker_color="grey",showlegend=False,orientation='h',width=0.5),row=1, col=1)
        #fig.add_trace(go.Bar(y=data1.index, x=data1[data1.columns[0]].values.tolist(),name="Good", opacity=0.6, marker_color="green",orientation='h'),row=1, col=1)
        fig.add_trace(go.Bar(y=data2.index, x=data2[data2.columns[0]].values.tolist(),name="Bad", opacity=0.6, marker_color="red",orientation='h'),row=1, col=1)
        
        cf.layout_v2(fig,"Facilities Most Likely to <br>Contribute to a Negative Review",500,600,order_red)
        st.plotly_chart(fig)