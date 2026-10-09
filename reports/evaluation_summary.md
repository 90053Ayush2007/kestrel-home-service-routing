# Evaluation Summary

## Best Model: LinearSVC
- **Validation Accuracy**: 95.10%
- **Macro F1**: 0.9500
- **Weighted F1**: 0.9511

## Model Comparison
             Model  Accuracy  Macro_F1
          Majority  0.289145  0.064084
            Policy  0.339492  0.137069
LogisticRegression  0.930716  0.930410
         LinearSVC  0.951039  0.949966

## Common Errors
Top 5 misrouting pairs:
      true_team        predicted_team  count
        Repairs Filters & Consumables     19
        Repairs       Warranty Claims      7
        Repairs               Billing      6
 Product Advice               Billing      5
Installs & Demo               Repairs      4
