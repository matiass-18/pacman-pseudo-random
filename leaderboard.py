import json, os, time
SCORES_FILE='scores.json'
VICTORIES_FILE='victories.json'

def _load(path):
    if not os.path.exists(path): return []
    try:
        with open(path,'r',encoding='utf-8') as f: return json.load(f)
    except Exception: return []

def _save(path, lst):
    with open(path,'w',encoding='utf-8') as f: json.dump(lst, f, indent=2)

def add_score(name, score):
    lst = _load(SCORES_FILE)
    lst.append({'name': (name or 'Player')[:12], 'score': int(score), 'ts': int(time.time())})
    lst.sort(key=lambda s: s['score'], reverse=True)
    _save(SCORES_FILE, lst[:10])

def top(n=10):
    lst = _load(SCORES_FILE)
    lst.sort(key=lambda s: s['score'], reverse=True)
    return lst[:n]

def add_victory(name, score, map_name, stars, elapsed_sec):
    hist = _load(VICTORIES_FILE)
    hist.append({'name': (name or 'Player')[:12], 'score': int(score), 'map': map_name, 'stars': int(stars), 'time': int(elapsed_sec)})
    _save(VICTORIES_FILE, hist)

def victories():
    return _load(VICTORIES_FILE)
