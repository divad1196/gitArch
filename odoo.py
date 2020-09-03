import os
from pathlib import Path
from .tools import load_json, json_dump, parent_dir
from .defaults import DEFAULT_REPOSITORY_ADDONS_FILENAME

def is_odoo_module(path):
    dir_list = os.listdir(path)
    manifests = [
        "__manifest__.py",
        "__openerp__.py"
    ]
    return any(manifest in dir_list for manifest in manifests)


def find_odoo_modules(path=Path()):
    path = Path(path)
    modules = []
    dir_list = os.listdir(path)
    if is_odoo_module(path):
        modules.append(path)
    else:
        for p in dir_list:
            next_path = path.joinpath(p)
            if next_path.is_dir():
                modules += find_odoo_modules(next_path)
    return modules

def find_odoo_addons(modules):
    paths = list(set([ parent_dir(module).resolve() for module in modules]))
    return paths

def gather_addons_infos(modules, base_path=Path.home()):
    base_path = Path(base_path).resolve()
    registry = {}

    for m in modules:
        addons = parent_dir(m).resolve()
        name = addons.stem
        if name not in registry:
            registry[name] = {
                "path": addons.relative_to(base_path),
                "modules": [m.stem]
            }
        else:
            registry[name]["modules"].append(m.stem)
    return paths


def _get_addons_info(addons, base_path):
    name = addons.stem
    data = {
        "path": addons.relative_to(base_path)
    }

    return name, data

def get_addons_registry(base_path=Path.home())
    base_path = Path(base_path).resolve()
    modules = find_odoo_modules(base_path)
    registry = gather_addons_infos(modules, base_path)
    return registry

def dump_addons_registry(filename=DEFAULT_REPOSITORY_ADDONS_FILENAME, base_path=Path.home()):
    registry = get_addons_registry(base_path)
    json_dump(filename, registry)
