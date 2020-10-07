# design-of-experiments
A Python Package for Design of Experiments

# Motivation
I worked with a research team investigating how Design of Experiments could be applied to Synthetic Biology over the summer of 2020, as part of this I made a general software review and was a little dissapointed at the sparsity of python packages for designing experiments, and what packages were available I found to be considerably inferior to the comercial DOE software like JMP, MODDE, or Minitab. So, I have created this python package to offer an open-source package for the Design of Experiments!

# Example
```python
>>>import design
>>>Factors = {'Height':[1.6,2],'Width':[0.2,0.4],'Depth':[0.2,0.3],'Temp':[10,20],'Pressure':[100,200]}
>>>design.Factorial.frac_fact_2level(Factors,10)

   Height  Width  Depth  Temp  Pressure
0     1.6    0.2    0.2    20       200
1     1.6    0.2    0.3    20       100
2     1.6    0.4    0.2    10       200
3     1.6    0.4    0.3    10       100
4     2.0    0.2    0.2    10       100
5     2.0    0.2    0.3    10       200
6     2.0    0.4    0.2    20       100
7     2.0    0.4    0.3    20       200
```
# Installation
```
pip install designofexperiment
```

#
