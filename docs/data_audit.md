# Data Audit Report

## 1. File Inspection & Data Shapes
- **train.csv**: 10,822 rows, 8 columns. No missing values, no duplicates.
  - Columns: `request_id`, `created_at_ist`, `channel`, `product_family`, `warranty_status`, `request_text`, `source`, `team_label`
- **test_unlabelled.csv**: 2,178 rows, 7 columns. No missing values, no duplicates.
  - Columns: Same as train, minus `team_label`.
- **resolution_log.csv**: 10,822 rows, 5 columns. No missing values, no duplicates.
  - Columns: `request_id`, `first_team`, `final_team`, `transfers`, `resolved_at`
- **sample_submission.csv**: 2,178 rows, 2 columns (`request_id`, `team`). Matches test rows exactly.

## 2. Historical Destination-Team Label
The field containing the historical label is `team_label` in `train.csv`. This represents the queue assigned by the existing bot. Note that `final_team` in `resolution_log.csv` is the team that ultimately resolved the issue.

## 3. Unique Identifiers and Output Format
- Unique Identifier: `request_id` (present and unique in all datasets).
- Output format: CSV with exactly two columns `request_id` and `team`. Order of rows must match `test_unlabelled.csv`.

## 4. The 7 Permitted Team Names
Based on `teams.csv` and the operations policy:
1. **Installs & Demo** (formerly Installations)
2. **Repairs**
3. **Filters & Consumables** (formerly Consumables)
4. **Billing**
5. **Returns & Replacement**
6. **Warranty Claims**
7. **Product Advice**

## 5. Team vs. Resolution Log
`team_label` in `train.csv` is the team assigned by the bot. `final_team` in `resolution_log.csv` is the team that actually closed the request (post-transfers). Since we want to predict the *correct* destination team to minimize transfers (which cost Rs 305 each), the true label we should be learning from is `final_team` from `resolution_log.csv`, mapping any legacy names to the new 7 permitted names.

## 6. Policy Rules and Specific Constraints
- **Billing**: Only when the problem is the payment itself (invoice, GST, double charge, refund, EMI conversion). Mentioning "paid" does not make it a billing request.
- **Transfers**: Cost Rs 305. Misroutes generate extra customer contact (Rs 260).
- **Time/Legacy**: "legacy_zoho" source means the request was before Oct 1, 2025. Legacy events may have odd text encoding and UTC timestamps instead of IST.
- **Team name changes**: Occurred on 15 Jan 2026.

## 7. Data Leakage Risks
- **resolution_log.csv** must not be used as an input feature for prediction because it contains post-routing outcomes (`transfers`, `resolved_at`, `final_team`).
- Legacy vs CRM source text differences.
- Duplicate requests from the same customer (no explicit customer_id provided, but `request_text` might have near-duplicates).
- `team_label` is the bot's prediction, NOT the ground truth. `final_team` is the true routing destination.

## 8. Expected Submission & Disclosure
- **Predictions**: `predictions.csv` with exactly 2178 rows.
- **Memo**: `memo_to_ritu.md` containing business evaluation (savings vs Rs 3.2 lakh cost).
- **Form**: Fill out submission form / AI-use disclosure.
