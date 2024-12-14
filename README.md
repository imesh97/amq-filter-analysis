# Approximate Membership Query (AMQ) Structures in Sports Analytics

## Overview

This research project implements and analyzes three Approximate Membership Query (AMQ) data structures: Bloom Filters, Cuckoo Filters, and Vacuum Filters. The project conducts a comprehensive performance analysis using two different approaches:

1. **Standard Dataset Analysis**

   - Generates random integer datasets of varying sizes (10,000, 100,000, 1,000,000)
   - Measures and compares performance metrics across different AMQ structures

2. **Basketball Dataset Analysis**
   - Uses a real-world dataset of basketball player statistics from the 2023-24 NBA season
   - Applies the same performance analysis techniques

### Performance Metrics

The analysis focuses on three key performance indicators:

- **False Positive Rate**: Probability of incorrectly identifying an item as present
- **Query Speed**: Time taken to query the filter
- **Memory Usage**: Memory consumption of the filter structure

### Output Generation

The scripts generate multiple output files:

- `results/amq_filters_performance.png`: Visualization of performance metrics
- `results/amq_filters_performance.csv`: Detailed performance data for standard datasets
- `results/basketball_amq_filters_performance.csv`: Performance data for basketball player dataset
- Console output with detailed performance statistics

## Installation Instructions

### Prerequisites

- Python 3.7+
- Ensure you have the following libraries installed:

```bash
pip install numpy pandas matplotlib
```

### Project Dependencies

- NumPy: Numerical computing
- Pandas: Data manipulation
- Matplotlib: Data visualization
- Bitarray: Efficient bit-level operations (usually preinstalled with Python)
- Hashlib: Hash value generation (usually preinstalled with Python)

## How to Run

### Standard Dataset Analysis

```bash
python main.py
```

This will generate random datasets and perform performance analysis on the Bloom, Cuckoo, and Vacuum filters.

### Basketball Dataset Analysis

```bash
python basketball.py
```

This will analyze the performance of AMQ structures on basketball player names.

### Important Notes

- Existing result files will be overwritten with each run
- Ensure `data/` and `results/` directories exist before running

## Project Structure

- `main.py`: Primary script for standard dataset analysis
- `basketball.py`: Script for basketball dataset analysis
- `data/`: Directory for input datasets
- `results/`: Directory for output files and visualizations
- `bloom_filter.py`, `cuckoo_filter.py`, `vacuum_filter.py`: Scripts for AMQ implementations

## Customization

- Modify `dataset_sizes` in `main.py` to adjust analysis scale
- Replace `data/basketball_data.csv` with your own dataset for custom analysis
