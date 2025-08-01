# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:33:22 2025

@author: pranjikl
"""

import streamlit as st
from PIL import Image
import os
import glob
from io import BytesIO
import base64

# Postavljanje stranice
st.set_page_config(
    page_title="MuraDrava-FFS Izvještaj",
    page_icon="🌊",
    layout="wide"
)

def find_report_image():
    patterns = [
        "*redovni*.png", "*posebni*.png",
        "*redovni*.jpg", "*posebni*.jpg",
        "*redovni*.jpeg", "*posebni*.jpeg"
    ]
    found_files = []
    for pattern in patterns:
        found_files.extend(glob.glob(pattern))
    found_files = list(set(found_files))
    found_files.sort()
    return found_files

def get_report_type(filename):
    filename_lower = filename.lower()
    if 'redovni' in filename_lower:
        return "📊 Redovni izvještaj"
    elif 'posebni' in filename_lower:
        return "⚠️ Posebni izvještaj"
    else:
        return "📋 Izvještaj"

def display_image_with_js_open(image, filename="slika.png"):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    b64 = base64.b64encode(buffered.getvalue()).decode()
    href = f"data:image/png;base64,{b64}"

    st.markdown(f"""
    <a href="{href}" target="_blank" rel="noopener noreferrer">
        <img src="{href}" style="width:100%; height:auto; border:1px solid #ccc;" />
    </a>
    <p style="font-size: 0.9em;">📱 Klikni na sliku za prikaz u novom tabu i pinch-to-zoom</p>
    """, unsafe_allow_html=True)

def main():
    st.title("🌊 MuraDrava-FFS Izvještaj")
    
    found_files = find_report_image()
    
    with st.sidebar:
        st.markdown("### 📋 Odabir izvještaja")
        
        if found_files:
            if len(found_files) == 1:
                selected_file = found_files[0]
                report_type = get_report_type(selected_file)
                st.success(f"✅ {report_type}")
                st.write(f"📁 `{selected_file}`")
            else:
                selected_file = st.selectbox(
                    "Odaberite izvještaj:",
                    found_files,
                    format_func=lambda x: f"{get_report_type(x).split()[-1]} - {x.split('/')[-1]}"
                )
        else:
            selected_file = None
            st.error("❌ Nema dostupnih izvještaja")
    
    if found_files and selected_file:
        report_type = get_report_type(selected_file)
        st.subheader(report_type)
        
        image = Image.open(selected_file)
        display_image_with_js_open(image, selected_file)
        
        with open(selected_file, "rb") as file:
            file_extension = selected_file.split('.')[-1]
            download_name = f"MuraDrava_{selected_file}"
            st.download_button(
                label="📥 Preuzmi izvještaj",
                data=file,
                file_name=download_name,
                mime=f"image/{file_extension}"
            )

    elif not found_files:
        st.error("❌ Nisu pronađene datoteke s nazivom 'redovni' ili 'posebni'")
        
        all_images = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
        
        if all_images:
            st.subheader("📁 Sve slike u direktoriju:")
            for img in all_images:
                st.write(f"• {img}")
        
        st.subheader("📤 Uploadajte sliku:")
        uploaded_file = st.file_uploader(
            "Odaberite PNG/JPG datoteku",
            type=['png', 'jpg', 'jpeg']
        )
        
        if uploaded_file is not None:
            report_type = get_report_type(uploaded_file.name)
            st.subheader(report_type)
            
            image = Image.open(uploaded_file)
            display_image_with_js_open(image, uploaded_file.name)
            
            st.download_button(
                label="📥 Preuzmi sliku",
                data=uploaded_file.getvalue(),
                file_name=f"MuraDrava_{uploaded_file.name}",
                mime=f"image/{uploaded_file.name.split('.')[-1]}"
            )

# Sidebar - kontakt
st.sidebar.markdown("---")
st.sidebar.markdown("📧 MuraDrava-FFS")
st.sidebar.markdown("🌊 Sustav za praćenje vodostaja")

if __name__ == "__main__":
    main()
