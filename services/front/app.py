import os
import streamlit as st

RULES_PATH = '../../rules/'
SCENES_PATH = '../../scenes/'
DERIVATION_MODES = {
    'maxpar': 'Max. Parallelism',
    'minpar': 'Min. Parallelism'
}

results = None

st.markdown("""
# P-System Simulator
""")


with st.sidebar:

    st.write('## Scene')
    rule_file = st.file_uploader(label='Select Scene File',
                                 accept_multiple_files=False,
                                 type=['xml'])
    

    st.write('## Rules')
    rule_file = st.file_uploader(label='Select Rules File',
                                 accept_multiple_files=False,
                                 type=['xml'])
    
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

    left, right = st.columns(2)
    with left:
        steps = st.number_input('**Simulation Steps**', value=None, step=1)

    with right:
        seed = st.number_input('**Random Seed**', value=None, step=1)

st.markdown('---')

st.markdown('# :material/play_arrow: Simulation Controls')

with st.container(border=True):
    st.markdown('**Simulation Controls**')

    left, middle, right = st.columns(spec=[0.45, 0.08, 0.45])
    if left.button(":material/play_arrow: Start", use_container_width=True, type="primary"):
        pass
    if middle.button(":material/pause:"):
        pass
    if right.button(":material/skip_next: Step Forward", use_container_width=True):
        pass

    stop_col, reset_col = st.columns(spec=[0.8, 0.2])
    if stop_col.button(":material/stop: Stop", use_container_width=True):
        pass
    if reset_col.button(":material/Replay: Reset", use_container_width=True):
        pass

st.markdown('---')

st.markdown('# :material/insert_chart: Results')

if not results:
    with st.container(border=True):
        st.markdown(":gray[Run a simulation to see some results]")

