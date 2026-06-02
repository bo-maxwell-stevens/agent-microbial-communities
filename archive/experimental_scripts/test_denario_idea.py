"""
Minimal Denario idea-generation test for the microbial communities project.

Purpose:
- initialize Denario safely
- use Azure-backed OpenAI-compatible model via Denario's OpenAI pathway
- avoid Gemini defaults
- work around Denario's apparent .tsv path parsing issue by using .txt symlinks
- generate an idea without running analyses or modifying raw data

Run from:
    /srv/hermes_projects/agent_microbial_communities

Usage:
    source .denario_env/bin/activate
    python scripts/test_denario_idea.py
"""

from __future__ import annotations

import os
import pprint
from pathlib import Path

from denario import Denario, LLM, models


PROJECT_DIR = Path("/srv/hermes_projects/agent_microbial_communities")
DATA_DIR = PROJECT_DIR / "data"
LINK_DIR = PROJECT_DIR / "data_denario_links"


# Original raw input files. These are read-only source files.
RAW_FILES = {
    "metadata": DATA_DIR / "Final_data_with_diversity_prefixed.csv",
    "amf_otu": DATA_DIR / "AMF_OTU_table_final.tsv",
    "amf_features": DATA_DIR / "AMF_feature_metadata.tsv",
    "bac_otu": DATA_DIR / "BAC_OTU_table_final.tsv",
    "bac_features": DATA_DIR / "BAC_feature_metadata.tsv",
    "euk_otu": DATA_DIR / "EUK_OTU_table_final.tsv",
    "euk_features": DATA_DIR / "EUK_feature_metadata.tsv",
    "its_otu": DATA_DIR / "ITS_OTU_table_final.tsv",
    "its_features": DATA_DIR / "ITS_feature_metadata.tsv",
}


def check_environment() -> None:
    """Check that required environment variables are present."""
    required = ["OPENAI_API_KEY", "OPENAI_BASE_URL"]
    missing = [x for x in required if not os.environ.get(x)]

    if missing:
        raise RuntimeError(
            "Missing required environment variables: "
            + ", ".join(missing)
            + "\nExpected at least OPENAI_API_KEY and OPENAI_BASE_URL."
        )


def create_denario_links() -> dict[str, Path]:
    """
    Create .txt symlinks to .tsv files because Denario appears to mis-parse
    .tsv paths as .ts in its path validator.

    The symlinks are not raw data copies; they point to the original files.
    """
    LINK_DIR.mkdir(exist_ok=True)

    denario_files: dict[str, Path] = {}

    for key, raw_path in RAW_FILES.items():
        if not raw_path.exists():
            raise FileNotFoundError(f"Missing expected input file: {raw_path}")

        if raw_path.suffix == ".tsv":
            link_path = LINK_DIR / f"{raw_path.stem}.txt"
            if link_path.exists() or link_path.is_symlink():
                link_path.unlink()
            link_path.symlink_to(raw_path)
            denario_files[key] = link_path
        else:
            denario_files[key] = raw_path

    return denario_files


def configure_denario_model() -> LLM:
    """
    Force Denario to use the OpenAI pathway rather than the default Gemini model.

    The model name must match the Azure deployment name exposed through your
    OpenAI-compatible endpoint.
    """
    azure_llm = LLM(
        name="gpt-4o-test",
        max_output_tokens=16384,
        temperature=0.5,
    )

    # Override Denario's built-in gpt-4o entry so internal OpenAI selection uses
    # your Azure deployment name.
    models["gpt-4o"] = azure_llm

    return azure_llm


def build_data_description(denario_files: dict[str, Path]) -> str:
    """Build Denario-compatible data description."""

    file_lines = "\n".join(
        f"- {str(path.resolve())}"
        for path in denario_files.values()
    )

    return f"""
This project contains microbial community data across multiple kingdoms.

Input data files:
{file_lines}

Dataset overview:
- ecological metadata for 99 samples
- AMF OTU tables
- bacterial OTU tables
- ITS fungal OTU tables
- eukaryotic OTU tables
- associated feature metadata tables

Important constraints:
- raw data must remain unchanged
- analyses should be reproducible
- prioritize interpretable ecological analyses
- avoid data leakage
- treat relationships as correlational unless explicitly tested
"""

def summarize_denario_object(den: Denario) -> None:
    """
    Print useful Denario object attributes after running idea generation.
    This helps determine where Denario stores the generated idea.
    """
    print("\n--- Denario object attributes likely to contain generated state ---")
    for attr in [
        "research",
        "idea",
        "ideas",
        "journal",
        "project_dir",
        "data_description",
    ]:
        if hasattr(den, attr):
            value = getattr(den, attr)
            print(f"\n[{attr}]")
            pprint.pp(value)


def main() -> None:
    check_environment()

    denario_files = create_denario_links()
    azure_llm = configure_denario_model()

    den = Denario(project_dir=str(PROJECT_DIR))
    prompt = build_data_description(denario_files)

    print("Setting Denario data description...")
    den.set_data_description(prompt)

    print("\nRunning Denario get_idea_fast()...")
    print("This should generate an idea only; it should not run analyses.")
    result = den.get_idea_fast(llm=azure_llm)

    print("\n--- Raw return value from get_idea_fast() ---")
    pprint.pp(result)

    summarize_denario_object(den)

    print("\nDone.")


if __name__ == "__main__":
    main()
