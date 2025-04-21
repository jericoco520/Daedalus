import subprocess
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)
subprocess.run(["bash", "./aes.sh", "zcrypt"])
