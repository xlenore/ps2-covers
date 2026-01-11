from pathlib import Path
import re
from collections import defaultdict
import yaml


def load_gamedb(path: Path):
    if not path.exists():
        return []

    if path.suffix.lower() in ('.yml', '.yaml'):

        with path.open('r', encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        games = []
        if isinstance(data, dict):
            for serial, info in data.items():
                    if isinstance(info, dict):
                        name = info.get('name-en') or info.get('name_en') or info.get('name') or ''
                    else:
                        name = ''
                    games.append({'name': name, 'codes': [serial]})
        elif isinstance(data, list):
            games = data
        return games

    return []


def collect_expected_codes(gamedb):
    by_prefix = defaultdict(set)
    for game in gamedb:
        for code in game.get('codes', []):
            if not code:
                continue
            code = code.strip()
            m = re.match(r'^([A-Za-z0-9]+)-', code)
            if m:
                prefix = m.group(1).upper()
            else:
                prefix = code.upper()
            by_prefix[prefix].add(code.upper())
    return by_prefix


def load_cover_names(covers_dir: Path):
    names = []
    if not covers_dir.exists():
        return names
    for p in covers_dir.iterdir():
        if not p.is_file():
            continue
        names.append(p.name.upper())
    return names


def format_percent(available: int, total: int) -> str:
    if total == 0:
        return "0.00%"
    return f"{available/total*100:.2f}%"


def main():
    main_root = Path(__file__).resolve().parent.parent
    covers_dir = main_root / 'covers' / 'default'

    gamedb_path = main_root / 'tools' / 'GameIndex.yaml'
    gamedb = load_gamedb(gamedb_path)
    expected_by_prefix = collect_expected_codes(gamedb)

    cover_names = load_cover_names(covers_dir)

    rows = []
    for p in sorted(expected_by_prefix.keys()):
        expected_codes = sorted(expected_by_prefix[p])
        total = len(expected_codes)
        available_count = 0
        print(f"Processing prefix {p} with {total} expected codes.")
        for code in expected_codes:
            found = any(name.startswith(code) for name in cover_names)
            if found:
                available_count += 1
        pct = format_percent(available_count, total)
        rows.append((p, available_count, total, pct))

    print("## Covers Stats\n")
    print("| Serial |  Available/Total |  Percentage  |")
    print("| ------ |  --------------- |  ----------  |")
    for p, a, total, pct in rows:
        print(f"| {p} | {a}/{total} | {pct} |")

    missing_entries = []
    print("\n\n\nCollecting missing covers...")
    for game in gamedb:
        name = game.get('name', '').strip()
        for code in game.get('codes', []):
            if not code:
                continue
            code_upper = code.strip().upper()
            if not any(n.startswith(code_upper) for n in cover_names):
                missing_entries.append((code.strip(), name))

    missing_path = main_root / 'missing_covers.txt'
    try:
        with missing_path.open('w', encoding='utf-8') as mf:
            for code, name in missing_entries:
                mf.write(f"{code}  ---  {name}\n")
    except Exception as e:
        print(f"Warning: could not write missing_covers.txt: {e}")


if __name__ == '__main__':
    main()
