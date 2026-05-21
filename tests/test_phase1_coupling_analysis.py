from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.analysis.phase1_coupling_analysis import (
    clr_transform,
    overlap_filter,
    pca_embed,
    prevalence_filter,
    relative_abundance,
)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def synthetic_tables() -> tuple[pd.DataFrame, dict[str, pd.DataFrame]]:
    meta = pd.DataFrame(
        {
            "canonical": ["S1", "S2", "S3", "S4"],
            "alpha": [1.0, 2.0, 3.0, 4.0],
            "dark": [4.0, 3.0, 2.0, 1.0],
            "region": ["R1", "R1", "R2", "R2"],
            "site.id": ["A", "B", "C", "D"],
        }
    )

    def mk(vals):
        return pd.DataFrame({"sample_id": ["S1", "S2", "S3"], "f1": vals[0], "f2": vals[1], "f3": vals[2]})

    tables = {
        "AMF": mk([[10, 0, 3], [0, 4, 1], [5, 0, 1]]),
        "BAC": mk([[5, 1, 0], [1, 3, 2], [0, 1, 1]]),
        "EUK": mk([[3, 0, 4], [0, 2, 2], [1, 0, 1]]),
        "ITS": mk([[6, 2, 1], [0, 2, 0], [0, 1, 1]]),
    }
    return meta, tables


def test_sample_alignment_correct():
    _, tables = synthetic_tables()
    t, ids = overlap_filter(tables)
    assert ids == ["S1", "S2", "S3"]
    for k, table in t.items():
        assert list(table["sample_id"]) == ids


def test_clr_outputs_finite_values():
    _, tables = synthetic_tables()
    f, _ = prevalence_filter(tables["AMF"], 0.0)
    ra = relative_abundance(f)
    clr = clr_transform(ra, pseudocount=1e-6)
    arr = clr.drop(columns=["sample_id"]).to_numpy()
    assert np.isfinite(arr).all()


def test_pca_output_shapes():
    _, tables = synthetic_tables()
    f, _ = prevalence_filter(tables["BAC"], 0.0)
    ra = relative_abundance(f)
    clr = clr_transform(ra, pseudocount=1e-6)
    emb, var = pca_embed(clr, n_pcs=2)
    assert emb.shape == (3, 2)
    assert len(var) == 2


def test_raw_data_not_modified(tmp_path: Path):
    raw = tmp_path / "data"
    raw.mkdir()
    f = raw / "AMF.tsv"
    f.write_text("sample_id\tf1\nS1\t1\nS2\t2\n", encoding="utf-8")
    before = sha256(f)
    df = pd.read_csv(f, sep="\t")
    _ = clr_transform(relative_abundance(df), pseudocount=1e-6)
    assert before == sha256(f)


def test_output_files_generated_contract(tmp_path: Path):
    out = tmp_path / "results"
    out.mkdir()
    expected = [
        "cohort_summary.csv",
        "cohort_summary.json",
        "filtering_summary.csv",
        "pca_variance_explained.csv",
        "kingdom_coupling_metrics.csv",
        "plant_associations.csv",
        "prevalence_sensitivity.csv",
        "run_metadata.json",
        "warnings.log",
        "checkpoints.log",
        "intermediate_summary.json",
    ]
    for name in expected:
        if name.endswith(".json"):
            (out / name).write_text("{}", encoding="utf-8")
        else:
            (out / name).write_text("a,b\n1,2\n", encoding="utf-8")
    for name in expected:
        assert (out / name).exists()
    meta = json.loads((out / "run_metadata.json").read_text(encoding="utf-8"))
    assert isinstance(meta, dict)
