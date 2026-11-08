# Notebooks

There is one notebook for each part of the course. They are not exercises and are not examined. They are meant to
be read alongside the notes.

Many of the experiments use Gaussian targets, for which we can calculate the sampling error and
compare it with the bounds in the notes. Mixtures let us examine the failure of Langevin dynamics to
move between well-separated modes. In both cases we vary the dimension and the time grid, rather than
judge the sampler from a picture alone.

Each notebook runs from top to bottom, and most sections end with suggestions of parameters to vary.
The notebooks include stored outputs. Runtimes are approximate.

## [Sampling and the score](sampling_and_the_score.ipynb)

Rejection sampling from the unit ball, using proposals from the cube, needs about $3\times10^{20}$ proposals
per accepted sample in dimension 40. Density estimation deteriorates too. With 20,000 Gaussian
training samples, the median relative error of a kernel density estimate at independent test points
rises from about 1% in dimension 1 to 99% in dimension 32.

For a Gaussian target, ULA has the stationary variance calculated in the notes, including its
discretisation bias. On the separated mixture used here, particles started between the two modes
fall into one of them and do not cross, so about 0.48 of them end in the lighter mode instead of
0.20. Near each mode the score depends very little on the mixture weights, so
accurate local motion does not ensure that the sampler gets the proportions right. The denoising
experiment compares the excess regression loss of a learned score, 0.0293, with its mean-square
error, 0.0287, as predicted by the identity of Chapter 2.

Further notebooks on Langevin dynamics, time reversal, convergence of diffusion models, and flows
and guidance will be released as the course progresses.

## Running the notebooks

You need Python 3.10 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
jupyter notebook
```

The first notebook takes under a minute on a laptop CPU.
