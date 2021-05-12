import matplotlib.pyplot as plt 
import numpy as np
comp_plot = def comp_plot(data,subplots_number,subplots_names,x_axis,title,y_axis):
    #plt.rcParams["figure.figsize"] = (3.5,7.2)
    
    fig = plt.figure(constrained_layout=True)
    ax_array = fig.subplots(subplots_number,1)
    fig.suptitle(title)
    for i in range(subplots_number):
         data.filter(like=subplots_names[i],axis=0).groupby([x_axis]).mean().plot(kind='bar',
                     logy=False,yerr=data.filter(like=subplots_names[0],axis=0).groupby([x_axis]).sem(),
                     legend=False, ax=ax_array[i], figsize=(10,10), 
                     title=subplots_names[i], sharex=True, ylabel=y_axis, 
                     color='darkred'
                     )
    plist = []
    tips = data.groupby([x_axis]).mean().index
    N = len(tips)
    ind = np.arange(N)    # the x locations for the groups
    width = 0.5 
    for x in subplots_names:
        conc=data.filter(like=x,axis=0).groupby([x_axis]).mean().Ratio
        sems=data.filter(like=x,axis=0).groupby([x_axis]).sem().Ratio
        plist.append(ax.bar(ind, conc, width, yerr=sems))
    for i in range(subplots_number):
        ax_array[i].bar_label(plist[i],fmt='%.2f',label_type='center')
    
    plt.show()