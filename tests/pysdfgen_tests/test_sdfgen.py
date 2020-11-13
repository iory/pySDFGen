import os
import os.path as osp
import unittest

from pysdfgen import obj2sdf


current_dir = osp.abspath(osp.dirname(__file__))
bunny_objpath = osp.join(current_dir, 'data', 'bunny.obj')
bunny_sdfpath = osp.join(current_dir, 'data', 'bunny.sdf')


class TestSDFGen(unittest.TestCase):

    def test_obj2sdf(self):
        dim = 10
        if osp.exists(bunny_sdfpath):
            os.remove(bunny_sdfpath)
        output_path = obj2sdf(bunny_objpath, dim=dim)
        self.assertEqual(output_path, bunny_sdfpath)

        output_path = obj2sdf(bunny_objpath, dim=dim, overwrite=True)
        self.assertEqual(output_path, bunny_sdfpath)

        with self.assertRaises(OSError):
            obj2sdf(bunny_objpath, overwrite=False)

        output_path = obj2sdf(bunny_objpath,
                              dim=dim,
                              output_filepath=bunny_sdfpath,
                              overwrite=True)
        self.assertEqual(output_path, bunny_sdfpath)

        with self.assertRaises(OSError):
            obj2sdf(bunny_objpath,
                    output_filepath=bunny_sdfpath,
                    overwrite=False)
