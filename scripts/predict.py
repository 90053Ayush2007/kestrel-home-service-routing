import pandas as pd
import joblib

print("Loading test data...")
test_df = pd.read_csv('test_unlabelled.csv')
sample_sub = pd.read_csv('sample_submission.csv')

# Ensure we have the same request_ids in the same order
if not test_df['request_id'].equals(sample_sub['request_id']):
    raise ValueError("request_id mismatch between test_unlabelled.csv and sample_submission.csv")

print("Loading best model...")
model = joblib.load('models/routing_model.pkl')

X_test = test_df[['request_id', 'request_text', 'product_family', 'channel', 'warranty_status']].copy()
X_test.loc[:, 'request_text'] = X_test['request_text'].fillna('')

print("Generating predictions...")
predictions = model.predict(X_test)

# Verify valid teams
valid_teams = {
    'Installs & Demo', 'Repairs', 'Filters & Consumables',
    'Billing', 'Returns & Replacement', 'Warranty Claims', 'Product Advice'
}

invalid_preds = set(predictions) - valid_teams
if invalid_preds:
    raise ValueError(f"Model generated invalid team names: {invalid_preds}")

# Create predictions dataframe matching sample submission exactly
submission = pd.DataFrame({
    'request_id': test_df['request_id'],
    'team': predictions
})

# Verify constraints
assert len(submission) == len(sample_sub), f"Expected {len(sample_sub)} rows, got {len(submission)}"
assert list(submission.columns) == list(sample_sub.columns), "Columns do not match sample_submission.csv"

print("Saving predictions.csv...")
submission.to_csv('predictions.csv', index=False)

# Quick stats
print(f"Generated {len(submission)} predictions.")
print("Team distribution:")
print(submission['team'].value_counts())
