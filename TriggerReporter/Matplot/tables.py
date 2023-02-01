from datetime import datetime
import math
import numpy as np
from matplotlib.backends.backend_pdf import PdfPages
import matplotlib.pyplot as plt


class MonitoringResultsTable:
    RESULTS_TYPE = ''
    COLUMN_HEADERS = ['Point ID', 'Date:Time', 'Convergence(mm)']
    ARRAYS_PER_ROW = 1
    ARRAYS_PER_PAGE = 4
    def __init__(self, report_data):
        self.report_data = report_data
        self.title_text = self.report_data.heading.site.name.title()
        self.header_text = f'Surveyor: {self.report_data.surveyor.title()}'
        self.fig_border = 'black'
        self.report_date = datetime.strftime(report_data.get_latest_date().date(),'%d %B %Y')

        with PdfPages(f'{self.report_data.heading.site.name}_{self.report_data.heading.name}_{self.report_date}_{self.RESULTS_TYPE}.pdf') as self.pdf:
            self.plt_setup()
            index = 0
            for num, array_data in enumerate(self.report_data.array_data):
                index += 1 
                if num != 0 and num % self.ARRAYS_PER_PAGE == 0:
                    #new page
                    index = 1
                    self.plt_save_close()
                    self.plt_setup()      
                self.create_table(array_data, index)
            self.plt_save_close()

    def plt_save_close(self):
        plt.draw()
        fig = plt.gcf()
        self.pdf.savefig(edgecolor=fig.get_edgecolor(),
                        facecolor=fig.get_facecolor(),
                        dpi=150)
        plt.close()
    
    def plt_setup(self):
        plt.figure(linewidth=2,
                    edgecolor=self.fig_border,
                    layout='constrained')
        plt.box(on=None)
        plt.suptitle(f'{self.report_data.heading.site.name.title()} {self.report_data.heading.name.title()} {self.RESULTS_TYPE.title()}\n {self.report_date}')
        plt.figtext(0.95, 0.05, self.header_text, horizontalalignment='right', size=6, weight='light')

    def create_table(self, array_data, index):
        array = array_data.array 
        axTable = plt.subplot(2,self.ARRAYS_PER_ROW, index, frame_on=False)
        
        row_headers = array.get_monitoring_point_ids()
        
        #Table Styles
        ccolors = plt.cm.BuPu(np.full(len(self.COLUMN_HEADERS), 0.1))
        rcolors = plt.cm.BuPu(np.full(len(row_headers), 0.1))

        cell_text = []
        cell_colours = []
        for mp in array.monitoring_points:
            latest_mp = mp.get_measurement_by_date(array_data.date)
            if latest_mp is not None:
                cell_text.append([latest_mp.point_id, str(latest_mp.date_time), f'{latest_mp.delta_dist:1.1f}'])
                colour = self.get_cell_colour(latest_mp.delta_dist, mp.triggers)
                cell_colours.append([colour,  colour, colour])
            else:
                #No monitoring data for that day
                cell_text.append([mp.point_id, '-', '-'])
                cell_colours.append(['grey',  'grey', 'grey'])
      
        axTable.set_title(f'Array {array.name.title()}')
        axTable.get_xaxis().set_visible(False)
        axTable.get_yaxis().set_visible(False)
        
        axTable.table(cellText=cell_text,
                      rowLoc='right',
                      colColours=ccolors,
                      colLabels=self.COLUMN_HEADERS,
                      loc='center',
                      cellColours=cell_colours)

    
    def get_cell_colour(self, value, triggers):
        """returns the trigger color based on the value passed in, checks last trigger first"""
        for trig in reversed(triggers): 
            if trig.value < 0:
                if value <= trig.value:
                    return trig.color 
            else:
                if value >= trig.value:
                    return trig.color 
        return 'w'

        
    
class ConvergenceMonitoringResultsTable(MonitoringResultsTable):
    RESULTS_TYPE = 'CONVERGENCE'
    COLUMN_HEADERS = ['Point ID', 'Date:Time', 'Convergence(mm)']
    ARRAYS_PER_ROW = 2


class DivergenceMonitoringResultsTable(MonitoringResultsTable):
    RESULTS_TYPE = 'DIVERGENCE'
    COLUMN_HEADERS = ['Point ID', 'Date:Time', 'Divergence(mm)']
    ARRAYS_PER_ROW = 2


class RadialMonitoringResultsTable(MonitoringResultsTable):
    RESULTS_TYPE = 'RADIAL'
    COLUMN_HEADERS = ['Point ID', 'Date:Time', 'Radial(mm)']
    ARRAYS_PER_ROW = 2

class Point3DMonitoringResultsTable(MonitoringResultsTable):
    RESULTS_TYPE = 'POINT 3D'
    COLUMN_HEADERS = ['Point ID', 'Date:Time', 'Delta E(mm)', 'Delta N(mm)', 'Delta H(mm)']
    ARRAYS_PER_ROW = 2 


class VectorMonitoringResultsTable(MonitoringResultsTable):
    RESULTS_TYPE = 'Vector'
    COLUMN_HEADERS = ['Point ID', 'Date:Time', 'Vector(mm)']
    ARRAYS_PER_ROW = 2 