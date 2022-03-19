import sys
from pathlib import Path

# TODO
# This is just a workaround, because python in my WSL
# adds the folder of the script to sys.path instead
# of the workspace folder of vscode, which is cwd, when
# you run or debug a script in vscode.
# We should resolve this by using a venv.
root = Path("./")
sys.path.insert(0, str(root.resolve()))

from deep_learning_compression.Storage.Storage import Storage

if __name__ == "__main__":

    s = Storage()
    sets = s.GetAllDataSetInformation()

    print("Found following datasets:")
    [print(f"\t- {s.Name}") for s in sets]
    print("\n")

    s.DownloadAndPrepareAllDatasets()
