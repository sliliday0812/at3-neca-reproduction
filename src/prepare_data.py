"""Offline preparation from an authorized DeepCA CCTA.zip or CCTA_GT/1.npy.

This step may read the reference to generate synthetic observations. Training is
separate and receives only the saved two-view observations and geometry.
"""
from pathlib import Path
import argparse,hashlib,io,json,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('source',type=Path,help='CCTA.zip or extracted CCTA_GT/1.npy')
    p.add_argument('--output',type=Path,required=True,help='New directory, to avoid overwriting submitted inputs')
    args=p.parse_args();out=args.output.resolve()
    if out.exists() and any(out.iterdir()):p.error('Output must be absent or empty')
    import numpy as np,torch,yaml
    if not torch.cuda.is_available():raise RuntimeError('Synthetic author ASTRA projection requires CUDA')
    sys.path.insert(0,str(ROOT/'vendor/NeCA'))
    from src.render.ct_geometry_projector import ConeBeam3DProjector
    from odl.tomo.util.utility import axis_rotation,rotation_matrix_from_to
    if args.source.suffix.lower()=='.zip':
        with zipfile.ZipFile(args.source) as z:raw=z.read('CCTA_GT/1.npy')
    else:raw=args.source.read_bytes()
    gt=np.load(io.BytesIO(raw),allow_pickle=False).astype('float32')
    if gt.shape!=(128,128,128) or not np.isfinite(gt).all() or not np.all((gt==0)|(gt==1)):
        raise ValueError('Expected finite binary author CCTA_GT/1.npy with shape128^3')
    ref=gt.reshape(64,2,64,2,64,2).max(axis=(1,3,5))
    geometry=yaml.safe_load((ROOT/'data/observed/geometry.yaml').read_text())
    def projector(i):
        dso=geometry['DSO'][i];angles=geometry[['first_projection_angle','second_projection_angle'][i]];a=[-angles[1],angles[0]]
        v=axis_rotation((0,0,1),angle=a[0]/180*np.pi,vectors=(0,-dso,0));r=axis_rotation((0,0,1),angle=a[0]/180*np.pi,vectors=(-1,0,0))
        v=axis_rotation(r[0],angle=a[1]/180*np.pi,vectors=v[0]);m=rotation_matrix_from_to((0,-dso,0),v[0])
        angle=np.arccos(np.clip((np.trace(m)-1)/2,-1,1));axis=np.array([m[2,1]-m[1,2],m[0,2]-m[2,0],m[1,0]-m[0,1]]);axis/=np.linalg.norm(axis)
        return ConeBeam3DProjector(np.array(geometry['nVoxel']),np.array(geometry['dVoxel']),angle,axis,np.array(geometry['nDetector']),np.array(geometry['dDetector']),geometry['DDE'][i],dso)
    x=torch.from_numpy(ref)[None].cuda()
    with torch.no_grad():obs=torch.cat([projector(i).forward_project(x) for i in range(2)],1).cpu().numpy()
    (out/'observed').mkdir(parents=True);(out/'evaluation_only').mkdir()
    np.save(out/'observed/projections.npy',obs);np.save(out/'evaluation_only/reference_A.npy',ref)
    (out/'observed/geometry.yaml').write_text(yaml.safe_dump(geometry))
    rec={'raw_member_sha256':hashlib.sha256(raw).hexdigest(),'reference_foreground':int(ref.sum()),'reference_shape':list(ref.shape),'observations_shape':list(obs.shape),'observations_finite':bool(np.isfinite(obs).all()),'source':'DeepCA CCTA_GT/1.npy, same-source processed array; author angle midpoint preserved','derivation':'2x2x2 max-pool then NeCA author continuous cone-beam projection; no smoothing','usage':'ground truth used only in offline input generation and later evaluation, never in train.py'}
    (out/'preparation.json').write_text(json.dumps(rec,indent=2));print(json.dumps(rec,indent=2))
if __name__=='__main__':main()
