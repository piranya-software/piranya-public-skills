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
