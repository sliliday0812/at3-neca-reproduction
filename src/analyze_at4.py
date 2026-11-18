"""Independently recompute every frozen AT4 run and reproduce summary/figures.

No training is performed; an empty short-budget prediction remains a negative result.
"""
from pathlib import Path
import csv,hashlib,json,sys,os,tempfile
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 from evaluate import evaluate
 ref=np.load(ROOT/'data/evaluation_only/reference_A.npy',allow_pickle=False)
 obs=np.load(ROOT/'data/observed/projections.npy',allow_pickle=False)
 spec=[('seed0_e5000','seed 0 / 5001',0,5001),('seed1_e5000','seed 1 / 5001',1,5001),('seed42_e1000','seed 42 / 1001',42,1001),('seed42_e3000','seed 42 / 3001',42,3001),('current','seed 42 / 5001',42,5001)]
 rows=[]
 for name,label,seed,updates in spec:
  folder=ROOT/('results/current' if name=='current' else 'results/at4/'+name)
  run=json.loads((folder/'run.json').read_text());vol=np.load(folder/'final_volume.npy',allow_pickle=False);pr=np.load(folder/'final_projections.npy',allow_pickle=False)
  assert list(vol.shape)==[64,64,64] and list(pr.shape)==[1,2,128,128]
  assert run['optimizer_updates']==updates and run['seed']==seed
  assert run['input_sha256']==sha(ROOT/'data/observed/projections.npy')
  assert run['training_reference_loaded'] is False and run['reload_max_abs_difference']<=1e-6
  ev=evaluate(vol,ref,pr,obs);assert ev['finite']
  receipt=json.loads((folder/'execution-receipt.json').read_text()) if (folder/'execution-receipt.json').exists() else None
  record={'name':name,'label':label,'seed':seed,'optimizer_updates':updates,'dice':ev['dice'],'iou':ev['iou'],'projection_mse':ev['projection_mse'],'foreground':ev['predicted_foreground'],'seconds':run['seconds_including_setup'],'reload_max_abs_difference':run['reload_max_abs_difference'],'date_utc':run['date_utc'],'volume_sha256':sha(folder/'final_volume.npy'),'projection_sha256':sha(folder/'final_projections.npy'),'nonempty_gate_pass':bool(ev['predicted_foreground']),'source':str(folder.relative_to(ROOT)),'optimizer_completed':True,'training_wrapper_exit':receipt['training_wrapper_exit'] if receipt else 0}
  init=json.loads((folder/'initial-network.json').read_text());record['initial_network_sha256']=init['network_initial_sha256'];rows.append(record)
 seeds=[r for r in rows if r['optimizer_updates']==5001];budget=sorted([r for r in rows if r['seed']==42],key=lambda x:x['optimizer_updates'])
 stats={m:{'mean':float(np.mean([r[m] for r in seeds])),'sample_sd':float(np.std([r[m] for r in seeds],ddof=1)),'n':3} for m in ['dice','iou','projection_mse']}
 same_init=len(set(r['initial_network_sha256'] for r in budget))==1
 assert same_init,'Seed42 initial parameter hashes differ; investigate before treating this as controlled budget comparison'
 b0,b1,b2=budget;span=max(x['dice'] for x in seeds)-min(x['dice'] for x in seeds)
 text={
 'abstract_new':f"三個種子條件的Dice均值為{stats['dice']['mean']:.4f}、樣本標準差{stats['dice']['sample_sd']:.4f}；固定seed42的1001、3001與5001更新Dice分別為{b0['dice']:.4f}、{b1['dice']:.4f}、{b2['dice']:.4f}。",
 'new_execution_note':'新增四條件於2026年11月18日在同一主機兩張A30上執行；5001更新的seed42沿用10月28日基線。三個seed42條件的初始參數SHA256一致。',
 'new_results_text':f"三種子Dice範圍為{min(x['dice'] for x in seeds):.4f}–{max(x['dice'] for x in seeds):.4f}，均值±樣本標準差為{stats['dice']['mean']:.4f}±{stats['dice']['sample_sd']:.4f}；IoU為{stats['iou']['mean']:.4f}±{stats['iou']['sample_sd']:.4f}。固定seed42時，1001更新的前景為{b0['foreground']}、Dice={b0['dice']:.4f}，投影MSE={b0['projection_mse']:.6g}；3001更新Dice={b1['dice']:.4f}、MSE={b1['projection_mse']:.6g}；5001更新Dice={b2['dice']:.4f}、MSE={b2['projection_mse']:.6g}。短預算已完成1001次更新並保存有限輸出，重載差為0，但固定0.5閾值下輸出為空，外層非空品質門檻因此退出1；其Dice與IoU均為0。本文保存此負結果，沒有提高預算、改閾值或刪除該條件來製造全數成功。",
 'discussion_new':f"三種子Dice相差{span:.4f}，提示單一種子的分數不能代表全部優化路徑。短預算的空輸出在更長預算下改善，與此例尚未充分優化的解釋相符；三個離散點仍不足以保證一般單調收斂。",
 'conclusion_new':'同例三種子與三種更新預算分析'
 }
 summary={'date':'2026-11-18','replication_unit':'one processed case; computational repeats, not patients','threshold':0.5,'runs':rows,'seed_statistics':stats,'budget_seed42_initial_hashes_match':same_init,'all_outputs_nonempty':all(x['foreground']>0 for x in rows),'empty_output_is_retained_negative_result':b0['foreground']==0,'manuscript_text':text}
 out=ROOT/'results/at4';out.mkdir(exist_ok=True,parents=True);(out/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
 with (out/'comparison.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 if '--no-plot' not in sys.argv:
  os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'at4-mpl-cache'))
  import matplotlib;matplotlib.use('Agg')
  import matplotlib.pyplot as plt
  plt.rcParams.update({'font.size':9,'axes.titlesize':10,'axes.labelsize':9,'legend.fontsize':8,'savefig.dpi':320,'pdf.fonttype':42})
  fig,axs=plt.subplots(1,3,figsize=(7.6,2.75),layout='constrained')
  x=np.arange(3);axs[0].plot(x,[r['dice'] for r in seeds],'o',color='#0072B2',label='Dice');axs[0].plot(x,[r['iou'] for r in seeds],'s',color='#D55E00',label='IoU');axs[0].set(xticks=x,xticklabels=['0','1','42*'],xlabel='Initialization seed',ylabel='3D overlap',ylim=(0,1),title='(a) Same case, 5001 updates');axs[0].legend()
  u=[r['optimizer_updates'] for r in budget];axs[1].plot(u,[r['dice'] for r in budget],'o-',color='#0072B2',label='Dice');axs[1].plot(u,[r['iou'] for r in budget],'s--',color='#D55E00',label='IoU');axs[1].set(xlabel='Optimizer updates',ylabel='3D overlap',ylim=(0,1),title='(b) Fixed seed 42');axs[1].set_xticks(u,['1001','3001','5001']);axs[1].legend()
  axs[2].semilogy(u,[r['projection_mse'] for r in budget],'D-',color='#009E73');axs[2].set(xlabel='Optimizer updates',ylabel='Projection MSE (log scale)',title='(c) Same budget conditions');axs[2].set_xticks(u,['1001','3001','5001'])
  for ax in axs:ax.grid(axis='y',alpha=.25)
  fig.savefig(ROOT/'figures/06_seed_budget.png',facecolor='white');fig.savefig(ROOT/'figures/06_seed_budget.pdf',facecolor='white');plt.close(fig)
  meta={'inputs':[{k:r[k] for k in ['source','volume_sha256','projection_sha256']} for r in rows],'description':'Discrete same-case seeds and budgets; no population confidence intervals; seed42/5001 is archived 2026-10-28, other runs 2026-11-18.','transformations':'fixed >0.5; full 3D Dice/IoU; float64 projection MSE; no smoothing; lines connect only observed budget points','replicates':'n=3 computational seeds on one processed case; no independence across patients'}
  (ROOT/'figures/06_seed_budget.provenance.json').write_text(json.dumps(meta,indent=2)+'\n')
 print(json.dumps({'verified_runs':len(rows),'seed_statistics':stats,'seed42_initial_hashes_match':same_init,'all_outputs_nonempty':summary['all_outputs_nonempty']},indent=2))
if __name__=='__main__':main()
