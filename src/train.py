"""Run the pinned author NeCA loop with portable paths and nonalgorithmic logging.

Training reads only the two observed projections plus geometry. The evaluation
reference is intentionally absent from this interface; evaluate.py is separate.
CUDA is required by the author hash encoder and ASTRA cone-beam projector.
"""
from __future__ import annotations
import argparse, copy, hashlib, json, os, platform, runpy, sys, time
from pathlib import Path
import numpy as np
import torch
import yaml

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'results/rerun')
    parser.add_argument('--epochs',type=int,default=5000,help='Author loop includes index0; updates=epochs+1')
    parser.add_argument('--seed',type=int,default=42)
    parser.add_argument('--projections',type=Path,default=ROOT/'data/observed/projections.npy')
    parser.add_argument('--geometry',type=Path,default=ROOT/'data/observed/geometry.yaml')
    args=parser.parse_args()
    if args.epochs<1:parser.error('--epochs must be positive')
    if not torch.cuda.is_available():raise RuntimeError('Author NeCA requires a CUDA GPU; CPU is supported only for evaluation/plots.')
    out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
    torch.manual_seed(args.seed);torch.cuda.manual_seed_all(args.seed);np.random.seed(args.seed)
    sys.path.insert(0,str(ROOT/'vendor/NeCA'))
    import odl,astra
    from src.trainer import Trainer
    from src.render import run_network
    geometry=yaml.safe_load(args.geometry.read_text())
    if any(k in geometry for k in ['GT','reference','reference_A']):raise ValueError('Training geometry must contain no evaluation reference')
    observations=np.load(args.projections,allow_pickle=False)
    if observations.shape!=(1,2,128,128) or not np.isfinite(observations).all():raise ValueError('Expected finite observations with shape (1,2,128,128)')
    geometry['datadir']=str(args.projections.resolve())
    geometry_file=out/'runtime-geometry.yaml';geometry_file.write_text(yaml.safe_dump(geometry))
    cfg=yaml.safe_load((ROOT/'vendor/NeCA/config/CCTA.yaml').read_text())
    cfg['exp'].update(expname='checkpoints',expdir=str(out),dataconfig=str(geometry_file))
    cfg['train'].update(epoch=args.epochs,resume=False)
    cfg['render']['netchunk']=32768
    cfg['log'].update(i_eval=args.epochs,i_save=args.epochs)
    runtime=out/'runtime-train.yaml';runtime.write_text(yaml.safe_dump(cfg))
    start=time.perf_counter();losses=[];initial={}
    original_start=Trainer.start;original_step=Trainer.train_step
    def instrument_start(self):
        digest=hashlib.sha256()
        for key,value in self.net.state_dict().items():digest.update(key.encode());digest.update(value.detach().cpu().numpy().tobytes())
        initial.update(seed=args.seed,network_initial_sha256=digest.hexdigest())
        (out/'initial-network.json').write_text(json.dumps(initial,indent=2))
        return original_start(self)
    def instrument_step(self,data,global_step,idx_epoch):
        result=original_step(self,data,global_step,idx_epoch)
        if idx_epoch%100==0 or idx_epoch==args.epochs:
            value=float(result['loss'].detach().cpu())
            if not np.isfinite(value):raise FloatingPointError('Nonfinite training loss')
            losses.append({'epoch_index':idx_epoch,'optimizer_update':global_step,'projection_mse_before_update':value})
        return result
    Trainer.start=instrument_start;Trainer.train_step=instrument_step
    previous_argv=sys.argv[:]
    try:
        sys.argv=['train.py','--config',str(runtime)]
        result=runpy.run_path(str(ROOT/'vendor/NeCA/train.py'),run_name='__main__')
    finally:
        sys.argv=previous_argv;Trainer.start=original_start;Trainer.train_step=original_step
    trainer=result['trainer'];trainer.net.eval()
    with torch.no_grad():
        volume=run_network(trainer.voxels,trainer.net,32768).squeeze()
        projections=torch.cat([trainer.ct_projector_first.forward_project(volume[None]),trainer.ct_projector_second.forward_project(volume[None])],1)
    np.save(out/'final_volume.npy',volume.cpu().numpy());np.save(out/'final_projections.npy',projections.cpu().numpy())
    checkpoint=out/'checkpoints/ckpt.tar'
    ck=torch.load(checkpoint,map_location='cuda',weights_only=False);trainer.net.load_state_dict(ck['network'])
    with torch.no_grad():reloaded=run_network(trainer.voxels,trainer.net,32768).squeeze()
    reload_difference=float((volume-reloaded).abs().max())
    metrics={'date_utc':__import__('datetime').datetime.now(__import__('datetime').timezone.utc).isoformat(),'seed':args.seed,'seconds_including_setup':time.perf_counter()-start,'epoch_index':int(ck['epoch']),'optimizer_updates':int(next(iter(ck['optimizer']['state'].values()))['step']),'shape':list(volume.shape),'finite':bool(volume.isfinite().all()),'foreground_at_0p5':int((volume>0.5).sum()),'projection_mse_total':float(((projections-trainer.train_dset.projs)**2).mean()),'reload_max_abs_difference':reload_difference,'checkpoint_sha256':sha(checkpoint),'input_sha256':sha(args.projections),'training_reference_loaded':False,'upstream_commit':'77246df0826a031c12072f6ea64bb3370a0baf6b','cuda_device':torch.cuda.get_device_name(0),'python':platform.python_version(),'torch':torch.__version__,'cuda':torch.version.cuda,'numpy':np.__version__,'odl':odl.__version__,'astra':astra.__version__,'source_note':'pinned author loop/network/projector/loss; only paths,64^3/128^2 config,and logging wrapper changed','determinism_note':'fixed seed, CUDA hash backward uses atomicAdd; exact bitwise repeated training is not claimed'}
    (out/'losses.json').write_text(json.dumps(losses,indent=2));(out/'run.json').write_text(json.dumps(metrics,indent=2))
    trainer.writer.close()
    if not metrics['finite'] or not metrics['foreground_at_0p5'] or reload_difference>1e-6:raise AssertionError('Final nonempty/finite/reload gate failed')
    print('NECA_RUN_COMPLETE '+json.dumps(metrics),flush=True)
if __name__=='__main__':main()
