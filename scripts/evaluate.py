import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import joblib

# Setup directories
os.makedirs('reports', exist_ok=True)
os.makedirs('models', exist_ok=True)

print("Loading data...")
train_df = pd.read_csv('train.csv')
res_df = pd.read_csv('resolution_log.csv')

# Merge
df = train_df.merge(res_df, on='request_id', how='left')

# Standardize team names based on policy
team_mapping = {
    'Installations': 'Installs & Demo',
    'Consumables': 'Filters & Consumables'
}
df['final_team_std'] = df['final_team'].replace(team_mapping)

print(f"Total merged records: {len(df)}")
print(f"Target distribution:\n{df['final_team_std'].value_counts()}")

# Features and target
X = df[['request_id', 'request_text', 'product_family', 'channel', 'warranty_status']]
# Fill na just in case
X.loc[:, 'request_text'] = X['request_text'].fillna('')
y = df['final_team_std']

# Train/Val split
X_train, X_val, y_train, y_val = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training set size: {len(X_train)}")
print(f"Validation set size: {len(X_val)}")

# 1. Majority Class Baseline
majority_class = y_train.mode()[0]
y_pred_maj = [majority_class] * len(y_val)
acc_maj = accuracy_score(y_val, y_pred_maj)
f1_maj = f1_score(y_val, y_pred_maj, average='macro')

# 2. Policy Baseline
# "A request belongs to Billing only when the problem is the payment itself (invoice, GST, double charge, refund of a payment, EMI conversion)."
def policy_baseline(row):
    text = str(row['request_text']).lower()
    billing_keywords = ['invoice', 'gst', 'double charge', 'refund', 'emi conversion']
    if any(k in text for k in billing_keywords):
        return 'Billing'
    return majority_class

y_pred_pol = X_val.apply(policy_baseline, axis=1)
acc_pol = accuracy_score(y_val, y_pred_pol)
f1_pol = f1_score(y_val, y_pred_pol, average='macro')

# 3. TF-IDF + Logistic Regression
preprocessor = ColumnTransformer(
    transformers=[
        ('text', TfidfVectorizer(max_features=5000, ngram_range=(1, 2), stop_words='english'), 'request_text'),
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['product_family', 'channel', 'warranty_status'])
    ],
    remainder='drop'
)

lr_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LogisticRegression(class_weight='balanced', max_iter=1000, random_state=42))
])

print("Training Logistic Regression...")
lr_pipeline.fit(X_train, y_train)
y_pred_lr = lr_pipeline.predict(X_val)
acc_lr = accuracy_score(y_val, y_pred_lr)
f1_lr = f1_score(y_val, y_pred_lr, average='macro')

# 4. TF-IDF + LinearSVC
svc_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('classifier', LinearSVC(class_weight='balanced', random_state=42, dual='auto'))
])

print("Training LinearSVC...")
svc_pipeline.fit(X_train, y_train)
y_pred_svc = svc_pipeline.predict(X_val)
acc_svc = accuracy_score(y_val, y_pred_svc)
f1_svc = f1_score(y_val, y_pred_svc, average='macro')

# Compare models
model_comparison = pd.DataFrame({
    'Model': ['Majority', 'Policy', 'LogisticRegression', 'LinearSVC'],
    'Accuracy': [acc_maj, acc_pol, acc_lr, acc_svc],
    'Macro_F1': [f1_maj, f1_pol, f1_lr, f1_svc]
})
print("\nModel Comparison:")
print(model_comparison)
model_comparison.to_csv('reports/model_comparison.csv', index=False)

# Select best model (assume LR for now, unless SVC is significantly better)
if f1_svc > f1_lr:
    best_model = svc_pipeline
    best_name = "LinearSVC"
    y_pred_best = y_pred_svc
else:
    best_model = lr_pipeline
    best_name = "LogisticRegression"
    y_pred_best = y_pred_lr

print(f"\nSelected Best Model: {best_name}")

# Metrics for best model
metrics = {
    'accuracy': float(accuracy_score(y_val, y_pred_best)),
    'macro_f1': float(f1_score(y_val, y_pred_best, average='macro')),
    'weighted_f1': float(f1_score(y_val, y_pred_best, average='weighted')),
    'train_size': len(X_train),
    'val_size': len(X_val)
}
with open('reports/metrics.json', 'w') as f:
    json.dump(metrics, f, indent=2)

# Classification report
report_dict = classification_report(y_val, y_pred_best, output_dict=True)
report_df = pd.DataFrame(report_dict).transpose()
report_df.to_csv('reports/classification_report.csv')
print("\nClassification Report:")
print(classification_report(y_val, y_pred_best))

# Confusion Matrix
labels = sorted(y_val.unique())
cm = confusion_matrix(y_val, y_pred_best, labels=labels)
cm_df = pd.DataFrame(cm, index=labels, columns=labels)
cm_df.to_csv('reports/confusion_matrix.csv')

# Error Analysis: Validation Predictions
val_results = X_val.copy()
val_results['true_team'] = y_val
val_results['predicted_team'] = y_pred_best
val_results['is_error'] = val_results['true_team'] != val_results['predicted_team']

# Probabilities/Confidence if available
if hasattr(best_model.named_steps['classifier'], 'predict_proba'):
    probs = best_model.predict_proba(X_val)
    confidence = np.max(probs, axis=1)
    val_results['confidence'] = confidence
else:
    # for SVC, use decision function
    decs = best_model.decision_function(X_val)
    # rudimentary confidence: max margin
    confidence = np.max(decs, axis=1)
    val_results['confidence'] = confidence

val_results.to_csv('reports/validation_predictions.csv', index=False)

# Summary of Errors
error_df = val_results[val_results['is_error']]
error_summary = error_df.groupby(['true_team', 'predicted_team']).size().reset_index(name='count')
error_summary = error_summary.sort_values('count', ascending=False)
error_summary.to_csv('reports/error_analysis.csv', index=False)
print("\nTop 5 misrouting pairs:")
print(error_summary.head(5))

# Save the best model
joblib.dump(best_model, 'models/routing_model.pkl')
print("\nModel saved to models/routing_model.pkl")

# Generate markdown evaluation summary
summary_md = f"""# Evaluation Summary

## Best Model: {best_name}
- **Validation Accuracy**: {metrics['accuracy']:.2%}
- **Macro F1**: {metrics['macro_f1']:.4f}
- **Weighted F1**: {metrics['weighted_f1']:.4f}

## Model Comparison
{model_comparison.to_string(index=False)}

## Common Errors
Top 5 misrouting pairs:
{error_summary.head(5).to_string(index=False)}
"""
with open('reports/evaluation_summary.md', 'w') as f:
    f.write(summary_md)
