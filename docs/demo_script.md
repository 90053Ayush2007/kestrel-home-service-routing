# Video Demo Walkthrough Script (3 Minutes)

## 0:00–0:30 — Explain the problem and the supplied data.
- **Visuals**: Show `train.csv` and `resolution_log.csv` side by side.
- **Script**: "Kestrel Home currently spends ₹3.2 Lakh annually on a vendor bot for service routing. The data provided includes 18 months of historical tickets. The crucial insight is that the bot's labels (`team_label`) are flawed. Instead, we extracted the true ground truth from `resolution_log.csv` (`final_team`), merging legacy team names per the operations policy to train on the correct 7 permitted destinations."

## 0:30–1:10 — Show the approaches attempted, model comparison and what was changed.
- **Visuals**: Open `reports/model_comparison.csv` and `scripts/evaluate.py`.
- **Script**: "We evaluated 4 approaches: a majority baseline, a policy-based rules engine for Billing, Logistic Regression, and LinearSVC. The simple baselines performed terribly (23-27%), but TF-IDF combined with LinearSVC on text and categorical features achieved 83.2% accuracy. We selected LinearSVC for deployment."

## 1:10–1:50 — Submit a request in the working interface and explain the prediction.
- **Visuals**: Bring up the React Dashboard. Click "Load Sample 1". Click "Route Request".
- **Script**: "Here is our React dashboard connected to the FastAPI backend. Submitting this 'Air Purifier' noise complaint instantly predicts 'Repairs' with high confidence. The backend extracts text features and checks policy rules, returning specific reasons for its choice."
- **Visuals**: Load an ambiguous sample. 
- **Script**: "For ambiguous cases, the UI flags a 'Human Review Recommended' warning, ensuring we don't confidently misroute tricky tickets."

## 1:50–2:25 — Show validation evidence, common errors and limitations.
- **Visuals**: Show `reports/confusion_matrix.csv` or `reports/error_analysis.csv`.
- **Script**: "Our validation strategy used a strict 80/20 stratified split. The error analysis shows that our model mostly struggles between 'Repairs', 'Installs & Demo', and 'Returns', where customer language is highly overlapping. Given this, 83.2% is a highly realistic expectation of true performance, whereas claiming 90% would be overfitting."

## 2:25–3:00 — Show predictions.csv, the business memo and what was discarded.
- **Visuals**: Show `predictions.csv` matching `sample_submission.csv` format, then open `memo_to_ritu.md`.
- **Script**: "Finally, we generated `predictions.csv` for the test set following the exact requested schema. The business memo to Ritu recommends a shadow-mode pilot. The AI deployment costs ~₹40k annually compared to the ₹3.2L bot, yielding an 87% overhead reduction. We discarded purely rule-based systems because they fail on the nuances of customer text."
