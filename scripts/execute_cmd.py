import sys
import subprocess


def execute_command(args):
    subprocess.check_call(args)


if __name__ == "__main__":
    from dependency_graph import package_build_order
    from utils import ChangeDir
    from color_logger import ColoredLogger

    logger = ColoredLogger("execute_cmd")

    for package_dir in package_build_order():
        with ChangeDir(str(package_dir)):
            logger.info(f"Running command: \"{' '.join(sys.argv[1:])}\" in {package_dir}")
            execute_command(sys.argv[1:])
