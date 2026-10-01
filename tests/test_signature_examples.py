"""Execute the documented HTTP example offline; requests is replaced before import."""
import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import types
import unittest
from unittest.mock import Mock, patch

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/jeepay-open-integration'
FIXTURE = json.loads((ROOT / 'tests/signature_vectors.json').read_text(encoding='utf-8'))


def load_http_example(path):
    blocks = re.findall(r'^```python\n(.*?)^```', path.read_text(encoding='utf-8'), re.M | re.S)
    blocks = [block for block in blocks if 'def call_jeepay_api(' in block]
    if len(blocks) != 1:
        raise AssertionError(f'{path}: expected one HTTP example, got {len(blocks)}')
    requests = types.ModuleType('requests')
    requests.post = Mock(return_value=types.SimpleNamespace(json=lambda: {'code': 0}))
    namespace = {}
    with patch.dict('sys.modules', {'requests': requests}):
        exec(compile(blocks[0], str(path), 'exec'), namespace)
    return namespace['call_jeepay_api'], requests.post


class SignatureExamplesTest(unittest.TestCase):
    def test_actual_http_examples_against_golden_vectors(self):
        for file in ['references/sdk-reminder.md', 'references/bundle.md']:
            call, post = load_http_example(SKILL / file)
            for vector in FIXTURE['vectors']:
                with self.subTest(file=file, vector=vector['name']):
                    params = copy.deepcopy(vector['params'])
                    original = copy.deepcopy(params)
                    with patch('time.time', return_value=FIXTURE['time_seconds']):
                        result = call(FIXTURE['api_key'], 'https://example.invalid', 'api/pay/unifiedOrder', params)
                    self.assertEqual(result, {'code': 0})
                    self.assertEqual(post.call_args.args, ('https://example.invalid/api/pay/unifiedOrder',))
                    payload = post.call_args.kwargs['json']
                    self.assertEqual(payload['sign'], vector['sign'])
                    self.assertEqual(payload['reqTime'], '1700000000123')
                    self.assertEqual(params, original, 'caller data must not retain injected fields/sign')

    def test_golden_digest_and_filtering(self):
        for vector in FIXTURE['vectors']:
            with self.subTest(vector=vector['name']):
                self.assertEqual(hashlib.md5(vector['canonical'].encode('utf-8')).hexdigest().upper(), vector['sign'])
                self.assertNotIn('OLD_SIGNATURE', vector['canonical'])
        zero = next(v for v in FIXTURE['vectors'] if v['name'] == 'zero')
        self.assertIn('amount=0&', zero['canonical'])
        empty = next(v for v in FIXTURE['vectors'] if v['name'] == 'null_empty')
        self.assertNotIn('absent=', empty['canonical'])
        self.assertNotIn('empty=', empty['canonical'])

    def test_documented_digest(self):
        text = (SKILL / 'references/sdk-reminder.md').read_text(encoding='utf-8')
        canonical = re.search(r'^排序拼接：(.*)$', text, re.M).group(1)
        expected = re.search(r'^MD5结果：([A-F0-9]{32})', text, re.M).group(1)
        self.assertEqual(hashlib.md5(canonical.encode('utf-8')).hexdigest().upper(), expected)

    def test_python_blocks_parse(self):
        for path in SKILL.rglob('*.md'):
            for index, block in enumerate(re.findall(r'^```python\n(.*?)^```', path.read_text(encoding='utf-8'), re.M | re.S)):
                with self.subTest(path=str(path.relative_to(ROOT)), block=index):
                    ast.parse(block)

    def test_signature_sorting_guidance_is_consistent(self):
        for path in SKILL.rglob('*.md'):
            with self.subTest(path=str(path.relative_to(ROOT))):
                self.assertNotRegex(path.read_text(encoding='utf-8'), r'按\s*(?:key 的 )?ASCII\s*码?升序')


if __name__ == '__main__':
    unittest.main()
