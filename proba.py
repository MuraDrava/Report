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
    
    if found_files:
        # Ako je pronađena samo jedna datoteka
        if len(found_files) == 1:
            image_path = found_files[0]
            report_type = get_report_type(image_path)
            
            st.subheader(report_type)
            st.success(f"✅ Pronađena datoteka: `{image_path}`")
            
            # Prikaži sliku
            image = Image.open(image_path)
            st.image(image, use_container_width=True)
            
            # Download opcija
            with open(image_path, "rb") as file:
                file_extension = image_path.split('.')[-1]
                download_name = f"MuraDrava_{report_type.split()[-1]}_{image_path}"
                
                btn = st.download_button(
                    label="📥 Preuzmi izvještaj",
                    data=file,
                    file_name=download_name,
                    mime=f"image/{file_extension}"
                )
        
        # Ako je pronađeno više datoteka, daj izbor
        else:
            st.subheader("📁 Pronađeno više izvještaja")
            
            # Selectbox za odabir datoteke
            selected_file = st.selectbox(
                "Odaberite izvještaj:",
                found_files,
                format_func=lambda x: f"{get_report_type(x)} - {x}")
            
            if selected_file:
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
                        label="📥 Preuzmi odabrani izvještaj",
                        data=file,
                        file_name=download_name,
                        mime=f"image/{file_extension}"
                    )
        
        # Prikaži listu svih pronađenih datoteka
        with st.expander("📋 Sve pronađene datoteke"):
            for file in found_files:
                file_type = get_report_type(file)
                file_size = os.path.getsize(file) / 1024  # KB
                st.write(f"• **{file}** - {file_type} - {file_size:.1f} KB")
    
    else:
        st.error("❌ Nisu pronađene datoteke s nazivom 'redovni' ili 'posebni'")
        st.info("""
        💡 **Molimo provjerite da datoteka sadrži:**
        - Riječ **'redovni'** ili **'posebni'** u nazivu
        - Ekstenziju **.png**, **.jpg** ili **.jpeg**
        
        **Primjeri validnih naziva:**
        - `2025-05-16_redovni_izvjestaj.png`
        - `posebni_2025-05-16.jpg`
        - `muradrava_redovni.png`
        """)
        
        # Prikaži sve PNG/JPG datoteke u direktoriju
        all_images = glob.glob("*.png") + glob.glob("*.jpg") + glob.glob("*.jpeg")
        
        if all_images:
            st.subheader("📁 Sve slike u direktoriju:")
            for img in all_images:
                st.write(f"• {img}")
        
        # Upload opcija
        st.subheader("📤 Ili uploadajte sliku:")
        uploaded_file = st.file_uploader(
            "Odaberite PNG/JPG datoteku",
            type=['png', 'jpg', 'jpeg'],
            help="Podržani formati: PNG, JPG, JPEG"
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

# Sidebar informacije
st.sidebar.markdown("### ℹ️ Kako koristiti")
st.sidebar.markdown("""
**Aplikacija automatski pronalazi slike s nazivima:**
- `*redovni*` (redovni izvještaji)
- `*posebni*` (posebni izvještaji)

**Podržani formati:** PNG, JPG, JPEG

**Primjeri validnih naziva:**
- `2025-05-16_redovni.png`
- `posebni_izvjestaj_16-05.jpg`
- `muradrava_redovni_prognoza.png`
- `hitni_posebni_2025.jpeg`

**Ako ima više datoteka:**
- Možete birati koju želite prikazati
""")

st.sidebar.markdown("---")
st.sidebar.markdown("📧 Za pomoć kontaktirajte admin")

if __name__ == "__main__":
    main()
