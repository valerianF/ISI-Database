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
            "Listening<br>Spot", "Lifespan", "Sound<br>Design", "Lighting<br>Design",
            "Role of<br>Sound", "Materials", "Dynamic", "Exhibition", "Outdoor", "Indoor",
            "School", "Prototype", "Adults", "Children", "Both", "None", "Non-Sonic<br>Elements",
             "Visual<br>interface", "Sonic<br>Elements", "Pathway", "No Specific<br>Path", "Sweet<br>Spot", "Ephemeral", 
             "Temporary", "Semi-Permanent", "Abstract", "Referential", "Sonification", "Local<br>Recordings", 
             "Pre-existing<br>Materials", "Auto-Generative", "Site's Acoustics<br>Involved",
             "None", "Spotlights", "Dynamic", "Expressive", "Informational", "Didactic"]
            self.values = [372, 40, 38, 62, 38, 37, 80, 34, 43, 73, 23]
            self.subs = ["SD_Mat", "LS_Dyn"]
            self.parentslabels = self.labels[:11]
            
        elif self.name == 'System Design':
            self.IDs = ["SyD", "TS", "SP", "SG", "TS_Env", "SP_Num", "SP_Hea", "SP_Pnt", "SP_Cnt", "SP_Dir", "SG_Obj"]
            self.parents = ["", "SyD", "SyD", "SyD", "TS", "SP", "SP", "SP", "SP", "SP", "SG"]
            self.values = [219, 43, 122, 54, 4, 28, 8, 34, 22, 30, 16]
            self.subs = ["TS_Env", "SP_Num", "SP_Hea", "SP_Pnt", "SP_Cnt", "SP_Dir", "SG_Obj"]
            self.labels = ["System<br>Design", "Type of<br>Input Device", "Spatialization", "Sound<br>Generation", "Environment",
              "Number of<br>Sources", "Headphones", "Diffusion<br>Orientation", "Control",
              "Directivity", "Sound<br>Object", "Pressure<br>Pad", "Piezoelectric<br>Sensor", 
              "Accelerometer", "Microphone", "Camera", "Motion<br>Sensing<br>Device", "Proximity<br>Sensor",
              "Server", "Touch-Sensitive<br>Device", "Torque<br>Sensor", "Potentiometer", "Solar<br>Panel",
              "Heat<br>Sensor", "Wind<br>Sensor", "One", "Two", "Multiple", "Stereo", "Towards the<br>Same Point",
              "Towards<br>Different Points", "Dynamic", "Channel-Based", "Algorithm-Based", "Directive", "Omnidirective",
              "Speakers", "Electronic", "Mechanical", "Resonant", "Musical<br>Instrument"]
            self.parentslabels = self.labels[:11]
            
        elif self.name == 'Interaction':
            self.IDs = ["IN", "IA", "IDof", "ODof", "FT", "MC", "IT"]
            self.parents = ["", "IN", "IN", "IN", "IN", "IN", "IN"]
            self.values =  [264, 40, 39, 37, 58, 37, 53]
            self.subs = ["rien"]
            self.labels = ["Interaction", "Inter-Actors", "Input Degrees<br>Of Freedom", "Output Degrees<br>Of Freedom",
              "Feedback<br>Type", "Musical<br>Control", "Interaction<br>Type", "Many", "Few", "One", "None",
              "One", "Several", "One", "Two", "Three or<br>More", "Visual", "Haptic", "Sonic", "Heat",
              "Process", "Note-Level", "Timbral", "Global<br>Activity", "Network", "Embodied", "Visitor's<br>Motion", 
              "Visitor's<br>Sounds", "Natural<br>Elements"]
            self.parentslabels = self.labels[:11]
            
            
        self.len = len(self.IDs)
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
                    