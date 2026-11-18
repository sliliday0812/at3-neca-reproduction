"""Run the expanded AT4 source tree; no archive extraction is required."""
from pathlib import Path
import argparse
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
ACTIONS = {
    'verify': ('src/verify_upstream.py', []),
    'analyze-at4': ('src/analyze_at4.py', []),
    'evaluate': ('src/evaluate.py', []),
    'plot': ('src/plot_results.py', []),
    'train': ('src/train.py', []),
    'agent-validate': ('agent/scripts/agent_lab.py', ['validate']),
    'agent-replay': ('agent/scripts/agent_lab.py', ['replay']),
    'agent-selfcheck': ('agent/scripts/self_check.py', []),
}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=ACTIONS)
    args, extra = parser.parse_known_args()
    script, prefix = ACTIONS[args.action]
    if args.action == 'agent-validate' and not extra:
        extra = ['max6']
    cwd = ROOT/'agent' if args.action.startswith('agent-') else ROOT
    env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
    raise SystemExit(subprocess.call([sys.executable, str(ROOT/script), *prefix, *extra], cwd=cwd, env=env))

if __name__ == '__main__':
    main()
