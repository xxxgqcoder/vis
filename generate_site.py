import os
import argparse
import re

from jinja2 import Template

parser = argparse.ArgumentParser()
parser.add_argument('--work_dir', help="work dir", type=str)
parser.add_argument('--home_page', help="file name of home page", type=str)
parser.add_argument('--pages_root_dir', help="root directory for pages", type=str)
parser.add_argument('--out_root_dir', help="output directory for pages", type=str)


def page_filter(root_dir, file_name):
    """
    filter pages whose file name has html as suffix and only contains: 0-9, a-z, _ for name part.
    turn true for directory.

    :param file_name: page file name with .html suffix
    :param root_dir: directory that contains file_name

    :return: true if file_name (except the .html suffix) matches pattern, false else
    """
    file_name = os.path.basename(file_name)
    if not os.path.isfile(os.path.join(root_dir, file_name)):
        return True
    dot_idx = file_name.rfind('.')
    if dot_idx == -1:
        return False
    if file_name[dot_idx:] != '.html':
        return False
    name = file_name[:dot_idx]
    m = re.match('^[a-z0-9_]+$', name)
    if not m:
        return False
    return True


def trim_prefix(prefix, s):
    return s[s.startswith(prefix) and len(prefix):]


def path_last_folder(p):
    return os.path.basename(os.path.normpath(p))


def process_pages(args):
    def dir_hanlder(pages_root_dir, root, dirs, files):
        root = trim_prefix(pages_root_dir, root)
        siblings = [os.path.join('/', root, p) for p in files + dirs]
        for s in siblings:
            f_path = os.path.join(pages_root_dir, trim_prefix('/', s))
            if os.path.isdir(f_path):
                continue
            with open(f_path) as f:
                content = f.read()
                data = {
                    "context": {
                        "siblings": sorted(siblings),
                        "current_path": s,
                    },
                }
                j2_template = Template(content)
                out_path = os.path.join(args.out_root_dir, trim_prefix('/', s))
                if os.path.isfile(out_path):
                    os.remove(out_path)
                os.makedirs(os.path.dirname(out_path), exist_ok=True)
                with open(out_path, 'w') as out:
                    out.write(j2_template.render(data))


    for root, dirs, files in os.walk(args.pages_root_dir, topdown=True):
        files = [f for f in files if page_filter(root, f)]
        print(f'processing directory: {root}')
        dir_hanlder(args.pages_root_dir, root, dirs, files)


def process(args):
    # process home page
    # process_home_page(args)

    # walk through pages dir and output generated pages
    process_pages(args)


    

def main():
    args = parser.parse_args()
    process(args)



if __name__ == "__main__":
    main()