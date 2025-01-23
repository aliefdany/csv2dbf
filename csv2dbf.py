#!/usr/bin/env python3
import csv
import dbf
import pandas as pd
import sys
import argparse
import numpy as np

def determine_field_specs(column):
    """
    Determine appropriate field specifications for a column
    """
    # Handle numeric columns
    if pd.api.types.is_numeric_dtype(column):
        # Get max absolute value to determine field length
        max_val = column.abs().max()
        is_float = column.dtype == float
        
        # Determine length and decimal places
        if pd.isna(max_val):
            length, decimals = 10, 2  # Default numeric field
        elif is_float:
            # Count max decimal places
            decimal_places = column.astype(str).str.split('.').str[1].str.len().max()
            total_length = len(str(int(max_val))) + decimal_places + 1  # +1 for decimal point
            length = max(total_length, 10)
            decimals = min(decimal_places, 4)  # Limit decimal places
        else:
            length = len(str(int(max_val))) + 1  # +1 for potential sign
            decimals = 0
        
        return f'N({min(length, 20)},{decimals})'
    
    # Handle date columns
    elif pd.api.types.is_datetime64_any_dtype(column):
        return 'D'
    
    # Handle string columns
    else:
        max_length = column.astype(str).str.len().max()
        return f'C({min(max_length, 254)})'

def csv_to_dbf(csv_file, dbf_file, delimiter=',', encoding='utf-8'):
    """
    Convert CSV to DBF with precise type handling
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file, delimiter=delimiter, encoding=encoding)
        
        # Prepare field specifications
        field_specs = []
        for column in df.columns:
            # Clean column name
            clean_column = ''.join(e for e in column if e.isalnum())[:10]
            
            # Determine field specification
            field_type = determine_field_specs(df[column])
            field_specs.append(f'{clean_column} {field_type}')
        
        # Create DBF table
        table = dbf.Table(dbf_file, ';'.join(field_specs), codepage='utf8')
        table.open(mode=dbf.READ_WRITE)
        
        # Write records
        for _, row in df.iterrows():
            record = []
            for column in df.columns:
                value = row[column]
                
                # Handle numeric columns to preserve exact value
                if pd.api.types.is_numeric_dtype(df[column]):
                    value = float(value) if pd.notnull(value) else None
                
                # Handle datetime columns
                elif pd.api.types.is_datetime64_any_dtype(df[column]):
                    value = value.date() if pd.notnull(value) else None
                
                # Handle other columns
                elif pd.isna(value):
                    value = None
                
                record.append(value)
            
            table.append(tuple(record))
        
        table.close()
        print(f"Successfully converted {csv_file} to {dbf_file}")
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
    
    args = parser.parse_args()
    
    success = csv_to_dbf(args.input, args.output, args.delimiter, args.encoding)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()