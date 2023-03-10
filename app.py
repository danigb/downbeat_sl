import pandas as pd
import streamlit as st
from madmom.features import DBNDownBeatTrackingProcessor, RNNDownBeatProcessor

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("Processing: ", uploaded_file.name)
    beat_processor = RNNDownBeatProcessor()
    beat_tracking = DBNDownBeatTrackingProcessor(beats_per_bar=[3, 4],fps=100)
    beats = beat_processor.process(uploaded_file)
    downbeats = beat_tracking.process(beats)
    st.write(downbeats)

