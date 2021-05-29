import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

#TODO: load csv file

exp_tensile_data = pd.read_csv('EN_GJS_1050_6_Buchholz_17_1.csv')



st.title('Tensile Testing Evaluation')

diameter = st.number_input('Enter specimen diameter')
area = np.pi*(diameter**2)/4
L0_length = exp_tensile_data['Standardweg ab'].values[0]
'diameter: ', diameter
'area: ', area
'L0 length: ', L0_length
'''
overview of experimental data
'''
st.write(exp_tensile_data)

# plot stress strain curve extensiometer
force = exp_tensile_data['Standardkraft'].values
extensiometer_displacement = exp_tensile_data['Standardweg'].values
traverse_displacement = exp_tensile_data['Traverse abs.'].values

traverse_displacement = traverse_displacement - traverse_displacement[0]

stress = force/area
extensiometer_strain = extensiometer_displacement/L0_length
traverse_strain = traverse_displacement/L0_length

diagram_data = np.row_stack((stress, extensiometer_strain, traverse_displacement))

diagram_data = diagram_data.transpose()

diagram_df = pd.DataFrame(data=diagram_data, columns=['stress', 'ext', 'trav'])
#print(diagram_data)
#diagram_df

threshold_stress = st.number_input('Enter threshold stress')

diagram_df['ext'].values[diagram_df['stress'] > threshold_stress] = np.nan
diagram_df['trav'].values[diagram_df['stress'] < threshold_stress-2] = np.nan

#save_value
#st.line_chart(np.random.randn(10,2))

import plotly.express as px

fig = px.line(diagram_df, x=['ext', 'trav'], y='stress')

st.write(fig)

ext_df = diagram_df[diagram_df['stress'] < threshold_stress]
trav_df = diagram_df[diagram_df['stress'] > threshold_stress-2]

#ext_df
#trav_df
der_ext = (ext_df['stress'].values[-1]-ext_df['stress'].values[-2]) / (ext_df['ext'].values[-1]-ext_df['ext'].values[-2])
#der_ext
# end of stress strain curve when strain drops
der_trav = (trav_df['stress'].values[1]-trav_df['stress'].values[0]) / (trav_df['trav'].values[1]-trav_df['trav'].values[0])
#der_trav

scaling_factor = der_ext / der_trav
#scaling_factor_2 = 0.1379/(trav_df['trav'].values[-1]*scaling_factor)
#scaling_factor = 0.1379 / trav_df['trav'].values[-1]

manual_scaling = st.number_input('Enter scaling factor')

diagram_df['trav'] /= scaling_factor/manual_scaling#*scaling_factor_2
ext_df = diagram_df[diagram_df['stress'] < threshold_stress]
trav_df = diagram_df[diagram_df['stress'] > threshold_stress-2]



diagram_df['trav'] -= trav_df['trav'].values[0]-ext_df['ext'].values[-1]



fig = px.line(diagram_df, x=['ext', 'trav'], y='stress')
st.write(fig)