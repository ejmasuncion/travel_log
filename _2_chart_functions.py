#%%
import numpy as np 
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from _1_load_data import Load_Data

#import streamlit as st

import warnings
warnings.filterwarnings('ignore')


class Chart_Functions:

    def __init__(self):
        pass


    def categorical_eda_plots_sns(self,df,column,title,target_mapping=None,column_mapping_list=None,    \
                    orientation='x',color='#6cc8ba',hue=False, \
                    time_series=False, month_data=False,week_data=False,pod_data=False, long_dates=False,ax=None,limited=False):
        
        ax = ax or plt.gca()
        
        data_df = df[[column]]
        
        #If hue column is specified (Target Variable)
        if hue!=False:  
            data_df = df[[column]+[hue]]
            #Target Mapping
            if target_mapping==None:
                data_df['Class'] = data_df[column]
            
            else:
                #print(data_df)
                data_df[hue] = data_df[hue].map(target_mapping)

        #Column Mapping
        if column_mapping_list!=None:
            data_df['Class'] = ['Local' if i in column_mapping_list else 'Foreign'
                        for i in df[column].values]
        
        #Order

        #If not timeseries, order by descending
        if time_series==False:
            order=data_df['Class'].value_counts().index
            
        
        #If timeseries, order by time
        else:
            order=data_df['Class'].value_counts().index.sort_values(ascending=True)
            
            
            if month_data==True:
                order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct", "Nov", "Dec"]
                if long_dates==True:
                    order=["January","February","March","April","May","June","July","August","September","October", "November", "December"]  
            if week_data==True:
                order=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] 
                if long_dates==True:
                    order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] 
                    
            if pod_data==True:
                order=["early morning","breakfast","lunch","afternoon","dinner"] 
                    #Would change this to off Hours
            
        #If you want to set a cap (too many categorical variables)
        if limited!=False:
            o=order[:limited]
            #print(o)
    
        # Set orientation (Vertical or horizontal)

        # No hue- Normal Bargraph
        if hue==False:  
            data_df["Class"] = pd.Categorical(data_df['Class'], order)
            if orientation=='x':
                #return sns.countplot(x=data_df['Class'], order=order,ax=ax, color=color)
                return sns.histplot(data_df, x="Class", stat="percent",ax=ax,multiple="layer", shrink=.4,common_norm=False,color=color)

            else:
                return sns.countplot(y=data_df['Class'],order=order ,ax=ax,color=color)
                #return sns.histplot(data_df, y="Class", hue="good_review", stat="percent",ax=ax,multiple="layer", shrink=.2,common_norm=False)

        #With hue- View Change in proportions  
        if hue!=False:  
            data_df["Class"] = pd.Categorical(data_df['Class'], order)
            if orientation=='x':
                return sns.histplot(data_df, x="Class", hue="good_review", stat="percent",ax=ax,multiple="layer", shrink=.4,common_norm=False)

            else:
                #data_df=data_df.iloc[::-1]
                return sns.histplot(data_df, y="Class", hue="good_review", stat="percent",ax=ax,multiple="layer", shrink=.2,common_norm=False)

        ax.set_title(title)
    


    def df_for_stack(self,mapping_dict,df,hue_column,order):


        #Create 3 stacks
        df_=df
        data1=df_[df[hue_column]==list(mapping_dict.values())[0]][["Class"]].value_counts(normalize=True).to_frame().reset_index().set_index("Class")*100
        data2=df_[df[hue_column]==list(mapping_dict.values())[1]][["Class"]].value_counts(normalize=True).to_frame().reset_index().set_index("Class")*100
        
        merged=pd.concat([data1,data2],axis=1)
        merged.columns=list(mapping_dict.values())
        merged
        

        min=merged.min(axis=1)
        merged=merged.sub(merged.min(axis=1).values, axis='rows')
        merged["Min"]=min


        data1_=merged[[merged.columns[0]]]
        data2_=merged[[merged.columns[1]]]
        data3_=merged[["Min"]]


        #Return custom Orders
        order_1_sorted=data1_.sort_values(by=merged.columns[0],ascending=False).index
        order_2_sorted=data2_.sort_values(by=merged.columns[1],ascending=False).index


        return data1_,data2_,data3_,order,order_1_sorted,order_2_sorted


    def categorical_eda_plots_plotly(self,df,column,target_mapping=None,column_mapping_list=None,others_name="Others",    \
                    hue=False, time_series=False, month_data=False,week_data=False,pod_data=False, long_dates=False,ax=None,limited=False):
        

        #Select Columns+ Target Mapping
        data_df = df[[column]]
        
            #If hue column is specified (Target Variable)
        if hue!=False:  
            data_df = df[[column]+[hue]]
            #print(data_df)
            #Target Mapping
            if target_mapping==None:
                data_df['Class'] = data_df[column]
            
            else:
                data_df[hue] = data_df[hue].map(target_mapping)

        #Column Mapping
        if column_mapping_list!=None:
            data_df['Class'] = [i if i in column_mapping_list else others_name
                        for i in df[column].values]

        else:
            data_df['Class']=data_df[column]
        
        #Order

        #If not timeseries, order by descending
        if time_series==False:
            order=data_df['Class'].value_counts().index
            
        
        #If timeseries, order by time
        else:
            order=data_df['Class'].value_counts().index.sort_values(ascending=True)
            
            
            if month_data==True:
                order=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct", "Nov", "Dec"]
                if long_dates==True:
                    order=["January","February","March","April","May","June","July","August","September","October", "November", "December"]  
            if week_data==True:
                order=["Mon","Tue","Wed","Thu","Fri","Sat","Sun"] 
                if long_dates==True:
                    order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"] 
                    
            if pod_data==True:
                order=["early morning","breakfast","lunch","afternoon","dinner"] 
                    
            
    

        

        # Return 
            # No hue- basic Formatted DF, order
            # With hue- 3 Stacks, order, custom orders
        if hue==False:  
            ret_df=data_df
            return data_df,order


        if hue!=False:  
            ret_df=data_df
            return self.df_for_stack(target_mapping,data_df,hue,order)
        
    
    def layout_v1(self,fig_,title,height,width,order,order_type='default', bgcolor="#F8FBFB",grid_color="white"):
        
        #Cutomizable
        #bgcolor="#F8FBFB"
        #grid_color
        #Plot and BG Color
        #Order


        if order_type=="default":
            x_axis={'categoryorder':'array', 'categoryarray':order}
        
        elif order_type=="ascending":
            x_axis={'categoryorder':'category ascending'}

        elif order_type=="descending":
            x_axis={'categoryorder':'category descending'}


        fig_.update_layout(barmode="stack", 
                            #barnorm="percent",
                            xaxis=x_axis,       
            
            legend=dict(
            orientation="v",
            groupclick="toggleitem"
            ),
                title={
                        'text': "<b>{}</b>".format(title),
                        'y':0.9,
                        'x':0.5,
                        'font_size':20,
                        'xanchor': 'center',
                        'yanchor': 'top'},

            height=height, width=width,
            #font_size=10,
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor
            )
        
        #Grid/Axis Formatting
        fig_.update_yaxes(showgrid=True, 
                        gridwidth=0.1, 
                        gridcolor=grid_color, 
                        griddash='dot',
                        #opacity=0.5,
                        zeroline=False)
        
        # fig.update_xaxes(showgrid=False,zeroline=False)


    #Layout_v2 for Vertical
    def layout_v2(self,fig_,title,height,width,order,order_type='default', bgcolor="#F8FBFB",grid_color="white"):
    
        #Cutomizable
        #bgcolor="#F8FBFB"
        #grid_color
        #Plot and BG Color
        #Order


        if order_type=="default":
            y_axis={'categoryorder':'array', 'categoryarray':order,'autorange': 'reversed'}
        
        elif order_type=="ascending":
            y_axis={'categoryorder':'category ascending','autorange': 'reversed'}

        elif order_type=="descending":
            y_axis={'categoryorder':'category descending','autorange': 'reversed'}


        fig_.update_layout(barmode="stack", 
                            #barnorm="percent",
                            yaxis=y_axis,       
            
            legend=dict(
            orientation="v",
            groupclick="toggleitem"
            ),
                title={
                        'text': "<b>{}</b>".format(title),
                        'y':0.9,
                        'x':0.5,
                        'font_size':20,
                        'xanchor': 'center',
                        'yanchor': 'top'},

            height=height, width=width,
            #font_size=10,
            paper_bgcolor=bgcolor,
            plot_bgcolor=bgcolor
            )
        
        #Grid/Axis Formatting
        fig_.update_yaxes(showgrid=True, 
                        gridwidth=0.1, 
                        gridcolor=grid_color, 
                        griddash='dot',
                        #opacity=0.5,
                        zeroline=False)
        
        # fig.update_xaxes(showgrid=False,zeroline=False)


    def update_layout(self,fig_,title,height,width,bgcolor,font_color,show_ygrid=True,
                            font_size=20,title_font_size="default",title_x=0.5,title_y=0.9):
        
        if title_font_size=="default":
            font_title=font_size
        else:
            font_title=title_font_size

        fig_.update_layout(
        # legend=dict(
        #     orientation="v",
        #     groupclick="toggleitem",
        #     yanchor="top",
        #     y=0.99,
        #     xanchor="left",
        #     x=0.25,
        #     #bgcolor = 'white',
            
        #     ),

        title={
                'text': "<b>{}</b>".format(title),
                #'font':"Times New Roman",
                'y':title_y,
                'x':title_x,
                'font_size':font_title,
                'xanchor': 'center',
                'yanchor': 'top'},

        paper_bgcolor=bgcolor,#F8FBFB
        plot_bgcolor=bgcolor,

        height=height, width=width,

        font=dict(
            family="sans-serif",
            size=font_size,
            color=font_color,
        ),
        

        title_font_family="sans-serif",       
        )


        fig_.update_yaxes(showgrid=show_ygrid, 
                    gridwidth=1, 
                    gridcolor=font_color, 
                    griddash='dot',
                    zeroline=False)

        fig_.update_xaxes(showgrid=False,zeroline=False)
        print("test")


    def update_layout_order(self,fig_,order=[],order_type="default",orientation="v"):
        if order_type=="default":
            axis={'categoryorder':'array', 'categoryarray':order}
        
        elif order_type=="ascending":
            axis={'categoryorder':'category ascending'}

        elif order_type=="descending":
            axis={'categoryorder':'category descending'}


        if orientation=="v":
            fig_.update_layout(barmode="stack", 
                                #barnorm="percent",
                                xaxis=axis,       

                )
        if orientation=="h":
            fig_.update_layout(barmode="stack", 
                                #barnorm="percent",
                                yaxis=axis,       

                )

    def update_layout_order_subplots(self,fig_,order=[],order_type="default",orientation="v",row=1,column=1):
        if order_type=="default":
            axis={'categoryorder':'array', 'categoryarray':order}
        
        elif order_type=="ascending":
            axis={'categoryorder':'category ascending'}

        elif order_type=="descending":
            axis={'categoryorder':'category descending'}


        if orientation=="v":
            fig_.update_layout(barmode="stack", 
                                #barnorm="percent",
                                xaxis=axis,row=row,column=column       

                )
        if orientation=="h":
            fig_.update_layout(barmode="stack", 
                                #barnorm="percent",
                                yaxis=axis,row=row,column=column        

                )


    def update_layout_legend(self,fig_,x,y,xanchor="left",yanchor="top",orientation="v",showlegend=True):
        fig_.update_layout(
        showlegend=showlegend,
        legend=dict(
            orientation=orientation,
            groupclick="toggleitem",
            yanchor=yanchor,
            y=y,
            xanchor=xanchor,
            x=x,
            #bgcolor = 'white',
            
            ),
        )


    def update_layout_margin(self,fig,left,right, bottom, top):
        fig.update_layout( margin=go.layout.Margin(
                l=left, #left margin
                r=right, #right margin
                b=bottom, #bottom margin
                t=top, #top margin
            ))

#%%
if __name__=='__main__':
    #print("Hello")
    cf=Chart_Functions()
    cf.categorical_eda_plots_plotly()


    