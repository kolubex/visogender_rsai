"""
This file either creates or updates an existing benchmark file with the resolution bias scores for CLIP-like and captioning models. 
This file also checks if the preliminary results have been run in isolation, and if not, these scores are calculated as well. 

Authors: @smhall97, @abrantesfg
"""
import os
import sys
import subprocess
import json
import copy

main_dir = os.getcwd().split("analysis")[0]
result_dir = os.path.join(main_dir, "results/model_outputs")
saving_path = os.path.join(main_dir, "results/resolution_bias_analysis/preliminary_analysis")
benchmark_path = os.path.join(main_dir, "results/finegrain_scores")
sys.path.append(main_dir) 

from src.data_utils import load_full_dataframe, check_op_and_oo_both_exist_preliminary_analysis
from src.analysis_utils import get_subset_dataframe, load_benchmark_dict, single_person_res_acc, two_person_res_acc, overall_res_acc


clip_models = ["clip"]
captioning_models = ["blipv2"]

# model_list = clip_models + captioning_models
model_list = clip_models

for model_name in model_list:

    # names based on original json as saved by output from models
    if model_name in clip_models:
        file_desc = f"clip_{model_name}" 
        exp_desc = "CLIP" 

    elif model_name in captioning_models:
        file_desc = f"captioning_{model_name}" 
        exp_desc = "CAPTIONING" 

    file_check = check_op_and_oo_both_exist_preliminary_analysis(saving_path, model_name)

    if not file_check:
        subprocess.run(["python", "run_preliminary_analysis.py"])
    
    full_df = load_full_dataframe(saving_path)

    output_file_name = f"benchmark_results_{exp_desc}_{model_name}.json"
    
    oo_subset_df = get_subset_dataframe(full_df, "context_OO", exp_desc, model_name)
    op_subset_df = get_subset_dataframe(full_df, "context_OP", exp_desc, model_name)
    
    # Define a list of sectors
    sectors = ["education", "medical", "office", "retail", "service"]
    occupations = ["teacher", "instructor", "counsellor", "physician", "specialist", "doctor", "lawyer", "paralegal",
                "accountant", "auditor", "broker", "advisor", "architect", "engineer", "supervisor", "clerk",
                "manager", "baker", "waiter", "bartender", "hairdresser", "veterinarian", "painter"]
    specialisations = ["institutional", "general_courses", "mental_health", "hospital_worker", "legal", "financial",
                    "structure", "general_office", "customer_facing", "food_service", "fashion", "animal", "household"]

    benchmark_dict = {"metadata": {"experiment_desc": f"{exp_desc}", "model_name": f"{model_name}"},
                        "resolution_bias": {"all_images": {"overall_accuracy": None},
                                            "single_person_images": {"RA_avg": None, "gender_gap": None},
                                            "two_person_images": {"RA_avg": None, "gender_gap": None},
                                            "two_person_images_same_gender": {"RA_avg": None, "gender_gap": None},
                                            "two_person_images_diff_gender": {"RA_avg": None, "gender_gap": None}
                                            },
                        "retrieval_bias": {"bias@5": {"mean": None, "sigma": None}, 
                                            "bias@10": {"mean": None, "sigma": None},
                                            "maxskew@5": {"mean": None, "sigma": None},
                                            "maxskew@10": {"mean": None, "sigma": None},
                                            "NDKL": {"mean": None, "sigma": None}
                                            }
                        }


    # Initialize a dictionary to store sector data for all sectors
    all_sector_benchmark_data = {}
    all_factor_benchmark_data = {}
    sections = {"sector":sectors,"occ":occupations,"specialisation":specialisations}
    
    for value in sections:
        all_factor_benchmark_data[value] = {}

    for value,section in sections.items():
        for factor in section:
            # Filter DataFrame for the current sector in both contexts
            oo_factor_df = oo_subset_df[oo_subset_df[value] == factor]
            op_factor_df = op_subset_df[op_subset_df[value] == factor]
            
            oo_res_acc = single_person_res_acc(oo_factor_df, benchmark_dict, exp_desc, model_name, "Context_OO")
            op_two_person_res_acc = two_person_res_acc(op_factor_df, benchmark_dict, exp_desc, model_name, "Context_OP")

            factor_benchmark_dict = overall_res_acc(benchmark_dict)
            factor_benchmark_dict_copy = copy.deepcopy(factor_benchmark_dict)
        
            # Add factor benchmark data to the all_factor_benchmark_data dictionary
            all_factor_benchmark_data[value][factor] = factor_benchmark_dict_copy
        
with open(os.path.join(benchmark_path,output_file_name), "w") as f:
    json.dump(all_factor_benchmark_data, f, indent=4)
print(f"Saved under {benchmark_path}/{output_file_name}")

