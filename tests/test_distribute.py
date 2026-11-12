import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'tools'))
SPEC = importlib.util.spec_from_file_location('distribute', ROOT / 'tools/distribute.py')
assert SPEC is not None and SPEC.loader is not None
d = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(d)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copyfile(ROOT / 'LICENSE', self.root / 'LICENSE')
        for folder in ('skills', 'packages', 'products'):
            shutil.copytree(ROOT / folder, self.root / folder)

    def test_reproducible_and_provider_parity(self):
        outputs = d.distribute(self.root)
        self.assertEqual(outputs, d.distribute(self.root, check=True))
        self.assertEqual(outputs, d.expected(self.root))
        for name in d.PACKAGES:
            a = d.pack.inspect(outputs['dist/' + name + '-claude.zip'])
            b = d.pack.inspect(outputs['dist/' + name + '-openai.zip'])
            self.assertEqual({k: v for k, v in a.items() if k.startswith('skills/')},
                             {k: v for k, v in b.items() if k.startswith('skills/')})
            source = json.loads(a['package-inputs.json'])['source']
            self.assertEqual(source, json.loads(b['package-inputs.json'])['source'])
            self.assertIn('tools/pack.py', source['builder_inputs'])
            for files, manifest in ((a, '.claude-plugin/plugin.json'), (b, 'plugin.json')):
                self.assertEqual(files['README.md'], (self.root / ('products/' + name + '.md')).read_bytes())
                self.assertEqual((self.root / ('plugins/' + name + '/README.md')).read_bytes(), files['README.md'])
                self.assertEqual(source['inputs']['products/' + name + '.md'], d.pack.digest(files['README.md']))
                self.assertEqual(files['LICENSE'], (ROOT / 'LICENSE').read_bytes())
                self.assertEqual(json.loads(files[manifest])['license'], 'MIT')
                self.assertEqual(source['inputs']['LICENSE'], d.pack.digest(files['LICENSE']))
            self.assertFalse(any('lock.json' in k for k in a))

    def test_product_sources_unchanged_and_readme_drift(self):
        sources = {p: p.read_bytes() for p in (self.root / 'products').glob('*.md')}
        d.distribute(self.root)
        self.assertEqual(sources, {p: p.read_bytes() for p in sources})
        target = self.root / 'plugins/reporting/README.md'
        target.write_bytes(b'Unreviewed edit')
        with self.assertRaises(ValueError):
            d.distribute(self.root, check=True)
        self.assertEqual(target.read_bytes(), b'Unreviewed edit')
        inventory = self.root / 'packages/reporting.json'
        inv = json.loads(inventory.read_bytes())
        del inv['readme_file']
        inventory.write_bytes(d.pack.encoded(inv))
        with self.assertRaises(ValueError):
            d.distribute(self.root)
        self.assertEqual(sources, {p: p.read_bytes() for p in sources})

    def test_check_missing_is_read_only(self):
        with self.assertRaises(ValueError):
            d.distribute(self.root, check=True)
        self.assertFalse((self.root / 'plugins').exists())
        self.assertFalse((self.root / 'dist').exists())

    def test_check_stale_is_read_only(self):
        d.distribute(self.root)
        target = self.root / 'plugins/reporting/.mcp.json'
        target.write_bytes(b'stale')
        with self.assertRaises(ValueError):
            d.distribute(self.root, check=True)
        self.assertEqual(target.read_bytes(), b'stale')

    def test_extra_rejected_before_any_write(self):
        outputs = d.distribute(self.root)
        extra = self.root / 'plugins/unmanaged.txt'
        extra.write_bytes(b'keep')
        for check in (False, True):
            with self.assertRaises(ValueError):
                d.distribute(self.root, check=check)
        self.assertEqual(extra.read_bytes(), b'keep')
        for name, data in outputs.items():
            self.assertEqual((self.root / name).read_bytes(), data)

    def test_empty_extra_directory_rejected(self):
        d.distribute(self.root)
        (self.root / 'plugins/extra').mkdir()
        with self.assertRaises(ValueError):
            d.distribute(self.root)

    def test_source_eol_is_stable(self):
        before = d.expected(self.root)
        for path in (self.root / 'skills').rglob('*.md'):
            path.write_bytes(path.read_bytes().replace(b'\n', b'\r\n'))
        self.assertEqual(before, d.expected(self.root))

    def test_unrelated_outputs_preserved(self):
        (self.root / 'dist').mkdir()
        other = self.root / 'dist/operator.lock.json'
        other.write_bytes(b'keep')
        d.distribute(self.root)
        self.assertEqual(other.read_bytes(), b'keep')

    def test_linked_output_rejected(self):
        outside = self.root / 'outside'
        outside.mkdir()
        try:
            (self.root / 'plugins').symlink_to(outside, target_is_directory=True)
        except OSError:
            self.skipTest('host does not permit symlink creation')
        with self.assertRaises(ValueError):
            d.distribute(self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_mocked_output_reparse_rejected(self):
        from types import SimpleNamespace
        from unittest.mock import patch
        d.distribute(self.root)
        original = Path.lstat
        def marked(path, *args, **kwargs):
            info = original(path, *args, **kwargs)
            if path.name == 'plugins':
                return SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400)
            return info
        with patch.object(Path, 'lstat', marked), self.assertRaises(ValueError):
            d.distribute(self.root)

    def test_fresh_checkout_check_without_ignored_zips(self):
        d.distribute(self.root)
        shutil.rmtree(self.root / 'dist')
        d.distribute(self.root, check=True)
        self.assertFalse((self.root / 'dist').exists())

    def test_unsafe_inventory_rejected(self):
        path = self.root / 'packages/reporting.json'
        inv = json.loads(path.read_bytes())
        inv['skills'] = {'../escape': ['SKILL.md']}
        path.write_bytes(d.pack.encoded(inv))
        with self.assertRaises(ValueError):
            d.distribute(self.root)
        self.assertFalse((self.root / 'plugins').exists())


if __name__ == '__main__':
    unittest.main()
