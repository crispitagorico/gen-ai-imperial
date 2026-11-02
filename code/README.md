# Notebooks

There is one notebook for each week. They are not exercises and are not examined. They are meant to
be read alongside the notes.

Many of the experiments use Gaussian targets, for which we can calculate the sampling error and
compare it with the bounds in the notes. Mixtures let us examine the failure of Langevin dynamics to
move between well-separated modes. In both cases we vary the dimension and the time grid, rather than
judge the sampler from a picture alone. The MNIST experiments are in dimension 784. Planar examples
are used where we want to draw a velocity field or follow individual trajectories.

Each notebook runs from top to bottom, and most sections end with suggestions of parameters to vary.
The notebooks are stored with their outputs, so they can be read on GitHub directly. The numbers
quoted below come from these stored runs, and the runtimes are approximate.

## Week 1. [Sampling and the score](week1_sampling_and_the_score.ipynb)

Rejection sampling from the unit ball, using proposals from the cube, needs about $10^{20}$ proposals
per accepted sample in dimension 40. Density estimation deteriorates too. With 20,000 Gaussian
training samples, the median relative error of a kernel density estimate at independent test points
rises from about 1% in dimension 1 to 99% in dimension 32.

For a Gaussian target, ULA has the stationary variance calculated in the notes, including its
discretisation bias. On the separated mixture used here, a trajectory started in one mode remains
there during the run. Near that mode the score depends very little on the mixture weights, so
accurate local motion does not ensure that the sampler gets the proportions right. The denoising
experiment compares the excess regression loss of a learned score, 0.0293, with its mean-square
error, 0.0287, as predicted by the identity of Chapter 2.

## Week 2. [Langevin dynamics](week2_langevin_dynamics.ipynb)

Two Langevin diffusions driven by the same Brownian motion approach each other at the rate predicted
by strong convexity. In dimension 200, the bound obtained through the $\chi^2$-divergence needs time
about 104 to guarantee a small total variation distance, while the bound through the relative entropy
needs about 6.6, close to the exact value 6.4. The $\chi^2$ bound
pays for starting far from equilibrium, since the initial divergence $e^{|m|^2}-1$ is exponentially
large. For a mixture of two modes at distance $2a$, the mean time to cross from one mode to the other
grows exponentially in $a^2$, and so does a lower bound on the Poincaré constant. Varying the step size also lets us measure
the stationary bias of ULA.

## Week 3. [Time reversal](week3_time_reversal.ipynb)

The target is a mixture of two well-separated modes, with weights 0.8 and 0.2. Langevin dynamics puts
weight 0.48 on the lighter mode, and simulated annealing puts 0.49. The reverse Ornstein–Uhlenbeck
process with the exact score gets 0.20. The forward marginals show how noising changes the target.
We compare the simulated reverse variance with its exact value, and use Tweedie's formula to examine
the denoised estimates at several noise levels. A diffusion model whose score is learned from
samples puts weight 0.19 on the lighter mode.

## Week 4. [Convergence of diffusion models](week4_convergence_of_diffusion_models.ipynb)

For Gaussian data the outputs of Euler–Maruyama, of the exponential integrator and of DDPM are again
Gaussian, so their errors can be computed exactly for any number of steps and any time grid. When the
data covariance is nearly singular (variance $10^{-4}$ in some directions), a uniform grid stays
inaccurate even with thousands of steps, because the score becomes very large at the end of the
reverse process. The two-phase grid of Chapter 6, which is geometric near the end, gives far smaller
errors with the same number of steps. In the second half a small U-Net is trained on MNIST, and we
sample from it with 10, 50 and 400 steps. To check that the model is not simply reproducing its
training set, the distance from each sample to the training set is compared with the same distance for
digits from the test set.

## Week 5. [Flows and guidance](week5_flows_and_guidance.ipynb)

The probability flow ODE and the reverse SDE produce the same histograms along very different paths.
For standard Gaussian data the ODE does not move at all. Flow matching is then trained on a mixture of
eight Gaussians in the plane, so that the trajectories can be drawn. The coupling of noise and data produced by the
learned flow has transport cost 7.88, against 18.21 for the independent coupling. Training a second
flow on this coupling (reflow) straightens the trajectories, and one or two Euler steps then already
give good samples.
In a linear-Gaussian model, guidance with scale $\gamma=2$ gives output mean 0.749 and variance 0.295,
while the formula of Chapter 8 predicts 0.750 and 0.292. The sharpened target one might have expected
has mean 0.667, so guidance overshoots it. The MNIST experiment compares classifier-free guidance
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
which takes about eight minutes each on a recent laptop GPU (Apple silicon or CUDA) and much longer on
a CPU. On a CPU, reduce `NUM_STEPS` in the training cell. The MNIST data are downloaded automatically,
and the trained networks are saved in `checkpoints/`, so rerunning a notebook does not retrain them.
