import os
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc


# Glossary page layout
layout = html.Div([

    html.H5("""Glossary. Click on a theme to display the associated terms and their definition.
        Categories with no associated reference are inferred from the database's installations."""),

    dcc.Link('Navigate to main page', href='/'),

    dcc.Link('List of installations', 
        href='/lists',
        style={'paddingLeft': '0.5cm'}
    ),


    html.P(style={'paddingBottom': '0.5cm'}),  

    html.Details([
        html.Summary('Artistic Intention', style={'fontSize': 35, 'fontFamily': 'FontBold'}),
        html.P(["""Relates to all the considerations and contextual aspects that are taken prior to
                the design process. It is the most conceptual theme and concerns the top-level reflections that occurs
                before implementation. From a protagonist metaphor, this aspect would relate to the Designer. """,
                html.A(href='https://hal.archives-ouvertes.fr/hal-01126429', children='(le Prado and Natkin 2014)')]),
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
            html.A(href='https://doi.org/10.1017/s1355771805000774', children='(Bandt 2005)')]), 
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
            html.A(href='https://doi.org/10.1162/pres.1997.6.4.482', children='(Pressing 1997)')]), 
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
                html.P(['Relate to the nature of the sound contents and their origin, and is mostly inspired from Landy\'s framework.',
                html.A(href='https://mitpress.mit.edu/books/understanding-art-sound-organization#:~:text=The%20art%20of%20sound%20organization%2C%20also%20known%20as%20electroacoustic%20music,%2C%20synthesized%2C%20and%20processed%20sounds.&text=He%20proposes%20a%20%E2%80%9Csound%2Dbased,as%20art%20and%20pop%20music.',
                    children='(Landy 2007)')]),
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
                    html.P(['Artificial generation of acoustic feedback through a combination of microphones and loudspeakers.',
                    html.A(href='https://www.bloomsbury.com/uk/between-air-and-electricity-9781501327605/', children='(Eck 2013)')])
                ]),
                html.Details([
                    html.Summary('Pre-existing Materials'),
                    html.P(["""Named samples in Landy\'s Framework. Sound Materials that existed before the creation of the
                        installation and where created in a different context."""])
                ]),
                html.Details([
                    html.Summary('Local Recordings'),
                    html.P(["""Sound recordings taken in proximity of the installation, or recordings from
                        local residents.""",
                    html.A(href='https://doi.org/10.1017/S1355771809000089', children='(Tittel 2009)')])
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
            html.Summary('Lighting Design', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P(["""Refers to specific lighting involved by the installation."""]), 
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

    html.Details([
        html.Summary('Interaction', style={'fontSize': 35, 'fontFamily': 'FontBold'}),
        html.P(["""Aims at situating the specific relation between the interactor - being a visitor, 
            a user, or the surrounding environment - and the installation. It is inspired from Birnbaum et al.'s 
            dimension space for musical devices.""",
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005)')]),
        html.Details([
            html.Summary('Inter-Actors', style={'fontSize': 25, 'fontFamily': 'FontBold'}),
            html.P("""Number of people simultaneously involved in the musical interaction."""),
                html.A(href='https://www.researchgate.net/publication/248128301_Towards_a_Dimension_Space_for_Musical_Devices',
                    children='(Birnbaum et al. 2005,'), 
                html.A(href='https://www.doi.org/10.1080/07494460600761021',
                    children='Bandt 2006)'),
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
    ], style = {'maxWidth': '800px'})
])