import os
import os.path as osp
import shutil
import subprocess
import tempfile
import warnings

import pkg_resources
import trimesh


try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


__version__ = pkg_resources.get_distribution('pysdfgen').version


SDFGen_executable = osp.join(
    osp.abspath(osp.dirname(__file__)), 'SDFGen')


def obj2sdf(*args, **kwargs):
    """Convert obj to sdf file.

    Deprecated.
    Use `pysdfgen.mesh2sdf` instead.
    """
    warnings.warn(
        'obj2sdf is deprecated. Use mesh2sdf instead.',
        DeprecationWarning)
    return mesh2sdf(*args, **kwargs)


def mesh2sdf(mesh_filepath, dim=100, padding=5,
             output_filepath=None,
             overwrite=False):
    """Convert mesh file to sdf file.

    Parameters
    ----------
    mesh_filepath : str or pathlib.Path
        filepath of mesh formats that trimesh supports.
    dim : int
        number of sdf dimension.
    padding : int
        number of padding.
    output_filepath : None or str, or pathlib.Path.
        output filepath
    overwrite : bool
        if `True`, overwrite sdf file.
    """
    mesh_filepath = str(mesh_filepath)
    _, ext = osp.splitext(mesh_filepath)

    parent = osp.dirname(mesh_filepath)
    basename = osp.basename(mesh_filepath)
    stem, _ = osp.splitext(basename)
    default_sdf_filepath = osp.join(parent, stem + ".sdf")

    is_obj_file = ext == '.obj'
    if is_obj_file:
        obj_filepath = mesh_filepath
    else:
        # create temporary directory and save obj file.
        tmp_directory = tempfile.mkdtemp()
        tmp_obj_filepath = osp.join(tmp_directory, 'tmp.obj')
        tmp_sdf_filepath = osp.join(tmp_directory, 'tmp.sdf')

        mesh = trimesh.load_mesh(mesh_filepath)
        trimesh.exchange.export.export_mesh(mesh, tmp_obj_filepath)
        obj_filepath = tmp_obj_filepath

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

    if is_obj_file:
        # becuase the output destination of SDFGen can't be specified...
        os.rename(default_sdf_filepath, sdf_filepath)
    else:
        os.rename(tmp_sdf_filepath, sdf_filepath)
        shutil.rmtree(tmp_directory)
    return sdf_filepath
