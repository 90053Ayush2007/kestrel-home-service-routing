# Decision Log

## Phase 1: Inspection & Ground Truth
- **Decision 1**: The training ground truth is `final_team` from `resolution_log.csv`, not `team_label` from `train.csv`.
  - **Reason**: `team_label` is the output of the *existing vendor bot*, which we know misroutes (causing transfers). `final_team` is the team that successfully closed the request. To build a system better than the bot, we must train on the final correct destination.
- **Decision 2**: Normalize team names to the 7 permitted teams.
  - **Reason**: The policy states that as of Jan 15, 2026, "Installations" became "Installs & Demo", and "Consumables" became "Filters & Consumables". Both the legacy labels and the current ones appear in the data. We will map the legacy names to the new names for all training data.
- **Decision 3**: Use text preprocessing to handle Zoho desk odd characters.
  - **Reason**: The email thread mentions that legacy_zoho records "came across with odd characters". We will apply standard cleaning (e.g., unicode normalization, regex filtering) to the `request_text`.
- **Decision 4**: Validation strategy will be a stratified train/val split (e.g., 80/20) on the mapped `final_team`.
  - **Reason**: We need to estimate real-world performance on unseen data before making business recommendations. Stratification ensures all 7 classes are proportionally represented.
- **Decision 5**: Use `request_text`, `product_family`, `warranty_status`, and `channel` as features.
  - **Reason**: These are the only features available at prediction time. `source` and `created_at_ist` might carry signal but are more likely to cause time-based leakage or dataset shift.

## Evaluation & Baseline
- We will evaluate Majority-Class, a Policy-based baseline (rule matching for Billing), and a TF-IDF + Logistic Regression/LinearSVC model.
- We will optimize for macro-F1 and Accuracy, ensuring we can predict the right queue to save transfer costs.
