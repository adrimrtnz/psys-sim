import os
import streamlit as st

RULES_PATH = '../../rules/'
SCENES_PATH = '../../scenes/'

rule_files = os.listdir(RULES_PATH)
scenes_files = os.listdir(SCENES_PATH)


if rule_files not in st.session_state:
    st.session_state.rule_files = rule_files

st.markdown("""
# Simulador
""")

with st.sidebar:
    st.write('## Rules')
    selected_rule = st.selectbox(label="Rule files",
                                 options=st.session_state.rule_files,
                                 index=None,
                                 placeholder="Choose a ruleset",
                                 key="rule_list")
    
    # uploaded_rule_files = st.file_uploader(label='Upload new ruleset',
    #                                        accept_multiple_files=True,
    #                                        type=['xml'],
    #                                        label_visibility='collapsed')
    
    st.write('## Scenes')
    selected_scene = st.selectbox(label="Scene files",
                                  options=scenes_files,
                                  index=None,
                                  placeholder="Choose a scene")

    # if uploaded_rule_files:
    #     for file in uploaded_rule_files:
    #         with open(os.path.join(RULES_PATH, 'test_' + file.name), 'wb') as f:
    #             f.write(file.getbuffer())
    #     st.session_state.rule_files = os.listdir(RULES_PATH)
    #     st.rerun()
