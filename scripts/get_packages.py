import json
import os

def extract_package_paths(workspace_file):
    with open(workspace_file, 'r') as file:
        workspace_data = json.load(file)

    return [
        folder['path']
        for folder in workspace_data['folders']
        if folder['name'] not in {'root', 'docs'}
        and os.path.isfile(os.path.join(folder['path'], 'pyproject.toml'))
    ]

workspace_file = 'python-monorepo.code-workspace'
package_paths = extract_package_paths(workspace_file)

print(f'''"{json.dumps(package_paths, separators=(',', ':'))}"''')
