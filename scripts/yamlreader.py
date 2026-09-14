import os
import json
import yaml

_loader = yaml.CFullLoader


def _unknown(loader, suffix, node):
    if isinstance(node, yaml.ScalarNode):
        constructor = loader.__class__.construct_scalar
    elif isinstance(node, yaml.SequenceNode):
        constructor = loader.__class__.construct_sequence
    elif isinstance(node, yaml.MappingNode):
        constructor = loader.__class__.construct_mapping
    return constructor(loader, node)


yaml.add_multi_constructor("!", _unknown, Loader=_loader)
yaml.add_multi_constructor("tag:", _unknown, Loader=_loader)


def load_yaml(file_path):
    with open(file_path, "r", encoding="UTF-8", newline="\n") as in_file:
        contents = yaml.load(in_file, Loader=_loader)
    json_data = json.loads(json.dumps(contents["MonoBehaviour"]).encode().decode("raw_unicode_escape"))
    meta_file = f"{file_path}.meta"
    if os.path.exists(meta_file):
        with open(meta_file, "r", encoding="UTF-8") as in_file:
            contents = yaml.load(in_file, Loader=_loader)
        json_data["_guid"] = contents["guid"]
    else:
        json_data["_guid"] = ""
    return json_data
