#!/usr/bin/env python3
import dbf
import pandas as pd
import sys
import argparse

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
        for column in df.columns:
            # Get column data for type inference
            column_data = df[column].dropna()
            max_length = df[column].astype(str).str.len().max()
            
            # Clean column name - remove spaces and special characters
            clean_column = ''.join(e for e in column if e.isalnum())[:10]
            
            # Determine field type based on data
            if pd.to_numeric(df[column], errors='coerce').notnull().all():
                if df[column].dtype == 'int64':
                    field_specs.append(f'{clean_column} N({min(max_length, 20)},0)')
                else:
                    field_specs.append(f'{clean_column} N({min(max_length, 20)},2)')
            elif pd.to_datetime(column_data, errors='coerce').notnull().all():
                field_specs.append(f'{clean_column} D')
            else:
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
                if pd.isna(value):
                    record.append(None)
                else:
                    record.append(value)
            table.append(tuple(record))
            
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