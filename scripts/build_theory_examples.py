"""Sinh ví dụ lý thuyết ngoại tuyến; không chạy thuật toán khi mở/chuyển tab."""
import itertools
import json
import random
import sys
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scheduling.greedy import greedy_schedule
from scheduling.genetic import genetic_algorithm, decode_permutation, crossover, mutate
from scheduling.branch_and_bound import branch_and_bound
from scheduling.tabu_search import tabu_search
from scheduling.cp_sat import cp_sat
from scheduling.metrics import evaluate_schedule

JOBS = [dict(id=1, p=9, d=4, w=6), dict(id=2, p=8, d=11, w=6),
        dict(id=3, p=2, d=6, w=3), dict(id=4, p=5, d=14, w=6),
        dict(id=5, p=4, d=4, w=4)]
ORDERS = {'lpt': [1, 2, 4, 5, 3], 'edd': [5, 1, 3, 2, 4], 'wspt': [3, 4, 5, 2, 1]}


def validate(schedule, jobs, machines, objective):
    assert len(schedule) == machines
    expected = {j['id']: j for j in jobs}
    seen = []
    for m, row in enumerate(schedule, 1):
        end = 0
        for task in sorted(row, key=lambda t: (t['start'], t['end'])):
            job = expected[task['id']]
            assert task['machine'] == m and task['start'] >= end
            assert task['end'] - task['start'] == job['p']
            assert all(task[k] == job[k] for k in ('p', 'd', 'w'))
            end = task['end']
            seen.append(task['id'])
    assert sorted(seen) == sorted(expected)
    assert evaluate_schedule(schedule)['objective'] == objective


def brute_force(jobs, machines):
    best = float('inf')
    for order in itertools.permutations(jobs):
        for assignment in itertools.product(range(machines), repeat=len(jobs)):
            times = [0] * machines
            cost = 0
            for j, machine in zip(order, assignment):
                times[machine] += j['p']
                cost += j['w'] * max(0, times[machine] - j['d'])
            best = min(best, cost)
    return best


def record(label, result, order=None):
    schedule = result['schedule']
    metrics = evaluate_schedule(schedule)
    validate(schedule, JOBS, 2, result.get('objective', metrics['objective']))
    tasks = [t for row in schedule for t in row]
    rows = []
    times = [0, 0]
    for task in (sorted(tasks, key=lambda t: order.index(t['id'])) if order else
                 sorted(tasks, key=lambda t: (t['start'], t['machine']))):
        tardiness = max(0, task['end'] - task['d'])
        rows.append({**task, 'before': times[:], 'tardiness': tardiness,
                     'cost': task['w'] * tardiness})
        times[task['machine'] - 1] = task['end']
    return dict(label=label, schedule=schedule, rows=rows, **{k: metrics[k] for k in ('objective', 'makespan')},
                status=result.get('status'), optimal=result.get('optimal', False), order=order)


def build_examples():
    state = random.getstate()
    try:
        results = {}
        for key, label in [('lpt', 'Greedy LPT'), ('edd', 'Greedy EDD'), ('wspt', 'Greedy WSPT')]:
            results[key] = record(label, {'schedule': greedy_schedule(JOBS, 2, key)}, ORDERS[key])
        random.seed(2718)
        results['ga'] = record('GA · seed 2718', genetic_algorithm(JOBS, 2, pop_size=20, generations=30))
        results['bb'] = record('B&B', branch_and_bound(JOBS, 2))
        results['ts'] = record('TS', tabu_search(JOBS, 2))
        cp = cp_sat(JOBS, 2)
        if cp['schedule'] is None:
            raise RuntimeError('Cần OR-Tools để kiểm chứng ví dụ ngoại tuyến')
        results['cp_sat'] = record('CP-SAT', cp)
        optimum = brute_force(JOBS, 2)
        assert optimum == results['bb']['objective'] == results['cp_sat']['objective']
        parents = [list(range(5)), list(reversed(range(5)))]
        with patch('scheduling.genetic.random.sample', return_value=[1, 3]):
            child = crossover(*parents)
        before = child[:]
        with patch('scheduling.genetic.random.sample', return_value=[0, 4]):
            mutate(child)
        ops = []
        for label, perm in [('Cha A', parents[0]), ('Cha B', parents[1]), ('Con sau lai', before), ('Con sau đột biến', child)]:
            obj, schedule = decode_permutation(perm, JOBS, 2)
            ops.append(dict(label=label, indices=perm, ids=[JOBS[i]['id'] for i in perm],
                            result=record(label, dict(objective=obj, schedule=schedule), [JOBS[i]['id'] for i in perm])))
        current = sorted(range(5), key=lambda i: JOBS[i]['d'])
        best = decode_permutation(current, JOBS, 2)[0]
        tabu = {}
        trace = []
        for iteration in range(3):
            candidates = []
            for i in range(5):
                for j in range(i + 1, 5):
                    move = tuple(sorted((current[i], current[j])))
                    perm = current[:]
                    perm[i], perm[j] = perm[j], perm[i]
                    obj, schedule = decode_permutation(perm, JOBS, 2)
                    if tabu.get(move, -1) > iteration and obj >= best:
                        continue
                    candidates.append((obj, perm, move))
            obj, current, move = min(candidates, key=lambda c: c[0])
            best = min(best, obj)
            tabu[move] = iteration + 8
            trace.append(dict(iteration=iteration + 1, ids=[i + 1 for i in current],
                              move=[i + 1 for i in move], current=obj, best=best, expiry=iteration + 8))
        return dict(jobs=JOBS, machines=2, results=results, optimum=optimum, operators=ops,
                    ts_trace=trace, provenance='Sinh ngoại tuyến bằng scripts/build_theory_examples.py; không đo runtime.')
    finally:
        random.setstate(state)


if __name__ == '__main__':
    data = build_examples()
    (ROOT / 'static/theory_examples.json').write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding='utf-8')
    print({key: item['objective'] for key, item in data['results'].items()})
    print('GA operators:', [(i['label'], i['ids'], i['result']['objective']) for i in data['operators']])
    print('TS trace:', data['ts_trace'])
