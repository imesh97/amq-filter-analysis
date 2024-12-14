import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
import sys

from bloom_filter import BloomFilter
from cuckoo_filter import CuckooFilter
from vacuum_filter import VacuumFilter

def generate_dataset(dataset_size, count):
    """
    Generate a random dataset of integers of size dataset_size
    """
    np.random.seed(42)  # Generate datasets
    original_dataset = np.random.randint(0, 10000000, dataset_size)
    test_dataset = np.random.randint(0, 10000000, dataset_size * 2)  # Test dataset is twice the size of the original dataset

    original_df = pd.DataFrame({  # Convert to DataFrames for CSV export
        'dataset_type': ['original'] * len(original_dataset),
        'value': original_dataset
    })
    test_df = pd.DataFrame({
        'dataset_type': ['test'] * len(test_dataset),
        'value': test_dataset
    })

    original_df.to_csv(f"data/original_dataset_{count}.csv", index=False)  # Export DataFrames to CSV
    test_df.to_csv(f"data/test_dataset_{count}.csv", index=False)

    return original_dataset, test_dataset  # Return tuple of the datasets and DataFrames

def check_insertion_time(dataset, filter):
    """
    Check insertion time of a filter
    """
    start_time = time.time()
    for item in dataset:
        filter.insert(item)
    return time.time() - start_time  # Return time difference between start and end of dataset inserts

def check_query_time_and_fpr(orig_dataset, test_dataset, filter):
    """
    Check query time and false positive rate of a filter
    """
    start_time = time.time()
    false_positives = sum(1 for item in test_dataset if item not in orig_dataset and item in filter)
    query_time = (time.time() - start_time) / len(test_dataset)  # Time difference between start and end of query divided by test dataset size
    false_positive_rate = false_positives / len(test_dataset)  # Number of detected false positives divided by test dataset size
    return query_time, false_positive_rate

def plot_results(dataframe):
    """
    Plot results of the performance analysis
    """
    plt.figure(figsize=(15, 5))  # Create visualization
    
    plt.subplot(131)  # False Positive Rate
    plt.title('False Positive Rate')
    plt.plot(dataframe['Dataset Size'], dataframe['Bloom False Positive Rate'], label='Bloom')
    plt.plot(dataframe['Dataset Size'], dataframe['Cuckoo False Positive Rate'], label='Cuckoo')
    plt.plot(dataframe['Dataset Size'], dataframe['Vacuum False Positive Rate'], label='Vacuum')
    plt.xlabel('Dataset Size')
    plt.ylabel('False Positive Rate')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.subplot(132)  # Memory Usage
    plt.title('Memory Usage')
    plt.plot(dataframe['Dataset Size'], dataframe['Bloom Memory Usage (KB)'], label='Bloom')
    plt.plot(dataframe['Dataset Size'], dataframe['Cuckoo Memory Usage (KB)'], label='Cuckoo')
    plt.plot(dataframe['Dataset Size'], dataframe['Vacuum Memory Usage (KB)'], label='Vacuum')
    plt.xlabel('Dataset Size')
    plt.ylabel('Memory Usage (KB)')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.subplot(133)  # Query Speed
    plt.title('Query Speed')
    plt.plot(dataframe['Dataset Size'], dataframe['Bloom Query Speed (s)'], label='Bloom')
    plt.plot(dataframe['Dataset Size'], dataframe['Cuckoo Query Speed (s)'], label='Cuckoo')
    plt.plot(dataframe['Dataset Size'], dataframe['Vacuum Query Speed (s)'], label='Vacuum')
    plt.xlabel('Dataset Size')
    plt.ylabel('Query Speed (operations / second)')
    plt.legend()
    plt.xscale('log')
    plt.yscale('log')
    
    plt.tight_layout()
    plt.savefig('amq_filters_performance.png')  # Save visualization to PNG
    plt.close()

def performance_analysis():
    """
    Conduct performance analysis of AMQ structures
    """
    dataset_sizes = [10000, 100000, 1000000]  # Different dataset sizes (small, medium, large)
    results = []  # Store results for visualization
    count = 1  # Count for dataset export
    print("\n\nSTARTING PERFORMANCE ANALYSIS OF AMQ STRUCTURES...")
    print("Note: It may take a while to complete the analysis...")

    for dataset_size in dataset_sizes:
        original_dataset, test_dataset = generate_dataset(dataset_size, count)  # Generate datasets for each dataset size
        print(f"\nOriginal dataset {count} exported: {len(original_dataset)} unique values")
        print(f"Test dataset {count} exported: {len(test_dataset)} values")

        print("\nPerforming Bloom Filter analysis...")  # BLOOM FILTER analysis
        bloom_size = int(dataset_size * 10)
        bloom = BloomFilter(bloom_size, num_hashes=3)  # Create Bloom Filter

        bloom_memory = sys.getsizeof(bloom.bit_array) / 1024  # Memory Usage (KB)
        bloom_insertion_time = check_insertion_time(original_dataset, bloom)  # Insertion Time
        bloom_query_time, bloom_false_positive_rate = check_query_time_and_fpr(original_dataset, test_dataset, bloom)  # Query Speed and False Positive Rate
        
        print("Performing Cuckoo Filter analysis...")  # CUCKOO FILTER analysis
        cuckoo = CuckooFilter(size=dataset_size)  # Create Cuckoo Filter

        cuckoo_memory = sys.getsizeof(cuckoo.buckets) / 1024  # Memory Usage (KB)
        cuckoo_insertion_time = check_insertion_time(original_dataset, cuckoo)  # Insertion Time
        cuckoo_query_time, cuckoo_false_positive_rate = check_query_time_and_fpr(original_dataset, test_dataset, cuckoo)  # Query Speed and False Positive Rate
        
        print("Performing Vacuum Filter analysis...")  # VACUUM FILTER analysis
        vacuum = VacuumFilter(size=dataset_size)  # Create Vacuum Filter

        vacuum_memory = sys.getsizeof(vacuum.count_array) / 1024  # Memory Usage (KB)
        vacuum_insertion_time = check_insertion_time(original_dataset, vacuum)  # Insertion Time
        vacuum_query_time, vacuum_false_positive_rate = check_query_time_and_fpr(original_dataset, test_dataset, vacuum)  # Query Speed and False Positive Rate
        
        results.append({  # Append results
            'Dataset Size': dataset_size,
            
            'Bloom Memory Usage (KB)': bloom_memory,  # Bloom Filter metrics
            'Bloom Insertion Time (s)': bloom_insertion_time,
            'Bloom Query Speed (s)': bloom_query_time,
            'Bloom False Positive Rate': bloom_false_positive_rate,
            
            'Cuckoo Memory Usage (KB)': cuckoo_memory,  # Cuckoo Filter metrics
            'Cuckoo Insertion Time (s)': cuckoo_insertion_time,
            'Cuckoo Query Speed (s)': cuckoo_query_time,
            'Cuckoo False Positive Rate': cuckoo_false_positive_rate,
            
            'Vacuum Memory Usage (KB)': vacuum_memory,  # Vacuum Filter metrics
            'Vacuum Insertion Time (s)': vacuum_insertion_time,
            'Vacuum Query Speed (s)': vacuum_query_time,
            'Vacuum False Positive Rate': vacuum_false_positive_rate
        })
        count = count + 1
    
    print("\nVisualizing results...")
    df = pd.DataFrame(results)  # Convert to DataFrame
    plot_results(df)  # Plot results to files
    df.to_csv('amq_filters_performance.csv', index=False)  # Save results to CSV
    
    print("\nPERFORMANCE ANALYSIS COMPLETE.")  # Print analysis results
    print("AMQ Analysis:\n")
    print(df.to_string(index=False))

def main():
    performance_analysis()  # Conduct performance analysis

if __name__ == "__main__":
    main()