import os
import sys
import math
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.subplots as sp
import plotly.graph_objects as go

from io import StringIO
from config import Config

sys.path.append('../engine')
from src.utils.parser_factory import ParserFactory


RULES_PATH = '../../rules/'
SCENES_PATH = '../../scenes/'
RUNS_PATH = '../../runs/'
DERIVATION_MODES = {
    'maxpar': 'Max. Parallelism',
    'minpar': 'Min. Parallelism'
}

config = Config()

if "engine" not in st.session_state:
    st.session_state.engine = None

if "results" not in st.session_state:
    st.session_state.results = None

if "scene" not in st.session_state:
    st.session_state.scene = None

if "rules" not in st.session_state:
    st.session_state.rules = None

if "last_seed" not in st.session_state:
    st.session_state.last_seed = None

st.markdown("""
# P-System Simulator
""")


with st.sidebar:

    st.write('## Scene')
    scene_file = st.file_uploader(label='Select Scene File',
                                 accept_multiple_files=False,
                                 type=['xml'])
    if scene_file is not None:
        stringio = StringIO(scene_file.getvalue().decode('utf-8'))
        file_path = os.path.join(SCENES_PATH, scene_file.name)
        name, _ = os.path.splitext(scene_file.name)
        config.scene = name
        if os.path.exists(file_path) and os.path.isfile(file_path) and scene_file.name != st.session_state.scene:
            st.toast(f'File {scene_file.name} already exists in location. Using it instead', icon=":material/info:")
            st.session_state.scene = scene_file.name
            if st.session_state.engine:
                st.session_state.engine = None
                st.session_state.results = None
                st.toast("Scene file changed, reseting engine")
        else:
            with open(file_path, 'w') as f:
                f.write(stringio.getvalue())

    st.write('## Rules')
    rule_file = st.file_uploader(label='Select Rules File',
                                 accept_multiple_files=False,
                                 type=['xml'])

    if rule_file is not None:
        stringio = StringIO(rule_file.getvalue().decode('utf-8'))
        file_path = os.path.join(RULES_PATH, rule_file.name)
        name, _ = os.path.splitext(rule_file.name)
        config.rules = name
        if os.path.exists(file_path) and os.path.isfile(file_path) and rule_file.name != st.session_state.rules:
            st.toast(f'File {rule_file.name} already exists in location. Using it instead', icon=":material/info:")
            st.session_state.rules = rule_file.name
            if st.session_state.engine:
                st.session_state.engine = None
                st.session_state.results = None
                st.toast("Rule file changed, reseting engine")
        else:
            with open(file_path, 'w') as f:
                f.write(stringio.getvalue())

st.markdown('---')

st.markdown('# :material/settings: Configuration')

with st.container(border=True):
    st.markdown('**Simulation Configuration**')
    # st.markdown(':gray[Configure the parameters for the simulation engine]')

    options = DERIVATION_MODES.keys()
    value = st.selectbox(
        "**Derivation Mode**",
        options=options,
        format_func=lambda x: DERIVATION_MODES[x]
    )
    config.inference = value

    left, right = st.columns(2)
    with left:
        steps = st.number_input('**Simulation Steps**', value=None, step=1)
        config.max_steps = steps

    with right:
        seed = st.number_input('**Random Seed**', value=None, step=1)
        config.seed = seed
        if config.seed != st.session_state.last_seed:
            st.session_state.engine = None
            st.session_state.results = None
            st.session_state.last_seed = config.seed
            st.toast("Seed changed, reseting engine")


st.markdown('# :material/play_arrow: Simulation Controls')

with st.container(border=True):
    st.markdown('**Simulation Controls**')

    play, forward, reset = st.columns(spec=[0.40, 0.40, 0.2])
    if play.button(":material/play_arrow: Start", use_container_width=True, type="primary"):
        if st.session_state.engine is None:
            # Parsear el modelo a partir de la configuración
            try:
                parser = ParserFactory(config=config)
                st.session_state.engine = parser.parse()
            except:
                st.error('Verify that all necessary fields are not empty', icon="🚨")
        if st.session_state.engine:
            try:
                with st.spinner("Running Simulation"):
                    st.session_state.engine.run(config.max_steps)
                    st.session_state.results = True
            except Exception as e:
                st.error(f'Error running the model: {str(e)}', icon="🚨")

    # if middle.button(":material/pause:"):
    #     pass
    if forward.button(":material/skip_next: Step Forward", use_container_width=True):
        if st.session_state.engine is None:
            # Parsear el modelo a partir de la configuración
            try:
                parser = ParserFactory(config=config)
                st.session_state.engine = parser.parse()
            except:
                st.error('Verify that all necessary fields are not empty', icon="🚨")
        if st.session_state.engine:
            try:
                with st.spinner("Running Simulation"):
                    st.session_state.engine.run(1)
                    st.session_state.results = True
            except Exception as e:
                st.error(f'Error running the model: {str(e)}', icon="🚨")

    if reset.button(":material/Replay: Reset", use_container_width=True):
        st.session_state.engine = None
        st.session_state.results = None

st.markdown('---')

st.markdown('# :material/insert_chart: Results')

if not st.session_state.results:
    with st.container(border=True):
        st.markdown(":gray[Run a simulation to see some results]")
else:
    data_path = os.path.join(RUNS_PATH, st.session_state.engine.output_file)
    df = pd.read_csv(data_path, index_col=False)

    objects = df.object.unique()
    n_objects = len(objects)

    # gráfico global
    fig_global = px.line(
        df, x="step", y="count", color="object",
        title="Evolution of all output objects"
    )
    st.plotly_chart(fig_global, use_container_width=True)


    # máximo 2 plots por fila
    n_cols = 2
    n_rows = math.ceil(n_objects / n_cols)

    fig = sp.make_subplots(rows=n_rows,
                           cols=n_cols,
                           subplot_titles=[f'Evolución objeto "{obj}"' for obj in objects])
    
    for i, obj in enumerate(objects):
        subset = df[df.object == obj]
        trace = px.line(subset, x='step', y='count').data[0]

        row = i // n_cols + 1
        col = i % n_cols + 1
        fig.add_trace(trace, row=row, col=col)

    fig.update_layout(
        height=400 * n_rows,
        width=1200,
        showlegend=False,
        title_text="Individual Plots"
    )

    st.plotly_chart(fig, use_container_width=True)
