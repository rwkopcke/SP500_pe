'''
    set global absolute paths for IO addresses
        using absolute path to "s&p500_pe" top-level dir
    use universal path expressions
        using Path() from pathlib
        
    access these values in other modules by
        import sp500_pe as sp
        sp.INPUT_DIR
'''

from pathlib import Path

# source of new data
SP_SOURCE = \
    "https://www.spglobal.com/spdji/en/search/?query=index+earnings&activeTab=all"
REAL_RATE_SOURCE = "https://fred.stlouisfed.org/series/DFII10"

# Project's data:
# Path() produces "universal path" and
#      allows simple appending for extensions
#      => no '/' at end of path, format of append provides it
BASE_DIR = Path.cwd()

RECORD_DICT_DIR = BASE_DIR
RECORD_DICT_FILE = "record_dict.json"
RECORD_DICT_ADDR = RECORD_DICT_DIR / RECORD_DICT_FILE

INPUT_DIR = BASE_DIR / "input_dir"
INPUT_RR_FILE = 'DFII10.xlsx'
INPUT_RR_ADDR = INPUT_DIR / INPUT_RR_FILE
# #INPUT_SPRICE_FILE = INPUT_DIR / 'SP500.xlsx'

ARCHIVE_DIR = \
   Path('/Users/richardkopcke/Dropbox/Stock Analysis/sp_data_archive')
# do the following only to reinitialize the projects' data files
# from the archived source .xlsx files:
# make sure that make sure that DFII10.xlsx is in archive_dir

# to reinitialize, uncomment:
# ==========================================
#INPUT_DIR = ARCHIVE_DIR
#INPUT_RR_ADDR = ARCHIVE_DIR / INPUT_RR_FILE
# ==========================================
# after reinitializing, recomment these lines

OUTPUT_DIR = BASE_DIR / "output_dir"
OUTPUT_HIST_FILE = 'sp500_pe_df_actuals.parquet'
OUTPUT_HIST_ADDR = OUTPUT_DIR / OUTPUT_HIST_FILE
OUTPUT_HIST_FILE = OUTPUT_DIR / 'sp500_pe_df_actuals.parquet'
OUTPUT_PROJ_DIR = OUTPUT_DIR / 'estimates'

BACKUP_DIR = BASE_DIR / 'backup_dir'
BACKUP_HIST_FILE = "backup_pe_df_actuals.parquet"
BACKUP_HIST_ADDR = BACKUP_DIR / BACKUP_HIST_FILE
BACKUP_RECORD_DICT =  "backup_record_dict.json"
BACKUP_RECORD_DICT_ADDR = BACKUP_DIR / BACKUP_RECORD_DICT

DISPLAY_DIR = BASE_DIR / "display_dir"
DISPLAY_0 = 'eps_page0.pdf'
DISPLAY_1 = 'eps_page1.pdf'
DISPLAY_2 = 'eps_page2.pdf'
DISPLAY_3 = 'eps_page3.pdf'
DISPLAY_0_ADDR = DISPLAY_DIR / DISPLAY_0
DISPLAY_1_ADDR = DISPLAY_DIR / DISPLAY_1
DISPLAY_2_ADDR = DISPLAY_DIR / DISPLAY_2
DISPLAY_3_ADDR = DISPLAY_DIR / DISPLAY_3
