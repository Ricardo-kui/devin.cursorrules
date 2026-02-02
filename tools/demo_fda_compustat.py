#!/usr/bin/env python3
"""
Demo script for FDA-Compustat merger tool.
Creates sample datasets and demonstrates the merger functionality.
"""

import sys
import os
import pandas as pd

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.fda_compustat_merger import FDACompustatMerger


def create_sample_fda_data():
    """Create sample FDA drug approval data."""
    data = [
        {
            'sponsor_name': 'Pfizer Inc.',
            'application_number': 'NDA021382',
            'product_name': 'Lipitor',
            'active_ingredient': 'Atorvastatin Calcium',
            'approval_date': '2023-01-15',
            'product_type': 'Tablet'
        },
        {
            'sponsor_name': 'Pfizer Inc.',
            'application_number': 'NDA050710',
            'product_name': 'Viagra',
            'active_ingredient': 'Sildenafil Citrate',
            'approval_date': '2023-03-20',
            'product_type': 'Tablet'
        },
        {
            'sponsor_name': 'Merck Sharp & Dohme Corp.',
            'application_number': 'NDA020895',
            'product_name': 'Januvia',
            'active_ingredient': 'Sitagliptin Phosphate',
            'approval_date': '2023-02-10',
            'product_type': 'Tablet'
        },
        {
            'sponsor_name': 'Johnson & Johnson',
            'application_number': 'BLA125276',
            'product_name': 'Stelara',
            'active_ingredient': 'Ustekinumab',
            'approval_date': '2023-04-05',
            'product_type': 'Injection'
        },
        {
            'sponsor_name': 'AbbVie Inc.',
            'application_number': 'BLA125057',
            'product_name': 'Humira',
            'active_ingredient': 'Adalimumab',
            'approval_date': '2023-05-12',
            'product_type': 'Injection'
        },
        {
            'sponsor_name': 'Novartis Pharmaceuticals Corporation',
            'application_number': 'NDA022092',
            'product_name': 'Gilenya',
            'active_ingredient': 'Fingolimod',
            'approval_date': '2023-06-18',
            'product_type': 'Capsule'
        },
        {
            'sponsor_name': 'Bristol-Myers Squibb Company',
            'application_number': 'BLA125554',
            'product_name': 'Opdivo',
            'active_ingredient': 'Nivolumab',
            'approval_date': '2023-07-22',
            'product_type': 'Injection'
        },
    ]
    
    return pd.DataFrame(data)


def create_sample_compustat_data():
    """Create sample Compustat financial data."""
    data = [
        {
            'company_name': 'Pfizer Inc.',
            'ticker': 'PFE',
            'year': 2023,
            'revenue': 58496,  # in millions USD
            'net_income': 9616,
            'total_assets': 197206,
            'market_cap': 245000,
            'employees': 83000,
            'rd_expense': 11400
        },
        {
            'company_name': 'Merck & Co., Inc.',
            'ticker': 'MRK',
            'year': 2023,
            'revenue': 59283,
            'net_income': 11113,
            'total_assets': 119584,
            'market_cap': 260000,
            'employees': 68000,
            'rd_expense': 13599
        },
        {
            'company_name': 'Johnson & Johnson',
            'ticker': 'JNJ',
            'year': 2023,
            'revenue': 85159,
            'net_income': 17941,
            'total_assets': 187378,
            'market_cap': 380000,
            'employees': 130000,
            'rd_expense': 14603
        },
        {
            'company_name': 'AbbVie Inc.',
            'ticker': 'ABBV',
            'year': 2023,
            'revenue': 54318,
            'net_income': 6989,
            'total_assets': 126084,
            'market_cap': 290000,
            'employees': 50000,
            'rd_expense': 6540
        },
        {
            'company_name': 'Novartis AG',
            'ticker': 'NVS',
            'year': 2023,
            'revenue': 45440,
            'net_income': 9017,
            'total_assets': 132815,
            'market_cap': 210000,
            'employees': 108000,
            'rd_expense': 9600
        },
        {
            'company_name': 'Bristol-Myers Squibb',
            'ticker': 'BMY',
            'year': 2023,
            'revenue': 46159,
            'net_income': 2291,
            'total_assets': 136894,
            'market_cap': 110000,
            'employees': 34000,
            'rd_expense': 9445
        },
    ]
    
    return pd.DataFrame(data)


def main():
    """Run the demo."""
    print("=" * 80)
    print("FDA-Compustat Merger Tool Demo")
    print("=" * 80)
    print()
    
    # Create merger instance
    merger = FDACompustatMerger()
    
    # Load sample data
    print("Creating sample FDA drug approval data...")
    fda_data = create_sample_fda_data()
    merger.fda_data = fda_data
    print(f"Created {len(fda_data)} FDA drug approval records")
    print()
    
    print("Sample FDA data:")
    print(fda_data.head())
    print()
    
    print("Creating sample Compustat financial data...")
    compustat_data = create_sample_compustat_data()
    merger.compustat_data = compustat_data
    print(f"Created {len(compustat_data)} Compustat financial records")
    print()
    
    print("Sample Compustat data:")
    print(compustat_data[['company_name', 'ticker', 'revenue', 'net_income', 'employees']])
    print()
    
    # Perform merge
    print("Merging datasets based on company names...")
    merged = merger.merge_datasets(merge_type='left')
    print(f"Merged {len(merged)} records")
    print()
    
    # Display merged results
    print("=" * 80)
    print("Merged Data Sample:")
    print("=" * 80)
    
    # Select key columns to display
    display_cols = [
        'sponsor_name', 'product_name', 'active_ingredient',
        'company_name', 'ticker', 'revenue', 'net_income', 'rd_expense'
    ]
    
    # Filter to columns that exist
    display_cols = [col for col in display_cols if col in merged.columns]
    
    print(merged[display_cols].to_string(index=False))
    print()
    
    # Get and display summary statistics
    print("=" * 80)
    print("Summary Statistics:")
    print("=" * 80)
    stats = merger.get_summary_statistics()
    
    print(f"Total merged records: {stats.get('total_records', 0)}")
    print(f"Unique companies: {stats.get('unique_companies', 0)}")
    print(f"Unique drugs: {stats.get('unique_drugs', 0)}")
    
    if 'avg_revenue' in stats:
        print(f"Average company revenue: ${stats['avg_revenue']:,.0f}M")
        print(f"Total revenue: ${stats['total_revenue']:,.0f}M")
    print()
    
    # Analyze drug approvals by company
    print("=" * 80)
    print("Drug Approvals by Company:")
    print("=" * 80)
    
    approvals_by_company = merged.groupby('sponsor_name').agg({
        'product_name': 'count',
        'revenue': 'first'
    }).rename(columns={'product_name': 'num_approvals'})
    approvals_by_company = approvals_by_company.sort_values('num_approvals', ascending=False)
    
    print(approvals_by_company.to_string())
    print()
    
    # Save results
    output_file = '/tmp/fda_compustat_demo.csv'
    merger.save_merged_data(output_file, format='csv')
    print(f"Results saved to: {output_file}")
    print()
    
    print("=" * 80)
    print("Demo completed successfully!")
    print("=" * 80)
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
