# hlfiles
handle lots of files for you

## Modules

### read
A basic module which provides a function `scan_files()` to read all files with a specified suffix in a root directory.

### convert
It provides a class `DataFileConverter`, which is used to generate file converting function, such as a function that converts all csv.gz files into parquet files (see example).

## Example
```Shell
pip install hlfiles
```


```Python
import pandas as pd
from hlfiles.convert import DataFileConverter


# You can create any file converting funcion by DataFileConverter
csvgz_to_parquet = DataFileConverter(
    read_func=pd.read_csv,
    write_func=lambda data, file_path: data.to_parquet(file_path),
    read_file_extension="csv.gz",
    write_file_extension="parquet",
    read_func_kwargs={"compression": "gzip"},
)


if __name__ == "__main__":
    root_dir = r"xxx"
    # Convert all csv.gz files into parquet files in root_dir
    csvgz_to_parquet(root_dir, inplace=True)
```