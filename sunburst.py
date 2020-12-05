import pandas as pd
import numpy as np
import re


class appObj:
    """ Compiles and defines arrays for sunburst creations.

    Attributes
    ----------
    self.data : pandas dataframe
        Data from csv file.
    self.name : str
        Type of sunburst chart
    self.IDs : list
        ID for each category.
    self.parents : list
        Parent for each category.
    self.values : list
        Number of elements for each category.
    self.subs : list
        Indicates which category contains subcategories, not used for field.
    self.labels : list
        Label for each category.
    self.df : pandas dataframe
        Contains IDs, values, labels and parents.
    self.len : int
        Number of categories. For Field sunburst, number of elements.
    self.parentslabel : list
        Indicates which category contains subcategories.
        Not used for Field Sunburst.
    """
    def __init__(self, data, name):
        """ Initializes instance variables.

        Parameters
        ----------
        data : pandas dataframe
            Data from csv file.
        name : str
            Indicates which sunburst the object refers to.
        """
        self.data = data
        self.name = name
        self.IDs = []
        self.parents = []
        self.values = []
        self.subs = []
        self.labels = []
        self.df = []
        self.len = 0
        self.parentslabels = []
        

    def initiate_arrays(self):
        """ Creates the instance parameters, depending of the sunburst name.
        """
        
        if self.name == 'Artistic Intention':
            self.IDs = ["AI", "CO", "AU", "IV", "LS", "LP", "SD", "LI", "RS", "SD_Mat", "LS_Dyn"]
            self.parents = ["", "AI", "AI", "AI", "AI", "AI", "AI", "AI", "AI", "SD", "LS"]
            self.labels = ["Artistic<br>Intention", "Context", "Audience", "Intervention<br>Visibility",
             "Listening<br>Position", "Lifespan", "Sound<br>Design", "Lighting<br>Design",
             "Role of<br>Sound", "Materials", "Dynamic", "Exhibition", "Outdoor", "Indoor",
             "School", "Prototype", "Transportation", "Care<br>Center", "Adults", "Children",
             "Both", "Non<br>Visible", "Non-Sonic<br>Elements", "Visual<br>interface", "Sonic<br>Elements",
             "Pathway", "No Specific<br>Path", "Sweet<br>Spot", "Ephemeral", 
             "Temporary", "Semi-Permanent", "Abstract", "Referential", "Sonification", "Local<br>Recordings", 
             "Pre-existing<br>Materials", "Feedback<br>Generated", "Auto-Generative", "Infrasounds",
             "Noise<br>Cancellation", "Site's Acoustics<br>Involved", "No<br>Lights", "Spotlights", "Dynamic",
            "Expressive", "Informational", "Didactic", "Therapeutic"]
            self.values = [1819, 232, 193, 323, 195, 194, 297, 175, 210, 286, 108]
            self.subs = ["SD_Mat", "LS_Dyn"]
            
        elif self.name == 'System Design':
            self.IDs = ["SyD", "TS", "SP", "SG", "TS_Ele", "TS_Mec", "TS_Ide", "TS_Mic", "TS_Ima",
              "TS_Bio", "TS_Con", "TS_Det", "TS_Env", "SP_Num", "SP_Hea", "SP_Pnt", "SP_Cnt", "SP_Dir", "SG_Obj"]
            self.parents = ["", "SyD", "SyD", "SyD", "TS", "TS", "TS", "TS", "TS", "TS", "TS", "TS", "TS", "SP",
             "SP", "SP", "SP", "SP", "SG"]
            self.values = [987, 225, 541, 221, 7, 15, 5, 53, 67, 3, 27, 24, 8, 132, 18, 138, 110, 143, 44]
            self.subs = ["TS_Ele", "TS_Mec", "TS_Ide", "TS_Mic", "TS_Ima", "TS_Bio", "TS_Con", "TS_Det", 
            "TS_Env", "SP_Num", "SP_Hea", "SP_Pnt", "SP_Cnt", "SP_Dir", "SG_Obj"]
            self.labels = ["System<br>Design", "Type of<br>Input Device", "Spatialization", "Sound<br>Generation",
              "Electric,<br>Magnetic Sensors", "Mechanical<br>Sensors", "Identification", "Microphones",
              "Image<br>Sensors", "Bio-signals<br>Sensors", "Controllers", "Detectors", "Environment",
              "Number of<br>Sources", "Headphones", "Diffusion<br>Orientation", "Control",
              "Directivity", "Sound<br>Object", 

              "Server", "Cartridge,<br>Tape Reader", "Voltage<br>Sensor", "Capacitance<br>Sensor",
              "Accelerometer,<br> Gyroscope", "Pressure<br>Sensor", "Bend<br>Sensor", "Torque<br>Sensor",
              "Potentiometer", "Radio-Frequency<br>Identification", "Barcode<br>Scanner", "Coin<br>Detector",
              "Piezoelectric<br>Sensor", "Microphone", "Camera", "Motion<br>Sensing<br>Device",
              "Fingerprint<br>Sensor", "Eletromyograph", "Electroencephalograph", "Remote Motion<br>Tracker",
              "Novint<br>Falcon", "Game<br>Controller", "Touch-Sensitive<br>Device", "Mouse and<br>Keyboard", 
              "Pressure<br>Pad", "Proximity<br>Sensor", "Light<br>Sensor", "Heat<br>Sensor", "Wind<br>Sensor", "Seismograph", 
              "One Source", "Two Sources", "Multiple<br>Sources", "Stereo", "Towards the<br>Same Point",
              "Towards<br>Different Points", "Evolving", "Channel-Based", "Algorithm-Based", "Directive", "Non<br>Directive",
              "Speakers", "Electronic", "Mechanical", "Resonant", "Musical<br>Instrument"]
            
        elif self.name == 'Interaction':
            self.IDs = ["IN", "IA", "IDof", "ODof", "FT", "MC", "IT"]
            self.parents = ["", "IN", "IN", "IN", "IN", "IN", "IN"]
            self.values =  [1351, 227, 190, 191, 316, 183, 244]
            self.subs = ["rien"]
            self.labels = ["Interaction", "Inter-Actors", "Input Degrees<br>Of Freedom", "Output Degrees<br>Of Freedom",
              "Feedback<br>Type", "Musical<br>Control", "Interaction<br>Type", "Many", "Few", "One Actor", "None",
              "One Degree", "Two Degrees", "Three or<br>More Degrees", "One ", "Two", "Three or<br>More", "Visual", "Haptic", "Sonic",
              "Heat", "Taste", "Smell", "Process", "Note-Level", "Timbral", "Global<br>Activity", "Network", "Embodied",
              "Visitor's<br>Motion", "Visitor's<br>Sounds", "Eyes'<br>Movements", "Facial<br>Expression", "Brain<br>Activity",
              "Natural<br>Elements"]       
            
        self.len = len(self.IDs)
        self.parentslabels = self.labels[:len(self.IDs)]
        self.df = pd.DataFrame(dict(
                    ids = self.IDs, 
                    parents = self.parents,
                    values = self.values, 
                    labels = self.labels[:self.len]
                    ))
       
        
        if self.name != 'Field':
            for col in self.data:      
                for ID in self.IDs:
                    if ID in col:
                        try:
                            value = self.data[col].sum()
                            if value > 0:
                                if col[:6] not in self.subs:
                                    self.parentslabels.append(self.labels[self.IDs.index(ID)])
                                    temp = pd.DataFrame(dict(
                                            ids = [col], 
                                            parents = [ID],
                                            labels = [self.labels[self.len]],
                                            values = [value]
                                            ))
                                    self.df = pd.concat([self.df, temp], sort=False)
                                    self.len += 1  
                                    break
                                elif col[:6] in self.subs:
                                    self.parentslabels.append(self.labels[self.IDs.index(ID)])
                                    temp = pd.DataFrame(dict(
                                            ids = [col], 
                                            parents =[col[:6]],
                                            labels = [self.labels[self.len]],
                                            values = [value]
                                            ))
                                    self.df = pd.concat([self.df, temp], sort=False) 
                                    self.len += 1 
                                    break
                        except IndexError:
                            break

        elif self.name == 'Field':
            self.parents = [""]
            self.labels = ["Subject<br>Area"]

            for n in range(0, len(self.data['Subject Area'])):
                self.len += len(str(self.data['Subject Area'][n]).split('; '))    
            self.values = np.zeros(self.len)
            for n in range(0, len(self.data['Subject Area'])):
                area = str(self.data['Subject Area'][n]).split('; ')
                field = str(self.data['Field'][n]).split('; ')
                for i in range(0, len(field)):
                    field[i] = re.sub(' ', '<br>', field[i])
                    area[i] = re.sub(' ', '<br>', area[i])
                    self.increment_area(area[i], field[i])                    
            self.IDs = self.labels
            self.values = self.values[:len(self.labels)]
            self.df = pd.DataFrame(dict(
                                    ids = self.IDs, 
                                    parents = self.parents,
                                    labels = self.labels,
                                    values = self.values
                                    ))
            self.df = self.df.sort_values(by='values', ascending=False)

    def increment_area(self, str_a, str_f):
        """ Used only for the field sunburst.
        Increments instance labels and parents with Global Subject Area, Subject Area, and Field.

        Parameters
        ----------
        str_a : str
            Subject Area.
        str_f : str
            Field.
        """

        if str_f == 'nan':
            return
        if str_f in self.parents:
            raise NameError(str_f + ' is a Subject Area, Not a Field')
        elif str_a in ['Physical<br>Sciences', 'Health<br>Sciences', 
            'Social<br>Sciences', 'Life<br>Sciences']:
            raise NameError(str_a + ' is a Global Subject Area, Not an Area')

        phys = ('Computer<br>Science', 'Engineering', 'Mathematics',
            'Physics<br>and<br>Astronomy', 'Materials<br>Science',
            'Environmental<br>Science')
        health = ('Medicine', 'Nursing', 'Health<br>Professions')
        social = ('Arts<br>and<br>Humanities', 'Decision<br>Sciences', 
            'Psychology', 'Social<br>Sciences<br>Area')
        life = ('Neuroscience')

        if str_a in phys:
            str_p = 'Physical<br>Sciences'
        elif str_a in health:
            str_p = 'Health<br>Sciences'
        elif str_a in social:
            str_p = 'Social<br>Sciences'
        elif str_a in life:
            str_p = 'Life<br>Sciences'
        else:
            raise NameError(str_a + ' is not in the list for Global Subject Areas')

        if str_f not in self.labels:
            self.parents.append(str_a)
            self.labels.append(str_f)
            if str_a not in self.labels:
                self.parents.append(str_p)
                self.labels.append(str_a)
                if str_p not in self.labels:
                    self.parents.append("Subject<br>Area")
                    self.labels.append(str_p)
                    #self.values[self.labels.index("Subject<br>Area")] += 1

        self.values[self.labels.index("Subject<br>Area")] += 1
        self.values[self.labels.index(str_p)] += 1
        self.values[self.labels.index(str_a)] += 1
        self.values[self.labels.index(str_f)] += 1





            
                    