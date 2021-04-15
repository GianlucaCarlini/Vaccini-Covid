# -*- coding: utf-8 -*-
"""
Created on Mon Apr 12 15:00:54 2021

@author: Gianluca
"""

# %% IMPORT

import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.models import Range1d, LinearAxis, HoverTool, ColumnDataSource
from bokeh.models import BoxSelectTool, BoxZoomTool, NumeralTickFormatter
from bokeh.layouts import layout
import datetime

# %% FUNCTION DEFINITIONS

PI = 3.141592

def convert_to_angle(total, x, rad = True):
    angle = (x/total) * 360
    
    if rad:
        angle = angle * (PI/180)
    
    return angle

def moving_average(x):
    avg = []
    for i in range(1, (len(x) - 7)):
        avg.append(np.mean(x[i:i+7]))
    for i in range(len(avg), len(x)):
        avg.append(0)
    return avg

def build_data(pop, df, fascia):
    
    prime_dosi = (df['prima_dose'].loc[df['fascia_anagrafica'] == fascia].sum())
    seconde_dosi = (df['seconda_dose'].loc[df['fascia_anagrafica'] == fascia].sum())
    percentuale_prime = (prime_dosi/pop[fascia]) * 100
    Percentuale_seconde = (seconde_dosi/pop[fascia]) * 100
    
    data = {'Prime Dosi' : [prime_dosi],
            'Seconde Dosi' : [seconde_dosi],
            'Percentuale Prime Dosi' : [percentuale_prime],
            'Percentuale Seconde Dosi' : [Percentuale_seconde]}
    
    return data

def build_annular(data, total, Title):
    
    tooltips = [('Prime Dosi', '@{Prime Dosi}{(0.00 a)}'),
                ('Seconde Dosi', '@{Seconde Dosi}{(0.00 a)}'),
                ('Percentuale Prime Dosi', '@{Percentuale Prime Dosi}{(0.00 a)}'),
                ('Percentuale Seconde Dosi', '@{Percentuale Seconde Dosi}{(0.00 a)}')]
    
    p = figure(title = Title, plot_width = 250, plot_height = 250,
                  x_range = (-1, 1), y_range = (-1, 1),
                  toolbar_location = None)
    p.annular_wedge(x = 0, y = 0, inner_radius = 0.65, outer_radius = 0.8,
                   source = data,
                   start_angle = 0, 
                   end_angle = -convert_to_angle(total, data['Prime Dosi'][0]),
                   direction = 'clock',
                   color = '#F7DE95')

    p.annular_wedge(x = 0, y = 0, inner_radius = 0.65, outer_radius = 0.8,
                   source = data,
                   start_angle = -convert_to_angle(total, 
                                                   data['Prime Dosi'][0]),
                   end_angle = 0,
                   direction = 'clock',
                   color = '#DDDDDD')

    p.annular_wedge(x = 0, y = 0, inner_radius = 0.5, outer_radius = 0.65,
                   source = data,
                   start_angle = 0, 
                   end_angle = -convert_to_angle(total, 
                                                 data['Seconde Dosi'][0]),
                   direction = 'clock',
                   color = '#94CFA0')

    p.annular_wedge(x = 0, y = 0, inner_radius = 0.5, outer_radius = 0.65,
                   source = data,
                   start_angle = -convert_to_angle(total,
                                                   data['Seconde Dosi'][0]),
                   end_angle = 0,
                   direction = 'clock',
                   color = '#DDDDDD')
    
    p.add_tools(HoverTool(tooltips = tooltips))

    p.outline_line_color = None

    p.grid.grid_line_color = None

    p.axis.visible = False
    
    return p
# %% DATA

POP_ITA = 50.773e6 # Over 16
OVER_80 = 4419707

pop_eta = {'90+'   :  791543,
           '80-89' : 3628160,
           '70-79' : 5968373,
           '60-69' : 7364364,
           '50-59' : 9414195,
           '40-49' : 8937229,
           '30-39' : 6854632,
           '20-29' : 6084382
           }

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

media_settimanale = moving_average(vaccini_giornalieri_italia)

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
                         'Seconde_dosi': seconde_dosi,
                         'Media_Mobile' : media_settimanale}


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

fascia_90_piu = build_data(pop_eta, somministrazioni, '90+')
fascia_80_89 = build_data(pop_eta, somministrazioni, '80-89')
fascia_70_79 = build_data(pop_eta, somministrazioni, '70-79')
fascia_60_69 = build_data(pop_eta, somministrazioni, '60-69')
fascia_50_59 = build_data(pop_eta, somministrazioni, '50-59')
fascia_40_49 = build_data(pop_eta, somministrazioni, '40-49')
fascia_30_39 = build_data(pop_eta, somministrazioni, '30-39')
fascia_20_29 = build_data(pop_eta, somministrazioni, '20-29')

# %% VISUALIZATION


somministrazioni_italia_cds = ColumnDataSource(somministrazioni_italia)

totali_italia_cds = ColumnDataSource(data_totali)

"""
Figura 1 - Giornaliere
"""

tooltips1 = [('Giorno', '@Giorno{%F}'),
            ('Somministrazioni Giornaliere', '@Somministrazioni_giornaliere{(0.00 a)}'),
            ('Somministrazioni Totali', '@Totale_somministrazioni{(0.00 a)}'),
            ('Prime Dosi', '@Prime_dosi{(0.00 a)}'),
            ('Seconde Dosi', '@Seconde_dosi{(0.00 a)}'),
            ('Media Mobile Settimanale', '@Media_Mobile{(0.00 a)}')]

formatters = {'@Giorno': 'datetime'}


fig = figure(y_range = (0, 1.1*np.max(vaccini_giornalieri_italia)),
                    title='Somministrazioni Italia', x_axis_label='Data',
                    y_axis_label='Vaccini Giornalieri', x_axis_type='datetime',
                    tools = 'wheel_zoom, reset',
                    toolbar_location = 'above',
                    plot_width = 1000, plot_height = 600)

fig.extra_y_ranges = {'totale': Range1d(start = 0,
                                        end = 1.1*np.max(totale_vaccini_italia))}

fig.vbar(x = 'Giorno', bottom = 0,
         top = 'Prime_dosi',
         source = somministrazioni_italia_cds, 
         legend_label = 'Prime Dosi',
         width = datetime.timedelta(days=0.5),
         color = '#F7DE95')

fig.vbar(x = 'Giorno', bottom = 'Prime_dosi',
         top = 'Somministrazioni_giornaliere',
         source = somministrazioni_italia_cds,
         width = datetime.timedelta(days=0.5),
         legend_label = 'Seconde Dosi',
         color = '#94CFA0')

fig.line(x = 'Giorno', y = 'Totale_somministrazioni',
         source = somministrazioni_italia_cds, 
         y_range_name = 'totale', color = '#93C4D7',
         legend_label = 'Totali', line_width = 3)

fig.line(x = 'Giorno', y = 'Media_Mobile',
         source = somministrazioni_italia_cds,
         color = 'black', legend_label = 'Media Mobile',
         line_width = 2)

fig.add_layout(LinearAxis(y_range_name='totale'), 'right')

fig.add_tools(HoverTool(tooltips = tooltips1, formatters = formatters,
                        mode = 'mouse'))

fig.add_tools(BoxSelectTool(dimensions = 'width'))

fig.add_tools(BoxZoomTool(dimensions = 'width'))

fig.legend.location = 'top_left'

fig.yaxis[0].formatter = NumeralTickFormatter(format="000k")
fig.yaxis[1].formatter = NumeralTickFormatter(format="0 a")
fig.yaxis[1].axis_label = 'Vaccini Totali'

"""
Figura 2 - Totale Italia
"""

tooltips2 = [('Prime Dosi', '@Totale_prime_dosi{(0.00 a)}'),
             ('Seconde Dosi', '@Totale_immunizzati{(0.00 a)}'),
             ('Percentuale prime dosi', '@Percentuale_prime_dosi{(0.00 a)}'),
             ('Percentuale Seconde Dosi', '@Percentuale_immunizzati{(0.00 a)}')]

fig2 = figure(title = 'Totale Italia', plot_width = 550, plot_height = 550,
              x_range = (-1, 1), y_range = (-1, 1),
              tools = 'wheel_zoom',
              toolbar_location = None)
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

tooltips3 = [('Regione', '@Regioni'), ('Prime dosi', '@{Prime dosi}{(0.00 a)}'),
            ('Seconde dosi', '@{Seconde dosi}{(0.00 a)}')]

fig3 = figure(x_range = Regioni, title = 'Somministrazioni Regioni',
              plot_width = 1000, plot_height = 600,
              toolbar_location = None)

fig3.vbar_stack(Legenda, x = 'Regioni', width = 0.9, color = colori,
                source = Dati_regioni, legend_label = Legenda)

fig3.xaxis.major_label_orientation = 1

fig3.add_tools(HoverTool(tooltips=tooltips3))

fig3.yaxis[0].formatter = NumeralTickFormatter(format="0.0a")
fig3.yaxis[0].axis_label = 'Vaccini Totali'

"""
Figura 4 - Over 80
"""

fig4 = build_annular(fascia_80_89, pop_eta['80-89'], '80 - 89 Anni')
fig5 = build_annular(fascia_70_79, pop_eta['70-79'], '70 - 79 Anni')
fig6 = build_annular(fascia_60_69, pop_eta['60-69'], '60 - 69 Anni')
fig7 = build_annular(fascia_50_59, pop_eta['50-59'], '50 - 59 Anni')
fig8 = build_annular(fascia_40_49, pop_eta['40-49'], '40 - 49 Anni')
fig9 = build_annular(fascia_30_39, pop_eta['30-39'], '30 - 39 Anni')
fig10 = build_annular(fascia_20_29, pop_eta['20-29'], '20 - 29 Anni')
fig11 = build_annular(fascia_90_piu, pop_eta['90+'],  '90+ Anni')


lay = layout([[fig, fig2], [fig11, fig4, fig5, fig6], [fig7, fig8, fig9, fig10],
              [fig3]])

show(lay)
