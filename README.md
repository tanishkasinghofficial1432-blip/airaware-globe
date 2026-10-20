# Air-Aware: AI-Driven Spatial Super-Resolution AQI Mapping

# An advanced Python MVP engineered for the hackathon to eliminate urban air quality blindspots. The system combines an AI web agent infrastructure with machine learning downscaling to map microclimate variations.

🔗 Live Application Dashboard
https://airaware-globe-3cnefqsgmae7gotkcmubhu.streamlit.app/

# Social Media Post: https://lnkd.in/p/dfYwPTh3

🚨 The Core Problem
Official air quality monitoring networks (such as India's CPCB network) rely on sparse, expensive static reference stations. Because ambient air pollution fluctuates block-by-block due to road traffic and localized construction dust, these static grids leave massive urban blind spots where citizens live, work, and commute.

⚙️ How It Works (Technical Framework)
- Dynamic Web Grounding: The system utilizes the TinyFish Search API to deploy an automated web lookup agent. This agent scans the live web context for current regional anchor data reported by official environmental portals.
- Feature Engineering Proxies: The project overlays spatial traffic congestion weights and local industrial emission indicators over a localized coordinate grid matrix.
- Spatial Super-Resolution: A Random Forest Regressor (built using Scikit-Learn) trains on live reference metrics to map out non-linear correlations, generating real-time predictive downscaling across hundreds of unmonitored coordinates simultaneously.
  
🛠️ Tech Stack & Dependencies
- Programming Language: Python 3
- Automation Agent Framework: TinyFish API (Dynamic Web Infrastructure)
- Machine Learning Core: Scikit-Learn (Random Forest Regressor)
- User Interface Framework: Streamlit Cloud Server Environment
- Spatial Map Visuals: PyDeck 3D Geographic Mapping Engine
  
# 💻 Local Setup & Execution Instructions
Clone or download this project repository folder to your laptop.

# Open your terminal inside the project directory and run the following command to install all tracking dependencies automatically:
pip install -r requirements.txt

# Boot up the interactive application on your local network server hosting stream:
streamlit run app.py
