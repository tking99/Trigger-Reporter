from datetime import datetime

from TriggerReporter.models import *
from TriggerReporter.Matplot.tables import ConvergenceMonitoringResultsTable, DivergenceMonitoringResultsTable, \
        RadialMonitoringResultsTable, VectorMonitoringResultsTable, Point3DMonitoringResultsTable

class ArrayFactory:
    ARRAYS = (ConvergenceArray, DivergenceArray, RadialArray, Point3DArray)
    @classmethod
    def get_array_class(cls, code_type):
        for Array in cls.ARRAYS:
            if code_type.strip().lower() == Array.CODE_TYPE.lower():
                return Array

class MeasurementPointFactory:
    MEASUREMENT_POINTS = (MeasurementDistancePoint, Measurement3DPoint)
    @classmethod 
    def get_measurement_point(cls, code_type):
        for MEASUREMENT_POINT in cls.MEASUREMENT_POINTS:
            if code_type.strip().lower() in MEASUREMENT_POINT.CODE_TYPES:
                return MEASUREMENT_POINT

  
class ResultsTableFactory:
    RESULTS_TABLES = (ConvergenceMonitoringResultsTable, DivergenceMonitoringResultsTable, RadialMonitoringResultsTable,
        Point3DMonitoringResultsTable, VectorMonitoringResultsTable)
    @classmethod 
    def get_results_tables(cls, result_settings):
        """returns a list of result table classes depending on the results 
        table passed in""" 
        result_tables = []
        
        if result_settings.point_3d:
            result_tables.append(Point3DMonitoringResultsTable)

        if result_settings.convergence:
            result_tables.append(ConvergenceMonitoringResultsTable)
        
        if result_settings.divergence: 
            result_tables.append(DivergenceMonitoringResultsTable)

        if result_settings.radial:
            result_tables.append(RadialMonitoringResultsTable) 

        if result_settings.vector_displacement:
            result_tables.append(VectorMonitoringResultsTable)

        return result_tables
            

class MonitoringResultsTableFactory:
    MONITORING_TABLES = (ConvergenceMonitoringResultsTable, DivergenceMonitoringResultsTable, RadialMonitoringResultsTable, \
        VectorMonitoringResultsTable, Point3DMonitoringResultsTable)
    @classmethod 
    def get_monitoring_table(cls, mt_type):
        for table in cls.MONITORING_TABLES:
            if table.RESULTS_TYPE.lower() == mt_type.lower():
                return table 
