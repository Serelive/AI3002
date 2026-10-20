"""Check feature-output routing without loading an LLM or requiring a GPU."""
import argparse
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import numpy as np

SCRIPT = Path(__file__).resolve().parents[1] / 'assignments/labs/lab1/scr/extract_intrep.py'
spec = importlib.util.spec_from_file_location('lab1_extract', SCRIPT)
extract = importlib.util.module_from_spec(spec)
spec.loader.exec_module(extract)


class ExtractionOutputTests(unittest.TestCase):
    def test_phase_defaults_and_explicit_override(self):
        for selection, phase, explicit in [('country', 'p02', False),
                                           ('last', 'p03', False),
                                           ('last', 'p03', True)]:
            with self.subTest(selection=selection, explicit=explicit), tempfile.TemporaryDirectory() as directory:
                lab = Path(directory) / 'lab1'
                source = lab / 'scr/datasets' / 'train.csv'
                source.parent.mkdir(parents=True)
                source.write_text('sentence,country\nWhere in Example?,Example\n')
                destination = lab / 'output/p03/custom' if explicit else None
                args = argparse.Namespace(input=source, model_dir=lab / 'model',
                                          layer=11, token_selection=selection,
                                          output_dir=destination)
                features = np.ones((1, 2560), dtype=np.float16)
                with patch.object(extract, '__file__', str(lab / 'scr/extract_intrep.py')), \
                     patch.object(extract, 'parse_args', return_value=args), \
                     patch.object(extract, 'load_model', return_value=(None, None)), \
                     patch.object(extract, 'extract_features', return_value=features):
                    extract.main()
                    expected = (destination or lab / 'output' / phase / 'features') / 'train.layer11.npy'
                    np.testing.assert_array_equal(np.load(expected), features)
                    self.assertFalse(source.with_suffix('.layer11.npy').exists())
                    with self.assertRaises(FileExistsError):
                        extract.main()


if __name__ == '__main__':
    unittest.main()
