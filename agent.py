"""Offline entry point for the AT3 NeCA Agent evidence archive."""
from pathlib import Path
import argparse,hashlib,os,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
ARCHIVE='AT3-Agent-evidence.D26092110395彭楚天.zip'
EXPECTED='02453dcd6d24cb44b099b5fb50bc400f85b885dcaf4f2f2c75c8e3591a356093'
PROJECT='AT3-Agent.D26092110395彭楚天'
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['validate','replay','selfcheck'])
    args,extra=parser.parse_known_args()
    archive=ROOT/ARCHIVE
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=EXPECTED:raise SystemExit('Archive SHA256 mismatch')
    project=ROOT/PROJECT
    if not project.exists():
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                p=Path(info.filename)
                if p.is_absolute() or '..' in p.parts or not p.parts or p.parts[0]!=PROJECT:raise SystemExit('Unsafe archive path')
            z.extractall(ROOT)
    if args.action=='selfcheck':command=[sys.executable,str(project/'scripts/self_check.py')]
    else:
        tail=['max6'] if args.action=='validate' and not extra else extra
        command=[sys.executable,str(project/'scripts/agent_lab.py'),args.action,*tail]
    raise SystemExit(subprocess.call(command,cwd=project,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}))
if __name__=='__main__':main()
