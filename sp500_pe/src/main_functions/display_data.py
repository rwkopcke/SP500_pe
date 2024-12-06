'''This program reads selected data from the output of update_data.py
   It then produces .pdf documents displaying these data which compare
   the earnings-price ratios to the 10-year TIPS interest rate.
   
   The addresses of documents for this project appear in this program's 
   project directory: S&P500_PE/sp500_pe/__init__.py
'''

import sys
import gc

import polars as pl
import json
import matplotlib.pyplot as plt

import sp500_pe as sp
import sp500_pe.src.helper_functions.display_helper_func as dh
import sp500_pe.src.helper_functions.plot_func as pf
# import sp500_pe.src.helper_functions.helper_func as hp


#=================  Global Parameters  ================================

# main titles for displays
PAGE0_SUPTITLE = " \nPrice-Earnings Ratios for the S&P 500"
PROJ_EPS_SUPTITLE = " \nCalendar-Year Earnings per Share for the S&P 500"
PAGE2_SUPTITLE = " \nEarnings Margin and Equity Premium for the S&P 500"
PAGE3_SUPTITLE = \
    " \nS&P 500 Forward Earnings Yield, 10-Year TIPS Rate, and Equity Premium"

# str: source footnotes for displays
E_DATA_SOURCE = \
    'https://www.spglobal.com/spdji/en/search/?query=index+earnings&activeTab=all'
RR_DATA_SOURCE = '10-year TIPS: latest rate for each quarter,' + \
    ' Board of Governors of the Federal Reserve System, ' + \
    '\nMarket Yield on U.S. Treasury Securities at 10-Year' + \
    ' Constant Maturity, Investment Basis, Inflation-Indexed,' +\
    '\nfrom Federal Reserve Bank of St. Louis, FRED [DFII10].'
PAGE0_SOURCE = E_DATA_SOURCE
PAGE1_SOURCE = E_DATA_SOURCE
PAGE2_SOURCE = E_DATA_SOURCE + '\n\n' + RR_DATA_SOURCE
PAGE3_SOURCE = E_DATA_SOURCE + '\n\n' + RR_DATA_SOURCE

# hyopothetical quarterly growth factor future stock prices
ROGQ = (1+0.05)**(1/4)

HIST_COL_NAMES = ['date', 'yr_qtr', 'price', 'op_eps', 'rep_eps',
                'op_p/e', 'rep_p/e', '12m_op_eps', '12m_rep_eps',
                'op_margin', 'real_int_rate']

DATA_COLS_RENAME  = {'op_margin': 'margin',
                    'real_int_rate': 'real_rate'}


# ================  MAIN =============================================+

# https://mateuspestana.github.io/tutorials/pandas_to_polars/
# https://www.rhosignal.com/posts/polars-pandas-cheatsheet/
# https://www.rhosignal.com/tags/polars/
# https://jrycw.github.io/ezp2p/
# https://docs.pola.rs/py-polars/html/reference/dataframe/api/polars.DataFrame.filter.html
# https://fralfaro.github.io/DS-Cheat-Sheets/examples/polars/polars/

def display_data():
    
# read record_dict
    if sp.RECORD_DICT_ADDR.exists():
        with sp.RECORD_DICT_ADDR.open('r') as f:
            record_dict = json.load(f)
        print('\n============================================')
        print(f'Read record_dict from: \n{sp.RECORD_DICT_ADDR}')
        print('============================================\n')
    else:
        print('\n============================================')
        print(f'No record_dict in \n{sp.RECORD_DICT_ADDR.name}')
        print(f'at: \n{sp.RECORD_DICT_ADDR}')
        print('Processing ended')
        print('============================================\n')
        sys.exit()
        
    # provide the date of projection
    
    date_this_projn = record_dict['latest_used_file'].split('.')[0][-10:]
    yr_qtr_current_projn = record_dict["proj_yr_qtrs"][0]
    
 # read hist_df
    if sp.OUTPUT_HIST_ADDR.exists():
        with sp.OUTPUT_HIST_ADDR.open('r') as f:
            data_df = pl.read_parquet(source= f,
                                      columns= HIST_COL_NAMES)\
                        .filter(pl.col('yr_qtr')
                                  .is_in(record_dict['proj_yr_qtrs']))
                        
            #pl.col("yr_qtr").is_in('proj_yr_qtrs'.replace_strict(record_dict))
            #pl.col('yr_qtr').map_elements(lambda x: x in record_dict['proj_yr_qtrs']
            
        print('\n============================================')
        print(f'Read data history from: \n{sp.OUTPUT_HIST_ADDR}')
        print('============================================\n')
    else:
        print('\n============================================')
        print(f'No data history in: \n{sp.OUTPUT_HIST_ADDR.name}')
        print(f'at: \n{sp.OUTPUT_HIST_ADDR}')
        print('Processing ended')
        print('============================================\n')
        sys.exit()
    
# +++++ read proj dfs +++++++++++++++++++++++++++++++++++++++++++++++++
# put dfs in proj_dict, key = dfs' 'yr_qtr' value (from file.name)
    proj_dict = dict()
    for file_name, yr_qtr in zip(record_dict['output_proj_files'],
                                 record_dict['proj_yr_qtrs']):
        file_addr = sp.OUTPUT_PROJ_DIR / file_name
        if file_addr.exists():
            with file_addr.open('r') as f:
                proj_dict[yr_qtr] = pl.read_parquet(f)
        else:
            print('\n============================================')
            print(f'No output file at \n{file_addr.name}')
            print(f'in: \n{file_addr}')
            print('Processing ended')
            print('============================================\n')

# DISPLAY THE DATA ====================================================
    # https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.subplot_mosaic.html
    # https://matplotlib.org/stable/api/axes_api.html
    # https://matplotlib.org/stable/api/axes_api.html#axes-position

# +++++ create the y-values (columns) for the series to be plotted

# page zero  ======================
# shows:  projected eps for current cy and future cy
# the projections shown for each quarter are the latest
# made in the quarter

    # create graphs
    fig = plt.figure(figsize=(8.5, 11), 
                     layout="constrained")
    # one plot above the other
    ax = fig.subplot_mosaic([['operating'],
                             ['reported']])
    fig.suptitle(
        f'{PROJ_EPS_SUPTITLE}\n{date_this_projn}',
        fontsize=13,
        fontweight='bold')
    fig.supxlabel(PAGE0_SOURCE, fontsize= 8)

    # subsets of columns for op eps (top panel)
    df = data_df.select(['yr_qtr', '12m_op_eps'])
    p_dict_columns = ['12m_op_eps', 'yr_qtr']
    df = dh.page0_df(df, proj_dict, p_dict_columns, '12m_op_eps')\
                .rename({'12m_op_eps': 'actual'})\
                .sort(by= 'yr_qtr')
    
    xlabl = '\ndate of projection\n'
    ylabl = '\nearnings per share\n'
    
    pf.plots_page0(ax['operating'], df,
                title= ' \nProjections of Operating EPS',
                ylim= (100, None),
                xlabl= xlabl,
                ylabl= ylabl)
    
    # subsets of columns for rep eps (bottom panel)
    df = data_df.select(['yr_qtr', '12m_rep_eps'])
    p_dict_columns = ['12m_rep_eps', 'yr_qtr']
    df = dh.page0_df(df, proj_dict, p_dict_columns, '12m_rep_eps')\
                .rename({'12m_rep_eps': 'actual'})\
                .sort(by= 'yr_qtr')
    
    pf.plots_page0(ax['reported'], df,
                title= ' \nProjections of Reported EPS',
                ylim= (75, None),
                xlabl= xlabl,
                ylabl= ylabl)
    
    # show the figure
    print('\n============================')
    print(sp.DISPLAY_0_ADDR)
    print('============================\n')
    fig.savefig(str(sp.DISPLAY_0_ADDR))
    
    del df
    gc.collect()
    
# page one  ======================
# shows:  historical 12m trailing pe plus
#    forward 12m trailing pe, using current p

    # create graphs
    fig = plt.figure(figsize=(8.5, 11), 
                     layout="constrained")
    # one plot above the other
    ax = fig.subplot_mosaic([['operating'],
                             ['reported']])
    fig.suptitle(
        f'{PAGE0_SUPTITLE}\n{date_this_projn}\n ',
        fontsize=13,
        fontweight='bold')
    fig.supxlabel(PAGE1_SOURCE, fontsize= 8)
    
    # create the top and bottom graphs for op and rep pe
    # new DF with cols for p/e and alt p/e, both using 12m trailing E
        #   also yr_qtr and actual cy
        #       0) yr_qtr (from df) 
        #       1) historical 12m trailing p/e (from df)
        #       2) alt1 using constant p for proj quarters
        #       3) alt2 using p growing at ROG for proj quarters
        #       4) rolling 12m E (hist+proj) for proj quarters
    
    # top panel
    df = data_df.select(['yr_qtr', '12m_op_eps', 'price'])
               
    p_df = proj_dict[yr_qtr_current_projn]\
                .select(['yr_qtr', '12m_op_eps'])
    
    df = dh.page1_df(df, p_df, '12m_op_eps', ROGQ )
    
    denom = 'divided by projected earnings'
    legend1 = f'price constant from {date_this_projn}\n{denom}'
    legend2 = f'price increases 5% ar from {date_this_projn}\n{denom}'
    
    df = df.rename({'pe': 'historical',
               'fix_proj_p/e': legend1,
               'incr_proj_p/e': legend2})
    
    title = 'Ratio: Price to 12-month Trailing Operating Earnings'
   
    pf.plots_page1(ax['operating'], df,
                    ylim= (None, None),
                    title= title,
                    ylabl= ' \n',
                    xlabl= ' \n')

    # bottom panel
    df = data_df.select(['yr_qtr', '12m_rep_eps', 'price'])
    
    p_df = proj_dict[yr_qtr_current_projn]\
               .select(['yr_qtr', '12m_rep_eps'])
    
    df = dh.page1_df(df, p_df, '12m_rep_eps', ROGQ )
    
    df = df.rename({'pe': 'historical',
                    'fix_proj_p/e': legend1,
                    'incr_proj_p/e': legend2})
    
    title = 'Ratio: Price to 12-month Trailing Reported Earnings'
    
    pf.plots_page1(ax['reported'], df,
                    ylim= (None, None),
                    title= title,
                    ylabl= ' \n',
                    xlabl= ' \n')
    
    print('\n============================')
    print(sp.DISPLAY_1_ADDR)
    print('============================\n')
    fig.savefig(str(sp.DISPLAY_1_ADDR))
    
    del df
    gc.collect()
    
# page two  ======================
# shows:  historical data for margins and 
# historical and current estimates for equity premium
    
    # create graphs
    fig = plt.figure(figsize=(8.5, 11), 
                     layout="constrained")
    # stack plots
    ax = fig.subplot_mosaic([['margin'],
                             ['quality'],
                             ['premium']])
    fig.suptitle(
        f'{PAGE2_SUPTITLE}\n{date_this_projn}\n',
        fontsize=13,
        fontweight='bold')
    fig.supxlabel(PAGE2_SOURCE, fontsize= 8)
    
    # create the top and bottom graphs for margins and premiums
    # create working df for op margins (top panel)

    df = data_df.rename({'op_margin' : 'margin'})\
                .select('yr_qtr', 'margin')\
                .with_columns((pl.col('margin') * 100)
                            .alias('margin100'))\
                .drop('margin')\
                .rename({'margin100': 'margin'})\
                .sort(by= 'yr_qtr')
    
    title = 'Margin: quarterly operating earnings relative to revenue'
    
    pf.plots_page2(ax['margin'], df,
                    ylim= (None, None),
                    title= title,
                    ylabl= ' \npercent\n ',
                    xlabl= ' \n ',
                    hrzntl_vals= [10.0])
    
    # create working df for ratio: reported / operating E
    df = data_df.rename({'12m_rep_eps': 'reported',
                         '12m_op_eps': 'operating'})\
                .select('yr_qtr', 'reported', 'operating')\
                .with_columns((pl.col('reported') / 
                               pl.col('operating') * 100)
                              .cast(pl.Int8)
                              .alias('quality'))\
                .drop('reported', 'operating')\
                .sort(by= 'yr_qtr')
    title = 'Quality of Earnings: ratio of 12-month reported to operating earings'
    
    pf.plots_page2(ax['quality'], df,
                    ylim= (None, None),
                    title= title,
                    ylabl= ' \npercent\n ',
                    xlabl= ' \n ',
                    hrzntl_vals= [80, 90])

    # create working df for premia (bottom panel)
    df = data_df.rename({'real_int_rate' : 'real_rate'})\
                .select('yr_qtr', '12m_rep_eps', 
                        'real_rate', 'price')\
                .with_columns(((pl.col('12m_rep_eps') /
                                pl.col('price')) * 100 -
                                pl.col('real_rate'))
                            .alias('premium'))\
                .drop('12m_rep_eps', 'real_rate', 'price')\
                .sort(by= 'yr_qtr')

    title = 'Equity Premium: \nratio of 12-month trailing reported earnings to price, '
    title += 'less 10-year TIPS rate'

    pf.plots_page2(ax['premium'], df,
                    ylim= (None, None),
                    title= title,
                    ylabl= ' \npercent\n ',
                    xlabl= ' \n ',
                    hrzntl_vals= [2.0, 4.0])
    
    print('\n============================')
    print(sp.DISPLAY_2_ADDR)
    print('============================\n')
    fig.savefig(str(sp.DISPLAY_2_ADDR))
    #plt.savefig(f'{output_dir}/eps_page2.pdf', bbox_inches='tight')
    
    del df
    gc.collect()
    
# page three  ======================
# shows:  components of the equity premium,
# using 12m forward projected earnings
    
    # create graphs
    fig = plt.figure(figsize=(8.5, 11), 
                     layout="constrained")
    # upper and lower plots
    ax = fig.subplot_mosaic([['operating'],
                             ['reported']])
    fig.suptitle(
        f'{PAGE3_SUPTITLE}\n{date_this_projn}\n',
        fontsize=13,
        fontweight='bold')
    fig.supxlabel(PAGE3_SOURCE, fontsize= 8)
    
    xlabl = '\nquarter of projection, price, and TIPS rate\n\n'
    ylabl = ' \npercent\n '
    
    # create the top and bottom graphs for premiums

    # create working df for op premium (top panel)
    # add a col: proj eps over the next 4 qtrs
    df = data_df.select('yr_qtr', 'price', 'real_int_rate',
                        'op_eps')
    df = dh.contemp_12m_fwd_proj(data_df, proj_dict,
                                 'op_eps', 'fwd_12mproj_op_eps')
    
    df = dh.page3_df(df, 'fwd_12mproj_op_eps')
    
    df = df.rename({'earnings / price': 'projected earnings / price'})
    
    title = 'Operating Earnings: projected over next 4 quarters'

    pf.plots_page3(ax['operating'], df,
                ylim= (None, 9),
                title= title,
                ylabl= ylabl,
                xlabl= xlabl,
                hrzntl_vals= [2.0, 4.0])
    
    # bottom panel
    df = data_df.select('yr_qtr', 'price', 'real_int_rate',
                        'rep_eps')
    
    # add a col : proj eps over the next 4 qtrs
    df = dh.contemp_12m_fwd_proj(data_df, proj_dict,
                                 'rep_eps', 'fwd_12mproj_rep_eps')
    df = dh.page3_df(df, 'fwd_12mproj_rep_eps')
    
    df = df.rename({'earnings / price': 'projected earnings / price'})
    
    title = 'Reported Earnings: projected over next 4 quarters'

    pf.plots_page3(ax['reported'], df,
                ylim= (None, 9),
                title= title,
                ylabl= ylabl,
                xlabl= xlabl,
                hrzntl_vals= [2.0, 4.0])
    
    print('\n============================')
    print(sp.DISPLAY_3_ADDR)
    print('============================\n')
    fig.savefig(str(sp.DISPLAY_3_ADDR))
    #plt.savefig(f'{output_dir}/eps_page3.pdf', bbox_inches='tight')
    
    del df
    gc.collect()


if __name__ == '__main__':
    display_data()
    