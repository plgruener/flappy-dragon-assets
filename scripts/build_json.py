import os
import json
import utils

if __name__ == "__main__":
    ASSET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dump")
    OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    utils.load_data(ASSET_DIR)
    file_data = (
        ("dragons", utils.DRAGONS),
        ("eggs", utils.EGGS),
        ("worlds", utils.WORLDS),
        ("augments", utils.AUGMENTS),
    )
    for fd in file_data:
        with open(os.path.join(OUTPUT_DIR, f"{fd[0]}.json"), "w", encoding="utf-8", newline="\n") as json_file:
            json.dump([d.data for d in fd[1].values()], json_file, indent=4, ensure_ascii=False)
            json_file.write("\n")
