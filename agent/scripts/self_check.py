"""Independent evidence and negative-case checks, without changing live runs."""
from pathlib import Path
import importlib.util, json, shutil, tempfile

P = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('lab', P/'scripts/agent_lab.py')
lab=importlib.util.module_from_spec(spec);spec.loader.exec_module(lab)
result={'replay':lab.replay(P), 'negative_checks':{}}
requests={k:lab.lines(P/f'runs/{k}/trajectory.jsonl') for k in ('max3','max6')}
for k, events in requests.items():
    obs=lab.lines(P/f'runs/{k}/tool-results.jsonl')
    assert [e['call_id'] for e in events] == [o['call_id'] for o in obs]
    assert all(lab.sha(lab.encode(o['result']).encode())==o['result_sha256'] for o in obs)
    assert all(o['ok'] for o in obs)
assert [(e['tool'],e['arguments']) for e in requests['max3']] == [(e['tool'],e['arguments']) for e in requests['max6'][:3]]
result['request_observation_pairs_and_hashes']='PASS'
result['first_three_requests_identical']='PASS'
with tempfile.TemporaryDirectory(prefix='at3-negative-') as td:
    work=Path(td)
    for case in ['unknown_citation','unread_source','changed_claim','altered_source']:
        copy=work/case;shutil.copytree(P,copy)
        run=copy/'runs/max6'; brief=run/'final-brief.md'
        if case=='unknown_citation':brief.write_text(brief.read_text().replace('[[S1:C1]]','[[S9:C9]]'))
        elif case=='unread_source':
            path=run/'tool-results.jsonl'
            path.write_text('\n'.join(lab.encode(e) for e in lab.lines(path) if e['call_id']!='max6-04')+'\n')
        elif case=='changed_claim':brief.write_text(brief.read_text().replace('主要為剛體旋轉與平移','已證明任意非剛體補償'))
        else:
            p=copy/'sources/S2.json';d=lab.read_json(p);d['title']='altered';lab.save(p,d)
        validation=lab.validate(copy,run)
        assert not validation['pass'],case
        result['negative_checks'][case]={'rejected':True,'failed_checks':[k for k,v in validation['checks'].items() if not v]}
    copy=work/'budget';shutil.copytree(P,copy)
    before=(copy/'runs/max3/trajectory.jsonl').read_bytes()
    denied=lab.tool(copy,'max3','read_source',{'source_id':'S3'})
    assert denied['executed'] is False and before==(copy/'runs/max3/trajectory.jsonl').read_bytes()
    result['negative_checks']['budget_bypass']={'rejected':True,'trace_unchanged':True}
    try:lab.tool(copy,'../outside','read_source',{'source_id':'S1'})
    except ValueError:result['negative_checks']['run_path_traversal']={'rejected':True}
    else:raise AssertionError('Run traversal accepted')
result['pass']=True
(P/'validation-tests.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
print(json.dumps(result,ensure_ascii=False,indent=2))
