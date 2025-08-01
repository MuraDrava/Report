# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:33:22 2025

@author: pranjikl
"""

import streamlit as st
from PIL import Image
import os
import glob
import base64
from io import BytesIO

# Postavljanje stranice
st.set_page_config(
    page_title="MuraDrava-FFS Izvještaj",
    page_icon="🌊",
    layout="wide"
)

def image_to_base64(image):
    """Konvertuj PIL sliku u base64 string"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def create_zoom_image(image, image_id="zoom_image"):
    """Kreira HTML/CSS kod za zoom sliku"""
    img_base64 = image_to_base64(image)
    
    html_code = f"""
    <div style="text-align: center; margin: 20px 0;">
        <div style="
            position: relative;
            display: inline-block;
            overflow: hidden;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            cursor: zoom-in;
            max-width: 100%;
            transition: transform 0.3s ease;
        " 
        onclick="toggleZoom('{image_id}')" 
        id="{image_id}_container">
            <img 
                id="{image_id}" 
                src="data:image/png;base64,{img_base64}" 
                style="
                    width: 100%;
                    height: auto;
                    transition: transform 0.3s ease;
                    cursor: zoom-in;
                "
            />
            <div style="
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(0,0,0,0.7);
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
                font-size: 12px;
                opacity: 0.8;
            ">
                🔍 Klikni za zoom
            </div>
        </div>
    </div>
    
    <script>
    function toggleZoom(imageId) {{
        const img = document.getElementById(imageId);
        const container = document.getElementById(imageId + '_container');
        
        if (img.style.transform === 'scale(2)') {{
            // Zoom out
            img.style.transform = 'scale(1)';
            img.style.cursor = 'zoom-in';
            container.style.cursor = 'zoom-in';
            container.style.overflow = 'hidden';
        }} else {{
            // Zoom in
            img.style.transform = 'scale(2)';
            img.style.cursor = 'zoom-out';
            container.style.cursor = 'zoom-out';
            container.style.overflow = 'auto';
        }}
    }}
    </script>
    """
    
    return html_code

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
        
        # Dodaj opciju za zoom način prikaza
        zoom_mode = st.checkbox("🔍 Omogući zoom funkciju", value=True)
        
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
        
        # Učitaj sliku
        image = Image.open(selected_file)
        
        # Prikaži sliku ovisno o zoom opciji
        if zoom_mode:
            st.markdown("### 🔍 Interaktivni prikaz s zoom funkcijom")
            st.markdown("*Kliknite na sliku za povećanje/smanjenje*")
            
            # Prikaži sliku s zoom funkcijom
            zoom_html = create_zoom_image(image, "main_image")
            st.components.v1.html(zoom_html, height=600)
        else:
            # Standardni prikaz
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
            
            # Dodaj zoom opciju i za uploaded slike
            zoom_mode = st.sidebar.checkbox("🔍 Omogući zoom za uploaded sliku", value=True)
            
            if zoom_mode:
                st.markdown("### 🔍 Interaktivni prikaz s zoom funkcijom")
                st.markdown("*Kliknite na sliku za povećanje/smanjenje*")
                
                zoom_html = create_zoom_image(image, "uploaded_image")
                st.components.v1.html(zoom_html, height=600)
            else:
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
st.sidebar.markdown("🌊 MuraDrava-FFS")

if __name__ == "__main__":
    main()
