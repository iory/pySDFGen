import os
import os.path as osp
import unittest

from pysdfgen import mesh2sdf
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
        # deprecated
        dim = 10
        if osp.exists(bunny_sdfpath):
            os.remove(bunny_sdfpath)
        output_path = obj2sdf(bunny_objpath, dim=dim)
        self.assertEqual(output_path, bunny_sdfpath)
        os.remove(bunny_sdfpath)

    def test_invalid_arg_to_command(self):
        if osp.exists(bunny_sdfpath):
            os.remove(bunny_sdfpath)
        # padding must be smaller than dim
        with self.assertRaises(ValueError):
            obj2sdf(bunny_objpath, dim=10, padding=10)

    def test_mesh2sdf(self):
        dim = 10
        if osp.exists(bunny_sdfpath):
            os.remove(bunny_sdfpath)
        output_path = mesh2sdf(bunny_objpath, dim=dim)
        self.assertEqual(output_path, bunny_sdfpath)

        output_path = mesh2sdf(bunny_objpath, dim=dim, overwrite=True)
        self.assertEqual(output_path, bunny_sdfpath)

        with self.assertRaises(OSError):
            mesh2sdf(bunny_objpath, overwrite=False)

        output_path = mesh2sdf(bunny_objpath,
                               dim=dim,
                               output_filepath=bunny_sdfpath,
                               overwrite=True)
        self.assertEqual(output_path, bunny_sdfpath)

        with self.assertRaises(OSError):
            mesh2sdf(bunny_objpath,
                     output_filepath=bunny_sdfpath,
                     overwrite=False)

        # testing the case when a custom output path is specified
        another_output_path = mesh2sdf(bunny_objpath,
                                       dim=dim,
                                       output_filepath=another_bunny_sdfpath,
                                       overwrite=True)
        self.assertEqual(another_output_path, another_bunny_sdfpath)
        self.assertTrue(os.path.exists(another_bunny_sdfpath))

        with self.assertRaises(OSError):
            mesh2sdf(bunny_objpath,
                     dim=dim,
                     output_filepath=another_bunny_sdfpath,
                     overwrite=False)

        # testing the case when a file is not an obj file
        if osp.exists(gripper_sdfpath):
            os.remove(gripper_sdfpath)
        output_path = mesh2sdf(gripper_stlpath, dim=dim)
        self.assertEqual(output_path, gripper_sdfpath)
        self.assertTrue(osp.exists(output_path))

        if osp.exists(another_gripper_sdfpath):
            os.remove(another_gripper_sdfpath)
        another_output_path = mesh2sdf(
            gripper_stlpath,
            output_filepath=another_gripper_sdfpath,
            dim=dim)
        self.assertEqual(another_output_path, another_gripper_sdfpath)
        self.assertTrue(osp.exists(another_output_path))
