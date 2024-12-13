import pandas as pd
import sys

from bloom_filter import BloomFilter
from cuckoo_filter import CuckooFilter
from vacuum_filter import VacuumFilter
from main import check_insertion_time, check_query_time_and_fpr, plot_results

def read_basketball_dataset(file_path):
    """
    Read dataset for basketball player stats
    """
    # Read the CSV file
    df = pd.read_csv(file_path)
    
    # Split into original and test datasets without shuffling
    split_index = int(len(df) * 0.8)  # 80% original, 20% test
    
    original_dataset = df.iloc[:split_index]['NAME'].tolist()
    test_dataset = df.iloc[split_index:]['NAME'].tolist()
    
    return original_dataset, test_dataset


def basketball_performance_analysis(file_path):
    """
    Comprehensive performance analysis of AMQ structures on basketball player dataset
    """
    print("\nSTARTING PERFORMANCE ANALYSIS OF AMQ STRUCTURES ON BASKETBALL PLAYER DATA...")
    
    
    original_dataset, test_dataset = read_basketball_dataset(file_path)  # Read dataset
    results = []
    
    dataset_size = len(original_dataset)
    print(f"\nAnalyzing dataset of size: {dataset_size}")
        
    
    print("Performing Bloom Filter analysis...")  # BLOOM FILTER analysis
    bloom_size = int(dataset_size * 10)
    bloom = BloomFilter(bloom_size, num_hashes=3)
    
    bloom_memory = sys.getsizeof(bloom.bit_array) / 1024
    bloom_insertion_time = check_insertion_time(original_dataset, bloom)
    bloom_query_time, bloom_false_positive_rate = check_query_time_and_fpr(original_dataset, test_dataset, bloom)
    
    print("Performing Cuckoo Filter analysis...")  # CUCKOO FILTER analysis
    cuckoo = CuckooFilter(size=dataset_size)
    
    cuckoo_memory = sys.getsizeof(cuckoo.buckets) / 1024
    cuckoo_insertion_time = check_insertion_time(original_dataset, cuckoo)
    cuckoo_query_time, cuckoo_false_positive_rate = check_query_time_and_fpr(original_dataset, test_dataset, cuckoo)
    
    print("Performing Vacuum Filter analysis...")  # VACUUM FILTER analysis
    vacuum = VacuumFilter(size=dataset_size)
    
    vacuum_memory = sys.getsizeof(vacuum.count_array) / 1024
    vacuum_insertion_time = check_insertion_time(original_dataset, vacuum)
    vacuum_query_time, vacuum_false_positive_rate = check_query_time_and_fpr(original_dataset, test_dataset, vacuum)
    
    results.append({
        'Dataset Size': dataset_size,
        
        'Bloom Memory Usage (KB)': bloom_memory,
        'Bloom Insertion Time (s)': bloom_insertion_time,
        'Bloom Query Time (s)': bloom_query_time,
        'Bloom False Positive Rate': bloom_false_positive_rate,
        
        'Cuckoo Memory Usage (KB)': cuckoo_memory,
        'Cuckoo Insertion Time (s)': cuckoo_insertion_time,
        'Cuckoo Query Time (s)': cuckoo_query_time,
        'Cuckoo False Positive Rate': cuckoo_false_positive_rate,
        
        'Vacuum Memory Usage (KB)': vacuum_memory,
        'Vacuum Insertion Time (s)': vacuum_insertion_time,
        'Vacuum Query Time (s)': vacuum_query_time,
        'Vacuum False Positive Rate': vacuum_false_positive_rate
        })
    
    print("\nVisualizing results...")
    df = pd.DataFrame(results)
    plot_results(df)
    df.to_csv('basketball_amq_filters_performance.csv', index=False)
    
    print("\nPERFORMANCE ANALYSIS COMPLETE.")
    print("AMQ Analysis for Basketball Player Data:\n")
    print(df.to_string(index=False))

def main(file_path):
    basketball_performance_analysis(file_path)

if __name__ == "__main__":
    # Replace with the path to your basketball stats CSV
    main('basketball_data.csv')