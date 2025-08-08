# -*- coding: utf-8 -*-
"""
Created on Wed Jul 30 16:33:22 2025

@author: pranjikl
"""

import streamlit as st
from PIL import Image
import glob
from io import BytesIO
import base64
import os

st.set_page_config(
    page_title="MuraDrava-FFS",
    page_icon="🌊",
    layout="wide"
)

def find_report_image():
    # Definiraj putanju do reports foldera
    reports_folder = "reports"
    
    # Provjeri postoji li reports folder, ako ne - stvori ga
    if not os.path.exists(reports_folder):
        os.makedirs(reports_folder)
    
    patterns = [
        "*redovni*.png", "*posebni*.png",
        "*redovni*.jpg", "*posebni*.jpg",
        "*redovni*.jpeg", "*posebni*.jpeg"
    ]
    
    found_files = []
    
    # Trazi datoteke u reports folderu
    for pattern in patterns:
        # Kombinuj putanju s pattern-om
        search_pattern = os.path.join(reports_folder, pattern)
        found_files.extend(glob.glob(search_pattern))
    
    found_files = list(set(found_files))
    found_files.sort()
    return found_files

def get_report_type(filename):
    # Uzmi samo naziv datoteke bez putanje
    filename_base = os.path.basename(filename)
    filename_lower = filename_base.lower()
    
    if 'redovni' in filename_lower:
        return "📊 Redovni izvještaj"
    elif 'posebni' in filename_lower:
        return "⚠️ Posebni izvještaj"
    else:
        return "📋 Izvještaj"

def display_image_with_openseadragon(image):
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()

    html = f"""
    <html>
    <head>
      <script src="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/3.1.0/openseadragon.min.js"></script>
      <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/openseadragon/3.1.0/openseadragon.min.css" />
      <style>
        #openseadragon-wrapper {{
          width: 100%;
          height: 400px;
          overflow: auto;
          border: 1px solid #ccc;
          margin-bottom: 20px;
        }}
        #openseadragon {{
          width: 100%;
          height: 400px;
          background-color: #ddd;
        }}
      </style>
    </head>
    <body>
      <div id="openseadragon-wrapper">
        <div id="openseadragon"></div>
      </div>
      <script>
        var viewer = OpenSeadragon({{
          id: "openseadragon",
          prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/3.1.0/images/",
          tileSources: {{
            type: 'image',
            url: "data:image/png;base64,{img_str}"
          }},
          gestureSettingsTouch: {{
            pinchRotate: false,
            pinchToZoom: true,
            flickEnabled: true,
            flickMinSpeed: 20,
            flickMomentum: 0.25
          }}
        }});
      </script>
    </body>
    </html>
    """
    st.components.v1.html(html, height=450)

def main():
    st.title("🌊 MuraDrava-FFS")

    found_files = find_report_image()

    with st.sidebar:
        st.markdown("### 📋 Odabir izvještaja")

        if found_files:
            if len(found_files) == 1:
                selected_file = found_files[0]
                report_type = get_report_type(selected_file)
                st.success(f"✅ {report_type}")
                # Prikazi samo naziv datoteke bez putanje
                st.write(f"📁 `{os.path.basename(selected_file)}`")
            else:
                selected_file = st.selectbox(
                    "Odaberite izvještaj:",
                    found_files,
                    format_func=lambda x: f"{get_report_type(x).split()[-1]} - {os.path.basename(x)}"
                )
        else:
            selected_file = None
            st.error("❌ Nema dostupnih izvještaja u `reports/` folderu")

    if found_files and selected_file:
        report_type = get_report_type(selected_file)
        st.subheader(report_type)

        image = Image.open(selected_file)
        display_image_with_openseadragon(image)

        with open(selected_file, "rb") as file:
            file_extension = selected_file.split('.')[-1]
            # Koristiti samo naziv datoteke za download
            download_name = f"MuraDrava_{os.path.basename(selected_file)}"
            st.download_button(
                label="📥 Preuzmi izvještaj",
                data=file,
                file_name=download_name,
                mime=f"image/{file_extension}"
            )

    elif not found_files:
        st.error("❌ Nisu pronađene datoteke s nazivom 'redovni' ili 'posebni' u `reports/` folderu")

        # Provjeri sve slike u reports folderu
        reports_folder = "reports"
        all_images = []
        if os.path.exists(reports_folder):
            all_images = (glob.glob(os.path.join(reports_folder, "*.png")) + 
                         glob.glob(os.path.join(reports_folder, "*.jpg")) + 
                         glob.glob(os.path.join(reports_folder, "*.jpeg")))

        if all_images:
            st.subheader("📁 Sve slike u reports/ direktoriju:")
            for img in all_images:
                st.write(f"• {os.path.basename(img)}")

        st.subheader("📤 Uploadajte sliku:")
        uploaded_file = st.file_uploader(
            "Odaberite PNG/JPG datoteku",
            type=['png', 'jpg', 'jpeg']
        )

        if uploaded_file is not None:
            report_type = get_report_type(uploaded_file.name)
            st.subheader(report_type)

            image = Image.open(uploaded_file)
            display_image_with_openseadragon(image)

            st.download_button(
                label="📥 Preuzmi sliku",
                data=uploaded_file.getvalue(),
                file_name=f"MuraDrava_{uploaded_file.name}",
                mime=f"image/{uploaded_file.name.split('.')[-1]}"
            )

# Sidebar - kontakt
st.sidebar.markdown("---")
st.sidebar.markdown("🌊 MuraDrava-FFS")

if __name__ == "__main__":
    main()



