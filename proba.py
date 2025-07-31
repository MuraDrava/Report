# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:33:22 2025

@author: pranjikl
"""

import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# Postavljanje stranice
st.set_page_config(
    page_title="Excel File Reader",
    page_icon="📊",
    layout="wide"
)

# Naslov aplikacije
st.title("📊 Excel File Reader")
st.markdown("---")