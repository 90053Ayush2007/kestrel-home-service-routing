# Kestrel Home - Service Routing (Variant B)

## Project Purpose
A machine learning and full-stack web application designed to automatically route incoming customer service requests (via Email, IVR, Chat, WhatsApp) to the correct internal department. This replaces a costly legacy vendor routing bot (saving ₹3.2L/year) and aims to minimize internal misrouting transfers.

## Architecture
- **Data & ML**: Python, Pandas, Scikit-Learn (TF-IDF + LinearSVC).
- **Backend API**: FastAPI, serving predictions, confidence scores, and reasoning via REST.
- **Frontend Dashboard**: React + Vite + TypeScript interface for operations review.

## Data Preprocessing
- Ground truth target mapped to the `final_team` extracted from `resolution_log.csv`, explicitly ignoring the vendor bot's flawed `team_label`.
- Legacy team names mapped to current 7 permitted queues ("Installations" -> "Installs & Demo", "Consumables" -> "Filters & Consumables").

## Validation Results
- **Validation Accuracy**: 83.2%
- **Macro F1**: 82.9%
Detailed metrics can be found in `reports/`.

## Setup & Run Instructions

**Prerequisites:** Python 3.10+, Node.js 18+.

**1. Clean Environment Setup**
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

**2. Model Training & Evaluation**
```bash
# Evaluate models and generate reports
python scripts/evaluate.py

# Generate test predictions.csv
python scripts/predict.py
```

**3. Run FastAPI Backend**
```bash
# From project root
$env:PYTHONPATH="."  # For Windows
# export PYTHONPATH="." # For Mac/Linux

uvicorn backend.main:app --reload
```
API runs on `http://localhost:8000`.

**4. Run React Frontend**
```bash
cd frontend
npm install
npm run dev
```
Dashboard runs on `http://localhost:5173`.

## Tests
```bash
$env:PYTHONPATH="." 
pytest tests/
```

## AI Use & Cost Disclosure
This repository was generated autonomously using Antigravity AI. The model selection heavily prioritizes local, open-source execution. There are no ongoing paid API costs (e.g., no OpenAI credits required). The deployment operates purely on Python/Scikit-Learn.
