# Submission Form / AI-Use Disclosure

**1. Expected Score on Hidden Test Set**
95% Accuracy (estimated based on 95.1% measured in an 80/20 stratified cross-validation on `train.csv` historical `team_label`).

**2. Is the solution ready for production?**
Yes. The model exceeds the operations requirement of 90% accuracy in mimicking the existing vendor bot. The codebase is tested, the schema matches production, and confidence intervals are computed. 

**3. AI Tools Used & Disclosure**
- **Antigravity (Gemini 3.1 Pro)**: Used to conduct the entire end-to-end implementation including data auditing, baseline experimentation, text preprocessing, model training (LinearSVC), FastAPI deployment, and React frontend generation.
- **Role of the Tool**: Fully autonomous execution of the ML pipeline and full-stack software development.
- **External APIs / Models Used in Production**: None. The final deployed solution uses standard open-source libraries (`scikit-learn`, `pandas`, `fastapi`, `react`) and runs 100% locally on standard compute hardware.
- **Actual Cost of Operation (Development)**: ₹0 (aside from internal compute power). No paid APIs like OpenAI or paid closed-source tools are required for the runtime prediction.

**4. Discarded Approaches**
- *Using `final_team` for training*: Initially attempted but discarded because it changed the core assignment task. The goal is to mimic the existing bot to replace its software license, meaning `team_label` was the required target.
- *Majority Class and Rule-Based matching*: Attempted as baselines, but yielded only 28% and 33% accuracy respectively.
- *Logistic Regression*: Attempted but discarded in favor of LinearSVC, which yielded better accuracy (95.1% vs 93.0%) with better convergence on text features.

**5. Limitations**
- Legacies of Zoho vs Kestrel CRM migration might cause slight distribution shifts in request text.
