import json
from json import JSONEncoder

import librosa
import numpy as np
import streamlit as st


def convert_seconds_to_timecode(seconds: float, fps: int):
    # Calculate the time base and the number of frames
    time_base = seconds + (1 / fps) / 2  # Add half a frame to round to the nearest frame
    frames = int(time_base * fps)

    # Convert to hours, minutes, seconds, and frames
    hours = frames // (3600 * fps)
    minutes = (frames // (60 * fps)) % 60
    seconds = (frames // fps) % 60
    frames = frames % fps

    # Combine into a string in the desired format
    timecode = f"{hours:02}:{minutes:02}:{seconds:02}:{frames:02}"
    return timecode


fps = st.slider('Frames per second', min_value=10, max_value=60, value=25, step=1)

uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    st.write("Processing: ", uploaded_file.name)
    y, sr = librosa.load(uploaded_file)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_time = librosa.frames_to_time(beat_frames, sr=sr)
    st.write("Beats: ", beat_time)
    st.download_button(label="Download beats in seconds", data=json.dumps(beat_time.tolist()), file_name="beats.json", mime="application/json")

    convert_func = np.vectorize(convert_seconds_to_timecode, otypes=[np.str])
    beat_timecode = convert_func(beat_time, fps)
    st.write("Beats time code:", beat_timecode)
    st.download_button(label="Download beats timecode", data=json.dumps(beat_timecode.tolist()), file_name="beats_timecode.json", mime="application/json")

