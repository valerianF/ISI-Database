#!/usr/bin/env python3
"""
Standalone data conversion: reads installationsList.csv → writes js/data.js.
Run: py convert_data.py

No dependency on apps/ — re-run whenever the CSV changes.
"""
import os, re, json
import pandas as pd
import numpy as np

# ── Hierarchy definitions ─────────────────────────────────────────────────────
# Each dict defines the STRUCTURE for one sunburst chart.
# 'ids'     : top-level node IDs (root first, then children)
# 'parents' : matching parent for each id ("" = root)
# 'labels'  : display labels for ALL nodes in order:
#             first len(ids) entries → top-level nodes
#             remaining entries     → leaf nodes, assigned in CSV column order
# 'subs'    : IDs that are intermediate parents (their CSV columns nest under them)

HIERARCHIES = {
    'AI': dict(
        ids = ["AI", "CO", "AU", "IV", "LS", "LP", "SD", "LI", "RS", "SD_Mat", "SD_Pro", "LS_Dyn"],
        parents = ["", "AI", "AI", "AI", "AI", "AI", "AI", "AI", "AI", "SD", "SD", "LS"],
        subs = ["SD_Mat", "SD_Pro", "LS_Dyn"],
        labels = ["Artistic<br>Intention", "Context", "Audience", "Intervention<br>Visibility",
             "Visitor\'s<br>Position", "Lifespan", "Sound<br>Design", "Lighting<br>Design",
             "Role of<br>Sound", "Material", "Process", "Dynamic", "Exhibition", "Outdoor", "Indoor",
             "School", "Prototype", "Transportation", "Care<br>Center", "Adults", "Children",
             "Both", "Non<br>Visible", "Non-Sonic<br>Elements", "Visual<br>interface", "Sonic<br>Elements",
             "Pathway", "No Specific<br>Path", "Sweet<br>Spot", "Ephemeral", 
             "Semi-Permanent", "Permanent", "Abstract", "Referential", "Local<br>Recordings", "Infrasounds",  
             "Pre-existing<br>Material", "Sonification", "Feedback<br>Generated", "Auto-Generated", 
             "Noise<br>Cancellation", "Site's Acoustics<br>Involved", "No<br>Lighting", "Static Lights", "Dynamic ",
            "Expressive", "Informational", "Didactic", "Therapeutic"],
    ),
    'SD': dict(
        ids = ["SyD", "TS", "SP", "SG", "TS_Ele", "TS_Mec", "TS_Ide", "TS_Mic", "TS_Ima",
              "TS_Bio", "TS_Con", "TS_Det", "TS_Env", "SP_Num", "SP_Hea", "SP_Pnt", "SP_Cnt", "SP_Dir", "SG_Obj"],
        parents = ["", "SyD", "SyD", "SyD", "TS", "TS", "TS", "TS", "TS", "TS", "TS", "TS", "TS", "SP",
             "SP", "SP", "SP", "SP", "SG"],
        subs = ["TS_Ele", "TS_Mec", "TS_Ide", "TS_Mic", "TS_Ima", "TS_Bio", "TS_Con", "TS_Det", 
            "TS_Env", "SP_Num", "SP_Hea", "SP_Pnt", "SP_Cnt", "SP_Dir", "SG_Obj"],
        labels = ["System<br>Design", "Type of<br>Input Device", "Spatialization", "Sound<br>Generation",
              "Electric,<br>Magnetic Sensors", "Force and<br>Pressure Sensors", "Identification", "Microphones",
              "Image<br>Sensors", "Bio-signals<br>Sensors", "Controllers", "Detectors", "Environment",
              "Number of<br>Sources", "Headphones", "Diffusion<br>Orientation", "Control",
              "Directivity", "Other<br>Sound<br>Sources", 

              "Server-Client", "Cartridge,<br>Tape Reader", "Voltage<br>Sensor", "Capacitance<br>Sensor",
              "Accelerometer,<br> Gyroscope", "Pressure<br>Sensor", "Bend<br>Sensor", "Torque<br>Sensor",
              "Potentiometer", "Radio-Frequency<br>Identification", "Barcode<br>Scanner", "Coin<br>Detector",
              "Piezoelectric<br>Sensor", "Microphone", "Camera", "Motion<br>Sensing<br>Device",
              "Fingerprint<br>Sensor", "Eletromyograph", "Electroencephalograph", "Remote Motion<br>Tracker",
              "Novint<br>Falcon", "Game<br>Controller", "Touch-Sensitive<br>Device", "Mouse and<br>Keyboard", 
              "Pressure<br>Pad", "Proximity<br>Sensor", "Light<br>Sensor", "Heat<br>Sensor", "Wind<br>Sensor", "Seismograph", "CO2<br>Sensor", "Rain<br>Sensor",
              "One   ", "Two   ", "Multiple<br>Sources", "Stereo", "Towards the<br>Same Point",
              "Towards<br>Different Points", "Dynamic  ", "Channel-Based", "Automated<br>Spatialization", "Directive", "Non<br>Directive",
              "Speakers", "Electronic", "Mechanical", "Resonant", "Musical<br>Instrument"],
    ),
    'IN': dict(
        ids = ["IN", "IA", "IDof", "ODof", "FT", "MC", "IT", "IT_Use", "IT_Ada"],
        parents = ["", "IN", "IN", "IN", "IN", "IN", "IN", "IT", "IT"],
        subs = ["IT_Use", "IT_Ada"],
        labels = ["Interaction", "Inter-Actors", "Input Degrees<br>Of Freedom", "Output Degrees<br>Of Freedom",
              "Feedback<br>Type", "Musical<br>Control", "Interaction<br>Type", "User<br>Interaction", "Adaptive", "Many", "Few", "One", "Countless", "None",
              "One  ", "Two ", "Three or<br>More ", "One ", "Two", "Three or<br>More", "Visual", "Haptic", "Auditory",
              "Heat", "Taste", "Smell", "Process", "Note-Level", "Timbral", "Global<br>Activity", "Network", "Embodied",
              "Visitor's<br>Motion", "Visitor's<br>Sounds", "Eyes'<br>Movements", "Facial<br>Expression", "Brain<br>Activity",
              "Natural<br>Elements"],
    ),
}


def build_hierarchy(data, h):
    """Compute sunburst data for one hierarchy from binary CSV columns.

    Replicates the logic of apps/sunburst.py appObj.initiate_arrays()
    without importing that module.
    """
    ids, parents_list, labels, subs = h['ids'], h['parents'], h['labels'], h['subs']
    n = len(ids)
    values = [0.0] * n
    non_subs = ids[:-len(subs)] if subs else ids
    sub_ids  = ids[len(ids)-len(subs):] if subs else []

    # Aggregate binary columns into node totals (matches original Python logic)
    for col in data.columns:
        for i, ID in enumerate(non_subs):
            if ID in col:
                s = float(data[col].sum())
                values[0] += s          # root
                values[i] += s
        for ID in sub_ids:
            if ID in col:
                values[ids.index(ID)] += float(data[col].sum())

    # Build leaf nodes from CSV columns (assigned in CSV column order)
    cur_len = n
    all_ids     = list(ids)
    all_parents = list(parents_list)
    all_labels  = list(labels[:n])
    all_values  = list(values)
    parent_labels = list(labels[:n])

    for col in data.columns:
        for ID in ids:
            if ID in col:
                col_val = float(data[col].sum())
                if col_val > 0 and cur_len < len(labels):
                    col_prefix6 = col[:6]
                    parent_id = col_prefix6 if col_prefix6 in subs else ID
                    parent_labels.append(labels[ids.index(ID)])
                    all_ids.append(col)
                    all_parents.append(parent_id)
                    all_labels.append(labels[cur_len])
                    all_values.append(col_val)
                    cur_len += 1
                break   # only the first matching ID is used per column

    return (
        {'ids': all_ids, 'parents': all_parents,
         'labels': all_labels, 'values': all_values},
        parent_labels
    )


# ── Load CSV ──────────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                         'data', 'installationsList.csv')
data = pd.read_csv(DATA_PATH)

# ── Build sunburst hierarchies ────────────────────────────────────────────────
sunburst = {}
parentslabels_map = {}
for key, h in HIERARCHIES.items():
    df_dict, plabels = build_hierarchy(data, h)
    sunburst[key] = df_dict
    parentslabels_map[key] = plabels

# ── Build dropdown arrays (compute offsets automatically from hierarchy) ──────
# Offsets = number of non-leaf nodes; leaf nodes start at index offset for each hierarchy
AI_h = HIERARCHIES['AI']
IN_h = HIERARCHIES['IN']
SD_h = HIERARCHIES['SD']

AI_offset = len(AI_h['ids'])
IN_offset = len(IN_h['ids'])
SD_offset = len(SD_h['ids'])

labellist  = (sunburst['AI']['labels'][AI_offset:]
            + sunburst['IN']['labels'][IN_offset:]
            + sunburst['SD']['labels'][SD_offset:])
IDlist     = (sunburst['AI']['ids'][AI_offset:]
            + sunburst['IN']['ids'][IN_offset:]
            + sunburst['SD']['ids'][SD_offset:])
parentlist = (parentslabels_map['AI'][AI_offset:]
            + parentslabels_map['IN'][IN_offset:]
            + parentslabels_map['SD'][SD_offset:])

def clean_br(s):
    return re.sub('<br>', ' ', str(s))

dropdown_options = [
    {'label': clean_br(parentlist[i]) + ' | ' + clean_br(labellist[i]),
     'value': labellist[i],
     'id':    IDlist[i]}
    for i in range(len(labellist))
]

# ── Build link options for network visualization ───────────────────────────────
# Intermediate parent node IDs that can be used as edge-coloring categories.
# Mirrors app.py: AI[1:non_subs], IN[1:non_subs], SD[1:-1] then filter.
_multi_prefix = ("TS_", "LS_", "SD_")
_exclude_ids  = {'IT', 'SP', 'IDof', 'ODof'}

_n_AI_ns = len(AI_h['ids']) - len(AI_h['subs'])   # non-sub node count for AI
_n_IN_ns = len(IN_h['ids']) - len(IN_h['subs'])   # non-sub node count for IN

_raw_link_pairs = (
    list(zip(AI_h['ids'][1:_n_AI_ns], AI_h['labels'][1:_n_AI_ns]))
  + list(zip(IN_h['ids'][1:_n_IN_ns], IN_h['labels'][1:_n_IN_ns]))
  + list(zip(SD_h['ids'][1:-1],       SD_h['labels'][1:-1]))        # exclude root & SG_Obj
)

link_options = [
    {'label': clean_br(label), 'value': id_}
    for id_, label in _raw_link_pairs
    if id_ not in _exclude_ids and not id_.startswith(_multi_prefix)
]

# ── Build installations array ─────────────────────────────────────────────────
def safe(val):
    s = str(val)
    return '' if s in ('nan', 'None', 'NaN') else s

installations = []
for i in range(len(data)):
    row = data.iloc[i]
    field_raw = safe(row['Field']) if 'Field' in data.columns else ''
    fieldParts = []
    if field_raw:
        for f in field_raw.split('; '):
            fp = re.sub(' ', '<br>', f.strip())
            if fp and fp not in ('nan', 'None'):
                fieldParts.append(fp)

    inst = {
        'name':        safe(row.iloc[1]),
        'creators':    safe(row.iloc[2]),
        'hyperlink':   safe(row.iloc[3]),
        'year':        safe(row.iloc[6]),
        'publication': safe(row.iloc[5]),
        'fieldParts':  fieldParts,
    }
    na_fields = []
    for col in data.columns[7:]:
        try:
            val = row[col]
            if pd.notna(val) and float(val) == 1.0:
                inst[col] = 1
            elif pd.isna(val):
                na_fields.append(col)
        except (ValueError, TypeError):
            pass
    if na_fields:
        inst['naFields'] = na_fields
    installations.append(inst)

# ── Write js/data.js ─────────────────────────────────────────────────────────
def jsdump(obj):
    return json.dumps(obj, ensure_ascii=False, indent=2)

js_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'js')
os.makedirs(js_dir, exist_ok=True)

out = (
    "// Auto-generated by convert_data.py — do not edit manually.\n"
    "// Re-run: py convert_data.py\n\n"
    "const SUNBURST = "         + jsdump(sunburst)          + ";\n\n"
    "const INSTALLATIONS = "    + jsdump(installations)     + ";\n\n"
    "const DROPDOWN_OPTIONS = " + jsdump(dropdown_options)  + ";\n\n"
    "const LABEL_LIST = "       + jsdump(labellist)         + ";\n\n"
    "const ID_LIST = "          + jsdump(IDlist)            + ";\n\n"
    "const PARENT_LIST = "      + jsdump(parentlist)        + ";\n\n"
    "const LINK_OPTIONS = "     + jsdump(link_options)      + ";\n"
)

outpath = os.path.join(js_dir, 'data.js')
with open(outpath, 'w', encoding='utf-8') as f:
    f.write(out)

print(f"Written {len(installations)} installations, {len(labellist)} dropdown options")
print(f"Sunburst nodes: AI={len(sunburst['AI']['ids'])}, "
      f"IN={len(sunburst['IN']['ids'])}, SD={len(sunburst['SD']['ids'])}")
print(f"Output: {outpath}")
