# Shoulder muscle geometry optimization
The goal of this project is to optimize the geometry of the muscle shoulder by comparison with MRI images.\
We run simulations of shoulder movement under LS-DYNA (finite element software) and follow the deformations of the surface of the muscles.
The variables to optimize are the material parameters of the material defining the mechanic behaviour of the mucle.\
It uses the qd-cae-dyna library to access the data in the simulation file. It also uses the Platypus library for the genetic algorithm used to optimize.
