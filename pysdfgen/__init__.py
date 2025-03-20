import os
import os.path as osp
import shutil
import subprocess
import tempfile
import warnings


try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'wb')


_version = None
_SUBMODULES = [
    "obj2sdf",
    "mesh2sdf",
]
__all__ = _SUBMODULES

SDFGen_executable = osp.join(
    osp.abspath(osp.dirname(__file__)), 'SDFGen')

_trimesh = None


def _lazy_trimesh():
    global _trimesh
    if _trimesh is None:
        import trimesh
        _trimesh = trimesh
    return _trimesh


def __getattr__(name):
    global _version
    if name == "__version__":
        if _version is None:
            import pkg_resources
            _version = pkg_resources.get_distribution(
                'pysdfgen').version
        return _version
    raise AttributeError(
        "module {} has no attribute {}".format(__name__, name))


def __dir__():
    return __all__ + ['__version__', '__file__']


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

        trimesh = _lazy_trimesh()
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
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()
    stdout_decoded = stdout.decode('utf-8').strip()
    stderr_decoded = stderr.decode('utf-8').strip()

    if p.returncode != 0:
        error_message = "SDFGen failed."
        if stdout_decoded:
            error_message += " stdout: '{}'".format(stdout_decoded)
        if stderr_decoded:
            error_message += " stderr: '{}'".format(stderr_decoded)
        raise ValueError(error_message)

    if is_obj_file:
        # becuase the output destination of SDFGen can't be specified...
        shutil.move(default_sdf_filepath, sdf_filepath)
    else:
        shutil.move(tmp_sdf_filepath, sdf_filepath)
        shutil.rmtree(tmp_directory)
    return sdf_filepath
