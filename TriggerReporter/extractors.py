from datetime import datetime

class AmbergMeasurementExtractor: 
    SPLIT = ';'   
    @classmethod
    def extract_point_id(cls, line):
        try: 
            return line[0] 
        except IndexError: 
            return False 

    @classmethod 
    def extract_monitoring_type(cls, line):
        try: 
            return line[2].strip()
        except (IndexError, ValueError):
            return False 
        
    @classmethod
    def extract_date_time(cls, line):
        try: 
            ds = f'{line[4].strip()}:{line[5].strip()}'
            datetime.strptime(ds,'%d.%m.%Y:%H:%M:%S')
        except (IndexError, ValueError) as e:
            return False
        return ds 
   
    @classmethod
    def extract_delta_l(cls, line):
        try:
            return line[16]
        except IndexError:
            return False 

    @classmethod 
    def extract_delta_h(cls, line):
        try:
            return line[17]
        except IndexError:
            return False 
 
    @classmethod
    def extract_distance(cls, line):
        try: 
            return line[6]
        except IndexError:
            return False 
    
    @classmethod
    def extract_delta_distance(cls, line):
        try:
            return line[10].split('\n')[0]
        except (IndexError, ValueError):
            return False 

    
class MonitoringPointCSVExtractor:
    SPLIT =','

    @classmethod 
    def extract_site_name(cls, line):
        try:
            return line[0]
        except IndexError:
            return False 
    
    @classmethod 
    def extract_heading_name(cls, line):
        try:
            return line[1]
        except IndexError:
            return False

    @classmethod
    def extract_convergence_array_name(cls, line):
        try:
            return line[2]
        except IndexError:
            return False
    
    @classmethod 
    def extract_point_id(cls, line):
        try:
            return line[3]
        except IndexError:
            return False 

    @classmethod 
    def extract_trigger_1(cls, line):
        try:
            return line[4]
        except IndexError:
            return False

    @classmethod 
    def extract_trigger_2(cls, line):
        try:
            return line[5]
        except IndexError:
            return False
    
    @classmethod 
    def extract_trigger_3(cls, line):
        try: 
            return line[6]
        except IndexError:
            return False

    @classmethod 
    def extract_monitoring_type(cls, line):
        try:
            return line[7]
        except IndexError:
            return False
    
    @classmethod
    def extract_drawining_no(cls, line):
        try:
            return line[-1].split('\n')[0]
        except (IndexError, ValueError):
            return False
    

    
    