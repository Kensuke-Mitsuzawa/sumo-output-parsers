import pickle
from pathlib import Path
from sumo_output_parsers.fcd_parser import FCDFileParser, FcdMatrixObject
from tempfile import mkdtemp


def test_fcd_output(resource_path_root: Path):
    parser = FCDFileParser(resource_path_root.joinpath('output/fcd-output.xml'))
    matrix_obj = parser.xml2matrix('timestep')
    path_temp = Path(mkdtemp())
    path_dest = path_temp.joinpath('fcd-matrix.pickle')

    matrix_obj.to_pickle(path_dest)
    matrix_obj_file = FcdMatrixObject.from_pickle(path_dest)


if __name__ == '__main__':
    test_fcd_output(Path('resources/'))
