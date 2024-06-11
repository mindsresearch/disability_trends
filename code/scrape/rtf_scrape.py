from pathlib import Path
import re
import json
import argparse

from striprtf.striprtf import rtf_to_text
from tqdm import tqdm

from metadata_parser import proc_meta
from token_cleaning import clean_text, lemma_warn


def proc_rtf(path: Path) -> dict:
    with open(path, 'r') as in_file:
        txt = rtf_to_text(in_file.read())

    body_split = re.split(r'\nBody\n', txt)
    meta = re.sub(r'\n+', '\n', body_split[0]).strip()
    body = re.split(r'\nLoad-Date', body_split[1])[0]
    body = re.sub(r'\n', ' ', body).strip()

    meta_lines = [line for line in meta.splitlines() if line != ' ']

    return {'meta': proc_meta(meta_lines), 'body': clean_text(body)}


def check_data_path(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f'Path {path} does not exist')
    rtfs = [f for f in path.rglob('*.rtf') if '_doclist' not in f.name]
    if len(rtfs) == 0:
        raise FileNotFoundError(f'Path {path} does not contain any .rtf files')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--term', default='disab', type=str)
    parser.add_argument('-d', '--decade', type=str, required=True)
    parser.add_argument('-n', '--nums', type=str, required=True, nargs='+')
    args = parser.parse_args()

    term = args.term
    decade = args.decade
    nums = args.nums

    script_loc = Path(__file__).resolve()
    data_path = script_loc.parent.parent/'data'
    check_data_path(data_path)
    out_path = data_path / term / f'{decade}s' / 'json'
    out_path.mkdir(exist_ok=True)

    for num in tqdm(nums, desc='processing batches'):
        name = f'{decade}s-{num}{term[0]}'
        root_path = data_path / term / f'{decade}s' / name
        rtf_files = [f for f in root_path.rglob('*.rtf') if '_doclist' not in f.name]

        data = [proc_rtf(p) for p in tqdm(rtf_files, leave=False, desc='processing rtfs')]

        with open(out_path / f'{name}.json', 'w') as out_file:
            json.dump(data, out_file, indent=2)
    print(f'Wrote {len(nums)} jsons to {out_path}')
