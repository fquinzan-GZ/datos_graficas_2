import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import time

@st.cache_data

def get_df(high_limit, low_limit, x_size, y_size):

    stime = time.time()

    st.session_state['df'] = pd.DataFrame(
            np.random.randint(
                low = low_limit,
                high=high_limit,
                size=(x_size, y_size)
            ),
            columns=("col %d" % i for i in range(y_size))
        )

    compute_time = time.time() - stime

    return compute_time

st.set_page_config(
    page_title="Streamlit Project 1",
    page_icon=":skull:",
    layout="wide", 
    initial_sidebar_state="expanded", 
    menu_items={
        'Get help': 'https://www.extremelycoolapp.com/help',
        'Report a Bug': 'https://www.extremelycoolapp.com/bug',
        'About': '# this is a header'
    }
    )

if 'df' not in st.session_state:
    st.session_state['df'] = pd.DataFrame()

def page_1():

    st.title(" Random Data Frame")
    st.title("Streamlit basics")
    st.markdown("A brief project on Streamlit widgets :sunglasses:")

def page_2():

    empty_widget = st.empty()

    generate_df = st.checkbox("Generate DF")

    mytext = st.sidebar.text_input("Your name", key="name")
    st.write(mytext)


    with st.expander("Data"):

        col1, col2, col3 = st.columns([3,6,2])

        with col1:
            with st.form("compute_form"):
                low_limit = st.slider(
                    "Low limit",
                    min_value=-1000,
                    max_value=1000,
                    value=-10,
                    step=1
                )

                high_limit = st.slider(
                    "High limit",
                    min_value=-1000,
                    max_value=1000,
                    value=10,
                    step=1
                )

                x_size = st.number_input(
                    "x size",
                    min_value=1,
                    max_value=10**9,
                    value=10,
                    step=1
                )

                y_size = st.number_input(
                    "y size",
                    min_value=1,
                    max_value=10**9,
                    value=10,
                    step=1
                )

                submitted = st.form_submit_button("Submit")   

        with col2:
            with st.spinner("Generating dataframe..."):
                if generate_df:
                    compute_time = get_df(high_limit, low_limit, x_size, y_size)
                    st.dataframe(st.session_state['df'])
                    empty_widget.write("Dataframe dimensions %d x %d" % (st.session_state['df'].shape))

        with col3:
            download_button = st.download_button(
                label = "Download DF",
                data = st.session_state['df'].to_csv(),
                file_name = " My dataframe.csv"
                )

    with st.expander("Metrics"):
                
        df_max = st.session_state['df'].max().max()
        df_min = st.session_state['df'].min().min()
        df_mean = st.session_state['df'].mean().mean()

        metrics_selection = st.multiselect(
            label = "Select metrics to show",
            options = ['Max', 'Min', 'Average'],
            placeholder="Choose an option",
        )

        if 'Max' in metrics_selection:
            st.metric(
                "Max value",
                df_max,
                delta = 'Max',
                delta_color="normal",
                help="Tha max value of the dataframe",
            )

        if 'Min' in metrics_selection:
            st.metric(
                "Min value",
                df_min,
                delta = 'Min',
                delta_color="inverse",
                help="Tha min value of the dataframe"
            )
        
        if 'Average' in metrics_selection:
            st.metric(
                "Mean value",
                df_mean,
                delta="Average",
                delta_color="normal",
                help="Tha mean value of the dataframe"
            )

    with st.expander("Plots"):

        colorscale = st.selectbox(
            "Choose color",
            options=[
                'viridis',
                'cividis',
                'inferno',
                'magma',
                'plasma',
                'Greys',
                'Blues',
                'Greens',
                'Oranges',
                'Reds',
                'Purples',
                'rainbow',
                'jet'
            ]
        )

        tab1, tab2, tab3 = st.tabs(["Matplotlib", "Plotly 2D", "Plotly 3D"])

        with tab1:
            fig = plt.figure()
            contour = plt.contour(
               st.session_state['df'],
               cmap = colorscale,
            )
            plt.colorbar(contour)
            st.pyplot(fig)

        with tab2:
            fig = go.Figure(
                data=
                go.Contour(
                    z = st.session_state['df'],
                    colorscale=colorscale,
                )
            )
            st.plotly_chart(fig) 

        with tab3:
            fig = go.Figure(
                data=
                go.Surface(
                    z = st.session_state['df'],
                    colorscale=colorscale,
                )
            )
            st.plotly_chart(fig)                               

pg = st.navigation(
    {
        "Home":[st.Page(page_1, title="Intro", icon="🚪")],
        "Data":[st.Page(page_2, title="Title and Plots", icon="📈")],
    }
    
    )
pg.run()