import pandas as pd

files = {
    'train': 'train.csv',
    'test': 'test_unlabelled.csv',
    'resolution': 'resolution_log.csv',
    'sample_sub': 'sample_submission.csv'
}

for name, path in files.items():
    print(f"\n--- {name.upper()} ---")
    try:
        df = pd.read_csv(path)
        print(f"Shape: {df.shape}")
        print("Columns:", df.columns.tolist())
        print("Missing values:\n", df.isnull().sum())
        print("Duplicate rows:", df.duplicated().sum())
        if 'request_id' in df.columns:
            print("Duplicate request_ids:", df['request_id'].duplicated().sum())
        if 'team_label' in df.columns:
            print("\nTeam Label Distribution:")
            print(df['team_label'].value_counts(dropna=False))
        if 'team' in df.columns:
            print("\nTeam Distribution:")
            print(df['team'].value_counts(dropna=False))
            
    except Exception as e:
        print(f"Error reading {path}: {e}")
