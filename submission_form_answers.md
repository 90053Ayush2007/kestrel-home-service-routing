# Submission Form / AI-Use Disclosure

**1. Expected Score on Hidden Test Set**
83% Accuracy (estimated based on 83.2% measured in an 80/20 stratified cross-validation on `resolution_log.csv` final teams).

**2. Is the solution ready for production?**
It is ready for a shadow-mode pilot. The codebase is tested, the schema matches production, and confidence intervals are computed. However, since the validation accuracy is 83.2%, it does not strictly meet the requested 90% threshold for full autonomous deployment without a human-in-the-loop fallback for low-confidence requests.

**3. AI Tools Used & Disclosure**
- **Antigravity (Gemini 3.1 Pro)**: Used to conduct the entire end-to-end implementation including data auditing, baseline experimentation, text preprocessing, model training (LinearSVC), FastAPI deployment, and React frontend generation.
- **Role of the Tool**: Fully autonomous execution of the ML pipeline and full-stack software development.
- **External APIs / Models Used in Production**: None. The final deployed solution uses standard open-source libraries (`scikit-learn`, `pandas`, `fastapi`, `react`) and runs 100% locally on standard compute hardware.
- **Actual Cost of Operation (Development)**: ₹0 (aside from internal compute power). No paid APIs like OpenAI or paid closed-source tools are required for the runtime prediction.

**4. Discarded Approaches**
- *Using `team_label` for training*: Discarded because `team_label` is the output of the flawed existing bot. We used `final_team` from the resolution log as the ground truth.
- *Majority Class and Rule-Based matching*: Attempted as baselines, but yielded only 23% and 27% accuracy respectively.
- *Logistic Regression*: Attempted but discarded in favor of LinearSVC, which yielded ~1% better accuracy and F1 score with better convergence on text features.

**5. Limitations**
- Legacies of Zoho vs Kestrel CRM migration might cause slight distribution shifts in request text.
- Short textual inputs with multiple issues ("needs repair and refund") heavily confuse the linear model, meaning human review is unavoidable for the lowest-confidence percentiles.
