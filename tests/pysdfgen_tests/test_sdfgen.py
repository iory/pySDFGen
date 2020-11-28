import os
import os.path as osp
import unittest

from pysdfgen import obj2sdf

current_dir = osp.abspath(osp.dirname(__file__))
bunny_objpath = osp.join(current_dir, 'data', 'bunny.obj')
bunny_sdfpath = osp.join(current_dir, 'data', 'bunny.sdf')

another_data_dir = osp.join(current_dir, "tmp")
another_bunny_sdfpath = osp.join(another_data_dir, 'bunny.sdf')
if not os.path.exists(another_data_dir):
    os.makedirs(another_data_dir)


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

        # testing the case when a custom output path is specified
        another_output_path = obj2sdf(bunny_objpath,
                                      dim=dim,
                                      output_filepath=another_bunny_sdfpath,
                                      overwrite=True)
        self.assertEqual(another_output_path, another_bunny_sdfpath)
        self.assertTrue(os.path.exists(another_bunny_sdfpath))

        with self.assertRaises(OSError):
            obj2sdf(bunny_objpath,
                    dim=dim,
                    output_filepath=another_bunny_sdfpath,
                    overwrite=False)
