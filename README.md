[![INFORMS Journal on Computing Logo](https://INFORMSJoC.github.io/logos/INFORMS_Journal_on_Computing_Header.jpg)](https://pubsonline.informs.org/journal/ijoc)

# frvcpy: An Open-Source Solver for the FRVCP

### Fast optimal solutions to rich FRVCPs

This archive is distributed in association with the [INFORMS Journal on
Computing](https://pubsonline.informs.org/journal/ijoc) under the [Apache license](LICENSE).

The software and data in this repository are a snapshot of the software and data
that were used in the research reported on in the paper [frvcpy: An Open-Source Solver for the Fixed Route Vehicle
Charging Problempaper](https://doi.org/10.1287/ijoc.2020.1035) by N. Kullman, A. Froger, JE Mendoza, and J. Goodson.
The snapshot is based on [this SHA](https://github.com/e-VRO/frvcpy/commit/2c6dc419a6a60fa2a9b5e88bdb5371c29f7b3b2d) in the development repository.

**Important: This code is being developed on an on-going basis at [https://github.com/e-VRO/frvcpy/](https://github.com/e-VRO/frvcpy/). Please go there if you would like to
get a more recent version or would like support.**

## What is an FRVCP?

Given an electric vehicle (EV) that's been assigned some sequence of locations to visit (a _fixed route_), the __fixed route vehicle charging problem__ (FRVCP) is the problem of finding the optimal insertion of recharging operations into the route that minimize the time required for the EV to traverse that route in an energy-feasible manner.

## Why does frvcpy exist?

FRVCPs arise in many EV routing problems. While algorithms solving FRVCPs exist, the good ones are often a challenge to implement and may ultimately deter researchers from using them. We released frvcpy with the hope of making it easier for researchers to solve EV routing problems, facilitating the development of optimization tools that may ultimately enable the mass adoption of electric vehicles.

## Citing frvcpy

To cite frvcpy, please cite the [research article](https://doi.org/10.1287/ijoc.2020.1035) and/or the software itself:

[![DOI](https://zenodo.org/badge/300479489.svg)](https://zenodo.org/badge/latestdoi/300479489)

Bibtex for this version of the code:
```
@article{frvcpy,
  author =        {N. Kullman, A. Froger, J.E. Mendoza, and J. Goodson},
  publisher =     {INFORMS Journal on Computing},
  title =         {{frvcpy} Version v2020.1035},
  year =          {2020},
  doi =           {10.5281/zenodo.4081736},
  url =           {https://github.com/INFORMSJoC/2020.1035},
}  
```
## Installation

In a virtual environment with Python 3.6+, frvcpy can be installed via

```bash
pip install frvcpy
```

### Testing the installation

```python
import frvcpy.test
frvcpy.test.runAll()
```

Or from the command line:

```bash
frvcpy-test
```

## Using frvcpy

With a compatible instance file ([see the schema](./data/frvcpy-instance.schema.json)), solve the FRVCP from a Python script:

```python
from frvcpy import solver

route = [0,40,12,33,38,16,0]        # route to make energy feasible
q_init = 16000                      # vehicle's initial energy level

# using an existing instance from file
frvcp_solver = solver.Solver("data/frvcpy-instance.json", route, q_init)

# run the algorithm
duration, feas_route = frvcp_solver.solve()

# write solution to file
frvcp_solver.write_solution("results/my-solution.xml", instance_name="frvcpy-instance")

print(f"Duration: {duration:.4}")
# Duration: 7.339

print(f"Energy-feasible route:\n{feas_route}")
# Energy-feasible route:
# [(0, None), (40, None), (12, None), (33, None), (48, 6673.379615520617), (38, None), (16, None), (0, None)]
```

Or from the command line:

```bash
frvcpy --instance=data/frvcpy-instance.json --route=0,40,12,33,38,16,0 --qinit=16000 --output=results/my-solution.xml
# Duration: 7.339
# Energy-feasible route:
# [(0, None), (40, None), (12, None), (33, None), (48, 6673.379615520617), (38, None), (16, None), (0, None)]
```

Solutions are written in the [VRP-REP](http://www.vrp-rep.org/) format for easy importing and visualization with the [VRP-REP Mapper](https://vrp-rep.github.io/mapper/) (_formal solution specification available [here](http://www.vrp-rep.org/resources.html)_).

_Note: Example problem instances are available in the `instances` directory on the [project's homepage](https://github.com/e-VRO/frvcpy/). For easy access to the example files, we recommend cloning that repository._

## Instance Translation

Instance translation is available for some E-VRP instances formatted according to the [VRP-REP specification](http://www.vrp-rep.org/resources.html).

Translation can be done with the Python API via

```python
from frvcpy import translator

# Option 1) write the translated instance to file
translator.translate("data/vrprep-instance.xml", to_filename="data/my-new-instance.json")

# Option 2) make instance object to be passed directly to the solver
frvcp_instance = translator.translate("data/vrprep-instance.xml")
```

Or with the command line:

```bash
# from CLI, only option is to write translated instance to file
frvcpy-translate data/vrprep-instance.xml data/my-new-instance.json
```

_Note: If an instance ending in ".xml" is passed to the solver, it is assumed to be a VRP-REP instance, and the solver will automatically attempt to translate it._

### Translation requirements for VRP-REP instances

frvcpy's translator assumes VRP-REP instances are formatted similarly to the [Montoya et al. (2017) instances](http://vrp-rep.org/datasets/item/2016-0020.html):

- CSs are identified as `<node>` elements having attribute `type="2"`
- Charging stations nodes have a `<custom>` child element which contains a `cs_type` element
- For each unique CS type `t` appearing in those `cs_type` elements, there exists a charging `function` element with attribute `cs_type=t`
- These `function` elements are part of a `charging_functions` element in a `vehicle_profile`'s `custom` element
- The depot has node ID 0, the N customers have IDs {1, ..., N}, and the CSs have IDs {N+1, ..., N+C}

A good example of such an instance is the [example VRP-REP instance in the repository](./data/vrprep-instance.xml).

Here is a smaller example meeting these requirements:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<instance>
  <network>
    <nodes>
      <node id="0" type="0">
        <cx>74.83</cx>
        <cy>51.85</cy>
      </node>
      <node id="1" type="1">
        <cx>68.77</cx>
        <cy>75.69</cy>
      </node>
      <node id="11" type="2">
        <cx>57.0</cx>
        <cy>57.04</cy>
        <custom>
          <cs_type>fast</cs_type>
        </custom>
      </node>
    </nodes>
    <euclidean/>
    <decimals>14</decimals>
  </network>
  <fleet>
    <vehicle_profile type="0">
      <departure_node>0</departure_node>
      <arrival_node>0</arrival_node>
      <speed_factor>25.0</speed_factor>
      <custom>
        <consumption_rate>0.125</consumption_rate>
        <battery_capacity>16.0</battery_capacity>
        <charging_functions>
          <function cs_type="fast">
            <breakpoint>
              <battery_level>0.0</battery_level>
              <charging_time>0.0</charging_time>
            </breakpoint>
            <breakpoint>
              <battery_level>13.6</battery_level>
              <charging_time>0.317</charging_time>
            </breakpoint>
            <breakpoint>
              <battery_level>15.2</battery_level>
              <charging_time>0.383</charging_time>
            </breakpoint>
            <breakpoint>
              <battery_level>16.0</battery_level>
              <charging_time>0.517</charging_time>
            </breakpoint>
          </function>
        </charging_functions>
      </custom>
    </vehicle_profile>
  </fleet>
  <requests>
    <request id="1" node="1">
      <service_time>0.5</service_time>
    </request>
  </requests>
</instance>
```

## The Solver

To solve FRVCPs, frvcpy implements the labeling algorithm from Froger et al. (2019), providing optimal solutions in low runtime. The algorithm accommodates realistic problem features such as nonlinear charging functions, heterogeneous charging station technologies, and multiple CS visits between stops.

## Additional information

For more information about the algorithm used in the solver, see [Froger et al. (2019)](https://www.sciencedirect.com/science/article/abs/pii/S0305054818303253).

The research article describing this software library can be found here (_link coming soon_).
