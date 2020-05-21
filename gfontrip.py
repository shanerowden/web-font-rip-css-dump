import requests, re, os, random
from sys import argv, exit
from pathlib import Path

try:
    script, url = argv
except ValueError:
    print('Usage: python gfontrip.py "https://fonts.googleapis.com/css?family=Bungee+Inline%7COrbitron:600..."')
    exit()

def get_google_css(link):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:73.0) Gecko/20100101 Firefox/73.0'}
    res = requests.get(link, headers=headers)
    res.raise_for_status()
    return res.text

def split_css_into_lines(data):
    return [line.strip() for line in data.split('\n')]

def isolate_selectors(data):
    selectors = []
    selector_props = []
    for line in data:
        if "@font-face {" in line:
            selector_props = []
        elif line == '}':
            selectors.append(selector_props)
        else:
            selector_props.append(line)
    return selectors

def selector_props_to_dicts(selectors):
    organized_selectors = []
    for sel in selectors:
        d = {}
        for prop in sel:
            if ': ' in prop:
                key, value = prop.split(': ')
                d[key] = value[:-1]
        organized_selectors.append(d)
    return organized_selectors

def make_dir(name):
    dir_path = Path.cwd().joinpath(name)
    if not dir_path.exists():
        print(f"Opening directory at {dir_path}")
        dir_path.mkdir()

def find_urls_in_text(css_text):
    url_regex = r'https://.*.woff2[)]'
    x = re.findall(url_regex, css_text)
    return x

def transform_dict(d):
    for each in d:
        src_url_tmp = each['src'].split(', ')[-1]
        url = find_urls_in_text(src_url_tmp)
        url = url[0][:-1]
        name = "".join(each['font-family'].strip("'").split(" ")) + \
               each['font-style'].capitalize() + \
               each['font-weight'] + '.woff2'

        download_font_file(name, url)

        new_src_head = ", ".join(each['src'].split(', ')[:-1]) + ", url("
        if new_src_head.startswith(", "):
            new_src_head = new_src_head[2:]
        new_src_tail = ") format('woff2')"

        each['src'] = new_src_head + f"'../fonts/{name}'" + new_src_tail
    return d


def download_font_file(name, url):
    res = requests.get(url)
    path = Path().cwd().joinpath('fonts', name)
    if not path.exists():
        with open(path, 'wb') as fo:
            fo.write(res.content)

def dump_new_css(d, text):
    path = Path().cwd().joinpath('css', 'ripped_google_fonts.css')
    with open(path, 'w') as fo:
        for each in d:
            fo.write("@font-face {\n")
            for k, v in each.items():
                fo.write(f"  {k}: {v};\n")
            fo.write('}\n\n')
    with open(path, 'a') as fo:
        fo.write("\n\n" + text)


def font_selectors(d):
    selectors = []
    text = ''
    font_types = ['sans-serif', 'cursive', 'monospace']
    r = random.choice(font_types)
    for each in d:
        name = "-".join(each['font-family'].strip("'").split(" "))
        selector_head = ".font-"+f"{name}".lower()+" {\n"
        selector_tail = f"   font-family: {each['font-family']}, {r};\n" + "}\n\n"
        selectors.append(selector_head + selector_tail)
    for sel in list(set(selectors)):
        text += sel
    return text

try:
    make_dir('static')
    os.chdir('static')
    make_dir('fonts')
    make_dir('css')
except PermissionError:
    print("Do you have read-write permissions in this directory?")
except FileExistsError:
    print("static/, static/fonts/, and static/css/ directories already exist.")

css_text = get_google_css(url)
lines = split_css_into_lines(css_text)
selectors = isolate_selectors(lines)
selector_dicts = selector_props_to_dicts(selectors)
new_dict = transform_dict(selector_dicts)
css_selectors = font_selectors(new_dict)
dump_new_css(new_dict, css_selectors)
