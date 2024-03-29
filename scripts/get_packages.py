import json
import os

def extract_package_paths(workspace_file = 'python-monorepo.code-workspace'):
    with open(workspace_file, 'r') as file:
        workspace_data = json.load(file)

    return [
        folder['path']
        for folder in workspace_data['folders']
        if folder['name'] not in {'root', 'docs', 'examples'}
        and os.path.isfile(os.path.join(folder['path'], 'pyproject.toml'))
    ]

if __name__ == '__main__':
    package_paths = extract_package_paths()
    packages = { "package": package_paths }

    print(json.dumps(packages))
