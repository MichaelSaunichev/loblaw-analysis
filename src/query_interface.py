import sqlite3
import pandas as pd

DB_PATH = "db/loblaw.db"

def get_baseline_tr1_melanoma_pbmc_samples(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)

    query = '''
    SELECT sample_id, project, response, sex
    FROM samples
    WHERE condition = 'melanoma'
      AND treatment = 'tr1'
      AND sample_type = 'PBMC'
      AND time_from_treatment = 0
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def summarize_baseline_subset(df: pd.DataFrame):
    summary = {}

    # Sample count per project
    summary['samples_per_project'] = df['project'].value_counts().to_dict()

    # Responder breakdown
    summary['responders_vs_non'] = df['response'].value_counts().to_dict()

    # Sex breakdown
    summary['sex_distribution'] = df['sex'].value_counts().to_dict()

    return summary
