import streamlit as st

st.set_page_config(page_title="Projek PSBI", layout="wide")

st.title("Projek PSBI — Streamlit Wrapper")

st.write("Ini adalah wrapper Streamlit sederhana. Repo utama adalah aplikasi Django; Streamlit hanya digunakan sebagai demo atau halaman statis cepat.")

st.markdown("- Untuk menjalankan situs utama: gunakan `python manage.py runserver` (Django).")
st.markdown("- Untuk menjalankan Streamlit demo: `streamlit run app.py`")

if st.button("Tampilkan struktur proyek"):
    import os
    for root, dirs, files in os.walk('.', topdown=True):
        # skip virtual env and .git
        dirs[:] = [d for d in dirs if d not in ('.venv', 'venv', '.git')]
        for f in files:
            st.text(os.path.join(root, f))
