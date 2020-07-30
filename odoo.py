import os
from pathlib import Path
from .tools import load_json, json_dump, parent_dir

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


def _get_addons_info(addons):
    name = addons.stem
    data = {
        "path": addons.relative_to()
    }

    return name, data