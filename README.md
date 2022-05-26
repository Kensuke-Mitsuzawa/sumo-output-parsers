# What's this?

Fast and lightweight file parsers for Eclipse SUMO(traffic simulator) output.

The SUMO outputs are huge in size and hard to handle.

SUMO team provides scripts to convert from xml into CSV, however, the procedure is troublesome (downloading XSD, executing python script...)

Also, machine learning users take care of matrix data format.

This package provides an easy-to-call python interface to obtain matrix form from SUMO xml files.

# Contributions

- easy-to-call python interfaces to obtain matrix form from SUMO xml files
- easy-to-call python interfaces to visualize SUMO simulations

# Gallery

You can generate a traffic animation by fcd output xml. 

![Example of animation](https://user-images.githubusercontent.com/1772712/135924848-4a938dd2-b2d3-4dfe-bfd6-94904086c382.gif)

You can visualize where a detector locates in a network.

![Visualization example of detector position](https://user-images.githubusercontent.com/1772712/170488284-79893a06-5979-45a0-a7c8-a87d9c89fa79.png)

You can visualize a transition of vehicle by vehrout.xml.

![Visualization example of traffic route](https://user-images.githubusercontent.com/1772712/170488281-3c7c5564-a3f2-403a-a9f5-779db6c7604f.png)

# Install

```
pip install sumo-output-parsers
```

Some submodules are not ready to use by default for which
we avoid errors relating Proproj or Cartopy. 

If you'd like to depict car flows or detector positions, install with

```
pip install "sumo-output-parsers[full]"
```

# Sample

See `sample.py` and `visualization_example.ipynb`

# Test

```
pytest tests/
```

If your package-dependency is complete including packages for visualization, 
then `pytest tests/ --visualization`


# For developers

Build with poetry.

# Install Guide

When you encounter any dependency issues, I recommend to use `conda`.
`cartopy` and `proj` cause the dependency issue frequently.
Conda helps you to install the compiled binaries.
See Proj [documentation](https://proj.org/install.html).

# License

```
@misc{sumo-output-parsers,
  author = {Kensuke Mitsuzawa},
  title = {sumo_output_parsers},
  year = {2021},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{}},
}
```