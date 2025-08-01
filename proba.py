# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:33:22 2025

@author: pranjikl
"""

import streamlit as st
from PIL import Image
import os

# Postavljanje stranice
st.set_page_config(
    page_title="MuraDrava-FFS Izvještaj",
    page_icon="🌊",
    layout="wide"
)

import streamlit as st
from PIL import Image
import os
import glob

# Postavljanje stranice
st.set_page_config(
    page_title="MuraDrava-FFS Izvještaj",
    page_icon="🌊",
    layout="wide"
)

def find_report_image():
    """Pronađi PNG datoteku koja sadrži 'redovni' ili 'posebni' u nazivu"""
    
    # Lista mogućih pattern-a za pretraživanje
    patterns = [
        "*redovni*.png",
        "*posebni*.png",
        "*redovni*.jpg", 
        "*posebni*.jpg",
        "*redovni*.jpeg",
        "*posebni*.jpeg"
    ]
    
    found_files = []
    
    # Prođi kroz sve pattern-e
    for pattern in patterns:
        files = glob.glob(pattern)
        found_files.extend(files)
    
    # Ukloni duplikate i sortiraj
    found_files = list(set(found_files))
    found_files.sort()
    
    return found_files

def get_report_type(filename):
    """Odredi tip izvještaja na temelju naziva datoteke"""
    filename_lower = filename.lower()
    if 'redovni' in filename_lower:
        return "📊 Redovni izvještaj"
    elif 'posebni' in filename_lower:
        return "⚠️ Posebni izvještaj"
    else:
        return "📋 Izvještaj"

def main():
    st.title("🌊 MuraDrava-FFS Izvještaj")
    
    # Pronađi sve relevantne datoteke
    found_files = find_report_image()
    
    # Sidebar za odabir izvještaja
    with st.sidebar:
        st.markdown("### 📋 Odabir izvještaja")
        
        if found_files:
            if len(found_files) == 1:
                # Ako je samo jedna datoteka, prikaži je u sidebaru
                selected_file = found_files[0]
                report_type = get_report_type(selected_file)
                st.success(f"✅ {report_type}")
                st.write(f"📁 `{selected_file}`")
            else:
                # Selectbox za odabir datoteke u sidebaru
                selected_file = st.selectbox(
                    "Odaberite izvještaj:",
                    found_files,
                    format_func=lambda x: f"{get_report_type(x).split()[-1]} - {x.split('/')[-1]}"
                )
        else:
            selected_file = None
            st.error("❌ Nema dostupnih izvještaja")
    
    # Glavni sadržaj
    if found_files and selected_file:
        report_type = get_report_type(selected_file)
        st.subheader(report_type)
        
        # Prikaži sliku
        image = Image.open(selected_file)
        st.image(image, use_container_width=True)
        
        # Download opcija
        with open(selected_file, "rb") as file:
            file_extension = selected_file.split('.')[-1]
            download_name = f"MuraDrava_{selected_file}"
            
            btn = st.download_button(
                label="📥 Preuzmi izvještaj",
                data=file,
                file_name=download_name,
                mime=f"image/{file_extension}"
            )
    
    elif not found_files:
        st.error("❌ Nisu pronađene datoteke s nazivom 'redovni' ili 'posebni'")
        
        # Prikaži sve PNG/JPG datoteke u direktoriju
        all_images = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
        
        if all_images:
            st.subheader("📁 Sve slike u direktoriju:")
            for img in all_images:
                st.write(f"• {img}")
        
        # Upload opcija
        st.subheader("📤 Uploadajte sliku:")
        uploaded_file = st.file_uploader(
            "Odaberite PNG/JPG datoteku",
            type=['png', 'jpg', 'jpeg']
        )
        
        if uploaded_file is not None:
            # Odredi tip na temelju naziva uploaded datoteke
            report_type = get_report_type(uploaded_file.name)
            st.subheader(report_type)
            
            image = Image.open(uploaded_file)
            st.image(image, use_container_width=True)
            
            # Download opcija za uploaded sliku
            st.download_button(
                label="📥 Preuzmi sliku",
                data=uploaded_file.getvalue(),
                file_name=f"MuraDrava_{uploaded_file.name}",
                mime=f"image/{uploaded_file.name.split('.')[-1]}"
            )

# Sidebar - samo kontakt
st.sidebar.markdown("---")
st.sidebar.markdown("📧 MuraDrava-FFS")
st.sidebar.markdown("🌊 Sustav za praćenje vodostaja")

if __name__ == "__main__":
    main()
