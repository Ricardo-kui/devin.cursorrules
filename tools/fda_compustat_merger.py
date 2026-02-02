#!/usr/bin/env python3
"""
FDA and Compustat Data Merger Tool

This tool merges FDA drug approval data with Compustat financial data.
It can fetch FDA drug approval data via the openFDA API and merge it with
financial data based on company identifiers.
"""

import pandas as pd
import requests
import json
from typing import Dict, List, Optional
import sys
from datetime import datetime


class FDACompustatMerger:
    """Merges FDA drug approval data with Compustat financial data."""
    
    FDA_API_BASE = "https://api.fda.gov/drug/drugsfda.json"
    
    def __init__(self):
        self.fda_data = None
        self.compustat_data = None
        self.merged_data = None
    
    def fetch_fda_approvals(self, limit: int = 100, search_term: Optional[str] = None) -> pd.DataFrame:
        """
        Fetch FDA drug approval data from openFDA API.
        
        Args:
            limit: Maximum number of records to fetch
            search_term: Optional search term to filter results (e.g., company name)
        
        Returns:
            DataFrame with FDA drug approval data
        """
        params = {
            'limit': limit
        }
        
        if search_term:
            params['search'] = f'sponsor_name:"{search_term}"'
        
        try:
            print(f"Fetching FDA drug approval data...", file=sys.stderr)
            response = requests.get(self.FDA_API_BASE, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            results = data.get('results', [])
            
            # Extract relevant fields
            records = []
            for item in results:
                sponsor_name = item.get('sponsor_name', '')
                products = item.get('products', [])
                
                for product in products:
                    record = {
                        'sponsor_name': sponsor_name,
                        'application_number': item.get('application_number', ''),
                        'product_name': product.get('brand_name', ''),
                        'active_ingredient': product.get('active_ingredients', [{}])[0].get('name', '') if product.get('active_ingredients') else '',
                        'approval_date': None,
                        'product_type': product.get('dosage_form', '')
                    }
                    
                    # Get approval date from submissions
                    submissions = item.get('submissions', [])
                    if submissions:
                        submission_status = submissions[0].get('submission_status', '')
                        submission_date = submissions[0].get('submission_status_date', '')
                        if submission_date:
                            record['approval_date'] = submission_date
                    
                    records.append(record)
            
            self.fda_data = pd.DataFrame(records)
            print(f"Fetched {len(self.fda_data)} FDA drug approval records", file=sys.stderr)
            return self.fda_data
            
        except requests.RequestException as e:
            print(f"Error fetching FDA data: {e}", file=sys.stderr)
            # Return empty DataFrame with expected columns
            self.fda_data = pd.DataFrame(columns=[
                'sponsor_name', 'application_number', 'product_name', 
                'active_ingredient', 'approval_date', 'product_type'
            ])
            return self.fda_data
    
    def load_compustat_data(self, data_source: str) -> pd.DataFrame:
        """
        Load Compustat financial data.
        
        Args:
            data_source: Path to CSV file or DataFrame
        
        Returns:
            DataFrame with Compustat financial data
        """
        if isinstance(data_source, pd.DataFrame):
            self.compustat_data = data_source
        elif isinstance(data_source, str):
            try:
                self.compustat_data = pd.read_csv(data_source)
                print(f"Loaded {len(self.compustat_data)} Compustat records from {data_source}", file=sys.stderr)
            except Exception as e:
                print(f"Error loading Compustat data: {e}", file=sys.stderr)
                self.compustat_data = pd.DataFrame()
        
        return self.compustat_data
    
    def create_sample_compustat_data(self, companies: List[str]) -> pd.DataFrame:
        """
        Create sample Compustat-like financial data for demonstration.
        
        Args:
            companies: List of company names
        
        Returns:
            DataFrame with sample financial data
        """
        import random
        
        records = []
        for company in companies:
            record = {
                'company_name': company,
                'ticker': company[:4].upper(),
                'year': 2023,
                'revenue': random.randint(1000, 50000),  # in millions
                'net_income': random.randint(-500, 5000),  # in millions
                'total_assets': random.randint(5000, 100000),  # in millions
                'market_cap': random.randint(10000, 200000),  # in millions
                'employees': random.randint(1000, 50000)
            }
            records.append(record)
        
        self.compustat_data = pd.DataFrame(records)
        return self.compustat_data
    
    def normalize_company_names(self, name: str) -> str:
        """
        Normalize company names for matching.
        
        Args:
            name: Company name
        
        Returns:
            Normalized company name
        """
        # Convert to lowercase and remove common suffixes
        name = name.lower().strip()
        
        # Common replacements for variations
        replacements = {
            'sharp & dohme corp.': '',  # Merck Sharp & Dohme Corp. -> Merck
            'sharp & dohme corp': '',  # Merck Sharp & Dohme Corp -> Merck
            'sharp & dohme': '',  # Merck Sharp & Dohme -> Merck
            'pharmaceuticals corporation': '',
            'squibb company': 'squibb',  # Bristol-Myers Squibb Company -> bristol-myers squibb
            '& co.': '',  # Merck & Co. -> Merck
        }
        
        for old, new in replacements.items():
            name = name.replace(old, new)
        
        # Remove common suffixes
        suffixes = [' inc', ' inc.', ' corporation', ' corp', ' corp.', 
                   ' ltd', ' ltd.', ' limited', ' llc', ' plc', ' co', ' co.', 
                   ' company', ' pharmaceuticals', ' pharma', ' ag']
        
        for suffix in suffixes:
            if name.endswith(suffix):
                name = name[:-len(suffix)]
        
        # Remove extra spaces and trailing punctuation
        name = ' '.join(name.split())
        name = name.rstrip('.,;:')
        
        return name.strip()
    
    def merge_datasets(self, 
                      fda_company_col: str = 'sponsor_name',
                      compustat_company_col: str = 'company_name',
                      merge_type: str = 'left') -> pd.DataFrame:
        """
        Merge FDA and Compustat datasets.
        
        Args:
            fda_company_col: Column name in FDA data containing company names
            compustat_company_col: Column name in Compustat data containing company names
            merge_type: Type of merge ('left', 'right', 'inner', 'outer')
        
        Returns:
            Merged DataFrame
        """
        if self.fda_data is None or self.fda_data.empty:
            print("Warning: FDA data is empty", file=sys.stderr)
            return pd.DataFrame()
        
        if self.compustat_data is None or self.compustat_data.empty:
            print("Warning: Compustat data is empty", file=sys.stderr)
            return pd.DataFrame()
        
        # Create normalized name columns for matching
        fda_normalized = self.fda_data.copy()
        fda_normalized['_normalized_name'] = fda_normalized[fda_company_col].apply(self.normalize_company_names)
        
        compustat_normalized = self.compustat_data.copy()
        compustat_normalized['_normalized_name'] = compustat_normalized[compustat_company_col].apply(self.normalize_company_names)
        
        # Perform the merge
        self.merged_data = pd.merge(
            fda_normalized,
            compustat_normalized,
            on='_normalized_name',
            how=merge_type,
            suffixes=('_fda', '_compustat')
        )
        
        # Drop the temporary normalized column
        self.merged_data = self.merged_data.drop(columns=['_normalized_name'])
        
        print(f"Merged {len(self.merged_data)} records", file=sys.stderr)
        return self.merged_data
    
    def save_merged_data(self, output_path: str, format: str = 'csv'):
        """
        Save merged data to file.
        
        Args:
            output_path: Path to save the file
            format: Output format ('csv', 'json', 'excel')
        """
        if self.merged_data is None or self.merged_data.empty:
            print("No merged data to save", file=sys.stderr)
            return
        
        try:
            if format == 'csv':
                self.merged_data.to_csv(output_path, index=False)
            elif format == 'json':
                self.merged_data.to_json(output_path, orient='records', indent=2)
            elif format == 'excel':
                self.merged_data.to_excel(output_path, index=False)
            
            print(f"Saved merged data to {output_path}", file=sys.stderr)
        except Exception as e:
            print(f"Error saving data: {e}", file=sys.stderr)
    
    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics of the merged data.
        
        Returns:
            Dictionary with summary statistics
        """
        if self.merged_data is None or self.merged_data.empty:
            return {}
        
        stats = {
            'total_records': len(self.merged_data),
            'unique_companies': self.merged_data['sponsor_name'].nunique() if 'sponsor_name' in self.merged_data.columns else 0,
            'unique_drugs': self.merged_data['product_name'].nunique() if 'product_name' in self.merged_data.columns else 0,
        }
        
        # Add financial statistics if available
        if 'revenue' in self.merged_data.columns:
            stats['avg_revenue'] = self.merged_data['revenue'].mean()
            stats['total_revenue'] = self.merged_data.groupby('sponsor_name')['revenue'].first().sum()
        
        return stats


def main():
    """Main function for command-line usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Merge FDA and Compustat data')
    parser.add_argument('--fda-limit', type=int, default=100, help='Limit of FDA records to fetch')
    parser.add_argument('--fda-search', type=str, help='Search term for FDA data (e.g., company name)')
    parser.add_argument('--compustat-file', type=str, help='Path to Compustat CSV file')
    parser.add_argument('--sample-data', action='store_true', help='Use sample Compustat data')
    parser.add_argument('--output', type=str, default='fda_compustat_merged.csv', help='Output file path')
    parser.add_argument('--format', type=str, default='csv', choices=['csv', 'json', 'excel'], help='Output format')
    parser.add_argument('--merge-type', type=str, default='left', choices=['left', 'right', 'inner', 'outer'], help='Type of merge')
    
    args = parser.parse_args()
    
    # Create merger instance
    merger = FDACompustatMerger()
    
    # Fetch FDA data
    fda_data = merger.fetch_fda_approvals(limit=args.fda_limit, search_term=args.fda_search)
    
    if fda_data.empty:
        print("No FDA data fetched. Exiting.", file=sys.stderr)
        return 1
    
    # Load or create Compustat data
    if args.compustat_file:
        compustat_data = merger.load_compustat_data(args.compustat_file)
    elif args.sample_data:
        # Create sample data based on companies in FDA data
        unique_companies = fda_data['sponsor_name'].unique()[:10]
        compustat_data = merger.create_sample_compustat_data(unique_companies)
    else:
        print("Error: Please provide --compustat-file or use --sample-data", file=sys.stderr)
        return 1
    
    # Merge datasets
    merged = merger.merge_datasets(merge_type=args.merge_type)
    
    if merged.empty:
        print("No records after merge. Exiting.", file=sys.stderr)
        return 1
    
    # Save results
    merger.save_merged_data(args.output, format=args.format)
    
    # Print summary
    stats = merger.get_summary_statistics()
    print("\n=== Merge Summary ===")
    print(json.dumps(stats, indent=2))
    
    # Print sample of merged data
    print("\n=== Sample of Merged Data ===")
    print(merged.head(10).to_string())
    
    return 0


if __name__ == '__main__':
    sys.exit(main())
