import streamlit as st
from streamlit_option_menu import option_menu
from pages import Pages
from charts_functions_compiled import charts
st.set_option('deprecation.showPyplotGlobalUse', False)


col1, col2, col3 = st.columns([20,60,20], gap="large")
with col1:
    st.write(" ")
with col2:
    st.image("pictures/Larana.png", width=400)
with col3:
    st.write(" ")
    
st.markdown(" ")


list_of_pages = [
    "Introduction",
    "Clusters",
    "Dashboard",
    "Model"
]

# Left the inside blank so that it really looks like a navbar
icons = ['building' , 'person','bar-chart-fill', 'gear']
selection = option_menu("", list_of_pages, orientation='horizontal', icons=icons)

if selection == "Introduction":
    Pages.page_one()

elif selection == "Clusters":
    Pages.page_two()
    
elif selection == "Dashboard":
    Pages.page_three()
    
elif selection == "Model":
    Pages.page_four()

