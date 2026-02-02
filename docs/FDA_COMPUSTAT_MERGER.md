# FDA-Compustat Data Merger Tool

## Overview

This tool merges FDA drug approval data with Compustat financial data based on company identifiers. It's designed to help researchers and analysts understand the relationship between pharmaceutical drug approvals and company financial performance.

## Features

- **FDA Data Fetching**: Retrieves drug approval data from the openFDA API
- **Smart Name Matching**: Normalizes company names to handle variations (e.g., "Pfizer Inc." matches "Pfizer")
- **Flexible Merging**: Supports different merge types (left, right, inner, outer)
- **Multiple Output Formats**: Export to CSV, JSON, or Excel
- **Summary Statistics**: Provides insights into merged data
- **Sample Data Generation**: Can create sample Compustat data for testing

## Installation

The tool requires the following Python packages (already in `requirements.txt`):

```bash
pip install pandas requests
```

## Usage

### Command Line

Basic usage with sample data:

```bash
python tools/fda_compustat_merger.py --fda-limit 50 --sample-data --output merged_data.csv
```

With your own Compustat data file:

```bash
python tools/fda_compustat_merger.py --fda-limit 100 --compustat-file path/to/compustat.csv --output merged_data.csv
```

Filter FDA data by company:

```bash
python tools/fda_compustat_merger.py --fda-search "Pfizer" --compustat-file compustat.csv --output pfizer_drugs.csv
```

### Command Line Options

- `--fda-limit`: Number of FDA records to fetch (default: 100)
- `--fda-search`: Search term to filter FDA data (e.g., company name)
- `--compustat-file`: Path to Compustat CSV file
- `--sample-data`: Use sample Compustat data for demonstration
- `--output`: Output file path (default: fda_compustat_merged.csv)
- `--format`: Output format - csv, json, or excel (default: csv)
- `--merge-type`: Type of merge - left, right, inner, or outer (default: left)

### Python API

```python
from tools.fda_compustat_merger import FDACompustatMerger

# Create merger instance
merger = FDACompustatMerger()

# Fetch FDA data
fda_data = merger.fetch_fda_approvals(limit=100, search_term="Pfizer")

# Load Compustat data
compustat_data = merger.load_compustat_data("compustat.csv")
# Or create sample data
# compustat_data = merger.create_sample_compustat_data(["Pfizer", "Merck"])

# Merge datasets
merged = merger.merge_datasets(merge_type='inner')

# Save results
merger.save_merged_data("output.csv", format='csv')

# Get summary statistics
stats = merger.get_summary_statistics()
print(stats)
```

## Data Format

### FDA Data Structure

The tool expects/produces FDA data with these columns:

- `sponsor_name`: Company name (sponsor)
- `application_number`: FDA application number
- `product_name`: Drug brand name
- `active_ingredient`: Active pharmaceutical ingredient
- `approval_date`: Approval date
- `product_type`: Type of product (tablet, injection, etc.)

### Compustat Data Structure

The tool expects Compustat data with at least these columns:

- `company_name`: Company name
- `ticker`: Stock ticker symbol (optional)
- `year`: Fiscal year
- `revenue`: Revenue in millions (optional)
- `net_income`: Net income in millions (optional)

Additional financial fields are supported and will be included in the merged output.

## Company Name Matching

The tool uses intelligent name normalization to match companies across datasets:

- Converts to lowercase
- Removes common suffixes: Inc., Corp., Ltd., etc.
- Handles variations like "Merck Sharp & Dohme" matching "Merck & Co."
- Normalizes "Bristol-Myers Squibb Company" to "Bristol-Myers Squibb"
- Removes pharmaceutical-specific terms

## Examples

### Demo Script

Run the demo to see the tool in action:

```bash
python tools/demo_fda_compustat.py
```

This will:
1. Create sample FDA drug approval data
2. Create sample Compustat financial data
3. Merge the datasets
4. Display summary statistics
5. Show sample merged records
6. Save results to `/tmp/fda_compustat_demo.csv`

### Example Output

```
================================================================================
Drug Approvals by Company:
================================================================================
                                      num_approvals  revenue
sponsor_name                                                
Pfizer Inc.                                       2    58496
AbbVie Inc.                                       1    54318
Bristol-Myers Squibb Company                      1    46159
Johnson & Johnson                                 1    85159
Merck Sharp & Dohme Corp.                         1    59283
Novartis Pharmaceuticals Corporation              1    45440
```

## Data Sources

### FDA Data

- **Source**: openFDA API (https://open.fda.gov/)
- **Endpoint**: `/drug/drugsfda.json`
- **Access**: Free, no authentication required
- **Rate Limits**: 240 requests per minute, 120,000 per day

### Compustat Data

- **Source**: S&P Global Market Intelligence
- **Access**: Subscription required
- **Alternative**: Use the sample data generator for testing

## Testing

Run the test suite:

```bash
PYTHONPATH=. pytest tests/test_fda_compustat_merger.py -v
```

Skip network-dependent tests:

```bash
SKIP_NETWORK_TESTS=1 PYTHONPATH=. pytest tests/test_fda_compustat_merger.py -v
```

## Use Cases

1. **Pharmaceutical Research**: Analyze the relationship between drug approvals and company financial performance
2. **Investment Analysis**: Identify companies with strong drug pipelines
3. **Market Research**: Track drug approval trends by company
4. **Regulatory Studies**: Study FDA approval patterns
5. **Due Diligence**: Assess pharmaceutical companies' product portfolios

## Limitations

- FDA API may have rate limits
- Company name matching is heuristic-based and may not be 100% accurate
- Compustat data requires a subscription or manual preparation
- Historical approval dates may be incomplete in the FDA API

## Contributing

To improve the company name normalization:

1. Add new replacements in the `normalize_company_names()` method
2. Add test cases in `tests/test_fda_compustat_merger.py`
3. Run tests to ensure no regressions

## License

MIT License (same as the parent project)
