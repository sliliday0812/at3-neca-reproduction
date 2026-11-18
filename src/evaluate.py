"""CPU-only independent evaluation after training outputs have been frozen."""
from __future__ import annotations
import argparse,hashlib,json
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def evaluate(volume,reference,projection,observations):
    pred=volume>0.5;ref=reference>0.5
    if pred.shape!=ref.shape:raise ValueError('Reference/volume shape mismatch')
    tp=int((pred&ref).sum());fp=int((pred&~ref).sum());fn=int((~pred&ref).sum())
    return {'threshold':0.5,'threshold_rule':'strict >0.5','tp':tp,'fp':fp,'fn':fn,'dice':2*tp/(2*tp+fp+fn) if 2*tp+fp+fn else 1.0,'iou':tp/(tp+fp+fn) if tp+fp+fn else 1.0,'predicted_foreground':int(pred.sum()),'reference_foreground':int(ref.sum()),'projection_mse':float(np.square(projection.astype('float64')-observations).mean()),'finite':bool(np.isfinite(volume).all() and np.isfinite(projection).all())}
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--run',type=Path,default=ROOT/'results/current')
    parser.add_argument('--output',type=Path,help='Alternate JSON destination; use for immutable historical runs')
    parser.add_argument('--reference',type=Path,default=ROOT/'data/evaluation_only/reference_A.npy')
    parser.add_argument('--observations',type=Path,default=ROOT/'data/observed/projections.npy')
    args=parser.parse_args();folder=args.run.resolve()
    volume=np.load(folder/'final_volume.npy',allow_pickle=False);ref=np.load(args.reference,allow_pickle=False)
    result=evaluate(volume,ref,np.load(folder/'final_projections.npy',allow_pickle=False),np.load(args.observations,allow_pickle=False))
    result['volume_sha256']=hashlib.sha256((folder/'final_volume.npy').read_bytes()).hexdigest()
    result['evaluation_reference_sha256']=hashlib.sha256(args.reference.read_bytes()).hexdigest()
    result['evaluation_scope']='one 64^3 processed digital reference, synthetic two-view geometry, not patient/generalization accuracy'
    (args.output or folder/'evaluation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
    if not result['finite'] or result['predicted_foreground']==0:raise SystemExit(1)
if __name__=='__main__':main()
