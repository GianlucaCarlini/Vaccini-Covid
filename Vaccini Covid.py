# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:00:54 2021

@author: Gianluca
"""

"""
COVID VACCINI
"""

# %% IMPORT

import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import Range1d, LinearAxis, HoverTool, ColumnDataSource
from bokeh.models import BoxSelectTool, BoxZoomTool, WheelZoomTool
from bokeh.layouts import row, column, gridplot

# %% FUNCTION DEFINITIONS

PI = 3.141592

def convert_to_angle(total, x, rad = True):
    angle = (x/total) * 360
    
    if rad:
        angle = angle * (PI/180)
    
    return angle

#def build_data(list_range, df, total):
    

# %% DATA

POP_ITA = 50.773e6 # Over 16
OVER_80 = 4419707

url_vaccini_summary = "https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/vaccini-summary-latest.csv"
url_somministrazioni_summary = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-summary-latest.csv'
url_somministrazioni = 'https://raw.githubusercontent.com/italia/covid19-opendata-vaccini/master/dati/somministrazioni-vaccini-latest.csv'
vaccini_summary = pd.read_csv(url_vaccini_summary)

somministrazioni_summary = pd.read_csv(url_somministrazioni_summary)

somministrazioni = pd.read_csv(url_somministrazioni)

somministrazioni_sorted = somministrazioni_summary.sort_values(by='data_somministrazione',
                                                               ascending=False)

somministrazioni_sorted.reset_index(inplace=True, drop=True)

somministrazioni_sorted.set_index(['data_somministrazione'], inplace=True)

giorni = somministrazioni_sorted.index.unique()

"""
Vaccini giornalieri
"""

vaccini_giornalieri_italia = []

for i in giorni:
    vaccini_giornalieri_italia.append(somministrazioni_sorted['totale'].loc[i].sum())

vaccini_giornalieri_italia = np.array(vaccini_giornalieri_italia)

"""
Prime dosi
"""

prime_dosi = []

for i in giorni:
    prime_dosi.append(somministrazioni_sorted['prima_dose'].loc[i].sum())
    
prime_dosi = np.array(prime_dosi)


"""
Seconde dosi
"""

seconde_dosi = []

for i in giorni:
    seconde_dosi.append(somministrazioni_sorted['seconda_dose'].loc[i].sum())

seconde_dosi = np.array(seconde_dosi)    

"""
Totale
"""

totale_vaccini_italia = []

for i in range(len(vaccini_giornalieri_italia)):
    totale_vaccini_italia.append(np.sum(vaccini_giornalieri_italia[i:]))

totale_vaccini_italia = np.array(totale_vaccini_italia)

totale_prime_dosi = np.sum(prime_dosi)
immunizzati = np.sum(seconde_dosi)

percentuale_prime_dosi = (totale_prime_dosi/POP_ITA) * 100
percentuale_immunizzati = (immunizzati/POP_ITA) * 100

data_somministrazioni = {'Giorno': pd.to_datetime(giorni),
                         'Totale_somministrazioni': totale_vaccini_italia,
                         'Somministrazioni_giornaliere': vaccini_giornalieri_italia,
                         'Prime_dosi': prime_dosi,
                         'Seconde_dosi': seconde_dosi,}


data_totali = {'Totale_prime_dosi' : [totale_prime_dosi],
               'Totale_immunizzati' : [immunizzati],
               'Percentuale_prime_dosi': [percentuale_prime_dosi],
               'Percentuale_immunizzati': [percentuale_immunizzati]}

somministrazioni_italia = pd.DataFrame(data_somministrazioni)


"""
Regioni
"""

Regioni = list(somministrazioni_summary['nome_area'].unique())

Prime_dosi_regioni = []
Seconde_dosi_regioni = []
Totale_regioni = []

for i in Regioni:
    Prime_dosi_regioni.append(somministrazioni_summary['prima_dose'].loc[somministrazioni_summary['nome_area'] == i].sum())
    Seconde_dosi_regioni.append(somministrazioni_summary['seconda_dose'].loc[somministrazioni_summary['nome_area'] == i].sum())
    Totale_regioni.append(somministrazioni_summary['totale'].loc[somministrazioni_summary['nome_area'] == i].sum())

Dati_regioni = {'Regioni' : Regioni,
                'Prime dosi' : Prime_dosi_regioni,
                'Seconde dosi' : Seconde_dosi_regioni}

Legenda = ['Prime dosi', 'Seconde dosi']

colori = ['#F7DE95', '#94CFA0']

"""
Categorie
"""

Prime_Dosi_Over_80 = (somministrazioni['prima_dose'].loc[somministrazioni['fascia_anagrafica'] == '80-89'].sum() + 
                      somministrazioni['prima_dose'].loc[somministrazioni['fascia_anagrafica'] == '90+'].sum())

Seconde_Dosi_Over_80 = (somministrazioni['seconda_dose'].loc[somministrazioni['fascia_anagrafica'] == '80-89'].sum() +
                        somministrazioni['seconda_dose'].loc[somministrazioni['fascia_anagrafica'] == '90+'].sum())

Percentuale_prime_80 = (Prime_Dosi_Over_80 / OVER_80) * 100
Percentuale_seconde_80 = (Seconde_Dosi_Over_80 / OVER_80) * 100 

Over_80 = {'Prime Dosi' : [Prime_Dosi_Over_80],
           'Seconde Dosi' : [Seconde_Dosi_Over_80],
           'Percentuale Prime' : [Percentuale_prime_80],
           'Percentuale Seconde' : [Percentuale_seconde_80]} 



Prime_Dosi_70 = (somministrazioni['prima_dose'].loc[somministrazioni['fascia_anagrafica'] == '80-89'].sum() + 
                 somministrazioni['prima_dose'].loc[somministrazioni['fascia_anagrafica'] == '90+'].sum())

Seconde_Dosi_Over_70 = (somministrazioni['seconda_dose'].loc[somministrazioni['fascia_anagrafica'] == '80-89'].sum() +
                        somministrazioni['seconda_dose'].loc[somministrazioni['fascia_anagrafica'] == '90+'].sum())

Percentuale_prime_70 = (Prime_Dosi_Over_80 / OVER_80) * 100
Percentuale_seconde_70 = (Seconde_Dosi_Over_80 / OVER_80) * 100 

Over_70 = {'Prime Dosi' : [Prime_Dosi_Over_80],
           'Seconde Dosi' : [Seconde_Dosi_Over_80],
           'Percentuale Prime' : [Percentuale_prime_80],
           'Percentuale Seconde' : [Percentuale_seconde_80]} 
# %% VISUALIZATION


somministrazioni_italia_cds = ColumnDataSource(somministrazioni_italia)

totali_italia_cds = ColumnDataSource(data_totali)

"""
Figura 1 - Giornaliere
"""

tooltips1 = [('Giorno', '@Giorno{%F}'),
            ('Somministrazioni Giornaliere', '@Somministrazioni_giornaliere'),
            ('Somministrazioni Totali', '@Totale_somministrazioni'),
            ('Prime Dosi', '@Prime_dosi'),
            ('Seconde Dosi', '@Seconde_dosi')]

formatters = {'@Giorno': 'datetime'}


fig = figure(y_range = (0, 1.1*np.max(vaccini_giornalieri_italia)),
                    title='Somministrazioni Italia', x_axis_label='Data',
                    y_axis_label='Numero Vaccini', x_axis_type='datetime',
                    tools = 'wheel_zoom, reset',
                    plot_width = 1000, plot_height = 600)

fig.extra_y_ranges = {'totale': Range1d(start = 0,
                                        end = 1.1*np.max(totale_vaccini_italia))}

fig.vbar(x = 'Giorno', bottom = 0,
         top = 'Prime_dosi',
         source = somministrazioni_italia_cds, 
         legend_label = 'Prime Dosi',
         color = '#EFB90A')

fig.vbar(x = 'Giorno', bottom = 'Prime_dosi',
         top = 'Somministrazioni_giornaliere',
         source = somministrazioni_italia_cds,
         legend_label = 'Seconde Dosi',
         color = 'Green')

fig.line(x = 'Giorno', y = 'Totale_somministrazioni',
         source = somministrazioni_italia_cds, 
         y_range_name = 'totale', color = '#93C4D7',
         legend_label = 'Totali', line_width = 2)

fig.add_layout(LinearAxis(y_range_name='totale'), 'right')

fig.add_tools(HoverTool(tooltips = tooltips1, formatters = formatters,
                        mode = 'vline'))

fig.add_tools(BoxSelectTool(dimensions = 'width'))

fig.add_tools(BoxZoomTool(dimensions = 'width'))

fig.legend.location = 'top_left'

"""
Figura 2 - Totale Italia
"""

tooltips2 = [('Prime Dosi', '@Totale_prime_dosi'),
             ('Immunizzati', '@Totale_immunizzati'),
             ('Percentuale prime dosi', '@Percentuale_prime_dosi'),
             ('Percentuale immunizzati', '@Percentuale_immunizzati')]

fig2 = figure(plot_width = 400, plot_height = 400,
              x_range = (-1, 1), y_range = (-1, 1),
              tools = 'wheel_zoom')
fig2.axis.visible = False

fig2.annular_wedge(x = 0, y = 0, inner_radius = 0.65, outer_radius = 0.8,
                   source = totali_italia_cds,
                   start_angle = 0, 
                   end_angle = -convert_to_angle(POP_ITA, totale_prime_dosi),
                   direction = 'clock',
                   color = '#F7DE95')

fig2.annular_wedge(x = 0, y = 0, inner_radius = 0.65, outer_radius = 0.8,
                   source = totali_italia_cds,
                   start_angle = -convert_to_angle(POP_ITA, 
                                                   totale_prime_dosi),
                   end_angle = 0,
                   direction = 'clock',
                   color = '#DDDDDD')

fig2.annular_wedge(x = 0, y = 0, inner_radius = 0.5, outer_radius = 0.65,
                   source = totali_italia_cds,
                   start_angle = 0, 
                   end_angle = -convert_to_angle(POP_ITA, immunizzati),
                   direction = 'clock',
                   color = '#94CFA0')

fig2.annular_wedge(x = 0, y = 0, inner_radius = 0.5, outer_radius = 0.65,
                   source = totali_italia_cds,
                   start_angle = -convert_to_angle(POP_ITA, immunizzati),
                   end_angle = 0,
                   direction = 'clock',
                   color = '#DDDDDD')

fig2.add_tools(HoverTool(tooltips = tooltips2))

fig2.outline_line_color = None

fig2.grid.grid_line_color = None

"""
Figura 3 - Regioni
"""

tooltips3 = [('Regione', '@Regioni'), ('Prime dosi', '@{Prime dosi}'),
            ('Seconde dosi', '@{Seconde dosi}')]

fig3 = figure(x_range = Regioni, title = 'Somministrazioni Regioni',
              plot_width = 1000, plot_height = 600,
              toolbar_location = None)

fig3.vbar_stack(Legenda, x = 'Regioni', width = 0.9, color = colori,
                source = Dati_regioni, legend_label = Legenda)

fig3.xaxis.major_label_orientation = 1

fig3.add_tools(HoverTool(tooltips=tooltips3))


"""
Figura 4 - Over 80
"""

tooltips4 = [('Prime Dosi', '@{Prime Dosi}'),
             ('Seconde Dosi', '@{Seconde Dosi}'),
             ('Percentuale Prime Dosi', '@{Percentuale Prime}'),
             ('Percentuale Seconde Dosi', '@{Percentuale Seconde}')]

fig4 = figure(title = 'Over 80', plot_width = 250, plot_height = 250,
              x_range = (-1, 1), y_range = (-1, 1),
              toolbar_location = None)

fig4.annular_wedge(x = 0, y = 0, inner_radius = 0.65, outer_radius = 0.8,
                   source = Over_80,
                   start_angle = 0, 
                   end_angle = -convert_to_angle(OVER_80, Prime_Dosi_Over_80),
                   direction = 'clock',
                   color = '#F7DE95')

fig4.annular_wedge(x = 0, y = 0, inner_radius = 0.65, outer_radius = 0.8,
                   source = Over_80,
                   start_angle = -convert_to_angle(OVER_80, 
                                                   Prime_Dosi_Over_80),
                   end_angle = 0,
                   direction = 'clock',
                   color = '#DDDDDD')

fig4.annular_wedge(x = 0, y = 0, inner_radius = 0.5, outer_radius = 0.65,
                   source = Over_80,
                   start_angle = 0, 
                   end_angle = -convert_to_angle(OVER_80, Seconde_Dosi_Over_80),
                   direction = 'clock',
                   color = '#94CFA0')

fig4.annular_wedge(x = 0, y = 0, inner_radius = 0.5, outer_radius = 0.65,
                   source = Over_80,
                   start_angle = -convert_to_angle(OVER_80, Seconde_Dosi_Over_80),
                   end_angle = 0,
                   direction = 'clock',
                   color = '#DDDDDD')

fig4.add_tools(HoverTool(tooltips = tooltips4))

fig4.outline_line_color = None

fig4.grid.grid_line_color = None

fig4.axis.visible = False

grid = gridplot([[fig, fig2], [fig3, fig4]])

show(grid)
