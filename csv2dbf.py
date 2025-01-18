#!/usr/bin/env python3
import csv
import dbf
import pandas as pd
import sys
import argparse
from datetime import datetime
import numpy as np

def determine_numeric_field_spec(series):
    """
    Determine appropriate numeric field specifications for a pandas series
    Returns tuple of (length, decimal_places)
    """
    max_val = series.abs().max()
    min_val = series.abs().min()
    
    # Handle integers
    if series.dtype in ['int64', 'int32']:
        str_len = len(str(int(max_val)))
        return (str_len + 1, 0)  # +1 for sign
    
    # Handle floats
    decimal_str = series.astype(str)
    max_decimals = 0
    max_total_len = 0
    
    for val in decimal_str:
        if '.' in val:
            integer_part, decimal_part = val.split('.')
            max_decimals = max(max_decimals, len(decimal_part))
            total_len = len(integer_part) + len(decimal_part) + 1  # +1 for decimal point
            max_total_len = max(max_total_len, total_len)
    
    # Ensure minimum field length and valid decimal places
    field_length = max(max_total_len + 1, 3)  # +1 for sign
    decimal_places = min(max_decimals, field_length - 2)  # Ensure decimal places are valid
    
    return (field_length, decimal_places)

def is_date(series):
    """
    Check if a series contains date values
    """
    try:
        pd.to_datetime(series.dropna(), errors='raise')
        return True
    except:
        return False

def format_date(value):
    """
    Format date value for DBF
    """
    if pd.isna(value):
        return None
    try:
        if isinstance(value, str):
            return pd.to_datetime(value).date()
        return pd.Timestamp(value).date()
    except:
        return None

def csv_to_dbf(csv_file, dbf_file, delimiter=',', encoding='utf-8'):
    """
    Convert a CSV file to DBF format using the dbf package
    
    Args:
        csv_file (str): Path to input CSV file
        dbf_file (str): Path to output DBF file
        delimiter (str): CSV delimiter character
        encoding (str): Input file encoding
    """
    try:
        # Read CSV file using pandas
        print(f"Reading CSV file: {csv_file}")
        df = pd.read_csv(csv_file, delimiter=delimiter, encoding=encoding)
        
        # Print original columns for debugging
        print("\nOriginal CSV columns:")
        for col in df.columns:
            print(f"- {col}")
        
        # Create field specifications for DBF
        field_specs = []
        date_columns = []  # Track date columns for conversion
        
        for column in df.columns:
            # Clean column name - remove spaces and special characters
            clean_column = ''.join(e for e in column if e.isalnum())[:10]
            
            # Get column data for type inference
            column_data = df[column].dropna()
            
            # Check for date fields first
            if is_date(df[column]):
                field_specs.append(f'{clean_column} D')
                date_columns.append(column)
            # Then check for numeric fields
            elif pd.to_numeric(df[column], errors='coerce').notnull().all():
                # Handle numeric fields
                length, decimals = determine_numeric_field_spec(pd.to_numeric(df[column]))
                field_specs.append(f'{clean_column} N({length},{decimals})')
            else:
                # Handle string fields
                max_length = df[column].astype(str).str.len().max()
                field_specs.append(f'{clean_column} C({min(max_length, 254)})')
        
        # Print field specifications for debugging
        print("\nDBF field specifications:")
        for spec in field_specs:
            print(f"- {spec}")
        
        # Create new DBF table
        table = dbf.Table(dbf_file, ';'.join(field_specs), codepage='utf8')
        table.open(mode=dbf.READ_WRITE)
        
        # Print actual DBF field names for debugging
        print("\nActual DBF field names:")
        for field in table.field_names:
            print(f"- {field}")
        
        # Write records
        total_records = len(df)
        print(f"\nWriting {total_records} records to DBF file...")
        
        for idx, row in df.iterrows():
            record = []
            for column in df.columns:
                value = row[column]
                # Handle date fields
                if column in date_columns:
                    value = format_date(value)
                # Handle other fields
                elif pd.isna(value):
                    value = None
                record.append(value)
            
            try:
                table.append(tuple(record))
            except Exception as e:
                print(f"Error writing record {idx + 1}: {str(e)}")
                print(f"Record data: {record}")
                continue
            
            # Print progress every 1000 records
            if (idx + 1) % 1000 == 0:
                print(f"Processed {idx + 1}/{total_records} records...")
        
        table.close()
        print(f"\nSuccessfully converted {csv_file} to {dbf_file}")
        return True
        
    except Exception as e:
        print(f"Error converting file: {str(e)}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description='Convert CSV files to DBF format')
    parser.add_argument('input', help='Input CSV file')
    parser.add_argument('output', help='Output DBF file')
    parser.add_argument('-d', '--delimiter', default=',', help='CSV delimiter (default: ,)')
    parser.add_argument('-e', '--encoding', default='utf-8', help='Input file encoding (default: utf-8)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    args = parser.parse_args()
    
    success = csv_to_dbf(args.input, args.output, args.delimiter, args.encoding)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()