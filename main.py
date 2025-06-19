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
    print("[7] Add a sample")
    print("[8] Remove sample")
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
            for sample_id in df['sample'].unique():
                sample_df = df[df['sample'] == sample_id]
                print("-" * 40)
                print(f"Sample: {sample_id}")
                print(sample_df[['population', 'count', 'percentage']].to_string(index=False))
            print("-" * 40)
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
        elif choice == "7":
            from src.data_loader import add_sample

            print("\nAdd a Sample Manually")

            meta_fields = {
                'sample_id': str,
                'project': str,
                'subject': str,
                'condition': str,
                'age': int,
                'sex': str,
                'treatment': str,
                'response': str,
                'sample_type': str,
                'time_from_treatment': int,
            }

            sample_metadata = {}
            for field, cast in meta_fields.items():
                raw = input(f"{field}: ").strip()
                if raw == '':
                    sample_metadata[field] = None
                else:
                    try:
                        sample_metadata[field] = cast(raw)
                    except ValueError:
                        print(f"Invalid input for '{field}'. Must be of type {cast.__name__}.")
                        return

            print("\nEnter immune cell counts:")
            count_fields = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']
            cell_counts = {}
            for field in count_fields:
                raw = input(f"{field}: ").strip()
                try:
                    cell_counts[field] = int(raw)
                except ValueError:
                    print(f"Invalid count for '{field}'. Must be an integer.")
                    return

            try:
                add_sample(sample_metadata, cell_counts)
            except Exception as e:
                print(f"Error adding sample: {e}")
        elif choice == "8":
            from src.data_loader import remove_sample
            sample_id = input("Enter sample: ")
            remove_sample(sample_id)
        elif choice == "0":
            print("Exiting.")
            sys.exit()
        else:
            print("Invalid option. Try again.")

if __name__ == "__main__":
    main()
