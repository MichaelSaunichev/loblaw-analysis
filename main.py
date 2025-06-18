import sys
from src.db_schema import init_db
from src.data_loader import load_data
from src.analysis import generate_summary_table, compare_responders_vs_nonresponders
from src.visualization import load_responder_data, plot_boxplots
from src.query_interface import get_baseline_tr1_melanoma_pbmc_samples, summarize_baseline_subset

def print_main_menu():
    print("\nLoblaw Bio Immune Cell Analysis")
    print("---------------------------------")
    print("[1] Initialize database")
    print("[2] Load data from CSV")
    print("[3] Generate summary table")
    print("[4] Compare responders vs non-responders (melanoma + tr1 + PBMC)")
    print("[5] Visualize relative frequencies (boxplot)")
    print("[6] Run baseline subset analysis")
    print("[0] Exit")

def main():
    while True:
        print_main_menu()
        choice = input("Enter a choice: ")

        if choice == "1":
            init_db()
        elif choice == "2":
            load_data()
        elif choice == "3":
            df = generate_summary_table()
            print("\nSummary Table (first 10 rows):")
            print(df.head(10))
        elif choice == "4":
            df = compare_responders_vs_nonresponders()
            print("\nResponder vs Non-responder Comparison:")
            print(df)
        elif choice == "5":
            df = load_responder_data()
            plot_boxplots(df)
        elif choice == "6":
            df = get_baseline_tr1_melanoma_pbmc_samples()
            summary = summarize_baseline_subset(df)
            print("\nSample counts per project:", summary['samples_per_project'])
            print("Responders vs Non-responders:", summary['responders_vs_non'])
            print("Sex distribution:", summary['sex_distribution'])
        elif choice == "0":
            print("Exiting.")
            sys.exit()
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
