import pandas as pd


class appObj:
    def __init__(self, data, name):
        self.data = data
        self.name = name
        self.IDs = []
        self.parents = []
        self.values = []
        self.subs = []
        self.labels = []
        self.df = []
        self.len = []
        self.parentslabels = []
        

    def initiateArray(self):
        
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
       
        
        for col in self.data[8+self.len:]:      
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
                    