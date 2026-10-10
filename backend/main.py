from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import pandas as pd
import numpy as np
import os
import json

app = FastAPI(title="Kestrel Home - Service Routing API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model on startup
MODEL_PATH = os.path.join(os.path.dirname(__file__), '..', 'models', 'routing_model.pkl')
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Warning: Could not load model: {e}")

class ServiceRequest(BaseModel):
    request_id: str
    created_at_ist: str = None
    channel: str
    product_family: str
    warranty_status: str
    request_text: str
    source: str = "crm"

from typing import Optional

class RouteResponse(BaseModel):
    predicted_team: str
    confidence: float
    reasons: list[str]
    signals: dict
    model_version: str
    needs_review: bool
    review_reason: Optional[str] = None
    is_safety_incident: bool = False
    safety_triggers: list[str] = []

@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    return {"status": "healthy", "model_loaded": True}

@app.get("/api/teams")
def get_teams():
    return [
        "Installs & Demo",
        "Repairs",
        "Filters & Consumables",
        "Billing",
        "Returns & Replacement",
        "Warranty Claims",
        "Product Advice"
    ]

@app.get("/api/model-info")
def get_model_info():
    metrics_path = os.path.join(os.path.dirname(__file__), '..', 'reports', 'metrics.json')
    try:
        with open(metrics_path, 'r') as f:
            metrics = json.load(f)
        return {"model_version": "v1.0.0 (LinearSVC)", "metrics": metrics}
    except Exception:
        return {"model_version": "v1.0.0 (LinearSVC)", "metrics": {}}

@app.post("/api/route", response_model=RouteResponse)
def route_request(req: ServiceRequest):
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Preprocess
    df = pd.DataFrame([{
        'request_id': req.request_id,
        'request_text': req.request_text,
        'product_family': req.product_family,
        'channel': req.channel,
        'warranty_status': req.warranty_status
    }])
    
    # Predict
    predicted_team = model.predict(df)[0]
    
    # Confidence
    # Since we used LinearSVC, it uses decision_function. 
    # We will approximate confidence or use max margin, but to be safe and calibrated we can just normalize it loosely 
    # or rely on distance to margin. Since it's not a probability, we must document this constraint.
    try:
        decisions = model.decision_function(df)[0]
        # Softmax over decision function for a pseudo-probability
        exp_dec = np.exp(decisions - np.max(decisions))
        probs = exp_dec / exp_dec.sum()
        confidence = float(np.max(probs))
    except Exception:
        confidence = 0.0
    
    # Safety Check
    import re
    safety_patterns = [r'\bfire\b', r'\bsmoke\b', r'\bburn(?:ing|t)?\b', r'electric(?:al)? shock', r'overheating', r'\bspark(?:s|ing)?\b']
    negation_patterns = [r'\bno\b', r'\bnot\b', r'\bdidn\'t\b', r'\bdoes not\b', r'\bnever\b', r'\bwithout\b']
    
    safety_triggers = []
    text_lower = req.request_text.lower()
    
    for pattern in safety_patterns:
        for match in re.finditer(pattern, text_lower):
            # Check context window (previous 3 words) for negations
            start = max(0, match.start() - 25)
            context = text_lower[start:match.start()]
            if not any(re.search(neg, context) for neg in negation_patterns):
                safety_triggers.append(match.group())
    
    # Deduplicate triggers
    safety_triggers = list(set(safety_triggers))
    is_safety_incident = len(safety_triggers) > 0

    # Reasons & Signals
    reasons = []
    signals = {
        "text_length": len(req.request_text),
        "product_family": req.product_family,
        "warranty_status": req.warranty_status
    }
    
    if is_safety_incident:
        reasons.append(f"CRITICAL: Message indicates a potential safety hazard (trigger words: {', '.join(safety_triggers)}).")
        
    billing_keywords = ['invoice', 'gst', 'double charge', 'refund', 'emi conversion']
    if any(k in text_lower for k in billing_keywords):
        reasons.append("Detected keywords related to payments or invoices.")
        
    return_keywords = ['damage', 'broken', 'wrong', 'missing', 'return', 'exchange', 'incomplete']
    if predicted_team == 'Returns & Replacement' and any(k in text_lower for k in return_keywords):
        reasons.append("Text mentions physical damage, returns, or wrong deliveries.")
        
    repair_keywords = ['noise', 'leak', 'not working', 'error', 'fault', 'broken']
    if predicted_team == 'Repairs' and any(k in text_lower for k in repair_keywords):
        reasons.append("Reported symptoms typically requiring a technician visit.")
    
    if req.warranty_status == 'out_of_warranty' and predicted_team == 'Repairs':
        reasons.append("Flagged as a chargeable repair due to out-of-warranty status.")
        
    if not reasons:
        reasons.append(f"Model routed to {predicted_team} based on historical patterns for {req.product_family}.")
    
    needs_review = confidence < 0.40 or is_safety_incident
    
    review_reason = None
    if needs_review:
        reasons_list = []
        if is_safety_incident:
            reasons_list.append("Potential safety hazard detected.")
        if confidence < 0.40:
            reasons_list.append(f"Low model confidence ({round(confidence*100, 1)}%).")
        review_reason = " ".join(reasons_list)

    # Hard policy checks
    
    return RouteResponse(
        predicted_team=predicted_team,
        confidence=round(confidence, 4),
        reasons=reasons,
        signals=signals,
        model_version="v1.0.0",
        needs_review=needs_review,
        review_reason=review_reason,
        is_safety_incident=is_safety_incident,
        safety_triggers=safety_triggers
    )
