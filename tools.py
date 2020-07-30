import os
from pathlib import Path
import git
import json

def _find_git_repositories(path=Path()):
    path = Path(path)
    repositories = []
    dir_list = os.listdir(path)
    if ".git" in dir_list:
        repositories.append(path)
    else:
        for p in dir_list:
            next_path = path.joinpath(p)
            if next_path.is_dir():
                repositories += _find_git_repositories(next_path)
    return repositories


def find_git_repositories(path=Path()):
    """
        Recursively looks for git repositories
        Starting at path
    """
    return [git.Repo(repo) for repo in _find_git_repositories(path)]

def _get_repo_remote(repo):
    remote = ""
    remotes = repo.remotes
    if remotes:
        urls = [url for url in remotes[0].urls]
        if urls:
            remote = urls[0]
    return remote

def _repo_name(repo):
    directory = Path(repo.working_dir)
    name = directory.stem
    return name

def _gather_repo_info(repo):
    home = Path.home()
    directory = Path(repo.working_dir)
    name = _repo_name(repo)
    data = {
        "path": str(directory.relative_to(home)),
        "remote": _get_repo_remote(repo),
    }
    return name, data

def gather_repos_info(repos):
    """
        Given a list of git.Repo object,
        Return their registery values
    """
    repositories = {}
    for repo in repos:
        name, data = _gather_repo_info(repo)
        repositories[name] = data
    return repositories

def _gather_repo_states(repo):
    name = _repo_name(repo)
    data = {
        "branch": repo.active_branch.name,
    }
    return name, data


def gather_repo_states(repos):
    """
        Given a list of git.Repo object,
        Return their current states
    """
    repositories = {}
    for repo in repos:
        name, data = _gather_repo_states(repo)
        repositories[name] = data
    return repositories


def registry_from_server(path=Path()):
    repositories = find_git_repositories(path)
    data = gather_repos_info(repositories)
    return data

def server_state(path=Path()):
    repositories = find_git_repositories(path)
    data = gather_repo_states(repositories)
    return data


def register_server_repositories(file, path=Path()):
    """
        Register all repositories found in the server
    """
    data = registry_from_server(path)
    json_dump(file, data)

def save_server_repositories_state(file, path=Path()):
    """
        Save the server's repositories states
    """
    data = server_state(path)
    json_dump(file, data)

def load_json(file):
    with open(file, "r") as f:
        data = json.load(f)
    return data

def json_dump(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)


def _ensure_repo(registry, name, data, base_path=Path.home()):
    registered_repo = registry.get(name)
    if registered_repo is None:
        raise Exception("Repo {name} is not in registry".format(
        name=name,
    ))
    path = registered_repo.get("path")
    if path is None:
        raise Exception("No path found in registery for {name}".format(
        name=name,
    ))
    path = Path(path)
    remote = registered_repo.get("remote")
    if remote is None:
        raise Exception("No remote found in registery for {name}".format(
        remote=remote,
    ))
    if not path.exists():
        git.Repo.clone_from(remote, base_path.joinpath(path), **data)
    repo = git.Repo(path)
    branch = data.get("branch")
    if branch is not None:
        active_branch = repo.active_branch.name
        if active_branch != branch:
            raise Exception("Active branch for repo {name} is {active_branch} instend of {branch}".format(
            name=name,
            active_branch=active_branch,
            branch=branch,
        ))

def ensure_server(registry_file, state_file, path=Path.home()):
    registry = load_json(registry_file)
    state = load_json(state_file)
    errors = []
    for name, data in state.items():
        try:
            _ensure_repo(registry, name, data, path)
        except Exception as e:
            errors.append(e)
    if errors:
        for e in errors:
            print(e)


