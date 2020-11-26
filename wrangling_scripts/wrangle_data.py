import pandas as pd
import plotly.graph_objs as go


def cleandata(dataset, keepcolumns = ['Country Name', '1990','1995','2000' ,'2015'], value_variables = ['1990', '1995','2000','2015']):
    """Clean world bank data for a visualizaiton dashboard

    Keeps data range of dates in keep_columns variable and data for the top 10 economies
    Reorients the columns into a year, country and value
    Saves the results to a csv file

    Args:
        dataset (str): name of the csv data file

    Returns:
        None

    """    
    df = pd.read_csv(dataset, skiprows=4)

    # Keep only the columns of interest (years and country name)
    df = df[keepcolumns]

    top10country = ['United States', 'China', 'Japan', 'Germany', 'United Kingdom', 'India', 'France', 'Brazil', 'Italy', 'Canada']
    df = df[df['Country Name'].isin(top10country)]

    # melt year columns  and convert year to date time
    df_melt = df.melt(id_vars='Country Name', value_vars = value_variables)
    df_melt.columns = ['country','year', 'variable']
    df_melt['year'] = df_melt['year'].astype('datetime64[ns]').dt.year

    # output clean csv file
    return df_melt

def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """

  # first chart plots arable land from 1990 to 2015 in top 10 economies 
  # as a line chart
    
    graph_one = []
    df = cleandata('data/WB_GDP_per_capita.csv', \
      keepcolumns = [ 'Country Name' ,'1990',   '1991',   '1992',   '1993',   '1994',   '1995',   '1996',   '1997',   '1998',   '1999',   '2000',   '2001',   '2002',   '2003',   '2004',   '2005',   '2006',   '2007',   '2008',   '2009',   '2010',   '2011',   '2012',   '2013',   '2014'],\
     value_variables = [ '1990',   '1991',   '1992',   '1993',   '1994',   '1995',   '1996',   '1997',   '1998',   '1999',   '2000',   '2001',   '2002',   '2003',   '2004',   '2005',   '2006',   '2007',   '2008',   '2009',   '2010',   '2011',   '2012',   '2013',   '2014'] ) # WB_GDP_per_capita API_AG.LND.ARBL.HA.PC_DS2_en_csv_v2
    df.columns = ['country','year','gdp']
    df.sort_values('year', ascending=False, inplace=True)
    countrylist = df.country.unique().tolist()
    
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].gdp.tolist()
      graph_one.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_one = dict(title = 'Change in GDP per capita <br> b/w 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'GDP'),
                )

# second chart plots ararble land for 2015 as a bar chart    
    graph_two = []
    df = cleandata('data/WB_Labor_force.csv')
    df.columns = ['country','year','laborforce']
    df.sort_values('laborforce', ascending=False, inplace=True)
    df = df[df['year'] == 2015] 

    graph_two.append(
      go.Bar(
      x = df.country.tolist(),
      y = df.laborforce.tolist(),
      )
    )

    layout_two = dict(title = 'Total Labor force in 2015',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = 'Total Labor Force'),
                )


# third chart plots percent of population that is rural from 1990 to 2015
    graph_three = []
    df = cleandata('data/WB_Elec_Pwr_cnsmp.csv', \
      keepcolumns = [ 'Country Name' ,'1990',   '1991',   '1992',   '1993',   '1994',   '1995',   '1996',   '1997',   '1998',   '1999',   '2000',   '2001',   '2002',   '2003',   '2004',   '2005',   '2006',   '2007',   '2008',   '2009',   '2010',   '2011',   '2012',   '2013',   '2014'],\
     value_variables = [ '1990',   '1991',   '1992',   '1993',   '1994',   '1995',   '1996',   '1997',   '1998',   '1999',   '2000',   '2001',   '2002',   '2003',   '2004',   '2005',   '2006',   '2007',   '2008',   '2009',   '2010',   '2011',   '2012',   '2013',   '2014'] )
    df.columns = ['country', 'year', 'elec']
    df.sort_values('year', ascending=False, inplace=True)
    for country in countrylist:
      x_val = df[df['country'] == country].year.tolist()
      y_val =  df[df['country'] == country].elec.tolist()
      graph_three.append(
          go.Scatter(
          x = x_val,
          y = y_val,
          mode = 'lines',
          name = country
          )
      )

    layout_three = dict(title = 'Change in Electricity Consumption <br> from 1990 to 2015',
                xaxis = dict(title = 'Year',
                  autotick=False, tick0=1990, dtick=25),
                yaxis = dict(title = 'Electricity Consumption'),
                )
    
# fourth chart shows rural population vs arable land
    graph_four = []
    
    valuevariables = [str(x) for x in range(1995, 2016)]
    keepcolumns = [str(x) for x in range(1995, 2016)]
    keepcolumns.insert(0, 'Country Name')

    df_one = cleandata('data/WB_GDP_per_capita.csv', keepcolumns = ['Country Name', '2010'], value_variables=['2010'])
    df_two = cleandata('data/WB_Labor_force.csv', keepcolumns = ['Country Name', '2010'], value_variables=['2010'])
    df_three = cleandata('data/WB_Elec_Pwr_cnsmp.csv', keepcolumns = ['Country Name', '2010'], value_variables=['2010'])
    
    df_one.columns = ['country', 'year', 'variable']
    df_two.columns = ['country', 'year', 'variable']
    df_three.columns = ['country', 'year', 'variable']
    
    df = df_one.merge(df_two, on=['country', 'year'])
    df = df.merge(df_three, on=['country', 'year'])

    for country in countrylist:
      x_val = df[df['country'] == country].variable_x.tolist()
      y_val = df[df['country'] == country].variable_y.tolist()
      z_val = df[df['country'] == country].variable.tolist()
      year = df[df['country'] == country].year.tolist()
      country_label = df[df['country'] == country].country.tolist()

      text = []
      for country, year in zip(country_label, year):
          text.append(str(country) + ' ' + str(year))

      graph_four.append(
          go.Scatter3d(
          x = x_val,
          y = y_val,
          z = z_val,
          text = text,
          name = country,
          textposition = 'top left'
          )
      )

    layout_four = dict(title = 'GDP vs Labor Force Vs <br> Electricity Consumption',
                xaxis = dict(xaxis_title = 'Rural Population'),
                yaxis = dict(title = 'Forest Area (square km)'),
                xaxis_title='X AXIS TITLE'
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))
    
    return figures