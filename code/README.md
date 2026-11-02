# Notebooks

There is one notebook for each week. They are not exercises and are not examined. They are meant to
be read alongside the notes.

Most results in the course bound an error by a constant times some function of the dimension, the
step size or the time horizon. A simulation proves nothing, but it can show what such a statement
leaves out. It shows how large the constants are, how far the bounds are from the exact errors, and what goes
wrong when a hypothesis fails. For this reason the
notebooks mostly use examples in which the exact answer is known, such as Gaussian data or mixtures
of Gaussians, and compare the simulation with the formula from the notes. Where the dimension
matters, the experiments let it vary, up to 784 for MNIST. Pictures in the plane are used only where
a vector field or a family of trajectories has to be drawn.

Each notebook runs from top to bottom, and most sections end with suggestions of parameters to vary.
The notebooks are stored with their outputs, so they can be read on GitHub directly.

## Week 1. [Sampling and the score](week1_sampling_and_the_score.ipynb)

The notebook starts with the curse of dimensionality. Rejection sampling from the unit ball with
proposals from the cube needs about $10^{20}$ proposals per sample in dimension 40. Kernel density
estimation with 20,000 samples has a median error of 1% in dimension 1, and of 99% in dimension 32.
It then turns to Langevin dynamics. The unadjusted Langevin algorithm has exactly the stationary
variance predicted in the notes, which is not that of the target. Started in one mode of a mixture,
Langevin dynamics stays there. Near a well-separated component, the score of a mixture hardly
depends on the weights, so a trajectory that cannot cross between the modes has no way of learning
them. The
last section checks denoising score matching against the identity of Chapter 2. The excess loss of a
learned score is 0.0293, and its actual mean-square error is 0.0287.

## Week 2. [Langevin dynamics](week2_langevin_dynamics.ipynb)

Two Langevin diffusions driven by the same Brownian motion approach each other at the rate predicted
by strong convexity. In dimension 200, the bound obtained through the $\chi^2$-divergence needs time
about 104 to guarantee a small total variation distance, while the bound through the relative entropy
needs about 6.6, close to the exact value 6.4. The $\chi^2$ bound
pays for starting far from equilibrium, since the initial divergence $e^{|m|^2}-1$ is exponentially
large. For a mixture of two modes at distance $2a$, the mean time to cross from one mode to the other
grows exponentially in $a^2$, and so does a lower bound on the Poincaré constant. The notebook ends by measuring the bias of ULA
as a function of the step size.

## Week 3. [Time reversal](week3_time_reversal.ipynb)

The target is a mixture of two well-separated modes, with weights 0.8 and 0.2. Langevin dynamics puts
weight 0.48 on the lighter mode, and simulated annealing puts 0.49. The reverse Ornstein–Uhlenbeck
process with the exact score gets 0.20. The rest of the notebook follows the forward process as it
blurs the data, checks that the reverse process has the exact variance at every time, and shows the
score acting as a denoiser at several noise levels. A diffusion model whose score is learned from
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
has mean 0.667, so guidance overshoots it. The notebook ends with classifier-free guidance on MNIST
for $\gamma=0,1,3,7$.

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
