import os
import os.path as osp
import shutil
import unittest

from pysdfgen import obj2sdf

current_dir = osp.abspath(osp.dirname(__file__))
bunny_objpath = osp.join(current_dir, 'data', 'bunny.obj')
bunny_sdfpath = osp.join(current_dir, 'data', 'bunny.sdf')
gripper_stlpath = osp.join(current_dir, 'data', 'gripper.stl')
gripper_sdfpath = osp.join(current_dir, 'data', 'gripper.sdf')

another_data_dir = osp.join(current_dir, "tmp")
another_bunny_sdfpath = osp.join(another_data_dir, 'bunny.sdf')
another_gripper_sdfpath = osp.join(another_data_dir, 'gripper.sdf')
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

        # testing the case when a file is not an obj file
        if osp.exists(gripper_sdfpath):
            os.remove(gripper_sdfpath)
        output_path = obj2sdf(gripper_stlpath)
        self.assertEqual(output_path, gripper_sdfpath)
        self.assertTrue(osp.exists(output_path))

    def tearDown(self):
        shutil.rmtree(another_data_dir)
        os.remove(bunny_sdfpath)
        os.remove(gripper_sdfpath)
