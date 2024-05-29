import json
from pathlib import Path

from token_cleaning import clean_text


def proc_meta(meta: list) -> dict:
    temp = [x.split(':\xa0') for x in meta]
    temp_meta = {'title': clean_text(temp[0][0]),
                 'service': temp[1][0],
                 'pubdate': clean_text(temp[2][0])}
    for t in temp:
        if len(t) == 2:
            temp_meta[t[0].lower()] = clean_text(t[1])
    return temp_meta


def _run_dev(name):
    in_path = Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/disab/2020s/json/{name}.json')
    data = json.load(in_path.open())
    new_data = []
    for d in data:
        new_data.append({'meta': proc_meta(d['meta']), 'body': d['body']})
    out_path = Path(f'/run/media/noah/TOSHIBA EXT/disab_trends_corp/disab/2020s/json/{name}-p.json')
    with open(out_path, 'w') as f:
        json.dump(new_data, f, indent=2)
    print(f'Wrote {out_path}')


if __name__ == '__main__':
    raise Exception("Don't run this file directly - Use rtf_scrape.py instead and/or refer to comment.")
    # This module can be run directly for development. To do so, remove
    # the proc_meta call in the return line of rtf_scrape.proc_rtf
    # and uncomment the below line, adjusting paths as needed.

    # _run_dev('2020s-1')
