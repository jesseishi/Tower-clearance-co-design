import json
import shutil
import sqlite3
import os

import numpy as np

SRC, DST = (
    "data/co-design/baseline_28823409/baseline.sql",
    "data/co-design/baseline_28823409/baseline_slim.sql",
)

# Promoted name (as in your dict) -> absolute name (as stored in the recorder)
abs_names = {
    "hub.cone": "wisdem.wt.wt_prop.wt_init.hub.hub_indep_vars.cone",
    "nacelle.overhang": "wisdem.wt.wt_prop.wt_init.nacelle.nac_indep_vars.overhang",
    "nacelle.uptilt": "wisdem.wt.wt_prop.wt_init.nacelle.nac_indep_vars.uptilt",
}

all_outputs = {
    # Did the run have a failure.
    "openfast_failed": {
        "key": "aeroelastic.openfast_failed",
        "scaling": lambda x: x[0],
        "label": "Openfast failed",
    },
    # ROSCO variables.
    "TCIPC_MaxTipDeflection": {
        "key": "tune_rosco_ivc.TCIPC_MaxTipDeflection",
        "scaling": lambda x: x[0],
        "label": "TCIPC deflection reference (m)",
    },
    "ps_percent": {
        "key": "tune_rosco_ivc.ps_percent",
        "scaling": lambda x: x[0],
        "label": "Peak shaving (-)",
    },
    "max_thrust_percent": {
        "key": "tune_rosco_ivc.ps_percent",
        "scaling": lambda x: 100 * x[0],
        "label": "Max thrust (%)",
    },
    "TCIPC_nHarmonics": {
        "key": "tune_rosco_ivc.TCIPC_nHarmonics",
        "scaling": lambda x: x[0],
        "label": "Number of harmonics",
    },
    "TCIPC_ZeroYawDeflection": {
        "key": "tune_rosco_ivc.TCIPC_ZeroYawDeflection",
        "scaling": lambda x: x[0],
        "label": "Zero yaw deflection",
    },
    "TCIPC_MaxPitchAmplitude": {
        "key": "tune_rosco_ivc.TCIPC_MaxPitchAmplitude",
        "scaling": lambda x: np.round(np.rad2deg(x[0]), 1),
        "label": "TCIPC max pitch amplitude (deg)",
    },
    # Design variables
    "cone": {
        "key": "hub.cone",
        "scaling": lambda x: np.rad2deg(x[0]),
        "label": "Cone angle (deg)",
    },
    "tilt": {
        "key": "nacelle.uptilt",
        "scaling": lambda x: np.rad2deg(x[0]),
        "label": "Tilt angle (deg)",
    },
    "overhang": {
        "key": "nacelle.overhang",
        "scaling": lambda x: x[0],
        "label": "Overhang (m)",
    },
    # Objective.
    "aep": {
        "key": "aeroelastic.AEP",
        "scaling": lambda x: 1e-6 * x[0],
        "label": "AEP (GWh)",
    },
    # Constraints.
    "max_eff_TipDxc_towerPassing": {
        "key": "aeroelastic.max_eff_TipDxc_towerPassing",
        "scaling": lambda x: x[0],
        "label": "max_eff_TipDxc_towerPassing",
    },
    "tower_clearance": {
        "key": "aeroelastic.minimum_tower_clearance",
        "scaling": lambda x: x[0],
        "label": "Tower clearance (m)",
    },
    "eff_tower_clearance": {
        "key": "aeroelastic.minimum_eff_tower_clearance",
        "scaling": lambda x: x[0],
        "label": "Tower clearance (m)",
    },
    "eff_tower_clearance_DLC": {
        "key": "aeroelastic.minimum_eff_tower_clearance_DLC",
        "scaling": lambda x: x[0],
        "label": "Tower clearance (m)",
    },
    "eff_tower_clearance_URef": {
        "key": "aeroelastic.minimum_eff_tower_clearance_URef",
        "scaling": lambda x: x[0],
        "label": "Tower clearance (m)",
    },
    # Structural loads.
    "max_eff_TwrBsMyt": {
        "key": "aeroelastic.max_eff_TwrBsMyt",
        "scaling": lambda x: x[0] / 1000,
        "label": "Tower ultimate (MNm)",
    },
    "max_eff_TwrBsMyt_DLC": {
        "key": "aeroelastic.max_eff_TwrBsMyt_DLC",
        "scaling": lambda x: str(x[0]),
        "label": "Max tower base Myt DLC (-)",
    },
    "max_eff_TwrBsMyt_URef": {
        "key": "aeroelastic.max_eff_TwrBsMyt_URef",
        "scaling": lambda x: x[0],
        "label": "Max tower base Myt U (m/s)",
    },
    "DEL_TwrBsMyt": {
        "key": "aeroelastic.DEL_TwrBsMyt",
        "scaling": lambda x: x[0] / 1000,
        "label": "Tower fatigue (MNm)",
    },
    "max_eff_RootMyb": {
        "key": "aeroelastic.max_eff_RootMyb",
        "scaling": lambda x: x[0] / 1000,
        "label": "Blade ultimate (MNm)",
    },
    "max_eff_RootMyb_DLC": {
        "key": "aeroelastic.max_eff_RootMyb_DLC",
        "scaling": lambda x: str(x[0]),
        "label": "Max root Myb DLC (-)",
    },
    "max_eff_RootMyb_URef": {
        "key": "aeroelastic.max_eff_RootMyb_URef",
        "scaling": lambda x: x[0],
        "label": "Max root Myb U (m/s)",
    },
    "DEL_RootMyb": {
        "key": "aeroelastic.DEL_RootMyb",
        "scaling": lambda x: x[0] / 1000,
        "label": "Blade fatigue (MNm)",
    },
    # Control activity.
    "max_pitch_rate_sim": {
        "key": "aeroelastic.max_pitch_rate_sim",
        "scaling": lambda x: x[0],
        "label": "Max pitch rate (deg/s)",
    },
    "max_pitch_rate_sim_DLC": {
        "key": "aeroelastic.max_pitch_rate_sim_DLC",
        "scaling": lambda x: str(x[0]),
        "label": "Max pitch rate DLC (-)",
    },
    "max_pitch_rate_sim_URef": {
        "key": "aeroelastic.max_pitch_rate_sim_U",
        "scaling": lambda x: x[0],
        "label": "Max pitch rate U (m/s)",
    },
    "avg_pitch_travel": {
        "key": "aeroelastic.avg_pitch_travel",
        "scaling": lambda x: x[0],
        "label": "Avg pitch travel (deg)",
    },
}

dict_keys = {v["key"] for v in all_outputs.values()}
keep = (dict_keys - set(abs_names)) | set(abs_names.values())
keep_prefixes = ("_auto_ivc.",)  # small; drop this line to save a bit more space
found = set()


def slim(s):
    if not isinstance(s, str) or s in ("", "{}"):
        return s
    d = json.loads(s)
    out = {k: v for k, v in d.items() if k in keep or k.startswith(keep_prefixes)}
    found.update(k for k in out if k in keep)
    return json.dumps(out)


shutil.copy(SRC, DST)
con = sqlite3.connect(DST)
ids = [r[0] for r in con.execute("SELECT id FROM driver_iterations")]

for i, rid in enumerate(ids, 1):
    inp, outp = con.execute(
        "SELECT inputs, outputs FROM driver_iterations WHERE id=?", (rid,)
    ).fetchone()
    con.execute(
        "UPDATE driver_iterations SET inputs=?, outputs=? WHERE id=?",
        (slim(inp), slim(outp), rid),
    )
    if i % 10 == 0:
        con.commit()
    print(f"{i}/{len(ids)}", end="\r")

con.commit()
con.execute("VACUUM")
con.close()
print("\nKept:", len(found), "of", len(keep))
print("Never matched:", sorted(keep - found))

full_mb = os.path.getsize(SRC) / 1e6
slim_mb = os.path.getsize(DST) / 1e6
print(f"\nFull file: {full_mb:,.1f} MB")
print(f"Slim file: {slim_mb:,.1f} MB")
print(f"Reduction: {100 * (1 - slim_mb / full_mb):.1f}%")
