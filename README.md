# What's this?

Fast and lightweight file parsers for Eclipse SUMO(traffic simulator) output.

The SUMO outputs are huge in size and hard to handle.

SUMO team provides scripts to convert from xml into CSV, however, the procedure is troublesome (downloading XSD, executing python script...)

Also, machine learning users take care of matrix data format.

This package provides an easy-to-call python interface to obtain matrix form from SUMO xml files.

# Contributions

- easy-to-call python interfaces to obtain matrix form from SUMO xml files
- easy-to-call python interfaces to visualize SUMO simulations

![Example of animation](https://user-images.githubusercontent.com/1772712/135924848-4a938dd2-b2d3-4dfe-bfd6-94904086c382.gif)

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

See `sample.py`

# Test

```
pytest tests
```

# For developers

Build with poetry.

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