import os.path as osp
import subprocess

import pkg_resources

try:
    from subprocess import DEVNULL
except ImportError:
    import os
    DEVNULL = open(os.devnull, 'wb')


__version__ = pkg_resources.get_distribution('pysdfgen').version


SDFGen_executable = osp.join(
    osp.abspath(osp.dirname(__file__)), 'SDFGen')


def obj2sdf(obj_filepath, dim=100, padding=5,
            output_filepath=None,
            overwrite=False):
    """Convert .obj to .sdf file.

    Parameters
    ----------
    obj_filepath : str or pathlib.Path
        filepath of .obj.
    dim : int
        number of sdf dimension.
    padding : int
        number of padding.
    output_filepath : None or str, or pathlib.Path.
        output filepath
    overwrite : bool
        if `True`, overwrite sdf file.
     """
    obj_filepath = str(obj_filepath)
    _, ext = osp.splitext(obj_filepath)
    if ext != '.obj':
        raise ValueError("The input file name should end with '.obj'.")

    parent = osp.dirname(obj_filepath)
    basename = osp.basename(obj_filepath)
    stem, _ = osp.splitext(basename)
    default_sdf_filepath = osp.join(parent, stem + ".sdf")

    if output_filepath is None:
        sdf_filepath = default_sdf_filepath
    else:
        sdf_filepath = output_filepath

    if overwrite is False and osp.exists(sdf_filepath):
        raise OSError("Output file ({}) already exists."
                      .format(sdf_filepath))
    p = subprocess.Popen(
        [SDFGen_executable,
         str(obj_filepath),
         str(dim),
         str(padding)],
        stdout=DEVNULL)
    p.wait()

    # becuase the output destination of SDFGen can't be specified...
    os.rename(default_sdf_filepath, sdf_filepath)
    return sdf_filepath
