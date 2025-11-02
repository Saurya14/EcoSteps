
EcoSteps — Deployable Streamlit Web App
--------------------------------------

This folder contains a ready-to-deploy Streamlit web app for 'EcoSteps' — a personal carbon footprint calculator oriented to India.

Files:
- app.py             : Streamlit application (main)
- requirements.txt   : Python packages required
- README.md          : This file

How to deploy (Streamlit Cloud):
1. Create a GitHub repository and upload the files from this folder (do NOT upload venv/).
2. Go to https://share.streamlit.io and log in with GitHub.
3. Click 'New app' → select your repo → branch → 'app.py' → Deploy.
4. Once deployed you'll get a URL usable on phones and laptops.

How to run locally (if you prefer):
1. Install Python 3.10 or 3.11 (recommended). Avoid Python 3.14 as of 2025.
2. Open a terminal in this folder.
3. python -m venv venv
4. venv\Scripts\activate   (Windows) or source venv/bin/activate (mac/linux)
5. pip install -r requirements.txt
6. streamlit run app.py

Notes:
- This app uses coarse emission factors for illustration. Not a full LCA.
- The UI is responsive and mobile-friendly. Theme can be toggled in the sidebar.
