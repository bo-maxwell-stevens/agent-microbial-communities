prompt = """
This project contains microbial community data for bacteria, AMF, ITS fungi,
and broader eukaryotes, plus environmental metadata.

Use these exact input data files:
- /srv/hermes_projects/agent_microbial_communities/data/Final_data_with_diversity_prefixed.csv
- /srv/hermes_projects/agent_microbial_communities/data/AMF_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/AMF_feature_metadata.tsv
- /srv/hermes_projects/agent_microbial_communities/data/BAC_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/BAC_feature_metadata.tsv
- /srv/hermes_projects/agent_microbial_communities/data/EUK_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/EUK_feature_metadata.tsv
- /srv/hermes_projects/agent_microbial_communities/data/ITS_OTU_table_final.tsv
- /srv/hermes_projects/agent_microbial_communities/data/ITS_feature_metadata.tsv

Rules:
- Do not modify raw data.
- Treat the data directory as read-only.
- Prefer exploratory, reproducible, interpretable ecological analyses.
- Focus on candidate research questions, not final claims.
"""
