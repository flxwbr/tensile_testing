import streamlit as st
# To make things easier later, we're also importing numpy and pandas for
# working with sample data.
import numpy as np
import pandas as pd

#TODO: load csv file

# = pd.read_csv('EN_GJS_1050_6_Buchholz_17_1.csv')

st.title('Tensile Testing Evaluation')

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
  print(uploaded_file.name)
  exp_tensile_data = pd.read_csv(uploaded_file)

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
diagram_df

threshold_stress = st.number_input('Enter threshold stress')

diagram_df['ext'].values[diagram_df['stress'] > threshold_stress+2] = np.nan
diagram_df['trav'].values[diagram_df['stress'] < threshold_stress-2] = np.nan

#save_value
#st.line_chart(np.random.randn(10,2))

import plotly.express as px

fig = px.line(diagram_df, x=['ext', 'trav'], y='stress')

st.write(fig)

ext_df = diagram_df[diagram_df['stress'] < threshold_stress]
trav_df = diagram_df[diagram_df['stress'] > threshold_stress]

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
trav_df = diagram_df[diagram_df['stress'] > threshold_stress]

distance_scaling = st.number_input('Enter distance scaling factor')

diagram_df['trav'] -= trav_df['trav'].values[0]-ext_df['ext'].values[-1]
diagram_df['ext'].values[diagram_df['stress'] > threshold_stress-distance_scaling] = np.nan
diagram_df['trav'].values[diagram_df['stress'] < threshold_stress+distance_scaling] = np.nan

ext_values = diagram_df['ext'].values
trav_values = diagram_df['trav'].values

total_values = []

for i in range(len(ext_values)):
    if np.isnan(ext_values[i]):
        total_values.append(trav_values[i])
    else:
        total_values.append(ext_values[i])

diagram_df['total'] = total_values
diagram_df['total'] = diagram_df['total'].interpolate()

diagram_df

fig = px.line(diagram_df, x=['total'], y='stress')

st.write(fig)

if st.button('Save Data'):
    diagram_df.to_csv('total_curve_'+uploaded_file.name)