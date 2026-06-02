from pathlib import Path
from denario import Denario, Research, LLM

PROJECT_DIR = "/srv/hermes_projects/agent_microbial_communities"

DATA_DESCRIPTION = """
Microbial ecology dataset with:
- AMF OTU tables
- bacterial OTU tables
- fungal ITS OTU tables
- eukaryotic OTU tables
- environmental metadata
- diversity metrics

Primary metadata table:
- /srv/hermes_projects/agent_microbial_communities/data/Final_data_with_diversity_prefixed.csv

Available OTU tables:
- /srv/hermes_projects/agent_microbial_communities/data/AMF_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/BAC_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/EUK_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/ITS_OTU_table_final.tsv

Goals:
- discover ecologically meaningful hypotheses
- identify cross-kingdom relationships
- prioritize interpretable analyses
- avoid data leakage
- preserve reproducibility
"""

input_dir = Path(PROJECT_DIR) / "denario_runs" / "input_files"
input_dir.mkdir(parents=True, exist_ok=True)

data_description_path = input_dir / "data_description.md"
data_description_path.write_text(DATA_DESCRIPTION, encoding="utf-8")

research = Research(
    topic="""
Cross-kingdom microbial ecology and environmental drivers
of microbial diversity and composition.
""",
    data_description=DATA_DESCRIPTION,
)

den = Denario(
    research=research,
    project_dir=f"{PROJECT_DIR}/denario_runs"
)

azure_llm = LLM(
    name="gpt-4o-test",
    max_output_tokens=4096,
    temperature=0.5,
)

print("Generating exploratory research idea...")

result = den.get_idea_fast(llm=azure_llm)

print("\n========== RESULT ==========\n")
print(result)
