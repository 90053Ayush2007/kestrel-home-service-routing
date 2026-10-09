# Data Audit Report

## 1. File Inspection & Data Shapes
- **train.csv**: 10,822 rows, 8 columns. No missing values, no duplicates.
- **test_unlabelled.csv**: 2,178 rows, 7 columns. No missing values, no duplicates.
- **resolution_log.csv**: 10,822 rows, 5 columns. No missing values, no duplicates.
- **sample_submission.csv**: 2,178 rows, 2 columns (`request_id`, `team`). Matches test rows exactly.

## 2. Historical Destination-Team Label
The field containing the historical routing label is `team_label` in `train.csv`. According to the assignment emails ("Kabir - the labels are eighteen months of real routing. 90% match is the bar."), this is the target variable. The `final_team` in `resolution_log.csv` is post-routing human outcome, which is not the objective of this predictive routing bot assignment.

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

## 5. Team Mapping
`team_label` in `train.csv` contains legacy names. We must map "Installations" to "Installs & Demo", and "Consumables" to "Filters & Consumables".

## 6. Policy Rules and Specific Constraints
- **Billing**: Only when the problem is the payment itself.
- **Transfers**: Cost Rs 305. Misroutes generate extra customer contact (Rs 260).
- **Time/Legacy**: "legacy_zoho" source means the request was before Oct 1, 2025. Legacy events may have odd text encoding.

## 7. Data Leakage Risks
- **resolution_log.csv** must not be used as an input feature for prediction because it contains post-routing outcomes (`transfers`, `resolved_at`, `final_team`).
- Duplicate requests from the same customer (no explicit customer_id provided, but `request_text` might have near-duplicates).

## 8. Expected Submission & Disclosure
- **Predictions**: `predictions.csv` with exactly 2178 rows.
- **Memo**: `memo_to_ritu.md` containing business evaluation (savings vs Rs 3.2 lakh cost).
- **Form**: Fill out submission form / AI-use disclosure.
