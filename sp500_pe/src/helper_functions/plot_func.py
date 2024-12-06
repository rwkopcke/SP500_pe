import polars as pl

def plots_page0(ax, df,
                title= None, 
                ylim = (None, None), 
                xlabl= None,
                ylabl= None):
    '''
        A helper function to show many line plots
        and a scatter plot
        x axis is the 1st col of df
        scatter series is the 2nd col
        the remaining cols are line plots
        the legend names of all plotted series
           are the col names in df, 
           list(df.columns)[2:]
    '''
    
    # create the title and labels for the plot
    ax.set_title(title, fontweight= 'bold', loc= 'left')
    ax.set_xlabel(xlabl, fontweight= 'bold')
    ax.set_ylabel(ylabl, fontweight= 'bold')
    
    # prepare labels for the horizontal axis
    [yq, x_tick_labels] = yq_and_ticklabels(df)
    
    #color_ = ['gray', 'blue', 'red']
    #style_ = ['dashed', 'dotted', 'dotted']
    
    # df.columns[1] is 'actual', see below
    for name in list(df.columns)[2:]:
        # if name has only one data point
        if df[name].count() == 1:
            ax.scatter(yq, df.select(name), 
               marker= 'o', 
               s= 15,
               label= name)
        # if name has several data points
        else:
            ax.plot(yq, df.select(name), 
                # with enumerate:
                #   linestyle= style_[idx],
                #   color= color_[idx],
                label= name)
        
    ax.scatter(yq, df.select('actual'), 
               marker= 's', 
               s= 15,
               color= 'black',
               label= 'actual')
    
    ax.set_ylim(ylim)

    # the 1st arg gets locs for the labels
    # the 2nd arg specs the labels for these locs             
    ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(), 
                  fontsize= 8)
    
    ax.set_xticks(ax.get_xticks(), x_tick_labels, 
                  rotation= 90, fontsize= 7)
    #ax.yaxis.set_ticks_position('both')
    
    ax0 = ax.twinx()
    ax0.set_ylim(ax.get_ylim())
    ax0.set_yticks(ax.get_yticks(), ax.get_yticklabels(),
                   fontsize= 8)
    ax0.set_ylabel(' ') #creates a space on the right side
    
    # https://matplotlib.org/stable/users/explain/axes/legend_guide.html
    ax.legend(title= 'for years:',
              title_fontsize= 9,
              fontsize= 8,
              loc= 'upper left')
    
    ax.hlines(y=200, color='lightgray',
              xmin= min(yq),
              xmax= max(yq),
              linestyle= 'dotted')
    ax.hlines(y=250, color='lightgray',
              xmin= min(yq),
              xmax= max(yq),
              linestyle= 'dotted')
    ax.hlines(y=150, color='lightgray',
              xmin= min(yq),
              xmax= max(yq),
              linestyle= 'dotted')
    
    return ax


def plots_page1(ax, df,
                ylim= (None, None),
                title = None,
                xlabl = None,
                ylabl = None):
    """
        Show one (composite) line plot
        the x axis labels are strings in the first col of df
        the data to be plotted are in the subsequent cols of df
    """
    
     # create the title and labels for the plot
    ax.set_title(title, fontweight= 'bold', loc= 'left')
    ax.set_xlabel(xlabl, fontweight= 'bold')
    ax.set_ylabel(ylabl, fontweight= 'bold')
    
    # prepare labels for the horizontal axis
    [yq, x_tick_labels] = yq_and_ticklabels(df)
    
    # fetch series name and plot it
    for name in list(df.columns)[1:]:
        if name == 'historical':
            ax.plot(yq, df.select(name), 
                    label= name)
        else: 
            ax.plot(yq, df.select(name),
                    label= name,
                    linestyle= 'dashed')
                
    # axis titles, tick labels, and legend
    ax.set_ylim(ylim)

    # the 1st arg gets locs for the labels
    # the 2nd arg specs the labels for these locs             
    ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(), 
                  fontsize= 8)
    ax.set_xticks(ax.get_xticks(), x_tick_labels, 
                  rotation= 90, fontsize= 8)
    
    ax0 = ax.twinx()
    ax0.set_ylim(ax.get_ylim())
    ax0.set_yticks(ax.get_yticks(), ax.get_yticklabels(),
                   fontsize= 8)
    ax0.set_ylabel(' ') #creates a space on the right side

    ax.legend(#title= 'price to 12-month trailing earnings',
              #title_fontsize= 10,
              fontsize= 9,
              loc= 'upper right')
    
    ax.hlines(y=20, color='lightgray',
              xmin= min(yq),
              xmax= max(yq),
              linestyle= 'dotted')
    
    return ax


def plots_page2(ax, df,
                ylim= (None, None),
                title = None,
                xlabl = None,
                ylabl = None,
                hrzntl_vals = None):
    """
        show simple line plots
        with dotted, light lines at specified hrzntl_vals
    """
    
    # create the title and labels for the plot
    ax.set_title(title, fontweight= 'bold', loc= 'left')
    ax.set_xlabel(xlabl, fontweight= 'bold')
    ax.set_ylabel(ylabl, fontweight= 'bold')
    
    # prepare labels for the horizontal axis
    [yq, x_tick_labels] = yq_and_ticklabels(df)
    
    # series name and plot it
    name = list(df.columns)[-1:]
    ax.plot(yq, df.select(name))
                
    # axis titles, tick labels, and legend
    ax.set_ylim(ylim)

    # the 1st arg gets locs for the labels
    # the 2nd arg specs the labels for these locs             
    ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(), 
                  fontsize= 8)
    ax.set_xticks(ax.get_xticks(), x_tick_labels, 
                  rotation= 90, fontsize= 8)
    
    ax0 = ax.twinx()
    ax0.set_ylim(ax.get_ylim())
    ax0.set_yticks(ax.get_yticks(), ax.get_yticklabels(),
                   fontsize= 8)
    ax0.set_ylabel(' ') #creates a space on the right side
    
    for val in hrzntl_vals:
        ax.hlines(y=val, color='lightgray',
              xmin= min(yq),
              xmax= max(yq),
              linestyle= 'dotted')
    
    return ax


def plots_page3(ax, df,
                ylim= (None, None),
                title = None,
                xlabl = None,
                ylabl = None,
                hrzntl_vals = None):
    """
        show simple line plots
        with dotted, light lines at specified hrzntl_vals
    """
    
     # create the title and labels for the plot
    ax.set_title(title, fontweight= 'bold', loc= 'left')
    ax.set_xlabel(xlabl, fontweight= 'bold')
    ax.set_ylabel(ylabl, fontweight= 'bold')
    
    # prepare labels for the horizontal axis
    [yq, x_tick_labels] = yq_and_ticklabels(df)
    
    # series name and plot it
    for idx, name in enumerate(list(df.columns)[1:]):
        if idx == 1:
            ax.plot(yq, df.select(name),
                    label= name)
        elif idx == 0:
            ax.plot(yq, df.select(name),
                    label= name,
                    linestyle= 'dashed')
        else:
            ax.plot(yq, df.select(name),
                    label= name,
                    linestyle= 'dotted')
                
    # axis titles, tick labels, and legend
    ax.set_ylim(ylim)

    # the 1st arg gets locs for the labels
    # the 2nd arg specs the labels for these locs             
    ax.set_yticks(ax.get_yticks(), ax.get_yticklabels(), 
                  fontsize= 8)
    ax.set_xticks(ax.get_xticks(), x_tick_labels, 
                  rotation= 90, fontsize= 8)
    
    ax0 = ax.twinx()
    ax0.set_ylim(ax.get_ylim())
    ax0.set_yticks(ax.get_yticks(), ax.get_yticklabels(),
                   fontsize= 8)
    ax0.set_ylabel(' ') #creates a space on the right side
    
    ax.legend(fontsize= 9,
              loc= 'upper right')
    
    for val in hrzntl_vals:
        ax.hlines(y=val, color='lightgray',
              xmin= min(yq),
              xmax= max(yq),
              linestyle= 'dotted')
    return ax


def yq_and_ticklabels(df):
    '''
        input a series of str in col yr_qtr of df
        return a list containing 2 lists
        1) a list of str, the entries in yr_qtr
        2) a list of str, the custom x_tick labels for plot
    '''
    yr_qtr = pl.Series(df['yr_qtr']).to_list()
    
    x_tick_labels = \
        [item if item[-1:] == '1' else item[-2:]
         for item in yr_qtr]
    return [yr_qtr, x_tick_labels]