from pathlib import Path
import subprocess,sys
root=Path(__file__).resolve().parents[3]
subprocess.run([sys.executable,str(root/"tools"/"build_diagrams.py")],check=True)
