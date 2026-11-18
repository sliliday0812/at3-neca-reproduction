"""Generate traceable figures from frozen arrays, without smoothing or mesh repair."""
from pathlib import Path
import json,hashlib
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from skimage.measure import marching_cubes
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'figures';OUT.mkdir(exist_ok=True)
plt.rcParams.update({'font.size':10,'axes.titlesize':11,'axes.labelsize':10,'figure.facecolor':'white','savefig.facecolor':'white'})
COLORS={'reference':'#0072B2','prediction':'#D55E00'}
records=[]
def save(fig,name,meaning):
    path=OUT/name;fig.savefig(path,dpi=220,bbox_inches='tight' if name.startswith('01_') else None,pad_inches=0.12);plt.close(fig)
    records.append({'file':name,'description':meaning,'pixel_size':__import__('PIL.Image',fromlist=['Image']).open(path).size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
def mesh(ax,volume,title,color):
    v,f,_,_=marching_cubes(volume.astype(float),level=.5,spacing=(1.6,1.6,1.6))
    v-=50.4
    ax.plot_trisurf(v[:,0],v[:,1],v[:,2],triangles=f,color=color,alpha=1,linewidth=0,antialiased=True,shade=True)
    for fn in [ax.set_xlim,ax.set_ylim,ax.set_zlim]:fn(-51.2,51.2)
    ax.set_box_aspect((1,1,1));ax.view_init(22,-57)
    ax.set(xlabel='A0',ylabel='A1',zlabel='A2',title=title)
    ax.xaxis.labelpad=-5;ax.yaxis.labelpad=-5;ax.zaxis.labelpad=-3
    ax.tick_params(labelsize=6,pad=-1)
run=ROOT/'results/current';ref=np.load(ROOT/'data/evaluation_only/reference_A.npy')>.5
pred=np.load(run/'final_volume.npy')>.5
obs=np.load(ROOT/'data/observed/projections.npy')[0]
projs=np.load(run/'final_projections.npy')[0]
metrics=json.loads((run/'evaluation.json').read_text())
# All surface panels use identical pose, field of view and >0.5 threshold. No smoothing.
fig=plt.figure(figsize=(10,6),layout='constrained')
for i in range(2):
    ax=fig.add_subplot(2,2,i+1);im=ax.imshow(obs[i],cmap='gray',vmin=0,vmax=float(obs.max()),origin='lower',interpolation='nearest')
    ax.set(title=f'Observed line-integral projection {"AB"[i]}',xlabel='Detector pixel u',ylabel='Detector pixel v')
    fig.colorbar(im,ax=ax,label='Synthetic line integral',shrink=.8)
mesh(fig.add_subplot(2,2,3,projection='3d'),ref,'Digital reference (evaluation only)',COLORS['reference'])
mesh(fig.add_subplot(2,2,4,projection='3d'),pred,f'NeCA current run | Dice {metrics["dice"]:.3f}',COLORS['prediction'])
fig.suptitle('Two-view NeCA reconstruction | 64 cubed | one synthetic case',fontsize=13)
save(fig,'01_inputs_and_3d.png','Inputs A/B share intensity limits. Lower surfaces use marching cubes at0.5, same camera and axes in nominal mm; no smoothing or connected-component removal. Occluded branches cannot be judged from this angle alone.')
fig,axs=plt.subplots(3,3,figsize=(10,6),layout='constrained')
for axis in range(3):
    for row,(vol,label) in enumerate([(ref,'Reference'),(pred,'Reconstruction')]):
        axs[row,axis].imshow(vol.max(axis=axis).T,cmap='gray',vmin=0,vmax=1,origin='lower',interpolation='nearest')
        axs[row,axis].set(title=f'{label} | collapse axis {axis}')
    rgb=np.ones((*ref.max(axis=axis).T.shape,3))
    tp=(ref&pred).max(axis=axis).T;fp=(pred&~ref).max(axis=axis).T;fn=(ref&~pred).max(axis=axis).T
    rgb[tp]=[.35,.35,.35];rgb[fp]=[.9,.6,0];rgb[fn]=[0,.45,.70]
    # Priority reflects projected presence, not a unique voxel classification along a ray.
    axs[2,axis].imshow(rgb,origin='lower',interpolation='nearest');axs[2,axis].set(title=f'Projected voxel errors | axis {axis}')
for ax in axs.flat:ax.set_xticks([0,32,63]);ax.set_yticks([0,32,63]);ax.tick_params(labelsize=8)
fig.suptitle('Orthogonal maximum projections | gray TP | orange FP | blue FN\nError colors show projected voxel classes; different depths may overlap',fontsize=12)
save(fig,'02_orthogonal_errors.png','Top/middle are binary reference/reconstruction MIPs across all three axes; bottom projects voxel TP/FP/FN with priority FN over FP over TP. MIPs can hide depth and overlap, so Dice is calculated in3D, never from these pictures.')
fig,axs=plt.subplots(2,3,figsize=(11,6.5),layout='constrained')
maxabs=float(np.abs(projs-obs).max())
for v in range(2):
    for k,(img,title,cmap,vm) in enumerate([(obs[v],'Observed','gray',float(obs.max())),(projs[v],'Reprojected','gray',float(obs.max())),(np.abs(projs[v]-obs[v]),'Absolute residual','magma',maxabs)]):
        im=axs[v,k].imshow(img,cmap=cmap,vmin=0,vmax=vm,origin='lower',interpolation='nearest');axs[v,k].set(title=f'View {"AB"[v]} | {title}',xlabel='u pixel',ylabel='v pixel');fig.colorbar(im,ax=axs[v,k],shrink=.8)
fig.suptitle('Projection fitting | matched scales | no intensity rescaling per image',fontsize=13)
save(fig,'03_projection_residuals.png','Per-view measured synthetic line integral, final forward projection and absolute residual; observed/reprojected share scales globally and residuals share a separate global scale. Good2D fit does not establish true3D accuracy.')
losses=json.loads((run/'losses.json').read_text())
fig,ax=plt.subplots(figsize=(9,3.2),layout='constrained')
ax.plot([r['optimizer_update'] for r in losses],[r['projection_mse_before_update'] for r in losses],color='#0072B2',marker='.',markersize=3,linewidth=1)
ax.set(yscale='log',xlabel='Optimizer update (sampled every100 epoch indices)',ylabel='Projection MSE before update',title='Current run loss | logarithmic y axis | no smoothing')
ax.grid(alpha=.2)
save(fig,'04_training_loss.png','Recorded pre-update MSE sampled every100 indices and final index; logarithmic y scale, no smoothing. The final reported projection MSE is evaluated after the final update and may differ from the last sampled pre-update loss.')
fig,axs=plt.subplots(1,3,figsize=(11,3.6),layout='constrained')
for col,case in enumerate(['C0','C1','C2']):
    d=ROOT/'results/historical'/case
    vol=np.load(d/'final_volume.npy')>.5;met=json.loads((d/'evaluation.json').read_text())
    axs[col].imshow(vol.max(axis=2).T,cmap='gray',vmin=0,vmax=1,origin='lower',interpolation='nearest')
    condition={'C0':'Synchronized','C1':'View B translated2mm','C2':'View B local deformation'}[case]
    axs[col].set(title=f'{case} {condition}\n3D Dice vs A {met["dice_A_reference"]:.3f}',xlabel='Axis0 voxel',ylabel='Axis1 voxel')
fig.suptitle('Historical controlled stress experiment | 2026-10-08 | one case per condition\nSame seed, initialization and5001 updates; not a population estimate',fontsize=12)
save(fig,'05_historical_stress.png','Previously executed C0/C1/C2 results under the same initialization, resolution and author geometry. MIPs collapse axis2; scores are full3D Dice against reference A. C1/C2 perturbation input magnitudes differ, so their difficulty cannot be ranked.')
manifest={'purpose':'AT3 classroom reproduction, general readable figures; no journal-specific compliance claim','canvas_note':'Figure01 intentionally uses a tight bounding box with padding to retain all3D axis labels; exported pixel sizes are recorded per figure',
'transforms':'threshold strictly >0.5; marching cubes level0.5; nominal1.6mm voxel; MIPs; absolute projection residual; log loss scale; no smoothing/mesh repair','sample_unit':'one processed digital reference, one current run; three historical conditions on same case, not independent patients','inputs_sha256':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [run/'final_volume.npy',run/'final_projections.npy',ROOT/'data/evaluation_only/reference_A.npy']},'matplotlib_version':matplotlib.__version__,'numpy_version':np.__version__,'figures':records,'software_reference':'Kassis et al.2026, Scientific Agent Skills, arXiv2609.00065 https://doi.org/10.48550/arXiv.2609.00065'}
(OUT/'figure-manifest.json').write_text(json.dumps(manifest,indent=2))
print('FIGURES_COMPLETE',len(records))
