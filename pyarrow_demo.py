# pyarrow_demo.py
import pyarrow as pa
import pyarrow.parquet as pq
import pyarrow.csv as csv
import pyarrow.feather as feather
import numpy as np
import pandas as pd
import tempfile
import os

def demonstrate_basic_operations():
    """Demonstrate basic Arrow array operations"""
    print("\n=== Basic Arrow Array Operations ===")
    
    # Create Arrow arrays
    int_array = pa.array([1, 2, 3, 4, 5], type=pa.int32())
    str_array = pa.array(["apple", "banana", "cherry"])
    bool_array = pa.array([True, False, True, False])
    
    print(f"Int Array: {int_array}")
    print(f"String Array: {str_array}")
    print(f"Boolean Array: {bool_array}")
    
    # Array operations
    print(f"\nSum of int array: {pa.compute.sum(int_array).as_py()}")
    print(f"Element-wise multiply: {pa.compute.multiply(int_array, 2)}")
    print(f"Filtered array: {int_array.filter(pa.array([True, False, True, False, True]))}")

def demonstrate_tables():
    """Demonstrate Arrow Tables"""
    print("\n=== Arrow Tables ===")
    
    # Create a table from arrays
    data = [
        pa.array([1, 2, 3, 4]),
        pa.array(["a", "b", "c", "d"]),
        pa.array([True, False, True, False])
    ]
    table = pa.Table.from_arrays(data, names=['col1', 'col2', 'col3'])
    
    print("Arrow Table:")
    print(table)
    print(f"\nSchema: {table.schema}")
    print(f"Column 'col2': {table.column('col2')}")
    
    # Convert to pandas
    df = table.to_pandas()
    print("\nPandas DataFrame:")
    print(df)

def demonstrate_record_batches():
    """Demonstrate RecordBatches"""
    print("\n=== RecordBatches ===")
    
    # Create a RecordBatch
    data = [
        pa.array([1, 2, 3, 4]),
        pa.array(["x", "y", "z", "w"]),
    ]
    batch = pa.RecordBatch.from_arrays(data, names=['num', 'char'])
    
    print("RecordBatch:")
    print(batch)
    print(f"\nNum columns: {batch.num_columns}")
    print(f"Num rows: {batch.num_rows}")
    
    # Convert to table
    table_from_batch = pa.Table.from_batches([batch])
    print("\nTable from RecordBatch:")
    print(table_from_batch)

def demonstrate_parquet_io():
    """Demonstrate Parquet I/O operations"""
    print("\n=== Parquet I/O ===")
    
    # Create a table to save
    data = [
        pa.array([1, 2, 3, 4]),
        pa.array(["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04"]),
    ]
    table = pa.Table.from_arrays(data, names=['id', 'date'])
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(suffix='.parquet') as f:
        pq.write_table(table, f.name)
        print(f"\nWrote Parquet file to: {f.name}")
        
        # Read back
        table_read = pq.read_table(f.name)
        print("\nRead back from Parquet:")
        print(table_read)
        
        # Read metadata
        metadata = pq.read_metadata(f.name)
        print(f"\nMetadata: {metadata}")

def demonstrate_feather_io():
    """Demonstrate Feather I/O operations"""
    print("\n=== Feather I/O ===")
    
    # Create a table to save
    data = [
        pa.array(np.random.randn(5)),
        pa.array(["a", "b", "c", "d", "e"]),
    ]
    table = pa.Table.from_arrays(data, names=['values', 'labels'])
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(suffix='.feather') as f:
        feather.write_feather(table, f.name)
        print(f"\nWrote Feather file to: {f.name}")
        
        # Read back
        table_read = feather.read_table(f.name)
        print("\nRead back from Feather:")
        print(table_read)

def demonstrate_csv_io():
    """Demonstrate CSV I/O operations"""
    print("\n=== CSV I/O ===")
    
    # Create a CSV file
    csv_data = """id,name,value
1,Alice,100
2,Bob,200
3,Charlie,300
"""
    with tempfile.NamedTemporaryFile(suffix='.csv', mode='w+') as f:
        f.write(csv_data)
        f.flush()
        
        # Read CSV
        table = csv.read_csv(f.name)
        print("\nRead from CSV:")
        print(table)
        
        # Write back to CSV
        output_csv = os.path.join(tempfile.gettempdir(), "output.csv")
        csv.write_csv(table, output_csv)
        print(f"\nWrote to CSV: {output_csv}")

def demonstrate_compute_functions():
    """Demonstrate Arrow compute functions"""
    print("\n=== Compute Functions ===")
    
    # Create arrays
    a = pa.array([1, 2, 3, 4, 5])
    b = pa.array([10, 20, 30, 40, 50])
    
    # Various compute operations
    sum_result = pa.compute.add(a, b)
    mean_result = pa.compute.mean(a)
    filter_result = pa.compute.filter(a, pa.array([True, False, True, False, True]))
    
    print(f"Sum: {sum_result}")
    print(f"Mean: {mean_result.as_py()}")
    print(f"Filtered: {filter_result}")

def demonstrate_schema_manipulation():
    """Demonstrate schema manipulation"""
    print("\n=== Schema Manipulation ===")
    
    # Create table with initial schema
    table = pa.table({
        'id': [1, 2, 3],
        'name': ['a', 'b', 'c']
    })
    
    print("Original schema:")
    print(table.schema)
    
    # Change schema
    new_schema = pa.schema([
        ('id', pa.int64()),
        ('name', pa.string()),
        ('new_col', pa.float64())
    ])
    
    # Add null column to match new schema
    table = table.append_column('new_col', pa.array([None, None, None], type=pa.float64()))
    print("\nModified schema:")
    print(table.schema)

def main():
    # Run all demonstrations
    demonstrate_basic_operations()
    demonstrate_tables()
    demonstrate_record_batches()
    demonstrate_parquet_io()
    demonstrate_feather_io()
    demonstrate_csv_io()
    demonstrate_compute_functions()
    demonstrate_schema_manipulation()

if __name__ == "__main__":
    main()
