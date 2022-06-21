import streamlit as st
from PIL import Image
import datetime

im2 = Image.open('AGP.jpg')
st.set_page_config(page_title='Cluster-App', layout="wide", page_icon=im2)
st.set_option('deprecation.showPyplotGlobalUse', False)


image = Image.open('AGP.jpg')
st.image(image, width=600)
st.title("""
Seguimiento de procesos de proyecto OEM X5
         """)
st.write("""
Esta App muestra variables de Proceso y Alertas para garantizar la eficiencia del Proyecto X5!
""")

st.markdown('Web App by [Manuel Castiblanco](https://github.com/mcastiblanco1251) y Orlando Pinto')


st.markdown('____________________________________________________________________')
