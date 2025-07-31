# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:33:22 2025

@author: pranjikl
"""

import streamlit as st
import pandas as pd
import os


# Postavljanje stranice
st.set_page_config(
    page_title="Mura Drava izvještaj",
    page_icon="📊",
    layout="wide"
)

# Naslov aplikacije
st.title("📊 Excel File Reader")
st.markdown("---")
