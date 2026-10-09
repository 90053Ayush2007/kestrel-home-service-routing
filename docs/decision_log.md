# Decision Log

## Phase 1: Inspection & Ground Truth
- **Decision 1**: The training ground truth is `team_label` from `train.csv`.
  - **Reason**: The operations director explicitly requested a classifier that matches the existing 18 months of labelled routing data at 90%+ to retire the bot. Training on `final_team` from the resolution log changes the task from mimicking the bot to predicting final human outcomes, which fails the core assignment instruction.
- **Decision 2**: Normalize legacy team names to the 7 permitted teams.
  - **Reason**: The policy states that as of Jan 15, 2026, "Installations" became "Installs & Demo", and "Consumables" became "Filters & Consumables". Both the legacy labels and the current ones appear in the data. We will map the legacy names to the new names for all training data.
- **Decision 3**: Use text preprocessing to handle Zoho desk odd characters.
  - **Reason**: The email thread mentions that legacy_zoho records "came across with odd characters". We will apply standard cleaning to the `request_text`.
- **Decision 4**: Validation strategy will be a stratified train/val split (80/20) on the mapped `team_label`.
  - **Reason**: We need to estimate real-world performance on unseen data before making business recommendations.
- **Decision 5**: Use `request_text`, `product_family`, `warranty_status`, and `channel` as features.
  - **Reason**: These are the only features available at prediction time. `source` and `created_at_ist` might carry signal but are more likely to cause time-based leakage or dataset shift.

## Evaluation & Baseline
- We evaluated Majority-Class, a Policy-based baseline, and TF-IDF + Logistic Regression/LinearSVC.
- LinearSVC proved optimal, achieving >95% accuracy, exceeding the 90% target threshold.
