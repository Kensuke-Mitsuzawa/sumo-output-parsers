import pickle
from pathlib import Path
from sumo_output_parsers import LoopDetectorParser, LoopDetectorMatrixObject
from tempfile import mkdtemp


def test_loop_output(resource_path_root: Path):
    parser = LoopDetectorParser(resource_path_root.joinpath('output/loop.out.xml'))
    for metric in parser.get_attributes():
        matrix_obj = parser.xml2matrix(metric)
        path_temp = Path(mkdtemp())
        path_dest = path_temp.joinpath('fcd-matrix.pickle')

        matrix_obj.to_pickle(path_dest)
        matrix_obj_file = LoopDetectorMatrixObject.from_pickle(path_dest)


if __name__ == '__main__':
    test_loop_output(Path('resources/'))
