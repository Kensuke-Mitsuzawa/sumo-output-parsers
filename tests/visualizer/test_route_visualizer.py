import pytest
from pathlib import Path
from tempfile import mkdtemp
from matplotlib import pyplot as plt
from uuid import uuid4


@pytest.mark.visualization
def test_router_visualizer(resource_path_root: Path):
    from sumo_output_parsers.visualizer.route_visualizer import RouteVisualizer

    path_net_xml = resource_path_root / "grid.net.xml"
    path_vehroute_xml = resource_path_root / 'output/vehroute-output.xml'
    path_output_png = Path(mkdtemp()) / f'{uuid4()}.png'
    route_v = RouteVisualizer()

    f, ax = plt.subplots(figsize=(15, 15))
    route_v.visualize(
        path_vehroute_xml=path_vehroute_xml,
        path_sumo_net=path_net_xml,
        path_output_png=path_output_png,
        target_vehicle_group=['10-to-38'],
        ax=ax,
        f_obj=f)

    f, ax = plt.subplots(figsize=(15, 15))
    route_v.visualize(
        path_vehroute_xml=path_vehroute_xml,
        path_sumo_net=path_net_xml,
        path_output_png=path_output_png,
        ax=ax,
        f_obj=f)


if __name__ == '__main__':
    test_router_visualizer(Path('../resources/'))

