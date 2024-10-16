from datetime import datetime

from TriggerReporter.extractors import MonitoringPointCSVExtractor, AmbergMeasurementExtractor
from TriggerReporter.models import *
from TriggerReporter.factories import MeasurementPointFactory, ArrayFactory


class MonitoringPointProcessor:
    ALLOWED_OVERLISATIONS = (Overalisation1, Overalisation2)
    def __init__(self, project, extractor=None):
        self.project = project
        self.extractor = MonitoringPointCSVExtractor

    def process_mass_monitoring_points(self, data_lines):
        for line in data_lines:
            self.process_mass_monitoring_point(line.split(self.extractor.SPLIT))
        
    def process_mass_monitoring_point(self, data_line):
        """proceess and creates a monitoring point from a mass line (site, heading...)"""
        #1) Extract monitoring point type
        mt_type = self.extractor.extract_monitoring_type(data_line)
        # check if compatiable
        if not self._check_mt(mt_type):
            # raise error mt type not allowed 
            return
        
        site_name = self.extractor.extract_site_name(data_line)
        heading_name = self.extractor.extract_heading_name(data_line)
        array_name = self.extractor.extract_convergence_array_name(data_line)
        mp_id = self.extractor.extract_point_id(data_line)
        drawing_no = self.extractor.extract_drawining_no(data_line)
    
        #2) Check if site exisits if not create a site. 
        site = self._get_site(site_name)

        #3) Check if heading name exists within site object if not create heading 
        heading = self._get_heading(site, heading_name)


        #4) Get master Array within the heading object if not create
        master_array = heading.get_array(array_name)
        if master_array is None: 
            master_array = MasterArray(site, heading, array_name)
            heading.arrays.append(master_array)

        array = master_array.get_array(mt_type)
        if array is None:
            array = self._create_array(site, heading, array_name, mt_type, drawing_no)
            # add array to heading 
            master_array.arrays.append(array)
 
        #5) Create Triggers 
        trigger_values =  [self.extractor.extract_trigger_1(data_line), 
            self.extractor.extract_trigger_2(data_line), self.extractor.extract_trigger_3(data_line)]
        
        triggers = self.create_triggers(trigger_values)
        
        # 6) check if overalisation point
        ovalisation = self._check_for_overalisation(mp_id)
        if ovalisation is not None:
            # check if ovalisation already exists
            oval = self._get_ovalisation_point(array, mp_id)
            if oval is None:
                oval = ovalisation(array)
                array.add_overalisation(oval)
            oval.add_triggers(triggers)
            
        else:
            #7) Get Monitoring Point within the array object
            mp = self._get_monitoring_point(array, mp_id)
            if mp is None:
                # no mp so need to create one
                mp = self._create_monitoring_point(array, mp_id)
            # add triggers
            mp.add_triggers(triggers)
            # add mp to array 
            array.add_monitoring_point(mp)        

    def _check_mt(self, mt_type):
        for mt in MonitoringTypes:
            if mt_type.lower() == mt.value.lower():
                return True 
        return False 
    
    def _get_site(self, site_name):
        """returns a site object based on the site name passed in"""
        site = self.project.get_site(site_name)
        if not site:
            site = Site(site_name.lower())
            self.project.add_site(site)
        return site 

    def _get_heading(self, site, heading_name):
        heading = site.get_heading(heading_name)
        if not heading:
            heading = Heading(site, heading_name.lower())
            site.add_heading(heading)
        return heading 

    def _create_array(self, site, heading, array_name, mt_type, drawing_no):
        Array_Cls = ArrayFactory.get_array_class(mt_type)
        if Array_Cls is not None:
            return Array_Cls(site, heading, array_name, drawing_no)

    def _get_monitoring_point(self, array, mp_id):
        return array.get_monitoring_point(mp_id)

    def _get_ovalisation_point(self, array, mp_id):
        return array.get_ovalisation_point(mp_id)

    def _create_monitoring_point(self, array, mp_id):
        return MonitoringPoint(mp_id.lower())

    
    def _check_for_overalisation(self, mp_id):
        for overalisation in self.ALLOWED_OVERLISATIONS:
            if overalisation.CODE_TYPE == mp_id:
                return overalisation

    def create_triggers(self, trigger_values):
        TRIGGER_COLORS =  ['forestgreen', 'orange', 'red']
        """create a Trigger values"""
        # get trigger object
        return [Trigger(color, float(value)) for color, value in zip(TRIGGER_COLORS, trigger_values)]

class MeasurementPointProcessor:
    MT_TYPES = ['radial displacement', 'convergence', 'divergence']
    def __init__(self, project, extractor=None):
        self.project = project 
        self.extractor = AmbergMeasurementExtractor

    def process_measurement_points(self, data_lines):
        for data_line in data_lines:
            self.process_measurement_point(data_line.split(self.extractor.SPLIT))

    def process_measurement_point(self, data_line):
        mt_type = self.extractor.extract_monitoring_type(data_line).lower()
        if mt_type not in self.MT_TYPES:
            return  
       
        point_class = self._get_measurement_point_class(mt_type)
        check = self.checker(mt_type, data_line)
        if check: 
            if point_class:
                point = None  
                if point_class == MeasurementDistancePoint:
                    point = self.create_measurement_dist_point(data_line)

                elif point_class == Measurement3DPoint:
                    point = self.create_measurement_3d_point(data_line)

                monitoring_point = self.project.get_monitoring_point(point.point_id, mt_type)
        
                if monitoring_point:
                    monitoring_point.measurement_points.append(point)

                # check if convergence if so also grab point from divergence data and add data
                if mt_type == MonitoringTypes.CONVERGENCE.value:
                    monitoring_point = self.project.get_monitoring_point(point.point_id, MonitoringTypes.DIVERGENCE.value)
                    if monitoring_point:
                        monitoring_point.measurement_points.append(point)


    def checker(self, mt_type, data_line):
        """checks a data line is good"""
        checker_types = {'radial displacement':['extract_point_id', 'extract_monitoring_type', 'extract_date_time',
                                            'extract_distance', 'extract_delta_distance'],
            'convergence':['extract_point_id', 'extract_monitoring_type', 'extract_date_time',
                            'extract_distance', 'extract_delta_distance'],
            'divergence':['extract_point_id', 'extract_monitoring_type', 'extract_date_time',
                            'extract_distance', 'extract_delta_distance'],
            'vector': ['extract_point_id', 'extract_monitoring_type', 'extract_date_time',
                            'extract_distance', 'extract_delta_distance'],
            '3d point': ['extract_point_id', 'extract_monitoring_type', 'extract_date_time',
                            'extract_delta_stng', 'extract_delta_l', 'extract_delta_h']
        }

        checkers = checker_types.get(mt_type)
        if checkers is None:
            return False  
        methods = [getattr(self.extractor, check) for check in checkers]
        for method in methods:
            result = method(data_line)
            if not result:
                return False 
        return True 
    
    def create_measurement_3d_point(self, data_line):
        return Measurement3DPoint(
            self.extractor.extract_point_id(data_line).lower(),
            datetime.strptime(self.extractor.extract_date_time(data_line),'%d.%m.%Y:%H:%M:%S'),
            float(self.extractor.extract_delta_stng(data_line)),
            float(self.extractor.extract_delta_l(data_line)),
            float(self.extractor.extract_delta_h(data_line)))

    def create_measurement_dist_point(self, data_line):
        return MeasurementDistancePoint(
            self.extractor.extract_point_id(data_line).lower(),
            datetime.strptime(self.extractor.extract_date_time(data_line),'%d.%m.%Y:%H:%M:%S'),
            float(self.extractor.extract_distance(data_line)),
            float(self.extractor.extract_delta_distance(data_line)))

    def _get_measurement_point_class(self, mon_type):
        return MeasurementPointFactory.get_measurement_point(mon_type)


class ReportDataProcessor: 
    def __init__(self, report_vars):
        self.report_vars = report_vars # heading: vars{}
        self.report_datas = [] #[report_data, ]
                    
    def process_report_data(self):
        for heading, report_var in self.report_vars.items():
            surveyor = report_var.surveyor.get()
            for master_array, array_var in report_var.array_vars.items():
                for mt_type, data in array_var.vars.items():
                    on_off = data[0].get()
                   
                    #date = datetime.strptime(date,'%d.%m.%Y:%H:%M:%S')
                    if on_off:
                        date = data[1].get()
                        date = datetime.strptime(date,'%Y-%m-%d %H:%M:%S')
                        report_data = self.get_report_data(heading, surveyor, mt_type)
                        array = master_array.get_array(mt_type)
                        if array is not None:
                            report_data.array_data.append(ArrayData(array, date))
        return self.report_datas
                        
    def get_report_data(self, heading, surveyor, mt_type):
        for report_data in self.report_datas:
            if report_data.heading == heading and report_data.mt_type == mt_type:
                return report_data 
        
        report_data = ReportData(heading, surveyor, mt_type)
        self.report_datas.append(report_data)
        return report_data 
        


