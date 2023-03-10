import os 
from datetime import timedelta
from pathlib import Path
from enum import Enum
from statistics import mean
import math

import tkinter as tk 
from tkinter import ttk


class TriggerReporterProject:
    FILETYPE = [('Trigger Reporter Project', '.trpj')]
    def __init__(self, path_str, name):
        self._project_path = Path(path_str)
        self.name = name
        self.sites = []

    @property 
    def project_path(self):
        return self._project_path 

    @project_path.setter
    def project_path(self, path_str):
        """Accepts a string path and coverts to Path 
        object befor assigning it to project path"""
        try:
            self._project_path = Path(path_str)
        except TypeError:
            pass 

    def get_site(self, name):
        for site in self.sites:
            if site.name.lower() == name.lower():
                return site 

    def add_site(self, site):
        for s in self.sites:
            if site.name.lower() == s.name.lower():
                return
        self.sites.append(site)

    def get_monitoring_point(self, point_id, mt_type):
        """returns the monitoring point based on point_id passed in"""
        for site in self.sites:
            for heading in site.headings:
                for master_array in heading.arrays:
                    for array in master_array.arrays:
                        if array.CODE_TYPE.lower() == mt_type.lower():
                            point = array.get_monitoring_point(point_id)
                            if point:
                                return point

    def __str__(self):
        return self.name


class MonitoringTypes(Enum):
    CONVERGENCE = 'convergence'
    DIVERGENCE = 'divergence'
    RADIAL = 'radial displacement'
    VECTOR = 'vector'
    POINT3D = '3d point'


class Site:
    def __init__(self, name):
        self.name = name 
        self.headings = []
        self.active = True 

    def toggle_active(self):
        self.active = not self.active 

    def get_heading(self, name):
        for heading in self.headings:
            if heading.name.lower() == name.lower():
                return heading

    def add_heading(self, heading):
        for h in self.headings:
            if heading.name.lower() == h.name.lower():
                return
        self.headings.append(heading)
    
    def __str__(self):
        return self.name 

    def __repr__(self):
        return self.name

class Heading:
    def __init__(self, site, name):
        self.site = site
        self.name = name 
        self.active = False
        self.arrays = [] # list of master arrays
    
    def toggle_active(self):
        self.active = not self.active 

    def has_active_array(self, mt_type):
        for array in self.arrays:
            if array.has_active_array(mt_type):
                return True
        return False
    
    def get_array(self, name):
        for array in self.arrays: 
            if array.name.lower() == name.lower():
                return array
 
    def add_array(self, arr):
        for array in self.arrays:
            if array.name == arr.name:
                return # raise error
        self.arrays.append(arr)

    def __str__(self):
        return self.name 

    def __repr__(self):
        return self.name


class MasterArray:
    def __init__(self, site, heading, name):
        self.site = site
        self.heading = heading 
        self.name = name 
        self.active = True 
        self.arrays = [] # list of arrays

    def activate_array(self, mt_type):
        for array in self.arrays:
            if array.CODE_TYPE.lower() == mt_type.lower():
                array.toggle_active()

    def has_active_array(self, mt_type):
        for array in self.arrays:
            if array.CODE_TYPE.lower() == mt_type.lower():
                return True 
        return False 

    def is_array_active(self, mt_type):
        array = self.get_array(mt_type)
        if array:
            return array.active
        return False 
    
    
    def get_array(self, mt_type):
        for array in self.arrays:
            if mt_type.lower() == array.CODE_TYPE.lower():
                return array 
    
    def add_array(self, arr):
        for array in self.arrays: 
            if arr.CODE_TYPE.lower() == array.CODE_TYPE.lower():
                return 
        self.arrays.append(arr)

    def get_latest_date(self, mt_type):
        for array in self.arrays:
            if array.CODE_TYPE.lower() == mt_type.lower():
                return array.get_latest_date()

    def get_monitoring_dates(self, mt_type):
        for array in self.arrays:
            if array.CODE_TYPE.lower() == mt_type.lower():
                return array.get_monitoring_dates()
        return set()

    def update_active(self):
        for array in self.arrays:
            array.active = array.has_active_measurements() 

    
    def __str__(self):
        return self.name 

    def __repr__(self):
        return self.name 


class Array:
    CODE_TYPE = ''
    def __init__(self, site, heading, name, drawing_no=''): 
        self.site = site 
        self.heading = heading
        self.name = name 
        self.active = True 
        self.monitoring_points = []
        self.overalisations = []
        self.drawing_no = drawing_no

    def __len__(self):
        return len(self.monitoring_points) + len(self.overalisations)
    
    def add_overalisation(self, oval):
        for overalisation in self.overalisations:
            if oval.CODE_TYPE.lower() == overalisation.CODE_TYPE.lower():
                # already exists don't add
                return 
        self.overalisations.append(oval)
    
    def toggle_active(self):
        if self.active:
            self.active = False 
        else:
            self.active = self.has_active_measurements()

    def has_active_measurements(self):
        """returns a boolean if the array has active measurements"""
        for point in self.monitoring_points:
            if point.has_active_measurements():
                return True 
        return False 
        
    def get_latest_date(self):
        """returns latest date of a monitoring point based on passed in mt_type"""
        latest_dates = [mon.get_latest_date() for mon in self.monitoring_points if mon.get_latest_date() is not None]
        if latest_dates:
            return max(latest_dates)

    def get_monitoring_dates(self):
        """returns a set of dates for measuresments"""
        dates = set()
        for mon in self.monitoring_points:
            for meas in mon.get_sorted_measurements():  
                    dates.add(meas.date_time)  
        
        return sorted(dates, reverse=True)

    def get_monitoring_point(self, point_id):
        for point in self.monitoring_points:
            if point.point_id.lower() == point_id.lower():
                return point
    
    def get_ovalisation_point(self, point_id):
        for oval in self.overalisations:
            if point_id.lower() == oval.CODE_TYPE.lower():
                return oval 

    def get_monitoring_point_m(self, m):
        """returns monitoring points if 'M1'.. 
        if within the name"""
        for point in self.monitoring_points:
            if m.lower() in point.point_id.lower():
                return point 

    def get_monitoring_point_ids(self):
        """returns a list of the monitoring point names"""
        return [mon.point_id for mon in self.monitoring_points]

    def add_monitoring_point(self, mp):
        for point in self.monitoring_points:
            if point.point_id.lower() == mp.point_id.lower():
                return 
            # doenst exist so add
        self.monitoring_points.append(mp)

    def __str__(self):
        return self.name 

    def __repr__(self):
        return self.name

    
class ConvergenceArray(Array):
    CODE_TYPE = MonitoringTypes.CONVERGENCE.value


class DivergenceArray(Array):
    CODE_TYPE = MonitoringTypes.DIVERGENCE.value


class RadialArray(Array):
    CODE_TYPE = MonitoringTypes.RADIAL.value


class Point3DArray(Array):
    CODE_TYPE = MonitoringTypes.POINT3D.value


class MonitoringPoint:
    TIME_RANGE = 3
    def __init__(self, point_id): 
        self.point_id = point_id 
        self._triggers = []
        self.measurement_points = []          
        self.active = True 

    @property
    def triggers(self):
        return self._triggers
    
    def toggle_active(self):
        self.active = not self.active 
    
    def add_triggers(self, triggers):
        """overwrites the existing triggers list with new uploaded triggers"""
        self._triggers = triggers

    def get_sorted_measurements(self):
        """returns a list of sorted measurements by date"""
        if self.measurement_points:
            return sorted(self.measurement_points, key=lambda m: m.date_time, reverse=True)
        return self.measurement_points

    def get_latest_measurement(self):
        meas = self.get_sorted_measurements()
        if meas:
            return meas[0]

    def get_measurement_by_date(self, date_time):
        """returns the measurement associated to the date within a 
        certain date range"""
        if self.measurement_points: 
            lower_range = date_time - timedelta(hours=self.TIME_RANGE) 
            upper_range = date_time + timedelta(hours=self.TIME_RANGE)
            for meas in self.get_sorted_measurements():
                if lower_range <= meas.date_time <= upper_range:
                    return meas

    def get_latest_date(self):
        """returns the latest date of measurmeents"""
        meas = self.get_latest_measurement()
        if meas:
            return meas.date_time

    def has_active_measurements(self):
        for meas in self.measurement_points:
            if meas.active == True:
                return True 
        return False 
     
    def __str__(self):
        return self.point_id

    def __repr__(self):
        return self.point_id 


class Overalisation:
    CODE_TYPE = ''
    def __init__(self, array):
        self.array = array
        self._triggers = []
        self.active = True

    @property
    def triggers(self):
        return self._triggers

    def add_triggers(self, triggers):
        """overwrites the existing triggers list with new uploaded triggers"""
        self._triggers = triggers


class Overalisation1(Overalisation):
    CODE_TYPE = '(M1+M5)-(M3+M7)'

    def compute_overalisation(self, date):
        m1 = self.array.get_monitoring_point_m('M1')
        m5 = self.array.get_monitoring_point_m('M5')
        m3 = self.array.get_monitoring_point_m('M3')
        m7 = self.array.get_monitoring_point_m('M7')
        if m1 is not None and m5 is not None and m3 is not None and m7 is not None: 
            m1_meas = m1.get_measurement_by_date(date)
            m5_meas = m5.get_measurement_by_date(date)
            m3_meas = m3.get_measurement_by_date(date)
            m7_meas = m7.get_measurement_by_date(date)

            if m1_meas is not None and m5_meas is not None and m3_meas is not None and m7_meas is not None:
                return (m1_meas.delta_dist + m5_meas.delta_dist) - (m3_meas.delta_dist + m7_meas.delta_dist)
        return 


class Overalisation2(Overalisation):
    CODE_TYPE = '(M2+M6)-(M4+M8)'
    def compute_overalisation(self, date):
        m2 = self.array.get_monitoring_point_m('M2')
        m6 = self.array.get_monitoring_point_m('M6')
        m4 = self.array.get_monitoring_point_m('M4')
        m8 = self.array.get_monitoring_point_m('M8')
        if m2 is not None and m6 is not None and m4 is not None and m8 is not None: 
            m2_meas = m2.get_measurement_by_date(date)
            m6_meas = m6.get_measurement_by_date(date)
            m4_meas = m4.get_measurement_by_date(date)
            m8_meas = m8.get_measurement_by_date(date)

            if m2_meas is not None and m6_meas is not None and m4_meas is not None and m8_meas is not None:
                return (m2_meas.delta_dist + m6_meas.delta_dist) - (m4_meas.delta_dist + m8_meas.delta_dist)
        return



class MeasurementPoint:
    CODE_TYPE = ''
    def __init__(self, point_id, date_time):
        self.point_id = point_id 
        self.date_time = date_time 
        self.active = True 

    def toggle_active(self):
        self.active = not self.active 
    
    def __str__(self):
        return self.point_id 
    
    def __repr__(self):
        return self.point_id


class MeasurementDistancePoint(MeasurementPoint):
    """Object that models a distance based measurement"""
    CODE_TYPES = (MonitoringTypes.CONVERGENCE.value, MonitoringTypes.DIVERGENCE.value,
     MonitoringTypes.RADIAL.value)
    def __init__(self, point_id, date_time, distance, delta_dist):
        super().__init__(point_id, date_time)
        self.distance = distance 
        self.delta_dist = delta_dist 


class Measurement3DPoint(MeasurementPoint):
    """Object that models a 3d point based measurement"""
    CODE_TYPES = (MonitoringTypes.POINT3D.value,)
    def __init__(self, point_id, date_time, delta_stng, delta_l, delta_h):
        super().__init__(point_id, date_time)
        self.delta_stng = delta_stng 
        self.delta_l = delta_l 
        self.delta_h = delta_h


class Trigger:
    def __init__(self, color, value, drawing_no=None):
        self.color = color 
        self.value = value
     

class ReportVar:
    def __init__(self, heading):
        self.heading = heading
        self.surveyor = tk.StringVar()
        self.array_vars = {} # Master Array: Arrayvar


class ArrayVar:
    def __init__(self, array):
        self.array = array
        self.vars = {
            MonitoringTypes.CONVERGENCE.value: [tk.BooleanVar(value=array.is_array_active(
                MonitoringTypes.CONVERGENCE.value)), tk.StringVar(value=array.get_latest_date(
                MonitoringTypes.CONVERGENCE.value))],
            MonitoringTypes.DIVERGENCE.value: [tk.BooleanVar(value=array.is_array_active(
                MonitoringTypes.DIVERGENCE.value)), tk.StringVar(value=array.get_latest_date(
                MonitoringTypes.DIVERGENCE.value))],
            MonitoringTypes.RADIAL.value: [tk.BooleanVar(value=array.is_array_active(
                MonitoringTypes.RADIAL.value)), tk.StringVar(value=array.get_latest_date(
                MonitoringTypes.RADIAL.value))], 
            MonitoringTypes.VECTOR.value: [tk.BooleanVar(array.is_array_active(
                MonitoringTypes.VECTOR.value)), tk.StringVar(value=array.get_latest_date(
                MonitoringTypes.VECTOR.value))], 
            MonitoringTypes.POINT3D.value: [tk.BooleanVar(array.is_array_active(
                MonitoringTypes.POINT3D.value)), tk.StringVar(value=array.get_latest_date(
                MonitoringTypes.POINT3D.value))], 
        } # MT_TYPE: Array On/Off, Date


class ReportData:
    def __init__(self, heading, surveyor, mt_type):
        self.heading = heading 
        self.surveyor = surveyor 
        self.mt_type = mt_type
        self.array_data = [] 

    def __len__(self):
        return math.ceil(mean((len(array.array) for array in self.array_data)))
    
    def get_latest_date(self):
        return max((array.date for array in self.array_data))
    
    def __str__(self):
        return f'{self.heading.site} - {self.heading} - {self.mt_type}'

    def __repr__(self):
        return f'{self.heading.site} - {self.heading} - {self.mt_type}'


class ArrayData:
    def __init__(self, array, date):
        self.array = array 
        self.date = date 

    def __str__(self):
        return self.array.name 

    def __repr__(self):
        return self.array.name


