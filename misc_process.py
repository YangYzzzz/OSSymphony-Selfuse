import os
import json
import random
import math
def get_result(target_dir):
    if not os.path.exists(target_dir):
        print("New experiment, no result yet.")
        return None

    all_result = []
    domain_result = {}
    all_result_for_analysis = {}

    for domain in os.listdir(target_dir):
        domain_path = os.path.join(target_dir, domain)
        if os.path.isdir(domain_path):
            for example_id in os.listdir(domain_path):
                example_path = os.path.join(domain_path, example_id)
                if os.path.isdir(example_path):
                    if "result.txt" in os.listdir(example_path):
                        # empty all files under example_id
                        if domain not in domain_result:
                            domain_result[domain] = []
                        result = open(os.path.join(example_path, "result.txt"), "r").read()
                        try:
                            domain_result[domain].append(float(result))
                        except:
                            domain_result[domain].append(float(eval(result)))

                        if domain not in all_result_for_analysis:
                            all_result_for_analysis[domain] = {}
                        all_result_for_analysis[domain][example_id] = domain_result[domain][-1]

                        try:
                            result = open(os.path.join(example_path, "result.txt"), "r").read()
                            try:
                                all_result.append(float(result))
                            except:
                                all_result.append(float(bool(result)))
                        except:
                            all_result.append(0.0)

    with open("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive.json", "r", encoding="utf-8") as f:
        origin_tasks = json.load(f)
    filterd_difficult_tasks = {}
    diffi_count = 0
    for domain, origin_task_list in origin_tasks.items():
        for task in origin_task_list:
            if task not in all_result_for_analysis[domain] or all_result_for_analysis[domain][task] == 0.0:
                if domain not in filterd_difficult_tasks:
                    filterd_difficult_tasks[domain] = []
                filterd_difficult_tasks[domain].append(task)
                diffi_count += 1
    print(f'困难任务共计: {diffi_count} 个')
    with open("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive_diffi_subset.json", "w") as f:
        json.dump(filterd_difficult_tasks, f, indent=4, ensure_ascii=False)

    for domain in domain_result:
        print("Domain:", domain, "Runned:", len(domain_result[domain]), "Success Rate:",
              sum(domain_result[domain]) / len(domain_result[domain]) * 100, "%")

    # print(">>>>>>>>>>>>>")
    # print("Office", "Success Rate:", sum(
    #     domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result[
    #         "libreoffice_writer"]) / len(
    #     domain_result["libreoffice_calc"] + domain_result["libreoffice_impress"] + domain_result[
    #         "libreoffice_writer"]) * 100, "%")
    # print("Daily", "Success Rate:",
    #       sum(domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]) / len(
    #           domain_result["vlc"] + domain_result["thunderbird"] + domain_result["chrome"]) * 100, "%")
    # print("Professional", "Success Rate:", sum(domain_result["gimp"] + domain_result["vs_code"]) / len(
    #     domain_result["gimp"] + domain_result["vs_code"]) * 100, "%")

    with open(os.path.join(target_dir, "all_result.json"), "w") as f:
        f.write(str(all_result_for_analysis))

    if not all_result:
        print("New experiment, no result yet.")
        return None
    else:
        print("Runned:", len(all_result), "Current Success Rate:", sum(all_result) / len(all_result) * 100, "%")
        return all_result

def filter_task_ids(data: dict) -> dict:
    """
    Filters a dictionary of lists, keeping approximately one-third of the items
    in each list, selected randomly.

    Args:
        data: A dictionary where keys are domain names (str) and values are
              lists of task IDs (list of str).

    Returns:
        A new dictionary with the same keys but with randomly sampled,
        smaller lists as values.
    """
    # Create an empty dictionary to hold the filtered results.
    filtered_data = {}

    # Iterate over each domain and its list of task IDs.
    for domain, id_list in data.items():
        original_length = len(id_list)

        # --- Core Logic ---
        # Calculate how many items to keep (approximately 1/3 of the original).
        # We use math.ceil to round up, ensuring that for lists with 1 or 2 items,
        # we still keep 1. For an empty list, it will correctly result in 0.
        num_to_keep = math.ceil(original_length / 3)

        # Use random.sample() to select a random, unique subset of the list.
        # This is more direct than shuffling and slicing.
        sampled_list = random.sample(id_list, num_to_keep)
        
        # Sort the result for consistent and clean output.
        sampled_list.sort()
        
        # Store the new, smaller list in our result dictionary.
        filtered_data[domain] = sampled_list
        
    return filtered_data

def instruction_statistcs(json_path):
    root_dir = "/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/examples"
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    instruction_list = []
    for domain, task_list in data.items():
        domain_dir = os.path.join(root_dir, domain)
        for task in task_list:
            task_file = os.path.join(domain_dir, f'{task}.json')
            with open(task_file, "r", encoding="utf-8") as f:
                task_data = json.load(f)
            instruction_list.append(task_data['instruction'])

    with open('instruciton.json', "w", encoding="utf-8") as f:
        json.dump(instruction_list, f, indent=4)

def process_another_diff_subset():
    diff_valid_path = "/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive_diffi_subset_for_valid.json"
    diff_path = "/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive_diffi_subset.json"
    with open(diff_valid_path, "r") as f:
        diff_valid_data = json.load(f)
    with open(diff_path, 'r') as f:
        diff_data = json.load(f)
    diff_another_data = {}
    for d, t_list in diff_data.items():
        if d not in diff_another_data:
            diff_another_data[d] = []
        for t in t_list:
            if t not in diff_valid_data[d]:
                diff_another_data[d].append(t)
    with open("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive_diffi_subset_for_another_valid.json", "w") as f:
        json.dump(diff_another_data, f, indent=4)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    process_another_diff_subset()
    # environment config
    # parser.add_argument("--root_dir", type=str, default="")
    # args = parser.parse_args()
    # # get_result(args.root_dir)
    # instruction_statistcs("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive.json")
    # filtered_data = filter_task_ids(json.load(open("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive_diffi_subset_for_valid.json", "r")))
    # json.dump(filtered_data, open("/nvme/yangbowen/yangbowen/OSWorld/evaluation_examples/test_nogdrive_diffi_subset_for_valid.json", "w"), indent=4)
