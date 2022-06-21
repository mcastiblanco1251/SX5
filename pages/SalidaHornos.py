from shareplum import Site, Office365
from shareplum.site import Version
import streamlit as st
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

class DatosSharepoint:
    def SharePoint(self):
        email = "opinto@agpglass.com"
        password = "AGPcol123"
        url = "https://agpglass-my.sharepoint.com"
        sitio = "https://agpglass-my.sharepoint.com/personal/opinto_agpglass_com/"

        self.authcookie = Office365(url, email, password).GetCookies()
        self.site =Site(sitio, version = Version.v365, authcookie=self.authcookie)
        return self.site

    def connect(self, list):
        self.auth_site = self.SharePoint()
        list_data = self.auth_site.List(list_name = list).GetListItems()
        return list_data
informacion = DatosSharepoint().connect(list="Seguimiento Piezas")
@st.cache(allow_output_mutation=True)
def botones(x):
    datos = pd.DataFrame()
    for i in range(len(informacion)):
        data =  informacion[i]
        if data["Pieza"] == x:
            datos = datos.append(data, ignore_index=True)
    return datos

st.subheader('Gráficas de control para salida de hornos.')

row1_1, row1_2, row1_3 = st.columns(3)
with row1_1:
    Pieza = st.selectbox('Pieza',["PBS","LDI","LDD","LEI","LED"])

Data = botones(Pieza)
Puntos = list(Data.columns.values)
Puntos
Puntos = Puntos[4:17]
Puntos
with row1_2:
    Punto = st.selectbox('Punto', Puntos)
chart = alt.Chart(Data).mark_circle(size=60).transform_fold(
    Puntos,
    as_=['Punto', 'Valor']
).encode(
    x='Modificado',
    y='Valor:Q',
    color='Punto:N',
    tooltip=['Modificado','ID','Title']
).transform_filter(
    alt.FieldEqualPredicate(field='Punto', equal=Punto)
)

st.altair_chart(chart, use_container_width = True)
