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
informacion = DatosSharepoint().connect(list="SEGUIMIENTO MOLDE")

@st.cache(allow_output_mutation=True)
def botones(x, y):
    datos = pd.DataFrame()
    for i in range(len(informacion)):
        data =  informacion[i]
        #data[data["1"]>6] = data[data["1"]>6].div(10)
        if data["Title"] == x and data["MOLDE"] == y:
            datos = datos.append(data, ignore_index=True)
    return datos

st.subheader('Gráficas de control para liberación de herramentales.')

row1_1, row1_2, row1_3 = st.columns(3)
with row1_1:
    Pieza = st.selectbox('Pieza',["PBS","LDI","LDD","LEI","LED"])

if Pieza == "PBS":
    Moldes = ["1","2","3","4","5","10"]
else:
    Moldes = ["1","2","3","4"]

with row1_2:
    Molde = st.selectbox('Molde', Moldes)

Data = botones(Pieza, Molde)
Puntos = list(Data.columns.values)
Puntos = Puntos[2:28]
with row1_3:
    Punto = st.selectbox('Punto', Puntos)


chart = alt.Chart(Data).transform_fold(
    Puntos,
    as_=['Punto', 'Valor']
).mark_circle(size=60).encode(
    x='Modificado',
    y='Valor:Q',
    color='Punto:N',
    tooltip=['Modificado','RESPONSABLE','Recibe']
).transform_filter(
    alt.FieldEqualPredicate(field='Punto', equal=Punto)
)

#hola =2.7
#line = alt.Chart(pd.DataFrame({'y': [hola]})).mark_rule(strokeDash=[5, 5], color = "red").encode(y='y')
#line1 = alt.Chart(pd.DataFrame({'yy': [2.3]})).mark_rule(strokeDash=[5, 5], color = "red").encode(y='yy')
#st.altair_chart(chart+line+line1, use_container_width = True)
st.altair_chart(chart, use_container_width = True)
st.dataframe(Data)
