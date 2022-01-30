"""This script simulates a classroom of 50 students and estimates the
probability that 3 people share a birthday"""

from PIL import Image
import streamlit as st
import numpy as np
import plotly as ply
from plotly import graph_objects as go
from numpy.random import Generator, PCG64

if 'number_of_sets' not in st.session_state:
    st.session_state.number_of_sets = int(1)
if 'number_of_classrooms' not in st.session_state:
    st.session_state.number_of_classrooms = int(20)

RNG = Generator(PCG64(12345))
NUMBER_OF_SETS = st.session_state.number_of_sets
# precision of value is 1/classrooms
NUMBER_OF_CLASSROOMS = st.session_state.number_of_classrooms  # precision of value is 1/classrooms

im = Image.open(r"C:\\Users\\hawle\\streamlit_projects\\favicon.ico")
st.set_page_config(page_title='Birthday Simulation',page_icon=im,
layout='centered',menu_items=None)
PLACEHOLDER = st.empty()

print('pillow version: ' + Image.__version__)
print('streamlit version: ' + st.__version__)
print('numpy version: ' + np.__version__)
print('plotly version: ' + ply.__version__)

def triple_found(first,second,third):
    '''See if the three arguments have the same value'''
    if first==second==third:
        return True
    else:
        return False

def run_trial(classrooms : int):
    '''Run a trial to estimate phat'''
    classroom_size = int(50)
    tally = int(0)
    index = int(0)
# classrooms in a trial
    while index < classrooms:
# 50 students in a classroom
        rints = RNG.integers(low=1, high=365, size=classroom_size)
        rints.sort()
        index += 1
        for i in range(0,classroom_size-3):
            if triple_found(rints[i],rints[i+1],rints[i+2]):
                tally += 1
                break
    return tally/float(classrooms)   # value of phat for this trial

def run_set_of_trials(classrooms : int):
    '''Run a set of 1000 trials'''
    set_of_trials = int(1000)
    return_data = np.ndarray(shape=(set_of_trials))
    for k in range(0,set_of_trials):
        phat = run_trial(classrooms) # classrooms
        return_data[k] = phat
    return return_data

def run_again():
    '''Run another set of trials for a new histogram'''
    global PLACEHOLDER
    PLACEHOLDER.empty()
    with PLACEHOLDER.container():
        fig = go.Figure()
        st.title('Birthday Simulation')
        st.subheader('What is the probability of 3 people having the same'
        +' birthday in a class of 50 students?')
        st.subheader('Class width is ' + str(1.0/float(NUMBER_OF_CLASSROOMS)))
        data_table = np.ndarray(shape=(1000,1), dtype=float)
#        bins = 1.0/float(NUMBER_OF_CLASSROOMS)
#        print(bins)
        for run_number in range(0,NUMBER_OF_SETS):
            data_table = run_set_of_trials(NUMBER_OF_CLASSROOMS)
            mean_value_str = f'{np.mean(data_table):.4f}'
            group_labels = ' median '+str(np.median(data_table))+' mean '+mean_value_str
            print("run number= " + str(run_number) + " label= " + group_labels)
            fig.add_trace(go.Histogram(x=data_table,name=group_labels,showlegend=True))
        fig.update_traces(opacity=0.75)
        fig.update_layout(title_text='Histogram for 1000 trials', # title of plot
        xaxis_title_text='Estimated Probability', # xaxis label
        yaxis_title_text='Frequency', # yaxis label
        barmode='overlay',
        bargap=0.2, # gap between bars of adjacent location coordinates
        bargroupgap=0.1 # gap between bars of the same location coordinates
        )
        st.plotly_chart(fig)

with st.form(key='my_form'):
    NUMBER_OF_SETS = st.number_input(
        'Enter the number of sets of trials that you want to run ',
        min_value=1, max_value=10, step=1,
        help='Each set is 1000 trials', key='number_of_sets')
    NUMBER_OF_CLASSROOMS = st.number_input('Enter the number of classrooms '+
    'you want to model for each set of trials that you want to run ',
    min_value=20, max_value=1000, value=25, step=10,
    help='This sets the bin size = 1/(number of classrooms)',
    key='number_of_classrooms')
    submit_button = st.form_submit_button(label='Run Again', on_click=run_again)

run_again()
