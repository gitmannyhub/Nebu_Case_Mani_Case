# Supply Planning Decision Engine

A Python + Streamlit decision support prototype developed as part of a Supply Chain & Logistics business case.

## Overview

This prototype demonstrates a structured supply planning decision framework for managing supply disruptions, inventory shortages and allocation decisions.

The planning engine follows a rule-based hierarchy inspired by real-world supply planning practices.

## Decision Hierarchy

```
Inventory Health
        ↓
Stock Balance
        ↓
Pull Logic (Oldest PO First)
        ↓
Push Logic (Newest PO First)
        ↓
PO Shortage
        ↓
Allocation Engine
        ↓
Backlog Risk
```

## Features

- Executive Summary
- Inventory Health
- Purchase Order Health
- Stock Balance
- Pull Logic
- Push Logic
- PO Shortage
- Allocation Engine
- Backlog Risk
- Supplier Health
- Decision Log
- AI Executive Summary

## Technologies

- Python
- Streamlit
- Pandas

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Disclaimer

This project is a demonstration prototype created for a supply planning business case. It is intended to illustrate planning logic and reporting concepts rather than production-ready software.