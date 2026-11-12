import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location('pack', Path(__file__).parents[1] / 'tools/pack.py')
assert SPEC is not None and SPEC.loader is not None
p = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(p)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        f = self.root / 'skills/demo/SKILL.md'
        f.parent.mkdir(parents=True)
        f.write_text('---\nname: demo\ndescription: Synthetic test\n---\nHello\n')
        self.inventory = {'name': 'demo', 'version': '0.1.0', 'description': 'Synthetic',
                          'skills': {'demo': ['SKILL.md']}, 'connectors': {}}

    def snapshot(self):
        return p.snapshot(self.root, self.inventory)

    def select_icon(self):
        self.inventory['assets'] = ['assets/icon.png']
        self.inventory['openai_interface'] = {'logo': './assets/icon.png', 'composerIcon': './assets/icon.png'}
        target = self.root / 'assets/icon.png'
        target.parent.mkdir(exist_ok=True)
        target.write_bytes((p.ROOT / 'assets/piranya-icon.png').read_bytes())
        return target

    def test_binary_binding_capture_and_tamper(self):
        from unittest.mock import patch
        target = self.select_icon()
        lock = self.snapshot()
        captured = p.inputs(self.root, self.inventory)
        target.write_bytes(b'tampered')
        for provider in ('openai', 'claude'):
            with self.assertRaises(ValueError):
                p.build(self.root, self.inventory, lock, provider)
            with patch.object(p, 'inputs', return_value=dict(captured)) as capture:
                raw = p.build(self.root, self.inventory, lock, provider)
                self.assertEqual(capture.call_count, 1)
                files = p.inspect(raw)
                self.assertEqual(files['assets/icon.png'], captured['assets/icon.png'])
                proof = json.loads(files['package-inputs.json'])
                self.assertEqual(proof['files']['assets/icon.png'], lock['inputs']['assets/icon.png'])
        target.write_bytes(captured['assets/icon.png'])
        self.inventory['openai_interface']['logo'] = './assets/other.png'
        with self.assertRaises(Exception):
            self.snapshot()

    def test_binary_selection_safety(self):
        target = self.select_icon()
        for name in ('../icon.png', 'assets/../icon.png', 'assets/icon.svg', 'assets/nested/icon.png', 'assets/icon.png\n'):
            with self.subTest(name=name), self.assertRaises(Exception):
                p.snapshot(self.root, {**self.inventory, 'assets': [name]})
        self.inventory['assets'].append('assets/Icon.png')
        with self.assertRaises(ValueError):
            self.snapshot()
        self.inventory['assets'] = ['assets/missing.png']
        self.inventory.pop('openai_interface')
        with self.assertRaises(FileNotFoundError):
            self.snapshot()
        self.inventory.pop('assets')
        files = p.inspect(p.build(self.root, self.inventory, self.snapshot(), 'claude'))
        self.assertNotIn('assets/icon.png', files)

    def test_claude_icon_selected_exact_bytes(self):
        self.select_icon()
        self.inventory['claude_icon'] = './assets/icon.png'
        lock = self.snapshot()
        for provider, path in [('claude', '.claude-plugin/plugin.json'), ('openai', 'plugin.json')]:
            files = p.inspect(p.build(self.root, self.inventory, lock, provider))
            manifest = json.loads(files[path])
            if provider == 'claude':
                self.assertEqual(manifest['icon'], './assets/icon.png')
            else:
                self.assertNotIn('icon', manifest)
            self.assertEqual(files['assets/icon.png'], (self.root / 'assets/icon.png').read_bytes())
        (self.root / 'assets/icon.png').unlink()
        with self.assertRaises(FileNotFoundError):
            self.snapshot()

    def test_claude_icon_references_fail_closed(self):
        self.select_icon()
        for reference in ('./assets/missing.png', './assets/icon.svg', '../assets/icon.png',
                          'assets/icon.png', './assets/nested/icon.png', './assets/icon.png\n'):
            with self.subTest(reference=reference), self.assertRaises(Exception):
                p.snapshot(self.root, {**self.inventory, 'claude_icon': reference})
        with self.assertRaises(Exception):
            p.snapshot(self.root, {**self.inventory, 'claude_interface': {'icon': './assets/icon.png'}})

    def test_icon_reparse_and_symlink_rejected(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        target = self.select_icon()
        original = Path.lstat
        for mode, attributes in ((0o120777, 0), (0o100644, 0x400)):
            def marked(path, *args, **kwargs):
                if path == target:
                    return SimpleNamespace(st_mode=mode, st_file_attributes=attributes)
                return original(path, *args, **kwargs)
            with patch.object(Path, 'lstat', marked), self.assertRaises(ValueError):
                self.snapshot()

    def test_png_structure_bounds_and_size(self):
        import struct
        import zlib
        target = self.select_icon()
        def chunk(kind, body):
            return struct.pack('>I', len(body)) + kind + body + struct.pack('>I', zlib.crc32(kind + body))
        def image(w, h, pixels=None):
            rows = pixels if pixels is not None else (b'\0' + bytes(w * 4)) * h
            return b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)) + chunk(b'IDAT', zlib.compress(rows)) + chunk(b'IEND', b'')
        for width in (48, 4096):
            p.png_check(image(width, width))
        valid = image(48, 48)
        for data in (b'not png', valid[:-1], valid + b'extra', valid[:30] + b'bad' + valid[33:],
                     image(47, 47), image(4097, 4097), image(48, 49), image(48, 48, b'bad'),
                     image(48, 48, (b'\5' + bytes(48 * 4)) * 48), valid + bytes(p.MAX_ASSET)):
            target.write_bytes(data)
            with self.assertRaises(Exception):
                self.snapshot()
        target.write_bytes(valid)
        lock = self.snapshot()
        target.write_bytes(image(49, 49))
        with self.assertRaises(ValueError):
            p.build(self.root, self.inventory, lock, 'openai')

    def test_interface_bounds_and_types(self):
        for field, limit in p.INTERFACE_TEXT_LIMITS.items():
            p.interface_check({field: 'x' * limit})
            for value in ('x' * (limit + 1), '', '   ', None, 1, 'bad\nline', 'bad\x00text'):
                if field == 'longDescription' and value == 'bad\nline':
                    continue
                with self.subTest(field=field, value=value), self.assertRaises(Exception):
                    p.interface_check({field: value})
        p.interface_check({'longDescription': 'Allowed\nparagraph'})
        for category in p.INTERFACE_CATEGORIES:
            p.interface_check({'category': category})
        for value in ('Unknown', '', None, 1):
            with self.assertRaises(Exception):
                p.interface_check({'category': value})

    def test_interface_known_fields_only(self):
        for field in ('logo', 'composerIcon', 'extensions', 'capabilities', 'brandColor', 'invented'):
            with self.assertRaises(Exception):
                p.interface_check({field: 'unsupported'})
        for field in ('extensions', 'interface'):
            with self.assertRaises(Exception):
                p.inventory_check({**self.inventory, field: {}})
        for value in (None, [], 'text'):
            with self.assertRaises(Exception):
                p.inventory_check({**self.inventory, 'openai_interface': value})

    def test_interface_urls(self):
        for field in p.INTERFACE_URLS:
            p.interface_check({field: 'https://support.piranya.dk/'})
            for value in ('http://public.org/', 'javascript:alert(1)', 'https://u:p@public.org/',
                          'https://@public.org/', 'https://public.org/?token=synthetic', 'https://public.org/#secret',
                          'https://localhost/', 'https://127.0.0.1/', 'https://public.internal/',
                          'https://public.org:8443/', 'https://public.org/../x',
                          'https://public.org/%2e%2e/x', 'https://public.org/%0asecret',
                          'https://public.org\\@other.org/', 'https://%70ublic.org/',
                          'https://public.org/' + 'x' * 1024, '', None):
                with self.subTest(field=field, value=value), self.assertRaises(Exception):
                    p.interface_check({field: value})

    def test_interface_prompts(self):
        for value in ('x' * 128, ['one', 'two', 'three'], []):
            p.interface_check({'defaultPrompt': value})
        for value in ('x' * 129, ['one'] * 2, ['a', ' a '], ['Ａ', 'A'],
                      ['a b', 'a  b'], ['a', 'b', 'c', 'd'], [''], [' '],
                      ['bad\nline'], ['@server do this'], [1], None):
            with self.subTest(value=value), self.assertRaises(Exception):
                p.interface_check({'defaultPrompt': value})

    def test_interface_provider_isolation_offline_and_stale_lock(self):
        from unittest.mock import patch
        self.inventory['openai_interface'] = {'displayName': 'Synthetic', 'defaultPrompt': ['Inspect first.']}
        lock = self.snapshot()
        with patch('socket.socket', side_effect=AssertionError('Network prohibited')):
            for provider, path in (('openai', 'plugin.json'), ('claude', '.claude-plugin/plugin.json')):
                raw = p.build(self.root, self.inventory, lock, provider)
                self.assertEqual(raw, p.build(self.root, self.inventory, lock, provider))
                manifest = json.loads(p.inspect(raw)[path])
                self.assertNotIn('openai_interface', manifest)
                if provider == 'openai':
                    self.assertEqual(manifest['extensions'], {'com.openai': {'interface': self.inventory['openai_interface']}})
                    p.validate(manifest, 'plugin.schema.json')
                else:
                    self.assertNotIn('extensions', manifest)
        self.inventory['openai_interface']['displayName'] = 'Changed'
        for provider in ('openai', 'claude'):
            with self.assertRaises(ValueError):
                p.build(self.root, self.inventory, lock, provider)
        del self.inventory['openai_interface']
        for provider in ('openai', 'claude'):
            with self.assertRaises(ValueError):
                p.build(self.root, self.inventory, lock, provider)
        manifest = json.loads(p.inspect(p.build(self.root, self.inventory, self.snapshot(), 'openai'))['plugin.json'])
        self.assertNotIn('extensions', manifest)

    def test_readme_mapping_and_lock_both_providers(self):
        self.inventory['readme_file'] = 'products/demo.md'
        path = self.root / 'products/demo.md'
        path.parent.mkdir()
        path.write_bytes(b'[Skill](skills/demo/SKILL.md) [Docs](https://public.org/docs)\n')
        lock = self.snapshot()
        for provider in ('openai', 'claude'):
            files = p.inspect(p.build(self.root, self.inventory, lock, provider))
            self.assertEqual(files['README.md'], path.read_bytes())
            self.assertNotIn('products/demo.md', files)
            proof = json.loads(files['package-inputs.json'])
            self.assertEqual(proof['source']['inputs']['products/demo.md'], p.digest(path.read_bytes()))
            self.assertEqual(proof['files']['README.md'], p.digest(path.read_bytes()))
        path.write_bytes(b'Changed\n')
        for provider in ('openai', 'claude'):
            with self.assertRaises(ValueError):
                p.build(self.root, self.inventory, lock, provider)

    def test_readme_missing_unsafe_and_closure(self):
        for name in ('README.md', '../demo.md', 'products/../demo.md', 'products/demo.txt',
                     'products/nested/demo.md', 'products/Demo.md', 'products/demo.md\n'):
            with self.subTest(name=name), self.assertRaises(Exception):
                p.snapshot(self.root, {**self.inventory, 'readme_file': name})
        self.inventory['readme_file'] = 'products/demo.md'
        with self.assertRaises(FileNotFoundError):
            self.snapshot()
        path = self.root / 'products/demo.md'
        path.parent.mkdir()
        for content in (b'[Missing](docs/guide.md)', b'[Escape](../LICENSE)', b'\xff'):
            path.write_bytes(content)
            with self.assertRaises((ValueError, UnicodeDecodeError)):
                self.snapshot()

    def test_readme_capture_and_inventory_drift(self):
        from unittest.mock import patch
        self.inventory['readme_file'] = 'products/demo.md'
        path = self.root / 'products/demo.md'
        path.parent.mkdir()
        path.write_bytes(b'Captured\n')
        lock = self.snapshot()
        genuine = p.inputs(self.root, self.inventory)
        for provider in ('openai', 'claude'):
            changed = {**genuine, 'products/demo.md': b'Unlocked'}
            with patch.object(p, 'inputs', return_value=changed) as capture:
                with self.assertRaises(ValueError):
                    p.build(self.root, self.inventory, lock, provider)
                self.assertEqual(capture.call_count, 1)
        del self.inventory['readme_file']
        with self.assertRaises(ValueError):
            p.build(self.root, self.inventory, lock, 'openai')
        files = p.inspect(p.build(self.root, self.inventory, self.snapshot(), 'openai'))
        self.assertNotIn('README.md', files)

    def test_repeat_build_and_skills_only(self):
        lock = self.snapshot()
        for provider in ('openai', 'claude'):
            a = p.build(self.root, self.inventory, lock, provider)
            self.assertEqual(a, p.build(self.root, self.inventory, lock, provider))
            self.assertIn('skills/demo/SKILL.md', p.inspect(a))

    def test_declared_author_both_providers(self):
        self.inventory['author'] = {'name': 'Synthetic Publisher'}
        for provider, path in [('openai', 'plugin.json'), ('claude', '.claude-plugin/plugin.json')]:
            manifest = json.loads(p.inspect(p.build(self.root, self.inventory, self.snapshot(), provider))[path])
            self.assertEqual(manifest['author'], self.inventory['author'])

    def test_explicit_license_both_providers_and_stale_lock(self):
        self.inventory.update(license='MIT', license_file='LICENSE')
        license_path = self.root / 'LICENSE'
        license_path.write_bytes(b'Synthetic license fixture\n')
        lock = self.snapshot()
        for provider, manifest_path in [('openai', 'plugin.json'), ('claude', '.claude-plugin/plugin.json')]:
            files = p.inspect(p.build(self.root, self.inventory, lock, provider))
            self.assertEqual(files['LICENSE'], license_path.read_bytes())
            self.assertEqual(json.loads(files[manifest_path])['license'], 'MIT')
            provenance = json.loads(files['package-inputs.json'])
            self.assertEqual(provenance['source']['inputs']['LICENSE'], p.digest(files['LICENSE']))
            self.assertEqual(provenance['files']['LICENSE'], p.digest(files['LICENSE']))
        license_path.write_bytes(b'Changed license\n')
        for provider in ('openai', 'claude'):
            with self.assertRaises(ValueError):
                p.build(self.root, self.inventory, lock, provider)

    def test_license_is_not_implicitly_included(self):
        (self.root / 'LICENSE').write_bytes(b'Unselected fixture')
        for provider in ('openai', 'claude'):
            files = p.inspect(p.build(self.root, self.inventory, self.snapshot(), provider))
            self.assertNotIn('LICENSE', files)

    def test_license_selection_restricted(self):
        for fields in ({'license': 'MIT'}, {'license_file': 'LICENSE'},
                       {'license': 'Apache-2.0', 'license_file': 'LICENSE'},
                       {'license': 'MIT', 'license_file': '../LICENSE'},
                       {'license': 'MIT', 'license_file': 'README.md'},
                       {'license': None, 'license_file': 'LICENSE'}):
            with self.subTest(fields=fields), self.assertRaises(Exception):
                p.snapshot(self.root, {**self.inventory, **fields})

    def test_missing_selected_license_fails(self):
        self.inventory.update(license='MIT', license_file='LICENSE')
        with self.assertRaises(FileNotFoundError):
            self.snapshot()

    def test_selected_license_uses_input_safety_checks(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        self.inventory.update(license='MIT', license_file='LICENSE')
        target = self.root / 'LICENSE'
        target.write_bytes(b'Synthetic fixture')
        original = Path.lstat
        def marked(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path == target:
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch.object(Path, 'lstat', marked), self.assertRaises(ValueError):
            self.snapshot()
        with patch.object(p, 'MAX_FILE', 4), self.assertRaises(ValueError):
            self.snapshot()
        target.write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError):
            self.snapshot()

    def test_unknown_source(self):
        lock = self.snapshot()
        (self.root / 'skills/demo/SKILL.md').write_text('changed')
        with self.assertRaises(ValueError):
            p.build(self.root, self.inventory, lock, 'openai')

    def test_build_verifies_captured_bytes_without_rereading(self):
        from unittest.mock import patch
        lock = self.snapshot()
        genuine = p.inputs(self.root, self.inventory)
        changed = {**genuine, 'skills/demo/SKILL.md': b'UNLOCKED BYTES'}
        with patch.object(p, 'inputs', side_effect=[changed, genuine]) as capture:
            with self.assertRaises(ValueError):
                p.build(self.root, self.inventory, lock, 'openai')
            self.assertEqual(capture.call_count, 1)

    def test_generic_connector_path(self):
        self.assertEqual(p.endpoint('https://connector.public.org/api/connector'), 'https://connector.public.org/api/connector')

    def test_private_file_not_archived(self):
        (self.root / 'credentials.txt').write_text('private synthetic value')
        self.assertNotIn('credentials.txt', p.inspect(p.build(self.root, self.inventory, self.snapshot(), 'openai')))

    def test_unsafe_paths(self):
        for name in ('../secret', '/secret', 'C:/secret', 'a\\b', 'a/../b', 'CON', 'a.'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                p.safe_name(name)

    def test_case_collision(self):
        self.inventory['skills']['demo'] += ['skill.md']
        with self.assertRaises(ValueError):
            self.snapshot()

    def test_links_closed(self):
        (self.root / 'skills/demo/SKILL.md').write_text('[private](../../private.md)')
        with self.assertRaises(ValueError):
            self.snapshot()

    def test_symlink(self):
        target = self.root / 'skills/demo/ref.md'
        try:
            target.symlink_to(self.root / 'credentials.txt')
        except OSError:
            self.skipTest('host does not permit symlink creation')
        self.inventory['skills']['demo'].append('ref.md')
        with self.assertRaises(ValueError):
            self.snapshot()

    def test_multiple_connectors(self):
        self.inventory['connectors'] = {'one': 'https://mcpserver.prod.core.piranya.io/mcp/site-management', 'two': 'https://mcpserver.prod.core.piranya.io/mcp/reporting'}
        for provider, transport in [('openai', 'streamable-http'), ('claude', 'http')]:
            data = p.inspect(p.build(self.root, self.inventory, self.snapshot(), provider))
            config = json.loads(data['mcp.json' if provider == 'openai' else '.mcp.json'])
            self.assertEqual(len(config['mcpServers']), 2)
            self.assertEqual(config['mcpServers']['one']['type'], transport)

    def test_wrong_transport_and_unknown_field(self):
        for obj in ({'$schema': p.MCP_ID, 'mcpServers': {'bad': {'type': 'http', 'url': 'https://example.com/mcp'}}}, {'$schema': p.MCP_ID, 'mcpServers': {}, 'invented': True}):
            with self.assertRaises(Exception):
                p.validate(obj, 'mcp.schema.json')

    def test_malformed_schema(self):
        with self.assertRaises(Exception):
            p.check_schema({'type': 'invented'})

    def test_unknown_inventory(self):
        self.inventory['private'] = 'no'
        with self.assertRaises(Exception):
            self.snapshot()

    def test_endpoint_rejections(self):
        for url in ('http://example.com/mcp', 'https://localhost/mcp', 'https://example.com/mcp', 'https://10.0.0.1/mcp', 'https://user:pass@public.com/mcp', 'https://public.com/${ENDPOINT}'):
            with self.subTest(url=url), self.assertRaises(ValueError):
                p.endpoint(url)

    def test_mocked_reparse_rejected(self):
        from unittest.mock import patch
        from types import SimpleNamespace
        original = Path.lstat
        def marked(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path.name == 'SKILL.md':
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch.object(Path, 'lstat', marked), self.assertRaises(ValueError):
            self.snapshot()

    def test_declared_reference_and_missing_reference(self):
        (self.root / 'skills/demo/SKILL.md').write_text('[Reference](ref.md)')
        (self.root / 'skills/demo/ref.md').write_text('Public synthetic reference')
        with self.assertRaises(ValueError):
            self.snapshot()
        self.inventory['skills']['demo'].append('ref.md')
        self.assertEqual(len(self.snapshot()['inputs']), 2)

    def test_private_selected_input(self):
        self.inventory['skills']['demo'].append('private.md')
        (self.root / 'skills/demo/private.md').write_text('synthetic')
        with self.assertRaises(ValueError):
            self.snapshot()

    def test_remote_schema_ref_never_allowed(self):
        with self.assertRaises(ValueError):
            p.check_schema({'$ref': 'https://example.com/never-fetch'})

    def test_input_size_limit(self):
        from unittest.mock import patch
        with patch.object(p, 'MAX_FILE', 4), self.assertRaises(ValueError):
            self.snapshot()

    def test_cli_snapshot_and_build(self):
        import subprocess
        import sys
        inv = self.root / 'inventory.json'
        inv.write_bytes(p.encoded(self.inventory))
        lock = self.root / 'snapshot.json'
        command = [sys.executable, str(p.ROOT / 'tools/pack.py')]
        common = ['--source', str(self.root), '--inventory', str(inv), '--lock', str(lock)]
        subprocess.run(command + ['lock'] + common, check=True, capture_output=True)
        for provider in ('openai', 'claude'):
            output = self.root / (provider + '.zip')
            result = subprocess.run(command + ['build'] + common + ['--provider', provider, '--output', str(output)], check=True, capture_output=True, text=True)
            self.assertIn('snapshot-only', result.stdout)
            self.assertIn('package-inputs.json', p.inspect(output.read_bytes()))
        result = subprocess.run(command + ['build'] + common + ['--provider', 'openai', '--output', str(output), '--release-commit', 'not-a-commit'], capture_output=True)
        self.assertNotEqual(result.returncode, 0)

    def test_duplicate_zip(self):
        import io
        b = io.BytesIO()
        with zipfile.ZipFile(b, 'w') as z:
            z.writestr('x', 'a')
            z.writestr('x', 'b')
        with self.assertRaises(ValueError):
            p.inspect(b.getvalue())


if __name__ == '__main__':
    unittest.main()
