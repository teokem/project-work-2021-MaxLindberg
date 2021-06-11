def ratio_maker2(input_data,n14_peaks,n15_peaks,fault_tolerance):   #for ratios of all isotope peaks summed.
    import pandas as pd
    n14=n14_peaks
    n15=n15_peaks
    values=[] # this list will gather all calculated ratios as the for loop below works through the sheets in the input data.
    index_list=[] # this will simultanously as the above gather well name and peak number to keep track on what ratios belong to what.
    all_N14 = {} # this collects all isotope peaks used for the sums (and by extension the ratios)
    all_N15 = {} # same as above 
    for x in input_data.keys():        
        df=input_data[x] # define the current dataframe as df for convenience 
        for i in range(len(n14)):
            tmp = df.loc[((df["m/z"]>(n14[i]-fault_tolerance)) & (df["m/z"]<(n14[i]+fault_tolerance)) |
               (df["m/z"]>(n15[i]-fault_tolerance)) & (df["m/z"]<(n15[i]+fault_tolerance))), ] 
            #makes a dataframe with only the peaks from masslist.xlsx that are within the fault tolerance from the theoretical cleavage peaks
            if len(tmp) > 2:
                tmp=tmp.sort_values('SN',ascending=False).iloc[0:2]
                # sometimes there is extra peaks very close to the ones of interest so this hopefully removes them
                # by only keeping the 2 with highest signal to noise ratio 
            if len(tmp) == 2:
                n14_isotopes= []
                # If tmp is exactly 2 rows long then we should only have the main N14 and N15 peak           
                n14_isotopes.append(df.loc[((df["m/z"]>(n14[i]-fault_tolerance)) & (df["m/z"]<(n14[i]+fault_tolerance))),])
                # we then add the peak that are 1 +- 0.1 Da heavier then the main N14 peak and then the one 1 Da heavier then that one and so on 
                # until there is no more peaks that are 1 +- 0.1 Da heavier. This collects all the isotope peaks to the right of the main peak. 
                a=1
                while (not df.loc[((df["m/z"]>(tmp.iloc[0]['m/z']+a-0.1)) & (df["m/z"]<(tmp.iloc[0]['m/z']+a+0.1))),].empty):
                    n14_isotopes.append(df.loc[((df["m/z"]>(tmp.iloc[0]['m/z']+a-0.1)) & (df["m/z"]<(tmp.iloc[0]['m/z']+a+0.1))),])
                    a+=1 
                # we then do the same in the other direction
                a=1
                while (not df.loc[((df["m/z"]>(tmp.iloc[0]['m/z']-a-0.1)) & (df["m/z"]<(tmp.iloc[0]['m/z']-a+0.1))),].empty):
                    n14_isotopes.append(df.loc[((df["m/z"]>(tmp.iloc[0]['m/z']-a-0.1)) & (df["m/z"]<(tmp.iloc[0]['m/z']-a+0.1))),])
                    a+=1
                # if we found any isotope peaks we concatenate them into one dataframe
                if len(n14_isotopes)>1:
                    df_14=pd.concat(n14_isotopes)
                # otherwise we just use the main peak initially found
                else:
                    df_14=n14_isotopes[0]
                # then we do the same for N15
                n15_isotopes= []
                n15_isotopes.append(df.loc[((df["m/z"]>(n15[i]-fault_tolerance)) & (df["m/z"]<(n15[i]+fault_tolerance))),])
                a=1
                while (not df.loc[((df["m/z"]>(tmp.iloc[1]['m/z']+a-0.1)) & (df["m/z"]<(tmp.iloc[1]['m/z']+a+0.1))),].empty):
                    n15_isotopes.append(df.loc[((df["m/z"]>(tmp.iloc[1]['m/z']+a-0.1)) & (df["m/z"]<(tmp.iloc[1]['m/z']+a+0.1))),])
                    a+=1 
                a=1
                while (not df.loc[((df["m/z"]>(tmp.iloc[1]['m/z']-a-0.1)) & (df["m/z"]<(tmp.iloc[1]['m/z']-a+0.1))),].empty):
                    n15_isotopes.append(df.loc[((df["m/z"]>(tmp.iloc[1]['m/z']-a-0.1)) & (df["m/z"]<(tmp.iloc[1]['m/z']-a+0.1))),])
                    a+=1
                if len(n15_isotopes)>1:
                    df_15=pd.concat(n15_isotopes) 
                else:
                    df_15=n15_isotopes[0]
                # then we sum all the intensities of the N14 peaks and divide that by the sum of the N15 peaks. These ratios are collected in the list "values"
                values.append((df_14['Intens.'].sum()/df_15['Intens.'].sum()))
                # we then add what well number and peak we are currently at.
                index_list.append((x.split("_")[-2],str(n14[i]).split('.')[0]))
                # the two lines below here fill up a dictionary each with all collected isotope peaks and their signal to noise, intensities and so on.
                # for the possibility to inspect what was done.
                all_N14[index_list[-1]]=df_14
                all_N15[index_list[-1]]=df_15
    # we then make a dataframe of the ratios
    data = pd.DataFrame({'Ratio':values})
    # give it a reasonable index
    data.index=pd.MultiIndex.from_tuples(index_list, names=["Well","peak"])
    # and return it all
    return data,all_N14,all_N15