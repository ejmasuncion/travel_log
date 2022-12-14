import streamlit as st
from streamlit_option_menu import option_menu
from pages import Pages
from charts_functions_compiled import charts
st.set_option('deprecation.showPyplotGlobalUse', False)


list_of_pages = [
    "Introduction",
    "Clusters",
    "Dashboard",
    "Model"
]

# Left the inside blank so that it really looks like a navbar
icons = ['building' , 'person','bar-chart-fill', 'gear']
selection = option_menu("", list_of_pages, orientation='horizontal', icons=icons,
        styles={
        "container": {"padding": "0!important", "background-color": "#448299"},
        "nav-link": {"font-size": "15px", "text-align": "left", "margin":"0px", "--hover-color": "#AB5474"},  
        "nav-link-selected": {"background-color": "#AB5474"},    
        })

if selection == "Introduction":
    Pages.page_one()

elif selection == "Clusters":
    Pages.page_two()
    
elif selection == "Dashboard":
    Pages.page_three()
    
elif selection == "Model":
    Pages.page_four()

