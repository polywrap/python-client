import subprocess

def generate():
    clone = subprocess.run(["git", "clone", "git@github.com:polywrap/wasm-test-harness.git"])
    print(clone)

    checkout = subprocess.run(["git", "checkout", "tags/v0.1.1"], cwd="./wasm-test-harness")
    print(checkout)

    move = subprocess.run(["mv", "./wasm-test-harness/wrappers", "./cases"])
    print(move)

    remove = subprocess.run(["rm", "-rf", "wasm-test-harness"])
    print(remove)
