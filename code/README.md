# Notebooks

There is one notebook for each week. They are not exercises and are not examined. They are meant to
be read alongside the notes.

Many of the experiments use Gaussian targets, for which we can calculate the sampling error and
compare it with the bounds in the notes. Mixtures let us examine the failure of Langevin dynamics to
move between well-separated modes. In both cases we vary the dimension and the time grid, rather than
judge the sampler from a picture alone. The MNIST experiments are in dimension 784. Planar examples
are used where we want to draw a velocity field or follow individual trajectories.

Each notebook runs from top to bottom, and most sections end with suggestions of parameters to vary.
The notebooks include stored outputs. The revised Gaussian comparison, flow-matching and guidance
experiments have been rerun. Runtimes are approximate.

## Week 1. [Sampling and the score](week1_sampling_and_the_score.ipynb)

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

## Week 2. [Langevin dynamics](week2_langevin_dynamics.ipynb)

Two Langevin diffusions driven by the same Brownian motion approach each other at least as fast
as strong convexity predicts. In dimension 200, the bound obtained through the $\chi^2$-divergence needs time
about 104 to guarantee a small total variation distance, while the bound through the relative entropy
needs about 6.6, close to the exact value 6.4. The $\chi^2$ bound
pays for starting far from equilibrium, since the initial divergence $e^{|m|^2}-1$ is exponentially
large. For a mixture of two modes at distance $2a$, the mean time to cross from one mode to the other
grows exponentially in $a^2$, and so does a lower bound on the Poincaré constant. Varying the step size also lets us measure
the stationary bias of ULA.

## Week 3. [Time reversal](week3_time_reversal.ipynb)

The target is a mixture of two well-separated modes, with weights 0.8 and 0.2. Langevin dynamics puts
weight 0.48 on the lighter mode, and so does tempering, which raises the inverse temperature to one
during the run. The reverse Ornstein–Uhlenbeck process with the exact score gets 0.21. The forward marginals show how noising changes the target.
We compare the simulated reverse variance with its exact value, and use Tweedie's formula to examine
the denoised estimates at several noise levels. A diffusion model whose score is learned from
samples puts weight 0.19 on the lighter mode.

## Week 4. [Convergence of diffusion models](week4_convergence_of_diffusion_models.ipynb)

Chapter 5 analyses the exponential integrator under uniformly Lipschitz scores. We compare its exact
Gaussian output error with Euler–Maruyama. The examples use variance 1 and variance $10^{-4}$, so their
uniform score Lipschitz constants are 1 and $10^4$. Uniform and two-phase grids show the numerical
cost of resolving a rapidly varying score. The grid comparison is empirical and illustrates the effect of a large Lipschitz constant.

A small U-Net is then trained on MNIST and sampled with 10, 50 and 400 steps. The sampler uses the
exponential integrator and a final Tweedie denoising step. Nearest-training-image distances provide a
check for direct copying, without establishing generalisation.

## Week 5. [Flows and guidance](week5_flows_and_guidance.ipynb)

Chapters 6 and 7 cover the probability flow ODE, flow matching and guidance. We compare ODE and SDE
marginals, then train a flow on eight planar Gaussian clusters and inspect its output at several Euler
step counts. Straight-line training paths need not give straight ODE trajectories.

The Gaussian guidance example compares the output law with the proposed sharpened target. For guidance
scale $\gamma=2$, Chapter 7 predicts mean $0.750$ (in units of the observation) and variance $0.292$;
the sharpened target instead has mean $0.667$. The MNIST experiment compares classifier-free guidance
at scales $\gamma=0,1,3,7$.

The small U-Net used in Weeks 4 and 5 is in [`mnist_unet.py`](mnist_unet.py). It predicts the noise,
so the score is minus its output divided by $\sigma_\tau$.

## Running the notebooks

You need Python 3.10 or later.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
jupyter notebook
```

Weeks 1–3 take under a minute each on a laptop CPU. Weeks 4 and 5 train a neural network on MNIST,
which takes about seven minutes each on a recent laptop GPU (Apple silicon or CUDA) and much longer on
a CPU. On a CPU, reduce `NUM_STEPS` in the training cell. The MNIST data are downloaded automatically,
and the trained networks are saved in `checkpoints/`, so rerunning a notebook does not retrain them.
