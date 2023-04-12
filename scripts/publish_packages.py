import subprocess
import os
import toml

class ChangeDir:
    def __init__(self, new_path):
        self.new_path = new_path
        self.saved_path = os.getcwd()

    def __enter__(self):
        os.chdir(self.new_path)

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.saved_path)


def is_package_published(package, version):
    output = subprocess.check_output(["poetry", "search", package]).decode()
    return f"{package} ({version})" in output

def patch_version(package, version, deps=None):
    deps = [] if deps is None else list(deps)
    print(f"deps: {deps}")

    with ChangeDir(f"packages/{package}"):
        subprocess.check_call(["poetry", "version", version])

        if deps and deps[0]:
            pass
            # patchedDeps = [f"{dep}@{version}" for dep in deps]
            # patchedDeps = joinByString(" ", *patchedDeps) + f"@{version}"
            # try:
            #     subprocess.check_call(["poetry", "add", patchedDeps])
            # except subprocess.CalledProcessError:
            #     print(f"Failed to add {patchedDeps} to {package}")
            #     subprocess.check_call(["cd", pwd])
            #     return False

        try:
            subprocess.check_call(["poetry", "lock"])
            subprocess.check_call(["poetry", "install", "--no-root"])
        except subprocess.CalledProcessError:
            print(f"Failed to lock or install {package}")
            return False
    return True

def publishPackage(package, version, username, password):
    pwd = subprocess.check_output(["echo", "$PWD"]).decode().strip()
    
    subprocess.check_call(["cd", f"packages/{package}"])
    
    if is_package_published(package, version):
        print(f"Skip publish: Package {package} with version {version} is already published")
        subprocess.check_call(["cd", pwd])
        return True
    
    try:
        subprocess.check_call(["poetry", "publish", "--build", "--username", username, "--password", password])
    except subprocess.CalledProcessError:
        print(f"Failed to publish {package}")
        subprocess.check_call(["cd", pwd])
        return False
    
    subprocess.check_call(["cd", pwd])
    return True

def waitForPackagePublish(package, version):
    pwd = subprocess.check_output(["echo", "$PWD"]).decode().strip()
    
    subprocess.check_call(["cd", f"packages/{package}"])
    
    seconds = 0
    
    while seconds < 600: # Wait for 10 minutes
        if is_package_published(package, version):
            print(f"Package {package} with version {version} is published")
            break
        
        time.sleep(5)
        seconds += 5
        print(f"Waiting for {seconds} seconds for the {package} to be published")
    
    subprocess.check_call(["cd", pwd])
    
    if seconds == 600:
        print(f"Package {package} with version {version} is not published")
        return False
    
    return True
