
class AmbergMeasurementExtractor: 
    SPLIT = ';'   
    @classmethod
    def extract_point_id(cls, line):
        return line[0] 

    @classmethod 
    def extract_monitoring_type(cls, line):
        return line[2].strip()
        
    @classmethod
    def extract_date_time(cls, line):
        return f'{line[4].strip()}:{line[5].strip()}'
   

    @classmethod 
    def extract_distance(cls, line):
        return line[6]
    
    @classmethod
    def extract_delta_distance(cls, line):
        return line[10].split('\n')[0]

    @classmethod 
    def extract_delta_stng(cls, line):
        return line[15]

    @classmethod 
    def extract_delta_l(cls, line):
        return line[16]
    
    @classmethod 
    def extract_delta_h(cls, line):
        return line[17]
        

class MonitoringPointCSVExtractor:
    SPLIT =','

    @classmethod 
    def extract_site_name(cls, line):
        return line[0]
    
    @classmethod 
    def extract_heading_name(cls, line):
        return line[1]

    @classmethod
    def extract_convergence_array_name(cls, line):
        return line[2]
    
    @classmethod 
    def extract_point_id(cls, line):
        return line[3]

    @classmethod 
    def extract_trigger_1(cls, line):
        return line[4]

    @classmethod 
    def extract_trigger_2(cls, line):
        return line[5]
    
    @classmethod 
    def extract_trigger_3(cls, line):
        return line[6]

    @classmethod 
    def extract_monitoring_type(cls, line):
        return line[-1].split('\n')[0]
 
    