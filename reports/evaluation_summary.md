# Evaluation Summary

## Best Model: LinearSVC
- **Validation Accuracy**: 83.23%
- **Macro F1**: 0.8291
- **Weighted F1**: 0.8329

## Model Comparison
             Model  Accuracy  Macro_F1
          Majority  0.234180  0.054213
            Policy  0.277136  0.130495
LogisticRegression  0.823095  0.819498
         LinearSVC  0.832333  0.829060

## Common Errors
Top 5 misrouting pairs:
      true_team        predicted_team  count
        Repairs       Installs & Demo     22
        Repairs Returns & Replacement     19
        Repairs Filters & Consumables     15
Installs & Demo Filters & Consumables     15
        Repairs       Warranty Claims     15
