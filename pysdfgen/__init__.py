# flake8: noqa

import pkg_resources
import os.path as osp
import subprocess

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


__version__ = pkg_resources.get_distribution('pysdfgen').version


SDFGen_executable = osp.join(
    osp.abspath(osp.dirname(__file__)), 'SDFGen')


def obj2sdf(obj_filepath, dim=100, padding=5):
    """Convert .obj to .sdf file.

    Parameters
    ----------
    obj_filepath : str or pathlib.Path
        filepath of .obj.
    dim : int
        dimension number.
    padding : int
        padding.
    """
    obj_filepath = str(obj_filepath)
    parent = osp.dirname(obj_filepath)
    basename = osp.basename(obj_filepath)
    stem, ext = osp.splitext(basename)
    if ext != '.obj':
        raise ValueError("The input file name should end with '.obj'.")
    sdf_filepath = osp.join(parent, stem + ".sdf")
    p = subprocess.Popen(
        [SDFGen_executable,
         str(obj_filepath),
         str(dim),
         str(padding)],
        stdout=DEVNULL)
    p.wait()
    return osp.join(parent, sdf_filepath)
