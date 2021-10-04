import dataclasses
from typing import Optional, Dict, List

import scipy.sparse
from scipy.sparse import csr_matrix
from pathlib import Path
import numpy as np

from sumo_output_parsers.models.parser import CsvBasedParser, MatrixObject


class SummaryFileParser(CsvBasedParser):
    def __init__(self,
                 path_xml_file: Path,
                 name_xsd: str = 'summary_file.xsd',
                 path_working_dir: Optional[Path] = None,
                 matrix_index: str = '',
                 matrix_column: str = ''
                 ):
        super(SummaryFileParser, self).__init__(path_xml_file=path_xml_file,
                                                  name_xsd=name_xsd,
                                                  path_working_dir=path_working_dir,
                                                  index_header_name=matrix_index,
                                                  column_header_name=matrix_column)

    def xml2matrix(self, target_element: str, agg_func = None):
        raise NotImplementedError('`xml2matrix() is not available for summary output.`')

