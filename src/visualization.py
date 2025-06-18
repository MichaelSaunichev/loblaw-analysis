import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

DB_PATH = "db/loblaw.db"
CELL_TYPES = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

def load_responder_data(db_path=DB_PATH):
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

    # Normalize
    df['total'] = df[CELL_TYPES].sum(axis=1)
    for cell in CELL_TYPES:
        df[cell + '_pct'] = df[cell] / df['total'] * 100

    return df

def plot_boxplots(df):
    melted = pd.melt(
        df,
        id_vars=['response'],
        value_vars=[f"{cell}_pct" for cell in CELL_TYPES],
        var_name="population",
        value_name="percentage"
    )
    melted['population'] = melted['population'].str.replace('_pct', '')

    plt.figure(figsize=(10, 6))
    sns.boxplot(data=melted, x='population', y='percentage', hue='response')
    plt.title('Immune Cell Population % by Response')
    plt.ylabel('Relative Frequency (%)')
    plt.xlabel('Cell Population')
    plt.legend(title='Response')
    plt.tight_layout()
    plt.show()
