"""
phase3_environmental_partitioning.py

This script performs environmental association analysis and residual Mantel tests to explore
relationships between environmental variables and microbial communities.

Workflow:
1. Load environmental and microbial data.
2. Preprocess and normalize datasets.
3. Conduct environmental association analysis.
4. Perform Mantel tests (including residual Mantel tests).
5. Save results and log outputs.

Outputs are saved to the `results/` directory.
"""

# Required Libraries
import os
import pandas as pd
import numpy as np
from scipy.spatial import distance
from scipy.stats import spearmanr
from sklearn.preprocessing import StandardScaler

# Define constants
RESULTS_DIR = "results/phase3_environmental_partitioning/"
os.makedirs(RESULTS_DIR, exist_ok=True)

def load_data():
        """
        Loads environmental and microbial data from the `data/` directory.
        Returns:
                environmental_data (pd.DataFrame): Environmental variables.
                microbial_data (pd.DataFrame): Microbial OTU abundances.
                sample_col (str): Sample ID column name.
        """
        def choose_meta_sample_col(metadata):
                for col in ["SampleID", "sample_id", "canonical"]:
                        if col in metadata.columns:
                                return col
                raise ValueError("No suitable sample identifier column found!")

        env_path = "data/Final_data_with_diversity_prefixed.csv"
        micro_path = "data/AMF_OTU_table_final.tsv"

        environmental_data = pd.read_csv(env_path, sep=",", low_memory=False)
        sample_col = choose_meta_sample_col(environmental_data)

        # Exclude columns with microbial/taxonomic prefixes or identifiers
        prefixes = [
                "Bac_", "Euk_", "ITS_", "AMF_", "VTX", "VT", "OTU", "ASV", "taxonomy",
                "taxon", "phylum", "class", "order", "family", "genus", "species"
                # Legitimate environmental metadata (e.g., site, climate) should not match these patterns
        ]
        # Debugging: Print all columns before filtering
        print("All columns in environmental data:", environmental_data.columns.tolist())

        # Identify numeric environmental variables not matching excluded prefixes
        print("Filtering environmental variables with prefixes:", prefixes)    # Debugging
        numeric_cols = [
                col for col in environmental_data.select_dtypes(include=[np.number]).columns 
                if not any(col.lower().startswith(prefix.lower()) or col.lower().__contains__(prefix.lower()) for prefix in prefixes)
        ]
        # Debugging: Validate excluded columns
        excluded_matches = [col for col in environmental_data.columns if any(col.lower().startswith(prefix.lower()) for prefix in prefixes)]
        print("Excluded columns (debug):", excluded_matches)

        environmental_data = environmental_data[[sample_col] + list(numeric_cols)]

        microbial_data = pd.read_csv(micro_path, sep="\t")

        return environmental_data, microbial_data, sample_col

def preprocess_data(environmental_data, microbial_data, sample_col):
        """
        Preprocesses environmental and microbial data.
        Saves environmental variable inventory and aligns sample IDs.

        Args:
                environmental_data (pd.DataFrame): Environmental metadata
                microbial_data (pd.DataFrame): Microbial abundance data
                sample_col (str): Identifier for samples

        Excludes constant columns and updates `validation_summary.txt`.

        Returns:
                Tuple: Filtered environmental and microbial data
        """
        excluded_cols = [col for col in environmental_data.columns if col not in [sample_col] + list(environmental_data.columns[1:])]
        retained_cols = [sample_col] + list(environmental_data.columns[1:])

from scripts.analysis.external_validation_summary_writer import write_validation_summary
write_validation_summary(excluded_cols=excluded_cols, retained_cols=retained_cols)

write_validation_summary(excluded_cols, retained_cols)
        summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
        summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
        excluded_cols = [col for col in environmental_data.columns if col not in [sample_col] + list(environmental_data.columns[1:])]
        retained_cols = [sample_col] + list(environmental_data.columns[1:])

        if excluded_cols:
            summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
        else:
            summary_file.write("No microbial/taxonomic columns were excluded.\n")

        if retained_cols:
            summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
        else:
                    summary_file.write("No columns were retained.\n")
                            
                                        summary_file.write("No columns were retained.\n")
                        
                        
                        
from scripts.analysis.external_validation_summary_writer import write_validation_summary
write_validation_summary(excluded_cols=excluded_cols, retained_cols=retained_cols)

write_validation_summary(excluded_cols, retained_cols)
    summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
    summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
    excluded_cols = [col for col in environmental_data.columns if col not in [sample_col] + list(environmental_data.columns[1:])]
    retained_cols = [sample_col] + list(environmental_data.columns[1:])

    if excluded_cols:
        summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
    else:
        summary_file.write("No microbial/taxonomic columns were excluded.\n")

    if retained_cols:
        summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
    else:
                summary_file.write("No columns were retained.\n")
                        
                                        summary_file.write("No columns were retained.\n")
                summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n\n")
except Exception as error:
        print(f"Error writing validation summary: {error}")
                        except Exception as error:
                                print(f"Error in writing to summary: {error}")
                        
                        summary_file.write("No microbial/taxonomic columns were excluded.\n\n")

                        pass
                                summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
                        
                                        summary_file.write("No columns were retained.\n")

        # Identify constant columns (no variability)
        constant_cols = [col for col in environmental_data.columns if col != sample_col and environmental_data[col].nunique() == 1]

        # Update validation summary for constant columns
        print(f"Constant environmental columns excluded: {constant_cols}")
        print(f"Excluded columns identified during initial metadata processing: {excluded_cols}")
        print("Debug: Writing validation summary.")
from scripts.analysis.external_validation_summary_writer import write_validation_summary
write_validation_summary(excluded_cols=excluded_cols, retained_cols=retained_cols)

write_validation_summary(excluded_cols, retained_cols)
    summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
    summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
    excluded_cols = [col for col in environmental_data.columns if col not in [sample_col] + list(environmental_data.columns[1:])]
    retained_cols = [sample_col] + list(environmental_data.columns[1:])

    if excluded_cols:
        summary_file.write("Excluded microbial/taxonomic columns:\n" + "\n".join(excluded_cols) + "\n")
    else:
        summary_file.write("No microbial/taxonomic columns were excluded.\n")

    if retained_cols:
        summary_file.write("Retained environmental columns:\n" + "\n".join(retained_cols) + "\n")
    else:
                summary_file.write("No columns were retained.\n")
                        
                                        summary_file.write("No columns were retained.\n")
                        if constant_cols:
        
                except Exception as e:
                print(f"Error writing validation_summary.txt: {str(e)}")
                        summary_file.write("\nConstant environmental columns:\n" + "\n".join(constant_cols) + "\n")

        # Remove constant columns before scaling
        environmental_data = environmental_data.drop(columns=constant_cols, errors='ignore')

        # Impute missing values before scaling
        environmental_data.iloc[:, 1:] = environmental_data.iloc[:, 1:].fillna(environmental_data.iloc[:, 1:].mean())
        scaler = StandardScaler()
        print(f"Before scaling - any NaN values in environmental data: {environmental_data.isna().any().any()}")
        if len(environmental_data.columns) > 1:
                scaled_environment = scaler.fit_transform(
                        environmental_data.iloc[:, 1:].astype(np.float64)
                )
                for idx, col in enumerate(environmental_data.columns[1:]):
                        environmental_data[col] = scaled_environment[:, idx].astype(np.float64)

        microbial_data.iloc[:, 1:] = microbial_data.iloc[:, 1:].div(
                microbial_data.iloc[:, 1:].sum(axis=1), axis=0
        )

        common_ids = set(environmental_data[sample_col]) & set(microbial_data.iloc[:, 0])
        print(f"Debug - Common sample IDs count: {len(common_ids)}")
        environmental_data = environmental_data[
                environmental_data[sample_col].isin(common_ids)
        ].set_index(sample_col)
        microbial_data = microbial_data[
                microbial_data.iloc[:, 0].isin(common_ids)
        ].set_index(microbial_data.columns[0])

        return environmental_data, microbial_data

def perform_environmental_association(environmental_data, microbial_data):
        """
        Conduct correlations between environmental variables and OTUs.
        Save results.
        """
        results = []
        for env_col in environmental_data.columns:
                for otu_col in microbial_data.columns:
                        corr, p = spearmanr(environmental_data[env_col], microbial_data[otu_col])
                        results.append({"Environment": env_col, "OTU": otu_col, "Correlation": corr, "P": p})

        pd.DataFrame(results).to_csv(f"{RESULTS_DIR}/environmental_associations.csv", index=False)


def perform_mantel_test(environmental_data, microbial_data):
        """
        Conduct Mantel test between environmental and microbial distances.
        Save results.
        """
        env_dist = distance.pdist(StandardScaler().fit_transform(environmental_data))
        print(f"Environmental distance matrix shape: {env_dist.shape}")
        micro_dist = distance.pdist(microbial_data)

        print(f"Microbial distance matrix shape: {micro_dist.shape}")
        print(f"Environmental distance matrix (sample): {env_dist[:5]}")
        print(f"Microbial distance matrix (sample): {micro_dist[:5]}")

        corr, p = spearmanr(env_dist, micro_dist)
        with open(f"{RESULTS_DIR}/mantel_results.txt", "w") as file:
                file.write(f"Correlation: {corr}, P: {p}")
        return {"Correlation": corr, "P": p}

def perform_residual_mantel_test(environmental_data, microbial_data):
        """
        Conduct residual Mantel test using Ridge regression for stabilization of covariates.
        Save results in a structured format.
        """
        from sklearn.impute import SimpleImputer
        imputer = SimpleImputer(strategy='mean')
        scaled_env = StandardScaler().fit_transform(
                np.nan_to_num(imputer.fit_transform(environmental_data), nan=0.0)
        )
        from sklearn.linear_model import Ridge
        ridge = Ridge(alpha=1e-5)
        ridge.fit(
                scaled_env, 
                microbial_data.fillna(microbial_data.mean()).values
        )
        residual_data = microbial_data - scaled_env @ ridge.coef_.T

        res_dist = distance.pdist(residual_data)
        corr, p = spearmanr(distance.pdist(scaled_env), res_dist, nan_policy='omit')

        with open(f"{RESULTS_DIR}/residual_mantel_results.txt", "w") as file:
                file.write(f"Residual Correlation: {corr}, P: {p}")

def main():
        environmental_data, microbial_data, sample_col = load_data()
        environmental_data, microbial_data = preprocess_data(environmental_data, microbial_data, sample_col)
        perform_environmental_association(environmental_data, microbial_data)
        perform_mantel_test(environmental_data, microbial_data)
        perform_residual_mantel_test(environmental_data, microbial_data)

if __name__ == "__main__":
        main()