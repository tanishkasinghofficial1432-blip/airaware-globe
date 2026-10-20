# TinyFish AI Integration Guide

This document explains how the **TinyFish** component is integrated into the **AirAware** architecture to support air quality index calculations and predictive AI modeling.

## Overview
TinyFish serves as a core processing layer in our data pipeline. It assists in transforming raw sensor/station telemetry into structured formats ready for evaluation by our predictive AI models.

## Integration Architecture

### 1. Frontend UI Preparation (Streamlit)
We designed explicit CSS styling structures to present TinyFish telemetry cards seamlessly inside the sidebar/dashboard environment.
```css
/* Extracted from your main application styles */
.tinyfish-card {
    background: linear-gradient(135deg, #17131F, #0C1423);
    border: 1px solid #3A2B30;
    border-radius: 13px;
    padding: 16px 18px;
    margin: 10px 0;
}

.tinyfish-step {
    color: #F3A45D;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}
```

### 2. Backend Data Fetching & Pipelines
TinyFish data metrics are ingested or linked via endpoints. Here is a conceptual representation of how data flows through our integrated script:

```
# To be expanded with your active backend endpoints
def fetch_tinyfish_metrics():
    # Placeholder for TinyFish device ingestion or API call
    # response = requests.get("TINYFISH_ENDPOINT")
    pass
```

## How to Verify the Integration
1. Run the Streamlit application: `streamlit run app.py`
2. Check the sidebar for the integrated TinyFish partner credits and telemetry cards.
3. Review data ingestion scripts to ensure telemetry inputs flow directly into the `get_demo_data()` processing layers.
