"""Offline explicit-inventory package builder. No network access at runtime."""
import argparse
import hashlib
import io
import ipaddress
import json
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import zlib
import subprocess
import unicodedata
from urllib.parse import unquote, urlsplit
import zipfile

from jsonschema import Draft202012Validator
from referencing import Registry

ROOT = Path(__file__).resolve().parents[1]
PLUGIN_ID = 'https://agent-plugins.org/schemas/1.0.0/plugin.schema.json'
MCP_ID = 'https://agent-plugins.org/schemas/1.0.0/mcp.schema.json'
MAX_ASSET = 5 * 1024 * 1024
MAX_FILE = 1024 * 1024
MAX_TOTAL = 16 * MAX_FILE
MAX_FILES = 256


def encoded(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load(path):
    def pairs(items):
        result = {}
        for k, v in items:
            if k in result:
                raise ValueError('Duplicate JSON key: ' + k)
            result[k] = v
        return result
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs)


def safe_name(name):
    if not isinstance(name, str) or not name or '\\' in name or ':' in name or name.startswith('/'):
        raise ValueError('Unsafe path')
    for part in name.split('/'):
        if not re.fullmatch(r'[A-Za-z0-9_.-]+', part) or part in ('.', '..') or part.endswith('.') or part.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *('COM'+str(i) for i in range(10)), *('LPT'+str(i) for i in range(10))}:
            raise ValueError('Unsafe path: ' + name)
    return name


def binary_asset(name):
    return bool(re.fullmatch(r'assets/[A-Za-z0-9_-]+\.png', name))


def png_check(data):
    if len(data) > MAX_ASSET or not data.startswith(b'\x89PNG\r\n\x1a\n'):
        raise ValueError('Invalid PNG signature or size')
    offset, chunks, compressed = 8, [], bytearray()
    width = height = channels = 0
    while offset < len(data):
        if offset + 12 > len(data):
            raise ValueError('Truncated PNG')
        size = struct.unpack_from('>I', data, offset)[0]
        kind = data[offset + 4:offset + 8]
        end = offset + size + 12
        if end > len(data) or not re.fullmatch(b'[A-Za-z]{4}', kind):
            raise ValueError('Invalid PNG chunk')
        body = data[offset + 8:end - 4]
        if zlib.crc32(kind + body) != struct.unpack_from('>I', data, end - 4)[0]:
            raise ValueError('PNG CRC mismatch')
        if not chunks and kind != b'IHDR':
            raise ValueError('Missing PNG header')
        if kind == b'IHDR':
            if chunks or size != 13:
                raise ValueError('Invalid PNG header')
            width, height, depth, color, comp, filt, interlace = struct.unpack('>IIBBBBB', body)
            if width != height or not 48 <= width <= 4096 or depth != 8 or color not in (2, 6) or comp or filt or interlace:
                raise ValueError('PNG requires square 48..4096 noninterlaced 8-bit RGB/RGBA')
            channels = 3 if color == 2 else 4
        elif kind == b'IDAT':
            if b'IDAT' in chunks and chunks[-1] != b'IDAT':
                raise ValueError('Noncontiguous PNG data')
            compressed.extend(body)
        elif kind == b'IEND':
            if size or end != len(data) or b'IDAT' not in chunks:
                raise ValueError('Invalid PNG end')
        elif kind == b'PLTE':
            if kind in chunks or b'IDAT' in chunks or not size or size % 3 or size > 768:
                raise ValueError('Invalid PNG palette')
        elif not kind[0] & 32 or kind in (b'acTL', b'fcTL', b'fdAT'):
            raise ValueError('Unsupported PNG chunk')
        chunks.append(kind)
        offset = end
    if not chunks or chunks[-1] != b'IEND':
        raise ValueError('Missing PNG end')
    expected = height * (1 + width * channels)
    decoder = zlib.decompressobj()
    pixels = decoder.decompress(bytes(compressed), expected + 1)
    if len(pixels) != expected or not decoder.eof or decoder.unused_data or decoder.unconsumed_tail:
        raise ValueError('Invalid PNG image stream')
    if any(pixels[i] > 4 for i in range(0, expected, 1 + width * channels)):
        raise ValueError('Invalid PNG row filter')


def read_input(root, name):
    safe_name(name)
    limit = MAX_ASSET if binary_asset(name) or re.fullmatch(r"plugins/[^/]+/assets/[A-Za-z0-9_-]+\.png", name) else MAX_FILE
    root = Path(root).absolute()
    path = root
    # Inspect ancestors too: resolve() alone would conceal reparse points.
    for ancestor in (*reversed(root.parents), root):
        info = ancestor.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('Linked source root')
    info = root.lstat()
    for part in name.split('/'):
        path /= part
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('Linked input')
    if not stat.S_ISREG(info.st_mode) or info.st_size > limit or info.st_nlink > 1:
        raise ValueError('Invalid input type, hardlink or size')
    with path.open('rb') as stream:
        data = stream.read(limit + 1)
    if len(data) > limit:
        raise ValueError('Input too large')
    return data


def check_schema(schema):
    Draft202012Validator.check_schema(schema)
    def walk(obj):
        if isinstance(obj, dict):
            for key, value in obj.items():
                if key in ('$ref', '$dynamicRef') and not value.startswith('#'):
                    raise ValueError('Nonlocal schema reference prohibited')
                walk(value)
        elif isinstance(obj, list):
            for value in obj:
                walk(value)
    walk(schema)


def validate(obj, schema_name):
    provenance = load(ROOT / 'schemas/provenance.json')
    record = next(r for r in provenance if r['file'] == schema_name)
    raw = read_input(ROOT / 'schemas', schema_name)
    if digest(raw) != record['sha256']:
        raise ValueError('Schema pin mismatch')
    schema = json.loads(raw)
    check_schema(schema)
    Draft202012Validator(schema, registry=Registry()).validate(obj)


def endpoint(url):
    parts = urlsplit(url)
    host = parts.hostname or ''
    if parts.scheme != 'https' or not host or parts.username or parts.password or parts.query or parts.fragment or parts.port not in (None, 443) or any(c in url for c in '${}<>'):
        raise ValueError('A concrete public HTTPS endpoint is required')
    if host in ('localhost', 'example.com', 'example.org', 'example.net') or host.endswith(('.local', '.internal', '.invalid', '.test', '.example')) or '.' not in host:
        raise ValueError('Nonpublic or placeholder endpoint')
    try:
        ip = ipaddress.ip_address(host)
    except ValueError:
        ip = None
    if ip is not None:
        raise ValueError('Endpoint must use a public DNS hostname')
    if any(ord(c) < 33 for c in url) or '\\' in url or any(p in ('.', '..') for p in unquote(parts.path).split('/')):
        raise ValueError('Unsafe endpoint path')
    return url


INTERFACE_TEXT_LIMITS = {'displayName': 30, 'shortDescription': 30,
                         'longDescription': 4000, 'developerName': 80}
INTERFACE_URLS = ('websiteURL', 'supportURL', 'privacyPolicyURL', 'termsOfServiceURL')
INTERFACE_CATEGORIES = ('Productivity', 'Creativity', 'Developer Tools', 'Business & Operations',
                        'Data & Analytics', 'Communication', 'Education & Research', 'Security',
                        'Finance', 'Healthcare', 'Travel', 'Entertainment', 'Other')


def interface_check(value):
    properties = {k: {'type': 'string', 'minLength': 1, 'maxLength': n}
                  for k, n in INTERFACE_TEXT_LIMITS.items()}
    properties.update({k: {'type': 'string', 'minLength': 1, 'maxLength': 1024}
                       for k in INTERFACE_URLS})
    properties.update({k: {'type': 'string', 'pattern': r'^\./assets/[A-Za-z0-9_-]+\.png$'} for k in ('logo', 'composerIcon')})
    properties['category'] = {'enum': list(INTERFACE_CATEGORIES)}
    prompt = {'type': 'string', 'minLength': 1, 'maxLength': 128}
    properties['defaultPrompt'] = {'oneOf': [prompt, {'type': 'array', 'maxItems': 3,
                                                     'uniqueItems': True, 'items': prompt}]}
    Draft202012Validator({'type': 'object', 'additionalProperties': False,
                         'properties': properties}).validate(value)
    for key, text in value.items():
        if key in INTERFACE_URLS:
            endpoint(text)
            host = urlsplit(text).hostname or ''
            if '@' in urlsplit(text).netloc or not re.fullmatch(r'(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+[A-Za-z][A-Za-z0-9-]{0,62}', host):
                raise ValueError('Unsafe listing hostname')
            if any(ord(c) < 33 or ord(c) == 127 for c in unquote(text)):
                raise ValueError('Unsafe encoded listing URL')
        elif key != 'defaultPrompt':
            listing_text(text, multiline=key == 'longDescription')
    prompts = value.get('defaultPrompt', [])
    if isinstance(prompts, str):
        prompts = [prompts]
    normalized = set()
    for text in prompts:
        listing_text(text)
        key = ' '.join(unicodedata.normalize('NFKC', text).split())
        if key in normalized or '@' in text:
            raise ValueError('Duplicate or mentioned starter prompt')
        normalized.add(key)


def listing_text(text, multiline=False):
    if not text.strip() or any(unicodedata.category(c).startswith('C') and not (multiline and c == '\n')
                               or (not multiline and c in '\u2028\u2029') for c in text):
        raise ValueError('Empty or unsupported listing text')


def inventory_check(inv):
    schema = {'type': 'object', 'required': ['name', 'version', 'description', 'skills', 'connectors'], 'additionalProperties': False,
              'properties': {'name': {'type': 'string', 'pattern': '^[a-z0-9]+(?:-[a-z0-9]+)*$'}, 'version': {'type': 'string', 'minLength': 1}, 'description': {'type': 'string', 'minLength': 1},
                             'skills': {'type': 'object', 'minProperties': 1, 'additionalProperties': {'type': 'array', 'minItems': 1, 'uniqueItems': True, 'items': {'type': 'string'}}},
                             'connectors': {'type': 'object', 'additionalProperties': {'type': 'string'}},
                             'assets': {'type': 'array', 'uniqueItems': True, 'maxItems': 16, 'items': {'type': 'string'}},
                             'openai_interface': {'type': 'object'},
                             'license': {'const': 'MIT'},
                             'license_file': {'const': 'LICENSE'},
                             'readme_file': {'type': 'string', 'pattern': r'^products/[a-z0-9]+(?:-[a-z0-9]+)*\.md$'},
                             'author': {'type': 'object', 'required': ['name'], 'additionalProperties': False,
                                        'properties': {'name': {'type': 'string', 'minLength': 1}}}}}
    Draft202012Validator(schema).validate(inv)
    if 'openai_interface' in inv:
        interface_check(inv['openai_interface'])
    if ('license' in inv) != ('license_file' in inv):
        raise ValueError('License metadata and explicit license_file must be selected together')
    if 'readme_file' in inv:
        safe_name(inv['readme_file'])
    for name in inv.get('assets', []):
        safe_name(name)
        if not binary_asset(name):
            raise ValueError('Unsupported asset path')
    for key in ('logo', 'composerIcon'):
        reference = inv.get('openai_interface', {}).get(key)
        if reference and reference[2:] not in inv.get('assets', []):
            raise ValueError('Artwork reference must be explicitly selected')
    for key, value in inv['connectors'].items():
        safe_name(key)
        endpoint(value)


def inputs(root, inv):
    inventory_check(inv)
    result = {}
    for name in inv.get('assets', []):
        if name.casefold() in {k.casefold() for k in result}:
            raise ValueError('Case-colliding asset')
        result[name] = read_input(root, name)
        png_check(result[name])
    if 'license_file' in inv:
        result[inv['license_file']] = read_input(root, inv['license_file'])
    if 'readme_file' in inv:
        result[inv['readme_file']] = read_input(root, inv['readme_file'])
    for skill, files in inv['skills'].items():
        safe_name(skill)
        if '/' in skill or 'SKILL.md' not in files:
            raise ValueError('Each skill needs SKILL.md')
        for relative in files:
            name = safe_name('skills/' + skill + '/' + relative)
            if name.casefold() in {k.casefold() for k in result}:
                raise ValueError('Case-colliding input')
            if any(re.search(r'(?i)(private|internal|credential|secret|\.env)', part) for part in relative.split('/')):
                raise ValueError('Nonpublic input filename')
            if not (relative.endswith('.md') or relative.endswith('.json') or relative.endswith('.txt')):
                raise ValueError('Unsupported public input type')
            if len(result) >= MAX_FILES:
                raise ValueError('Input count limit exceeded')
            result[name] = read_input(root, name)
            if sum(map(len, result.values())) > MAX_TOTAL:
                raise ValueError('Input size limit exceeded')
    if len(result) > MAX_FILES or sum(map(len, result.values())) > MAX_TOTAL:
        raise ValueError('Input limits exceeded')
    members = {('README.md' if n == inv.get('readme_file') else n): b for n, b in result.items()}
    for source_name, data in result.items():
        name = 'README.md' if source_name == inv.get('readme_file') else source_name
        if binary_asset(source_name):
            continue
        text = data.decode('utf-8')
        if re.search(r'(?i)(docs-private|docs-local|BEGIN .*PRIVATE KEY|sk-[a-z0-9]{20}|bearer\s+[a-z0-9._-]{12})', text):
            raise ValueError('Sensitive-content heuristic matched: ' + name)
        if name.endswith('.md'):
            links = re.findall(r'!?\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)', text)
            links += re.findall(r'^\s*\[[^\]]+\]:\s*(\S+)', text, flags=re.M)
            for link in links:
                if link.startswith('#'):
                    continue
                parsed = urlsplit(link)
                if parsed.scheme == 'https':
                    continue
                target = unquote(link.split('#')[0])
                if parsed.scheme or target.startswith('/') or '\\' in target or '?' in target:
                    raise ValueError('Unsafe reference')
                combined = str(PurePosixPath(name).parent / target)
                safe_name(combined)
                if combined not in members:
                    raise ValueError('Undeclared reference: ' + combined)
    return result


def snapshot(root, inv, files=None):
    if files is None:
        files = inputs(root, inv)
    builder_files = ['tools/pack.py', 'schemas/provenance.json', 'schemas/plugin.schema.json', 'schemas/mcp.schema.json']
    return {'format': 1, 'inventory_sha256': digest(encoded(inv)),
            'builder_inputs': {n: digest(read_input(ROOT, n)) for n in builder_files},
            'inputs': {n: digest(b) for n, b in sorted(files.items())}}


def inspect(raw):
    if len(raw) > MAX_TOTAL * 2:
        raise ValueError('Archive too large')
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        entries = z.infolist()
        if len(entries) > MAX_FILES + 8 or sum(e.file_size for e in entries) > MAX_TOTAL:
            raise ValueError('Archive limits exceeded')
        result = {}
        for e in entries:
            safe_name(e.filename)
            if e.filename.casefold() in {n.casefold() for n in result} or e.file_size > (MAX_ASSET if binary_asset(e.filename) else MAX_FILE) or stat.S_ISLNK(e.external_attr >> 16):
                raise ValueError('Unsafe archive entry')
            result[e.filename] = z.read(e)
        return result


def build(root, inv, lock, provider, release_commit=None):
    if provider not in ('openai', 'claude'):
        raise ValueError('Unknown provider')
    files = inputs(root, inv)
    if snapshot(root, inv, files) != lock:
        raise ValueError('Source differs from explicit content lock')
    if release_commit:
        if not re.fullmatch('[0-9a-f]{40}', release_commit):
            raise ValueError('Release requires full Git commit pin')
        def git(*parts):
            return subprocess.check_output(['git', '-C', str(root), *parts], text=True).strip()
        if git('rev-parse', 'HEAD') != release_commit or git('status', '--porcelain', '--untracked-files=all'):
            raise ValueError('Release requires clean pinned source checkout')
        for name, data in files.items():
            if subprocess.check_output(['git', '-C', str(root), 'show', release_commit + ':' + name]) != data:
                raise ValueError('Packaged bytes not pinned by release commit')
    manifest = {k: inv[k] for k in ('name', 'version', 'description')}
    if 'author' in inv:
        manifest['author'] = inv['author']
    if 'license' in inv:
        manifest['license'] = inv['license']
    if provider == 'openai':
        if 'openai_interface' in inv:
            manifest['extensions'] = {'com.openai': {'interface': inv['openai_interface']}}
        manifest['$schema'] = PLUGIN_ID
        validate(manifest, 'plugin.schema.json')
        manifest_path, mcp_path, transport = 'plugin.json', 'mcp.json', 'streamable-http'
    else:
        # Deliberately narrow documented Claude subset, not an official Claude schema.
        manifest_path, mcp_path, transport = '.claude-plugin/plugin.json', '.mcp.json', 'http'
        properties: dict = {k: {'type': 'string'} for k in ('name', 'version', 'description')}
        properties['license'] = {'const': 'MIT'}
        properties['author'] = {'type': 'object', 'required': ['name'], 'additionalProperties': False,
                                'properties': {'name': {'type': 'string', 'minLength': 1}}}
        Draft202012Validator({'type': 'object', 'required': ['name', 'version', 'description'], 'additionalProperties': False, 'properties': properties}).validate(manifest)
    if 'readme_file' in inv:
        files['README.md'] = files.pop(inv['readme_file'])
    files[manifest_path] = encoded(manifest)
    if inv['connectors']:
        mcp: dict = {'mcpServers': {n: {'type': transport, 'url': endpoint(u)} for n, u in sorted(inv['connectors'].items())}}
        if provider == 'openai':
            mcp['$schema'] = MCP_ID
            validate(mcp, 'mcp.schema.json')
        files[mcp_path] = encoded(mcp)
    files['package-inputs.json'] = encoded({'source': lock, 'provider': provider, 'files': {n: digest(b) for n, b in sorted(files.items())}})
    out = io.BytesIO()
    with zipfile.ZipFile(out, 'w', compression=zipfile.ZIP_STORED) as z:
        for name, data in sorted(files.items()):
            entry = zipfile.ZipInfo(name, (1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            z.writestr(entry, data)
    raw = out.getvalue()
    if inspect(raw) != files:
        raise ValueError('Generated archive differs from selected inputs')
    return raw


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=['lock', 'build'])
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--inventory', type=Path, required=True)
    parser.add_argument('--lock', type=Path, required=True)
    parser.add_argument('--provider', choices=['openai', 'claude'])
    parser.add_argument('--output', type=Path)
    parser.add_argument('--release-commit')
    args = parser.parse_args()
    inv = load(args.inventory)
    if args.action == 'lock':
        args.lock.parent.mkdir(parents=True, exist_ok=True)
        args.lock.write_bytes(encoded(snapshot(args.source, inv)))
        print('Locked explicit input hashes: ' + str(args.lock))
        return
    if not args.provider or not args.output:
        parser.error('build requires --provider and --output')
    raw = build(args.source, inv, load(args.lock), args.provider, release_commit=args.release_commit)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(raw)
    print(str(args.output) + ' sha256=' + digest(raw) + (' release-pin-checked' if args.release_commit else ' snapshot-only; not release approved'))


if __name__ == '__main__':
    main()
