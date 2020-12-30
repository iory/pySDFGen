import os
import os.path as osp
import shutil
import subprocess
import tempfile

import pkg_resources

import trimesh

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


__version__ = pkg_resources.get_distribution('pysdfgen').version


SDFGen_executable = osp.join(
    osp.abspath(osp.dirname(__file__)), 'SDFGen')


def obj2sdf(mesh_filepath, dim=100, padding=5,
            output_filepath=None,
            overwrite=False):
    """Convert .obj to .sdf file.

    Parameters
    ----------
    mesh_filepath : str or pathlib.Path
        filepath of .obj or other formats that trimesh supports.
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
    if not is_obj_file:
        tmp_directory = tempfile.mkdtemp()
        tmp_obj_filepath = osp.join(tmp_directory, 'tmp.obj')
        tmp_sdf_filepath = osp.join(tmp_directory, 'tmp.sdf')

        mesh = trimesh.load_mesh(mesh_filepath)
        V = mesh.vertices
        F = mesh.faces
        with open(tmp_obj_filepath, mode='w') as f:
            for vert in V:
                f.write("v {0} {1} {2}\n".format(vert[0], vert[1], vert[2]))
            for face_ in F:
                face = face_ + 1  # in trimesh index starts from 0
                f.write("f {0} {1} {2}\n".format(face[0], face[1], face[2]))
        obj_filepath = tmp_obj_filepath
    else:
        obj_filepath = mesh_filepath

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

    if not is_obj_file:
        os.rename(tmp_sdf_filepath, sdf_filepath)
        shutil.rmtree(tmp_directory)
    else:
        # becuase the output destination of SDFGen can't be specified...
        os.rename(default_sdf_filepath, sdf_filepath)
    return sdf_filepath
