import numpy, pandas, matplotlib.pyplot, seaborn   # import libraries ->numpy, pandas, matplotlib.pyplot, seaborn
# numpy will be used for linear algebra
# pandas  will be used for data reading and initila analysis and also for soime kind of visualization from dataframe
# matplotlib  will be used for data visualization
# seaborn will be used to show correlation chart (heatmap)
# Country Selection
cnset=["Afghanistan", "Brazil", "China", "United Kingdom", "Russian Federation", "India", "Sudan"]
# Inducator Selection
indwb=["Urban population (% of total population)", "Electric power consumption (kWh per capita)"]

def corprep_df(ppel):    # function data preparation for indicator correlation
    ppelcols=ppel.columns    # columns of data (whcih will be converted tom numeric)
    ppelidx=ppel.index      # data frame indices
    ppelarr=numpy.array(ppel.values,int)    # transform to numeric
    ppel=pandas.DataFrame(ppelarr,columns=ppelcols,index=ppelidx)    # Prepare dataframe
    return ppel    # return data
def read_data(popelt): # reading data
    # assigning parameters for read_csv for data reading
    readeng, skipping='python', 3
    popel=pandas.read_csv(popelt,engine=readeng,skiprows=skipping)    # read csv data
    popel=popel.fillna(popel.mean())    # Clean missing values of the data
    years=popel.columns.tolist()[4:-1]    # get the columns for years
    popel=popel[(popel['Indicator Name']==indwb[0])|((popel['Indicator Name']==indwb[1]))]    # data preaparion by indicators
    fltr=popel['Country Name'].isin(cnset)    # check is the countries available in the taken data and if yes, take all records of those countries
    popel=popel[fltr]     # craete the data by subsetting the filter
    cntr=popel['Country Name'].tolist()     # get Country Names
    indx=popel['Indicator Name'].tolist()     # get Indicator Names
    nw=[]
    for i in range(len(indx)):
        nw.append(cntr[i])    # craeting new column by conbining country and indicator
    popel.insert(4,"Countries",nw)    # insertion of new feature into data
    ppelnw=popel.T.iloc[4:][:-1]    # transpose the data read from 4th rows and upto the last but one column
    drops=['Unnamed: 65','Country Code','Indicator Code','Countries']
    # drop features which are not required
    popel=popel.reset_index(drop=True).drop(drops,axis=1)
    ppelnw.columns=ppelnw.iloc[0]    # assign column names by taking 0th row
    ppelnw=ppelnw.iloc[1:]      # assign data from the first row
    ppelnw['Year']=years    # assign year into data
    ppelnw=ppelnw.set_index("Year")    # set year feature to index
    return popel,ppelnw  
df,df1=read_data("API_19_DS2_en_csv_v2_3931355.csv")
df=df.drop('Indicator Name',axis=1)
df.head()   # Data with Year Column
df1.head()   # Data with country column
print(df.describe())    # shwo data statistics
print(df.info())    # show data information
print("Data Statistics for Electric power consumption")
print(df1.loc[:,df1.columns.duplicated()].describe().T )       # show data statistics 
print("Data Statistics for Urban Population")
print(df1.loc[:,~df1.columns.duplicated()].describe().T)        # show data statistics 
print(df1.info())    # show data information
df1.loc[:,df1.columns.duplicated()].kurtosis().plot(kind='barh',title="Analysis of Outliers using Kurtoris for Urban population", figsize=(7,4))
matplotlib.pyplot.show()
df1.loc[:,~df1.columns.duplicated()].kurtosis().plot(kind='barh',title="Analysis of Outliers using Kurtoris for Urban population Electric power consumption", figsize=(7,4))
matplotlib.pyplot.show()
df1.loc[:,df1.columns.duplicated()].skew().plot(kind='barh',title="Analysis of Skewness (Data Distribution) for Urban population", figsize=(7,4))
matplotlib.pyplot.show()
df1.loc[:,~df1.columns.duplicated()].skew().plot(kind='barh',title="Analysis of Skewness (Data Distribution) for Electric power consumption", figsize=(7,4))
matplotlib.pyplot.show()
# # Data Analysis
def TSGraph(dtpe,ft1,ft2):    # for displayimng time series chart
    dtpex = dtpe.loc[:,~dtpe.columns.duplicated()].copy()     # create data for Urban population
    dtpex.plot(kind='line',figsize=(8,4)) # create graph
    matplotlib.pyplot.title("{} by Year".format(ft1),fontsize=20,color="b")     # graph title  
    matplotlib.pyplot.xlabel("{}".format(ft1),fontsize=20,color="b")   # graph label (x-axis)
    matplotlib.pyplot.ylabel("Value",fontsize=20,color="b")   # graph label (x-axis)
    matplotlib.pyplot.grid()      # Graph grid
    matplotlib.pyplot.show()      # display bar chart
    
    dtpex = dtpe.loc[:,dtpe.columns.duplicated()].copy()       # create data for Electric power consumption
    dtpex.plot(kind='line',figsize=(8,4)) # create graph
    matplotlib.pyplot.title("{} by Year".format(ft2),fontsize=20,color="b")     # graph title 
    matplotlib.pyplot.xlabel("{}".format(ft2),fontsize=20,color="b")   # graph label (x-axis)
    matplotlib.pyplot.ylabel("Value",fontsize=20,color="b")   # graph label (x-axis)
    matplotlib.pyplot.grid()      # Graph grid
    matplotlib.pyplot.show()      # display bar chart
TSGraph(df1,"Urban population","Electric power consumption")
def calc_stat(dtpl,st,flst):
    valueup,valueep=[],[]
    for i in range(len(cnset)):
        dtpl_t=dtpl[dtpl['Country Name']==cnset[i]]    # prepare data by country
        if st=="Minimum":   # if the variable st if Minimum
            valueup.append(round(dtpl_t.iloc[0,1:].min(),2))    # calculate statsitical value for Urban population
            valueep.append(round(dtpl_t.iloc[1,1:].min(),2))    # calculate statsitical value for Electric power consumption
        elif st=="Average":   # if the variable st if Average
            valueup.append(round(dtpl_t.iloc[0,1:].mean(),2))    # calculate statsitical value for Urban population
            valueep.append(round(dtpl_t.iloc[1,1:].mean(),2))
        elif st=="Maximum":   # if the variable st is Maximum
            valueup.append(round(dtpl_t.iloc[0,1:].max(),2))    # calculate statsitical value for Urban population
            valueep.append(round(dtpl_t.iloc[1,1:].max(),2))
    flst[0].append(valueup)
    flst[1].append(valueep)
    return allst
allst=[[],[]]   # to store all statsitics (Minimum ,Average ,Maximum )
allst=calc_stat(df,"Average",allst)
allst=calc_stat(df,"Minimum",allst)
allst=calc_stat(df,"Maximum",allst)
data_df=pandas.DataFrame({
    "Country":cnset,
    "Urban population(Average)":allst[0][0],
    "Electric power consumption(Average)":allst[1][0],
    "Urban population(Minimum)":allst[0][0],
    "Electric power consumption(Minimum)":allst[1][0],
    "Urban population(Maximum)":allst[0][0],
    "Electric power consumption(Maximum)":allst[1][0]
})    # prepare dataframe with average, minimum and maximum values
data_df=data_df.set_index("Country")   # put country column to index
print(data_df)
def barchrt(dt,ftpt,ttl_plot):
    dt[ftpt].sort_values().plot(kind="barh",color=["g","y","deeppink"],figsize=(8,4)) # create graph
    matplotlib.pyplot.title("{}".format(ttl_plot),fontsize=18,color="k")     # graph title  
    matplotlib.pyplot.xlabel("Country",fontsize=14,color="k")   # graph label (x-axis)
    matplotlib.pyplot.ylabel("{}".format(ftpt),fontsize=14,color="k")   # graph label (x-axis)
    matplotlib.pyplot.grid()      # graph Grid
    matplotlib.pyplot.show()      # display bar chart
cls=data_df.columns.tolist()
uc=[0,2,4]    # take indices for columns concerning Urban population
ec=[1,3,5]    # take indices for columns concerning Electric power consumption
ucol=[cls[i] for i in uc]    # prepare list of columns as taken the indices earlier
ecol=[cls[i] for i in ec]    # prepare list of columns as taken the indices earlier
for x in range(len(ucol)):   # create loop wheer in each loop the barchart fucntion will be called
    barchrt(data_df,ucol[x],"{} Urban population by Country".format(ucol[x].split("(")[1][:-1]))
    barchrt(data_df,ecol[x],"{} Electric power consumption by Country".format(ucol[x].split("(")[1][:-1]))
df2=corprep_df(df1)
matplotlib.pyplot.figure(figsize=(13,7))    # set figure size
matplotlib.pyplot.title("Correlation Outcome",fontsize=20,color="m")     # set title
seaborn.heatmap(df2.corr(),annot=True,fmt="0.3f",cmap="plasma")    # show correlation outcomes through heatmap
matplotlib.pyplot.show()    # show heatmap