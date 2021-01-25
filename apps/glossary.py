import os
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc


# Glossary page layout
layout = html.Div([

    html.H5("""Glossary. Click on a theme to display the associated terms and their definition.
        Categories with no associated reference are inferred from the database's installations.""",
        style={'maxWidth': '800px'}),

    dcc.Link('Navigate to main page', href='/'),

    dcc.Link('List of installations', 
        href='/lists',
        style={'paddingLeft': '0.5cm'}
    ),


    html.P(style={'paddingBottom': '0.5cm'}),  

    # ARTISTIC INTENTION
    html.Details([
        html.Summary('Artistic Intention', 
            style={
                'fontSize': 46,
                'fontFamily': 'FontBold', 
                'paddingBottom' : '3rem',
                'borderTop': '1px solid grey',
                'paddingTop': '2rem'
                }
        ),
        html.P(["""Relates to all the considerations and contextual aspects that are taken prior to
                the design process. It is the most conceptual theme and concerns the top-level reflections that occurs
                before implementation. From a protagonist metaphor, this aspect would relate to the Designer. """,
                html.A(href='https://hal.archives-ouvertes.fr/hal-01126429', children='(le Prado and Natkin 2014)', target='_blank')],
                style={'marginTop': '-2rem'}),
        html.Details([
            html.Summary('Context', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Information about the overall type of space in which the installation is built. 
                      Induced from the various contexts surrounding the corpus’ installations."""),
            html.Details([
                html.Summary('Outdoor Public Space'),
                html.P('Outdoor spaces accessible to all peoples such as plazas, squares or parks.')
            ]),
            html.Details([
                html.Summary('Indoor Public Space'),
                html.P('Indoor spaces accessible to all peoples such as libraries.')
            ]),
            html.Details([
                html.Summary('Exhibition'),
                html.P('The installation is/was exhibited, for instance at a gallery or in a conference.')
            ]),
            html.Details([
                html.Summary('School'),
                html.P('School from kindergarten to secondary school.')
            ]),
            html.Details([
                html.Summary('Prototype'),
                html.P('The installation has a temporary design that is subject to improvements.')
            ]),
            html.Details([
                html.Summary('Care Center'),
                html.P('Place dedicated to health care such as hospitals or nursing homes.')
            ]),
            html.Details([
                html.Summary('Transportation'),
                html.P('The installation is situated in a transportation means such as a car or a boat.')
            ]),
        ]),
        html.Details([
            html.Summary('Audience', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Type of audience targeted by the installation. Induced from the corpus."""),
            html.Details([
                html.Summary('Adults'),
                html.P("""Though children may or may not be able to access it, they are not 
                the primary target of the concerned installation.""")
            ]),
            html.Details([
                html.Summary('Children'),
                html.P('The concerned installation is specifically made for a young audience.')
            ]),
            html.Details([
                html.Summary('Both'),
                html.P('The concerned installation can be equally approched by all audiences.')
            ]),
        ]),
        html.Details([
            html.Summary('Lifespan', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Duration in which the installation was or is planned to remain
            active. It is a common approach to categorize sounding artwork, since it is determinant for
            the design process. """,
            html.A(href='https://doi.org/10.1017/s1355771805000774', children='(Bandt 2005)', target='_blank')]), 
            html.Details([
                html.Summary('Ephemeral'),
                html.P('No more than several months, for example in a temporary exhibition.')
            ]),
            html.Details([
                html.Summary('Temporary'),
                html.P('Can last several years while not being permanently integrated to urban infrastructures.')
            ]),
            html.Details([
                html.Summary('Semi-permanent'),
                html.P('Permanent integration to urban infrastructures.')
            ])      
        ]),
        html.Details([
            html.Summary('Role of Sound', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Inspired from Pressing's categories for sound roles in electronic media. """,
            html.A(href='https://doi.org/10.1162/pres.1997.6.4.482', children='(Pressing 1997)', target='_blank')]), 
            html.Details([
                html.Summary('Expressive'),
                html.P('Expressive or artistic purposes. Can also consist in Pressing\'s environmental category.')
            ]),
            html.Details([
                html.Summary('Informational'),
                html.P('Sound emphasizes information transfer such as speech.')
            ]),
            html.Details([
                html.Summary('Didactic'),
                html.P('The sound implies not only an information transfer but aims in bringing knowledge or skills to the user.')
            ]),
            html.Details([
                html.Summary('Therapeutic'),
                html.P('For reeducation or musical therapy pursposes.')
            ])      
        ]),
        html.Details([
            html.Summary('Visitor\'s Position', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Concerns the visitor's potential motion around or inside the installation."""]), 
            html.Details([
                html.Summary('Sweet Spot'),
                html.P('The visitor is required to have a static position.')
            ]),
            html.Details([
                html.Summary('Dynamic'),
                html.P('The visitor is free to move inside or around the installation with no specific path.')
            ]),
            html.Details([
                html.Summary('Sound Pathway'),
                html.P('The visitor is able to move across a path determined by the installation\'s creator.')
            ])  
        ]),
        html.Details([
            html.Summary('Intervention Visibility', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Gives detail about what can or can't be seen from an installation."""]), 
            html.Details([
                html.Summary('Sonic Elements'),
                html.P('Sound-emitting devices can be clearly seen by the visitor.')
            ]),
            html.Details([
                html.Summary('Non-sonic Elements'),
                html.P('Parts of the installation that do not emit sounds can be clearly seen by the visitor.')
            ]),
            html.Details([
                html.Summary('Visual Interface'),
                html.P("""A visible component of the installation from which visual properties can be altered through 
                    interaction. Typically consists of a screen but is not limited to it.""")
            ]),
            html.Details([
                html.Summary('Non visible'),
                html.P('The installation can\'t be seen by the visitor.')
            ]) 
        ]),
        html.Details([
            html.Summary('Sound Design Approach', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Materials and technics used for sound design."""]), 
            html.Details([
                html.Summary('Materials'),
                html.P(['Relate to the nature of the sound contents and their origin, and is mostly inspired from Landy\'s framework. ',
                html.A(href='https://mitpress.mit.edu/books/understanding-art-sound-organization#:~:text=The%20art%20of%20sound%20organization%2C%20also%20known%20as%20electroacoustic%20music,%2C%20synthesized%2C%20and%20processed%20sounds.&text=He%20proposes%20a%20%E2%80%9Csound%2Dbased,as%20art%20and%20pop%20music.',
                    children='(Landy 2007)', target='_blank')]),
                html.Details([
                    html.Summary('Abstract'),
                    html.P('Sounds that can\'t be ascribed to any real or imaginary provenance.')
                ]),
                html.Details([
                    html.Summary('Referential'),
                    html.P('Recorded sounds that suggest or at least don\'t hide the source to which they belong.')
                ]),
                html.Details([
                    html.Summary('Sonification'),
                    html.P('Refers to a mapping process for representation of non-sonic data through sound.')
                ]),
                html.Details([
                    html.Summary('Feedback Generated'),
                    html.P(['Artificial generation of acoustic feedback through a combination of microphones and loudspeakers. ',
                    html.A(href='https://www.bloomsbury.com/uk/between-air-and-electricity-9781501327605/', children='(Eck 2013)', target='_blank')])
                ]),
                html.Details([
                    html.Summary('Pre-existing Materials'),
                    html.P(["""Named samples in Landy\'s Framework. Sound Materials that existed before the creation of the
                        installation and where created in a different context."""])
                ]),
                html.Details([
                    html.Summary('Local Recordings'),
                    html.P(["""Sound recordings taken in proximity of the installation, or recordings from
                        local residents. """,
                    html.A(href='https://doi.org/10.1017/S1355771809000089', children='(Tittel 2009)', target='_blank')])
                ]),
                html.Details([
                    html.Summary('Auto-generated'),
                    html.P(["""Sound materials are emitted in the absence of interaction. In other words, the installation
                        can generate sounds autonomously."""])
                ]),
                html.Details([
                    html.Summary('Infrasounds'),
                    html.P(["""Sound materials from whitch frequency content is below the auditory threshold."""])
                ])
            ]),
            html.Details([
                html.Summary('Site\'s Acoustics Involved'),
                html.P('Acoustic properties of the space surrounding the installation are explicitely used.')
            ]),
            html.Details([
                html.Summary('Noise Cancellation'),
                html.P("""Specific use of noise cancellation technology.""")
            ])
        ]),
        html.Details([
            html.Summary('Lighting Design', style={'fontSize': 25, 'fontFamily': 'FontBold', 'paddingBottom':'2rem'}),
            html.P(["""Refers to specific lighting involved by the installation."""],
                style={'marginTop': '-2rem'}), 
            html.Details([
                html.Summary('Spotlights'),
                html.P('Spotlights or similar structures are used to emit static rays of light.')
            ]),
            html.Details([
                html.Summary('Dynamic'),
                html.P('The lighting involved by the installation is dynamic and typically reacts to the user.')
            ]),
            html.Details([
                html.Summary('No Lights'),
                html.P('There is no specific lighting involved by the installation.')
            ])  
        ]),
    ], style={'maxWidth' : '800px'}),

    # INTERACTION
    html.Details([
        html.Summary('Interaction', 
            style={
                'fontSize': 46,
                'fontFamily': 'FontBold', 
                'paddingBottom' : '3rem',
                'borderTop': '1px solid grey',
                'paddingTop': '2rem'
                }
        ),
        html.P(["""Aims at characterizing the mutual relation between the interactor - being a visitor, 
            a user, or the surrounding environment - and the installation. It is associated to the in-between reflections
            between the foremost intentions and the ultimate technical implementations and would relate to the interactor.""",
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005, ', target='_blank'),
                html.A(href='https://hal.archives-ouvertes.fr/hal-01126429', children='le Prado and Natkin 2014)', target='_blank')],
                style={'marginTop': '-2rem'}),
        html.Details([
            html.Summary('Inter-Actors', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Number of people simultaneously involved in the musical interaction. """,
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005, ', target='_blank'), 
                html.A(href='https://www.doi.org/10.1080/07494460600761021',
                    children='Bandt 2006)', target='_blank')]),
            html.Details([
                html.Summary('One'),
                html.P('One user is required for the interaction.')
            ]),
            html.Details([
                html.Summary('Several'),
                html.P('Between two and ten people can simultaneously interact with the installation.')
            ]),
            html.Details([
                html.Summary('Many'),
                html.P('More than ten people can simultaneously interact with the installation.')
            ]),
            html.Details([
                html.Summary('None'),
                html.P("""The installation does not require an user for the interaction. In some cases, concerns 
                installations in which the number of people that can interact with the installation is countless.""")
            ]),
        ]),
        html.Details([
            html.Summary('Interaction Type', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Also named Type of Control, it refers to the specific nature of the relation between
                the interactor and the installation. """,
                html.A(href='https://www.researchgate.net/publication/308305196_ENGAGEMENT_AND_INTERACTION_IN_PARTICIPATORY_SOUND_ART',
                    children='(Goudarzi and Gioti 2016)', target='_blank')]),
            html.Details([
                html.Summary('Embodied'),
                html.P(['Possesses a physical embodiment or tangible interface for interaction. ',
                html.A(href='https://www.researchgate.net/publication/308305196_ENGAGEMENT_AND_INTERACTION_IN_PARTICIPATORY_SOUND_ART',
                    children='(Goudarzi and Gioti 2016)', target='_blank')]),
            ]),
            html.Details([
                html.Summary('Visitor\'s Motion'),
                html.P('The input for interaction is the visitor\'s or part of its body\'s motion.')
            ]),
            html.Details([
                html.Summary('Visitor\'s Sounds'),
                html.P('The input for interaction are the sounds emitted or that arise from the visitor.')
            ]),
            html.Details([
                html.Summary('Network'),
                html.P("""The installation queries information coming from visitor via contactless digital networks (GSM, Bluetooth, GPS, Internet).""")
            ]),
            html.Details([
                html.Summary('Nature and Environment'),
                html.P("""The installation queries information from the natural realm, for instance through a form of biomimetics or
                through meteorological information.""")
            ]),
            html.Details([
                html.Summary('Global Activity'),
                html.P("""The installation records information from the surrounding human activity such as crowd
                frequentation or roadway traffic.""")
            ]),
            html.Details([
                html.Summary('Facial Expression'),
                html.P("""The installation tracks facial expressions from the visitor(s) such as a smile.""")
            ]),
            html.Details([
                html.Summary('Eye\'s Movement'),
                html.P("""The installation tracks the visitor(s)\'s eye\'s movement by measuring the point of gaze
                or the position of the eyes relative to the head.""")
            ]),
            html.Details([
                html.Summary('Brain Activity'),
                html.P("""The installation tracks the visitor(s)\'s brain activity, for instance through Electroencephalography.""")
            ]),
        ]),
        html.Details([
            html.Summary('Feedback Type', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Refers to the output modalities regardless of the type output device, also called Feedback Modalities. """,
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005)', target='_blank')]),
            html.Details([
                html.Summary('Sonic'),
                html.P('Emission of sound.'),
            ]),
            html.Details([
                html.Summary('Visual'),
                html.P('Emission of visual information.')
            ]),
            html.Details([
                html.Summary('Haptic'),
                html.P('Conveys information related to the sense of touch. Can consist for instance in tactile feedback or force feedback.')
            ]),
            html.Details([
                html.Summary('Heat'),
                html.P("""Emission of information related to thermoception. Temperature is artificially regulated as a result of interaction.""")
            ]),
            html.Details([
                html.Summary('Smell'),
                html.P("""Emission of odorant fragrance as a result of interaction.""")
            ]),
            html.Details([
                html.Summary('Taste'),
                html.P("""Regulated alteration of taste, for example by delivering vibrations through 
                the lips, tongue and teeth.""")
            ])
        ]),
        html.Details([
            html.Summary('Musical Control', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Indicates the level of control a visitor exerts over the resulting musical output of the system. """,
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005)', target='_blank')]),
            html.Details([
                html.Summary('Timbral'),
                html.P("""The visitor controls continuous timbral parameters such as the amount of noise or 
                spectral properties"""),
            ]),
            html.Details([
                html.Summary('Note-Level'),
                html.P('The visitor controls discrete musical events such as musical notes or rythmic patterns.')
            ]),
            html.Details([
                html.Summary('Process'),
                html.P('The visitor controls musical processes such as loops or complex patterns playback.')
            ])
        ]),
        html.Details([
            html.Summary('Input/Output Degrees of Freedom', style={'fontSize': 25, 'fontFamily': 'FontBold', 'paddingBottom':'2rem'}),
            html.P(["""Refers to the number of input and output modalities available to the user or visitor. It does 
            not represent the number of input and output controls as in birnbaum's dimension space. """,
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005)', target='_blank')],
                style={'marginTop': '-2rem'})
        ]),
    ], style = {'maxWidth': '800px'}),

    # SYSTEM DESIGN
    html.Details([
        html.Summary('System Design', 
            style={
                'fontSize': 46,
                'fontFamily': 'FontBold', 
                'paddingBottom' : '3rem',
                'borderTop': '1px solid grey',
                'paddingTop': '2rem'
                }
        ),
        html.P(["""Concerns the practical realization of the installation, from its components to its diffusion parameters.
            It emphasizes on the practical realization of artistic intentions as well as interaction design, and
            would relate to the System. """,
            html.A(href='https://hal.archives-ouvertes.fr/hal-01126429', children='(le Prado and Natkin 2014)', target='_blank')],
                style={'marginTop': '-2rem'}),
        html.Details([
            html.Summary('Spatialization', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Refers to the number of sources used, their spatial disposition as well as their diffusion and 
            control parameters that are used to create a spatial musical experience for users or visitors. """,
                html.A(href='https://mitpress.mit.edu/books/understanding-art-sound-organization#:~:text=The%20art%20of%20sound%20organization%2C%20also%20known%20as%20electroacoustic%20music,%2C%20synthesized%2C%20and%20processed%20sounds.&text=He%20proposes%20a%20%E2%80%9Csound%2Dbased,as%20art%20and%20pop%20music.',
                    children='(Landy 2007,', target='_blank'), 
                html.A(href='https://www.doi.org/10.1080/07494460600761021',
                    children='Bandt 2006)', target='_blank')]),
            html.Details([
                html.Summary('Number of sources'),
                html.P("""Number of sound-emitting sources belonging to the installation, regardless of their 
                associated sound generation technique. Multiple sources is accounted when the installation takes use
                of three or more sources. """)
            ]),
            html.Details([
                html.Summary('Diffusion Orientation'),
                html.P("""Concerns the number of direction(s) to which the sound is diffused by the installation,
                as well as their evolution through time. """),
                html.Details([
                    html.Summary('Towards the same point'),
                    html.P('All sources points towards a unique point. ')
                ]),
                html.Details([
                    html.Summary('Towards different points'),
                    html.P('The installation\'s sources point toward different points in the space. ')
                ]),
                html.Details([
                    html.Summary('Evolving'),
                    html.P('The diffusion orientation(s) dynamically evolve through time or with interaction. ')
                ])
            ]),
            html.Details([
                html.Summary('Directivity'),
                html.P('Relates to the directionnal nature of the sound source(s).'),
                html.Details([
                    html.Summary('Directive'),
                    html.P("""Relates for instance on parametric loudspeakers and beamforming. More rarely, 
                    can be associated to installations that take use of non-directive sources if they are meant 
                    to radiate in a specific area covered by the installations without affecting the others. """)
                ]),
                html.Details([
                    html.Summary('Non-Directive'),
                    html.P("""Sound sources are non-directive and are not intended to radiate in a specific area 
                    covered by the installation without affecting the others. """)
                ])
            ]),
            html.Details([
                html.Summary('Headphones'),
                html.P("""The visitor(s) use stereo headphones as a sonic interface
                with the installation.""")
            ]),
            html.Details([
                html.Summary('Control'),
                html.P(["""Refers to the nature of the playback algorithm or diffusion method across sound sources.""",
                html.A(href='https://mitpress.mit.edu/books/understanding-art-sound-organization#:~:text=The%20art%20of%20sound%20organization%2C%20also%20known%20as%20electroacoustic%20music,%2C%20synthesized%2C%20and%20processed%20sounds.&text=He%20proposes%20a%20%E2%80%9Csound%2Dbased,as%20art%20and%20pop%20music.',
                    children='(Landy 2007)', target='_blank')]),
                html.Details([
                    html.Summary("""Automated"""),
                    html.P(["""Refers to automated spatialization systems, in which some or all aspects of the way sonic material
                    is presented spatially are automated. """,
                    html.A(href='https://mitpress.mit.edu/books/understanding-art-sound-organization#:~:text=The%20art%20of%20sound%20organization%2C%20also%20known%20as%20electroacoustic%20music,%2C%20synthesized%2C%20and%20processed%20sounds.&text=He%20proposes%20a%20%E2%80%9Csound%2Dbased,as%20art%20and%20pop%20music.',
                        children='(Landy 2007)', target='_blank')])
                ]),
                html.Details([
                    html.Summary('Channel-based'),
                    html.P("""Refers to simple track-based playback across sources. In other words, 
                    each sound source plays the same or different soundtracks or loops. """)
                ])
            ])
        ]),
        html.Details([
            html.Summary('Sound Generation', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Concerns the nature of the installation's sound-emitting devices. Note that a given installation
            can use multiple sources that rely on differing generation techniques. """),
            html.Details([
                html.Summary('Speakers'),
                html.P("""Speakers are here defined as systems containing both an electro-acoustic transducer 
                and the enclosure to which they are embedded into, if there is one. """)
            ]),
            html.Details([
                html.Summary('Musical Instrument'),
                html.P(["""Various definitions are provided in the literature for what is, or not, 
                a musical instrument. It is proposed here to define musical instruments as standalone tools
                that can be used alone and by a single user to generate sound. It can consist in traditional 
                acoustic instruments but also of digital musical instruments. """,
                html.A(href='https://www.taylorfrancis.com/chapters/embodied-cognition-digital-musical-instruments-joseph-malloch-marcelo-wanderley/e/10.4324/9781315621364-48',
                    children='(Malloch and Wanderley 2017,', target='_blank'),
                html.A(href='http://doi.org/10.1145/2466627.2466633',
                    children='Bengler and Bryan-Kinns 2013)', target='_blank')
                ]),
            ]),
            html.Details([
                html.Summary('Other Sound Sources'),
                html.P(["""Sources that are neither speakers nor musical instruments. They are segmented along
                three generations techniques inspired from Lacey's three approaches for transforming sound environments. """,
                html.A(href='https://www.researchgate.net/publication/305733346_Sonic_Placemaking_Three_approaches_and_ten_attributes_for_the_creation_of_enduring_urban_sound_art_installations',
                    children='(Lacey 2016)', target='_blank')]),
                html.Details([
                    html.Summary('Electronic'),
                    html.P("""Electro-acoustic transducers that are not embedded into a speaker but rather inside an obect
                    that has or used to have a different or additional purpose (typically an old TV or radio).""")
                ]),
                html.Details([
                    html.Summary('Resonant'),
                    html.P("""Sources that rely on resonant properties of specific materials such as tubes or pipes. 
                    As in Lacey's framework, resonances from the room in which is located the installation 
                    are not considered in this category.""")
                ]),
                html.Details([
                    html.Summary('Mechanical'),
                    html.P("""Sources that emit sound through contact of different materials such as friction, while not
                    explicitely relying on acoustic resonances. """)
                ])
            ])
        ]),
        html.Details([
            html.Summary('Type of Input Device', style={'fontSize': 25, 'fontFamily': 'FontBold', 'paddingBottom':'2rem'}),
            html.P(["""Describes the kind of device that receives information that is processed for 
            interaction. It can consist in a sensor or in a device containing several sensors. A classification
            is provided among the nature of the measurand along White's classification scheme for basic sensors, and 
            among the global nature of the device for others. Complex devices such as touch-sensitive devices may 
            rely on basic sensors such as capacitance sensors. However, for those types of input devices, only the 
            entire built-in device is accounted for, regardless of the sensors it is constitued from. """,
            html.A(href='https://doi.org/10.1109/T-UFFC.1987.26922', children='(White 1987)', target='_blank')],
                style={'marginTop': '-2rem'}),
            html.Details([
                html.Summary('Electric, Magnetic Sensors'),
                html.P('Measures either eletric or magnetic information. '),
                html.Details([
                    html.Summary('Capacitance Sensor'), 
                    html.P('Measures and detect anything that is conductive via direct or non-direct contact.')
                ]),
                html.Details([
                    html.Summary('Cartridge, Tape Reader'),
                    html.P('Magnetic tape cartridge reader')
                ]),
                html.Details([
                    html.Summary('Voltage Sensor'),
                    html.P('Determinates the amount of voltage in an object (either AC or DC).')
                ]),
                html.Details([
                    html.Summary('Potentiometer'),
                    html.P('Measures variation of electric potential through sliders, thumbwheels or spinning knobs.')
                ])
            ]),
            html.Details([
                html.Summary('Mechanical Sensors'),
                html.P('Measures mechanical force such as pressure or acceleration.'),
                html.Details([
                    html.Summary('Accelerometer, Gyroscope'),
                    html.P('Measures proper acceleration or anglar velocity, relative to the sensor\'s position')
                ]),
                html.Details([
                    html.Summary('Torque Transducer'),
                    html.P('Converts torque into an electrical signal.')
                ]),
                html.Details([
                    html.Summary('Pressure Sensor'),
                    html.P('Device that measures pressure inside a fluid (gases or liquids). ')
                ]),
                html.Details([
                    html.Summary('Bend Sensor'),
                    html.P('Also called Flex Sensor, it is a sensor that measures the amount of deflection or bending. ')
                ])
            ]),
            html.Details([
                html.Summary('Image Sensors'),
                html.P('Detects electromagnetic radiations such as visible light or infrared. '),
                html.Details([
                    html.Summary('Camera'),
                    html.P('Detects visible light.')
                ]),
                html.Details([
                    html.Summary('Motion Sensing Device'),
                    html.P("""Detects complex motion through infrared sensors. Typically consists in a built-in device 
                    such as a kinect. """)
                ])
            ]),
            html.Details([
                html.Summary('Microphones'),
                html.P('Specific type of mechanical sensor that is categorized apart due to its frequent use. '),
                html.Details([
                    html.Summary('Microphone'),
                    html.P(""""Sensors that converts acoustic waves in the air into electrical signal, regardless of the technology used 
                    (for instance MEMS, dynamic, condenser microphones...). """)
                ]),
                html.Details([
                    html.Summary('Piezoelectric Sensor'),
                    html.P('Contact microphone that detects vibrations of a material through a piezoelectric material. ')
                ])
            ]),
            html.Details([
                html.Summary('Controllers'),
                html.P("""Remote built-in input devices that conveys information through various sensors and protocols,
                and that were initialy designed for video games or office work. """),
                html.Details([
                    html.Summary('Touch-Sensitive Device'),
                    html.P("""Flat device that responds to touch by transmitting the coordinates of the touched point 
                    to a computer. May consist in a screen. """)
                ]),
                html.Details([
                    html.Summary('Remote Motion Tracker'),
                    html.P("""Remote device - typically wireless - containing accelerometers and/or gyroscopes
                    to track variations in its position or angular velocity. Typically consists in Weemotes or in 
                    cellphones. """)
                ]),
                html.Details([
                    html.Summary('Mouse and Keyboard'),
                    html.P("""Devices initially designed as computer input devices. A mouse is a handheld pointing 
                    device that detects two-dimensional motion relative to a surface. A keyboard uses an arrangement of buttons 
                    that act as mechanical levers or electronic switches and is used to enter symbols and typewriting. """)
                ]),
                html.Details([
                    html.Summary('Game Controller'),
                    html.P("""Remote controller initially designed for video games that does not track its relative motion. 
                    Typically includes several joysticks and buttons.""")
                ]),
                html.Details([
                    html.Summary('Novint Falcon'),
                    html.P(["""Specific kind of remote controller that tracks 3D position of a handle. 
                    Also provides haptic feedback. """,
                    html.A(href='https://www.sciencedirect.com/science/article/pii/S2212017312002435',
                        children='(Rodriguez and Velazquez, 2012)', target='_blank')])
                ])
            ]),
            html.Details([
                html.Summary('Detectors'),
                html.P('Actuators that are triggered by a discrete event. '),
                html.Details([
                    html.Summary('Pressure Pad'),
                    html.P("""Pad that is triggered when pressed (typically by a foot or a hand) thanks to a mechanical 
                    lever or electronic switch. """)
                ]),
                html.Details([
                    html.Summary('Proximity Sensor'),
                    html.P("""Switch that is triggered by any proximity (contactless) motion, such as the motion of a visitor. 
                    Typically consistes in an infrared actuator. """)
                ])
            ]),
            html.Details([
                html.Summary('Server-Client'),
                html.P("""Client computer system that receives information from a distant server through 
                various protocols such as GPS or Internet. Can also consist in personal or local area network,
                for example by using Bluetooth technology. """)
            ]),
            html.Details([
                html.Summary('Identification'),
                html.P("""Devices designed to detect specific objects to which is embedded an identification pattern, 
                regardless of the measurand. """),
                html.Details([
                    html.Summary('Radio-Frequency Identificator'),
                    html.P('Device that uses radio waves to passively detect a tagged object. ')
                ]),
                html.Details([
                    html.Summary('Coin Detector'),
                    html.P('Detects insertion of a coin. May be able to identify the type of coin inserted. ')
                ]),
                html.Details([
                    html.Summary('Barcode Scanner'),
                    html.P('Also called barcode reader. Optical scanner that can read and decode printed barcodes. ')
                ])
            ]),
            html.Details([
                html.Summary('Bio-Signals Sensors'),
                html.P('Devices that detect physiological or biometric information from the visitor(s).'),
                html.Details([
                    html.Summary('Electromyograph'),
                    html.P('Evaluates the electrical activity from skeletal muscles. ')
                ]),
                html.Details([
                    html.Summary('Electroencephalograph'),
                    html.P('Records electrical activity from the brain. ')
                ]),
                html.Details([
                    html.Summary('Fingerprint Sensor'),
                    html.P('Identifies fingerprint from a finger when dragged or lied over a scanning area. ')
                ])
            ]),
            html.Details([
                html.Summary('Environment'),
                html.P("""Input device that receives information from the installation's surrounding 
                environment rather than to the Visitor(s)\'s."""),
                html.Details([
                    html.Summary('Light Sensor'),
                    html.P('Measures illuminance by converting light energy into electrical signal. ')
                ]),
                html.Details([
                    html.Summary('Temperature Sensor'),
                    html.P('Senses the amont of heat energy and its evolution around the sensor.')
                ]),
                html.Details([
                    html.Summary('Wind Sensor'),
                    html.P('Measures wind speed and direction. ')
                ]),
                html.Details([
                    html.Summary('Seismometer'),
                    html.P('Sensor that responds to ground motion such as motion caused by earthquakes. ')
                ])
            ])
        ])
    ], style = {'maxWidth': '800px'})

])