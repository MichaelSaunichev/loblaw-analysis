import sqlite3
import pandas as pd
from scipy.stats import ttest_ind

DB_PATH = "db/loblaw.db"

CELL_TYPES = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

def generate_summary_table(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)

    query = '''
    SELECT s.sample_id, b_cell, cd8_t_cell, cd4_t_cell, nk_cell, monocyte
    FROM cell_counts cc
    JOIN samples s ON s.sample_id = cc.sample_id
    '''

    df = pd.read_sql_query(query, conn)
    summary_rows = []

    for _, row in df.iterrows():
        total = sum([row[cell] for cell in CELL_TYPES])
        for cell in CELL_TYPES:
            summary_rows.append({
                'sample': row['sample_id'],
                'total_count': total,
                'population': cell,
                'count': row[cell],
                'percentage': round((row[cell] / total) * 100, 2)
            })

    conn.close()
    return pd.DataFrame(summary_rows)

def compare_responders_vs_nonresponders(db_path=DB_PATH):
    conn = sqlite3.connect(db_path)

    query = f'''
    SELECT s.sample_id, s.response, {", ".join(CELL_TYPES)}
    FROM cell_counts cc
    JOIN samples s ON s.sample_id = cc.sample_id
    WHERE s.condition = 'melanoma'
      AND s.treatment = 'tr1'
      AND s.sample_type = 'PBMC'
    '''

    df = pd.read_sql_query(query, conn)
    conn.close()

    # Prepare percentages
    df['total'] = df[CELL_TYPES].sum(axis=1)
    for cell in CELL_TYPES:
        df[cell + '_pct'] = df[cell] / df['total'] * 100

    stats_results = []
    for cell in CELL_TYPES:
        responders = df[df['response'] == 'y'][cell + '_pct']
        non_responders = df[df['response'] == 'n'][cell + '_pct']
        stat, pval = ttest_ind(responders, non_responders, equal_var=False)

        stats_results.append({
            'population': cell,
            'responder_mean': round(responders.mean(), 2),
            'non_responder_mean': round(non_responders.mean(), 2),
            'p_value': round(pval, 4),
            'significant': pval < 0.05
        })

    return pd.DataFrame(stats_results)
