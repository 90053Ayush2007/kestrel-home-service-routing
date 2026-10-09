# Expected Score Estimate

## Score Expectation
Based on our rigorous cross-validation strategy on historical data, we expect the deployed model's accuracy on the hidden test set to be **approximately 83% (83.2% measured in validation)**. 

The weighted F1 score and Macro F1 score also cluster around **83%**.

## Validation Result Supporting This Estimate
Our validation split was an 80/20 stratified split trained on 8,657 records and tested on 2,165 records. We trained on the true ground truth `final_team` extracted from the `resolution_log.csv` rather than the faulty bot's predictions (`team_label`). We mapped legacy team names exactly as defined in the operations policy. 
Because the validation sample is large, randomly stratified, and represents the identical data distribution as the recent unlabeled requests, the validation accuracy strongly correlates with expected performance.

## Major Sources of Uncertainty and Failure Cases
- **Ambiguous language**: Some requests overlap heavily between "Repairs" and "Returns & Replacement", or "Repairs" and "Installs & Demo". For instance, a customer reporting a brand-new item not working could be a repair, an installation issue, or a return depending on precise wording.
- **Legacy Artifacts**: The training set contains Zoho desk data migrating to the Kestrel CRM. The test set is the "most recent requests", likely entirely CRM data. This distribution shift could mean our text feature distribution shifts slightly, potentially reducing accuracy by a small margin.
- **Why it might differ**: The hidden evaluation might weigh specific classes more heavily, or recent customer queries may contain emerging product issues not captured well in the 18-month history. 
- **Missing the 90% Target**: The current accuracy is below the 90% bar set by Ritu Deshpande. To reach 90% without risking a massive overfit or inventing data, Kestrel may need to route the ambiguous cases (where the model has low confidence) to a human reviewer.

## Conclusion
We confidently predict ~83% accuracy. We cannot guarantee 90% based on this architecture and features without human-in-the-loop fallback for the most uncertain predictions.
