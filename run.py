"""Verified entry point for the complete NeCA coursework source archive."""
from pathlib import Path
import argparse,hashlib,subprocess,sys,zipfile
ROOT=Path(__file__).resolve().parent
ARCHIVE='AT3-NeCA-code.D26092110395彭楚天.zip'
EXPECTED='8e23ce0c730fd37da79c28d3819eac63ea71ecbf8ec5c5669aa1ea2e8a36ebfa'

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=['verify','evaluate','plot','train'])
    args,extra=parser.parse_known_args()
    archive=ROOT/ARCHIVE
    if hashlib.sha256(archive.read_bytes()).hexdigest()!=EXPECTED:raise SystemExit('Archive SHA256 mismatch')
    project=ROOT/'NeCA-reproduction'
    if not project.exists():
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                p=Path(info.filename)
                if p.is_absolute() or '..' in p.parts or p.parts[0]!='NeCA-reproduction':raise SystemExit('Unsafe archive path')
            z.extractall(ROOT)
    script={'verify':'verify_upstream.py','evaluate':'evaluate.py','plot':'plot_results.py','train':'train.py'}[args.action]
    raise SystemExit(subprocess.call([sys.executable,str(project/'scripts'/script),*extra],cwd=project))
if __name__=='__main__':main()
