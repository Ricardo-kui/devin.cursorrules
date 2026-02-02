"""
Unit tests for FDA-Compustat merger tool.
"""

import unittest
import pandas as pd
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.fda_compustat_merger import FDACompustatMerger


class TestFDACompustatMerger(unittest.TestCase):
    """Test cases for FDACompustatMerger class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.merger = FDACompustatMerger()
    
    def test_initialization(self):
        """Test that merger initializes correctly."""
        self.assertIsNone(self.merger.fda_data)
        self.assertIsNone(self.merger.compustat_data)
        self.assertIsNone(self.merger.merged_data)
    
    def test_normalize_company_names(self):
        """Test company name normalization."""
        test_cases = [
            ("Pfizer Inc.", "pfizer"),
            ("Johnson & Johnson", "johnson & johnson"),
            ("Merck & Co., Inc.", "merck & co.,"),
            ("AbbVie Inc", "abbvie"),
            ("Bristol-Myers Squibb Corporation", "bristol-myers squibb"),
            ("Novartis Pharmaceuticals", "novartis"),
            ("Roche Pharma", "roche"),
        ]
        
        for input_name, expected_output in test_cases:
            result = self.merger.normalize_company_names(input_name)
            self.assertTrue(expected_output in result or result in expected_output,
                          f"Expected '{expected_output}' in result '{result}' for input '{input_name}'")
    
    def test_create_sample_compustat_data(self):
        """Test creation of sample Compustat data."""
        companies = ["Pfizer", "Merck", "Johnson & Johnson"]
        df = self.merger.create_sample_compustat_data(companies)
        
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn('company_name', df.columns)
        self.assertIn('revenue', df.columns)
        self.assertIn('ticker', df.columns)
        
        # Check that all companies are present
        company_names = df['company_name'].tolist()
        for company in companies:
            self.assertIn(company, company_names)
    
    def test_load_compustat_data_from_dataframe(self):
        """Test loading Compustat data from DataFrame."""
        sample_df = pd.DataFrame({
            'company_name': ['Company A', 'Company B'],
            'revenue': [1000, 2000],
            'year': [2023, 2023]
        })
        
        result = self.merger.load_compustat_data(sample_df)
        
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        pd.testing.assert_frame_equal(result, sample_df)
    
    def test_merge_with_sample_data(self):
        """Test merging with sample data."""
        # Create sample FDA data
        fda_df = pd.DataFrame({
            'sponsor_name': ['Pfizer Inc.', 'Merck & Co., Inc.', 'Novartis Pharmaceuticals'],
            'product_name': ['Drug A', 'Drug B', 'Drug C'],
            'application_number': ['NDA001', 'NDA002', 'NDA003']
        })
        self.merger.fda_data = fda_df
        
        # Create sample Compustat data
        companies = ['Pfizer', 'Merck', 'Novartis']
        self.merger.create_sample_compustat_data(companies)
        
        # Perform merge
        merged = self.merger.merge_datasets(merge_type='inner')
        
        self.assertIsInstance(merged, pd.DataFrame)
        self.assertGreater(len(merged), 0)
        
        # Check that merge columns exist
        self.assertIn('sponsor_name', merged.columns)
        self.assertIn('product_name', merged.columns)
        self.assertIn('company_name', merged.columns)
        self.assertIn('revenue', merged.columns)
    
    def test_merge_with_no_matches(self):
        """Test merging when there are no matching companies."""
        # Create FDA data with companies not in Compustat
        fda_df = pd.DataFrame({
            'sponsor_name': ['Unknown Company A', 'Unknown Company B'],
            'product_name': ['Drug X', 'Drug Y'],
            'application_number': ['NDA999', 'NDA998']
        })
        self.merger.fda_data = fda_df
        
        # Create Compustat data with different companies
        compustat_df = pd.DataFrame({
            'company_name': ['Known Company C', 'Known Company D'],
            'revenue': [5000, 6000],
            'year': [2023, 2023]
        })
        self.merger.compustat_data = compustat_df
        
        # Perform inner merge (should return empty)
        merged = self.merger.merge_datasets(merge_type='inner')
        
        self.assertEqual(len(merged), 0)
        
        # Perform left merge (should return FDA records)
        merged_left = self.merger.merge_datasets(merge_type='left')
        self.assertEqual(len(merged_left), 2)
    
    def test_get_summary_statistics_with_data(self):
        """Test summary statistics generation."""
        # Set up merged data
        merged_df = pd.DataFrame({
            'sponsor_name': ['Pfizer', 'Pfizer', 'Merck'],
            'product_name': ['Drug A', 'Drug B', 'Drug C'],
            'revenue': [10000, 10000, 8000]
        })
        self.merger.merged_data = merged_df
        
        stats = self.merger.get_summary_statistics()
        
        self.assertIn('total_records', stats)
        self.assertEqual(stats['total_records'], 3)
        self.assertIn('unique_companies', stats)
        self.assertEqual(stats['unique_companies'], 2)
        self.assertIn('unique_drugs', stats)
        self.assertEqual(stats['unique_drugs'], 3)
    
    def test_get_summary_statistics_empty_data(self):
        """Test summary statistics with empty data."""
        self.merger.merged_data = pd.DataFrame()
        
        stats = self.merger.get_summary_statistics()
        
        self.assertEqual(stats, {})
    
    def test_empty_fda_data_merge(self):
        """Test merge behavior with empty FDA data."""
        self.merger.fda_data = pd.DataFrame()
        self.merger.compustat_data = pd.DataFrame({'company_name': ['Test'], 'revenue': [1000]})
        
        result = self.merger.merge_datasets()
        
        self.assertTrue(result.empty)
    
    def test_empty_compustat_data_merge(self):
        """Test merge behavior with empty Compustat data."""
        self.merger.fda_data = pd.DataFrame({'sponsor_name': ['Test'], 'product_name': ['Drug']})
        self.merger.compustat_data = pd.DataFrame()
        
        result = self.merger.merge_datasets()
        
        self.assertTrue(result.empty)


class TestFDADataFetching(unittest.TestCase):
    """Test cases for FDA data fetching (requires internet connection)."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.merger = FDACompustatMerger()
    
    @unittest.skipIf(os.environ.get('SKIP_NETWORK_TESTS'), 'Skipping network tests')
    def test_fetch_fda_approvals(self):
        """Test fetching FDA approval data (requires internet)."""
        df = self.merger.fetch_fda_approvals(limit=10)
        
        self.assertIsInstance(df, pd.DataFrame)
        # Should have fetched some records (might be fewer than limit)
        self.assertGreaterEqual(len(df), 0)
        
        # Check expected columns exist
        expected_columns = ['sponsor_name', 'application_number', 'product_name']
        for col in expected_columns:
            self.assertIn(col, df.columns)


if __name__ == '__main__':
    unittest.main()
