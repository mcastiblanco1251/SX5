import adodbapi as ADO
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import math
import streamlit as st
from PIL import Image
import datetime
import pandas as pd
import altair as alt

@st.cache(allow_output_mutation=True)
def ObtenerGraficas (OP, horno, entrada, salida):
    db = ADO.connect('provider=iHistorian OLE DB Provider;data source=localhost;mode=Read')
    a = db.cursor()

    sqlBase = "SELECT Value, timestamp FROM ihrawdata "
    if horno == "H2" or horno=="h2":
        sqlDatos =  "WHERE RowCount = 0 AND Tagname = 'FIX.PV_CURVADO.F_CV' AND timeStamp >= '"+str(entrada)+"' AND timeStamp < '"+str(salida)+"' AND samplingmode = 'RawByTime'"
        sqlRef =  "WHERE RowCount = 0 AND Tagname = 'FIX.SV_CURVADO.F_CV' AND timeStamp >= '"+str(entrada)+"' AND timeStamp < '"+str(salida)+"' AND samplingmode = 'RawByTime'"

        a.execute(sqlBase+sqlDatos)
        data = a.fetchall()

        a.execute(sqlBase+sqlRef)
        ref = a.fetchall()

        datosHorno = data.ado_results[0]
        datosHornoMAX = datosHorno.index(max(datosHorno))
        referencia = ref.ado_results[0]
        tiemposY = ref.ado_results[1]

        time = []
        for i in tiemposY:
            temp = str(i).rstrip("00:00")
            time.append(datetime.datetime.strptime(temp.rstrip("+"),'%Y-%m-%d %H:%M:%S'))
        Datos = pd.DataFrame({"Current":datosHorno, "Set":referencia,"Tiempo":time})
    else:
        sqlDatos =  "WHERE RowCount = 0 AND Tagname = 'FIX.FONDO_DER_S1.F_CV' AND timeStamp >= '"+str(entrada)+"' AND timeStamp < '"+str(salida)+"' AND samplingmode = 'RawByTime'"
        sqlRef =  "WHERE RowCount = 0 AND Tagname = 'FIX.SP_TECHO_CENTRO_S1.F_CV' AND timeStamp >= '"+str(entrada)+"' AND timeStamp < '"+str(salida)+"' AND samplingmode = 'RawByTime'"

        a.execute(sqlBase+sqlDatos)
        data = a.fetchall()

        a.execute(sqlBase+sqlRef)
        ref = a.fetchall()

        datosHorno = data.ado_results[0]
        datosHornoMAX = datosHorno.index(max(datosHorno))
        referencia = ref.ado_results[0]
        tiemposY = ref.ado_results[1]

        time = []
        for i in tiemposY:
            temp = str(i).rstrip("00:00")
            time.append(datetime.datetime.strptime(temp.rstrip("+"),'%Y-%m-%d %H:%M:%S'))
        Datos = pd.DataFrame({"Current":datosHorno, "Set":referencia,"Tiempo":time})
    return datosHorno, referencia, time, Datos

hornos=['S1', 'H2']
actual = datetime.datetime.now()
diferenciaTiempo =  actual - datetime.timedelta(hours=8)

row1_1, row1_2 = st.columns((2, 2))
with row1_1:
    orden = st.text_input('Orden') #10613790
    f_1=st.date_input( "Fecha Inicio")
    f_2 =st.date_input( "Fecha Final") #'12-Jun-2022 03:00:00'
with row1_2:
    h1=st.selectbox('Hornos',hornos)
    t1=st.time_input('Hora Incio', value= diferenciaTiempo.time())
    t2=st.time_input('Hora Final', value=actual.time())

f1=datetime.datetime.combine(f_1,t1)
f1 = f1.strftime("%d-%m-%Y %H:%M:%S")
f2=datetime.datetime.combine(f_2,t2)
f2 = f2.strftime("%d-%m-%Y %H:%M:%S")

st.subheader('Gráfica de curvado en el horno '+h1)

row1_1, row1_2 = st.columns((2, 2))
with row1_1:
    st.write(f'**De**: {f1}')
with row1_2:
    st.write(f'**Hasta**: {f2}')

# orden = 1
# h1 = "S1"
# f1 = "13-06-2022 01:00:00"
# f2 = "14-06-2022 01:00:00"

a,b,t, d = ObtenerGraficas(orden, h1, f1, f2)
chart = alt.Chart(d).mark_line().transform_fold(
    ["Current", "Set"],
    as_=['Tipo', 'Valor']
).encode(
    x='Tiempo',
    y='Valor:Q',
    color='Tipo:N',
    tooltip=['Tipo:N']
)
st.altair_chart(chart, use_container_width = True)
