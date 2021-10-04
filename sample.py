from sumo_output_parsers import LoopDetectorParser, LoopDetectorMatrixObject
from sumo_output_parsers import FCDFileParser, FcdMatrixObject
from pathlib import Path

path_fcd_output = Path('tests/resources/output/fcd-output.xml')
path_loop_output = Path('tests/resources/output/loop.out.xml')

fcd_parser = FCDFileParser(path_fcd_output)
for metric in fcd_parser.get_attributes():
    fcd_matrix_obj = fcd_parser.xml2matrix(metric)
    fcd_matrix_obj.to_pickle(path_fcd_output.parent.joinpath(f'fcd-matrix-{metric}.pickle'))

loop_parser = LoopDetectorParser(path_loop_output)
print(loop_parser.get_attributes())
for metric in loop_parser.get_attributes():
    loop_metric_matrix_obj = loop_parser.xml2matrix(metric)
    loop_metric_matrix_obj.to_pickle(path_loop_output.parent.joinpath(f'loop-detector-{metric}.pickle'))