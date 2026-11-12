"""Generate reviewed in-repository Claude trees and both provider ZIPs."""
import argparse
import json
from pathlib import Path
import re
import stat
import tempfile

import pack

PACKAGES = ('site-management', 'reporting')
ROOT = Path(__file__).resolve().parents[1]


def expected(root):
    """Capture explicit inputs once; locks remain in memory, never release files."""
    result = {}
    with tempfile.TemporaryDirectory() as temporary:
        stage = Path(temporary)
        for name in PACKAGES:
            raw = pack.read_input(root, 'packages/' + name + '.json')
            inv = json.loads(raw)
            pack.inventory_check(inv)
            if not re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', inv['version']):
                raise ValueError('Distribution version must be numeric semver')
            selected = pack.inputs(root, inv)
            for path, data in selected.items():
                target = stage / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data.replace(b'\r\n', b'\n'))
            lock = pack.snapshot(stage, inv)
            for provider in ('claude', 'openai'):
                archive = pack.build(stage, inv, lock, provider)
                result['dist/' + name + '-' + provider + '.zip'] = archive
                if provider == 'claude':
                    for path, data in pack.inspect(archive).items():
                        result['plugins/' + name + '/' + path] = data
    return result


def guard(path):
    for component in (*reversed(path.parents), path):
        if component.exists() or component.is_symlink():
            info = component.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
                raise ValueError('Linked output path: ' + str(component))


def members(root, relative):
    base = root / relative
    guard(base)
    if not base.exists():
        return set()
    if not base.is_dir():
        raise ValueError('Output root is not a directory')
    found = set()
    for child in base.iterdir():
        guard(child)
        name = child.relative_to(root).as_posix()
        pack.safe_name(name)
        if child.is_dir():
            nested = members(root, name)
            if not nested:
                raise ValueError('Unexpected empty output directory: ' + name)
            found.update(nested)
        else:
            pack.read_input(root, name)
            found.add(name)
    return found


def distribute(root=ROOT, check=False):
    root = Path(root).absolute()
    guard(root)
    outputs = expected(root)
    plugin_names = {n for n in outputs if n.startswith('plugins/')}
    actual = members(root, 'plugins')
    if actual - plugin_names:
        raise ValueError('Unexpected generated members: ' + ', '.join(sorted(actual - plugin_names)))
    # dist is shared with the existing builder; only these four ZIPs are owned.
    for name in outputs:
        guard(root / name)
        if (root / name).exists():
            pack.read_input(root, name)
    if check:
        missing = [n for n, data in outputs.items()
                   if not (n.startswith('dist/') and not (root / n).exists())
                   and (not (root / n).is_file() or (root / n).read_bytes() != data)]
        if missing:
            raise ValueError('Missing or stale distribution: ' + ', '.join(missing))
    else:
        for name, data in outputs.items():
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    return outputs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Verify exact bytes and membership without writing')
    args = parser.parse_args()
    outputs = distribute(check=args.check)
    print(('Checked' if args.check else 'Generated') + ' ' + str(len(outputs)) + ' files (2 Claude trees, 4 ZIPs)')


if __name__ == '__main__':
    main()
