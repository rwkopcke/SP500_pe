# S&P500 index and earnings
#### initiated:  2023 08
#### current version:  2024 12 06
### Uses current and historical data
- index of stock prices for the S&P500
- operating and reported earnings for the S&P500
- projections of operating and reported earnings
- interest rate on 10-year TIPS
- operating margins for the S&P500

### Future extension
- composition of earnings by "industry"

### update_data.py
- reads new data from .xlsx workbooks in input_dir
- S&P data downloaded from S&P's weekly posts
- TIPS data downloaded from FRED database
- writes json and parquet files to output_dir
- archives the workbooks from input_dir
### display_data.py
- reads the files in output_dir
- produces pdf documents in display_dir
- presents quarterly data, 2018 through the present
    - page0: projected versus actual earnings
    - page1: future and historical price-earnings ratios
    - page2: margin and equity premium using trailing earnings
    - page3: equity premium usingnprojected earnings
### sources
- https://www.spglobal.com/spdji/en/search/?query=index+earnings&activeTab=all
- https://fred.stlouisfed.org/series/DFII10/chart
### file structure
S&P500_PE/
- README.md
- pyproject.toml
- poetry.lock
- .venv
- sp500_pe/
    - \_\_pycache__
    - \_\_init__.py
    - src
        - main_functions
            - \_\_pycache__
            - update_data.py
            - display_data.py
        - helper_functions
            - \_\_pycache__
            - helper_func.py
            - read_data_func.py
            - plot_func.py
            - display_helper_func.py
- input_dir/
- output_dir/
    - sp500_pe_df_actuals.parquet
    - estimates/
        - sp-500-eps-est YYYY MM DD.parquet
- display_dir/
    - eps_page0.pdf
    - eps_page1.pdf
    - eps_page2.pdf
    - eps_page3.pdf
- record_dict.json<br>
<br>
<br>

## Instructions
### prepare new data if any
1. Put new .xlsx from S&P into input_dir
    - https://www.spglobal.com/spdji/en/search/?query=index+earnings&activeTab=all
    - name: sp-500-eps-est YYYY MM DD.xlsx
    - date from top of ESTIMATES&PEs sheet
    - update_data.py also reads this sheet's date
2. Put new .xlsx from FRED into input_dir
    - https://fred.stlouisfed.org/series/DFII10/chart
    - name: DFII10.xlsx
    - select quarterly, end-of-period observations
    - select max period in FRED
    - sdownload as .xls from FRED
    - add observation for current quarter in xls
    - save .xls as .xlsx file
### update_data.py
1. set ARCHIVE_DIR in sp500_pe/\_\_init__.py to your archive
2. put the new S&P and FRED workbooks in input_dir/
3. launch update_data.py
    - reads files in input_dir/
    - moves input files to archive
    - writes the existing .json to backup_dir/
    - writes new .json file to sp500_pe/
    - moves sp500_pe_df_actuals.parquet to backup_dir/
    - writes new sp500_pe_df_actuals.parquet
    - writes output files to output_dir/estimates/
### display_data.py
launch display_data.py
- reads files in output_dir/
- writes .pdf pages to display_dir/
- pdf pages comprise the output
<br>
<br>

## Other Information
### __init__.py
Contains global variables with addresses for all files
- user must specify location of ARCHIVE
- addresses of other files relative to location of S&P500_PE/
- uses Path()
### output_dir/
#### sp-500-eps-est YYYY MM DD.parquet
- polars dataframe with projected earnings
- from sp-500-eps-est YYYY MM DD.xlsx
- for the latest date in each quarter
- new output file for each new input file

#### sp500_pe_df_actuals.parquet
- one polars dataframe for all historical data
- completely udated by new input data
### record_dict.json
- records files read
- records files used and written
- maintains date of latest file read
- maintains list of quarters covered by data
<br>
<br>

## Recreate/reinitialize entire set of data files from all history
1. \_\_init__.py under ARCHIVE_DIR
    - remove # before INPUT_DIR = ARCHIVE_DIR
    - remove # before INPUT_RR_ADDR = ARCHIVE_DIR / INPUT_RR_FILE
2. delete record_dict.json file
3. output_dir/
    - delete sp500_pe_df_actuals.parquet
    - delete all files inside estimates/ subdirectory
4. launch update_data.py
