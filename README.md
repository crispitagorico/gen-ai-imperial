# Generative Modelling with Stochastic Differential Equations

MSc in Mathematical Finance, Imperial College London, 2026–27. Lectures by Cristopher Salvi.

## About the course

How can we learn a distribution from data and draw new samples from it? We will use stochastic analysis to build up an answer, from Langevin dynamics and score matching to diffusion models, flow matching, and guidance.

### 1. Sampling in high dimension

We will start with two ways a sampling problem can arise. Sometimes we know a density up to a normalising constant. Sometimes we have only observations and want to generate new ones like them. We will use histograms, kernel density estimation, and maximum likelihood to see how a density can be fitted, then look at rejection sampling. In high dimension, nearby observations and accepted proposals can both be rare. This will motivate a sampler that uses the local slope of the density.

### 2. Langevin dynamics and the score

We will build that sampler using the score $\nabla\log\mu$, which points towards higher density and is independent of the normalising constant. Adding Brownian noise to motion along the score gives the Langevin diffusion. We will show that it preserves the target distribution and see, in a Gaussian example, how discretising it introduces bias. When we have only data, we will learn the score using score matching and denoising score matching.

### 3. Convergence of the Langevin diffusion and of ULA

Once we have a Langevin sampler, we will ask how long to run it and how small to make its steps. We will show that two diffusions driven by the same noise move closer together when the potential is strongly convex. We will also use the Fokker–Planck equation to study convergence in relative entropy and chi-squared divergence. For the discretised sampler, we will separate the error from stopping early, the bias from taking finite steps, and the effect of using an estimated score. Slowly mixing targets with separated modes will motivate a different approach.

### 4. Noising and time reversal

To handle separated modes, we will use the Ornstein–Uhlenbeck process to add Gaussian noise gradually. The modes begin to overlap and the distribution approaches a standard Gaussian. We will then derive the equation that runs this process backwards. Its drift depends on the score of the noised data at each time, which we can learn by denoising regression using Tweedie’s formula. This gives a way to generate data by starting from Gaussian noise and progressively removing it.

### 5. Convergence of diffusion models

The reverse process gives an ideal sampler. We will now ask how close a practical implementation comes to it. The implementation starts from a standard Gaussian, uses an estimated score, and runs in discrete steps. We will use Girsanov’s theorem to connect errors in the drift to errors in the output law. For Lipschitz scores, the resulting bound shows how dimension and desired accuracy affect the number of steps.

### 6. ODE and flow-based generative models

We will then ask whether an ODE can make the same journey from noise to data. We will derive the probability flow ODE and show that it matches the reverse diffusion’s distribution at each time when both start from the same law. Flow matching gives another way to build such an ODE. We will interpolate between noise and data and use regression to learn how fast and in which direction points should move.

### 7. Guidance and the Doob h-transform

So far the goal has been to generate an unconditional sample. We will now ask how to generate a sample with a specified label. Bayes’ rule gives a correction to the unconditional score, and we will see how classifier and classifier-free guidance obtain it. The Doob $h$-transform explains when the corrected dynamics give exact conditional samples. A Gaussian example will show what can happen when we amplify the correction.

### 8. Discrete diffusion models

Finally, we will adapt noising and reversal to discrete data. On the Boolean cube, random coordinate flips move the distribution towards uniform, and the reverse jump rates depend on probability ratios between neighbouring states. We will learn these ratios with a denoising loss and use uniformisation to simulate the learned chain without discretising time. We will finish with masked diffusion for token sequences.

## Course material

Please attend lectures and take notes. The lecture notes will be available at the end of the course. Exercise sheets are released chapter by chapter and use the numbering in the notes.

| Week | Chapter                                             | Exercises                                  | Notebook                                                                     |
| ---- | --------------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| 1    | 1. Sampling in high dimension                       | [Sheet 1](exercises/exercises_chapter1.pdf) | [Sampling and the score](code/sampling_and_the_score.ipynb)                   |
| 1    | 2. Langevin dynamics and the score                  | to come                                    | [Sampling and the score](code/sampling_and_the_score.ipynb)                   |
| 2    | 3. Convergence of the Langevin diffusion and of ULA | to come                                    | [Langevin dynamics](code/langevin_dynamics.ipynb)                             |
| 3    | 4. Noising and time reversal                        | to come                                    | [Time reversal](code/time_reversal.ipynb)                                     |
| 4    | 5. Convergence of diffusion models                  | to come                                    | [Convergence of diffusion models](code/convergence_of_diffusion_models.ipynb) |
| 5    | 6. ODE and flow-based generative models             | to come                                    | [Flows and guidance](code/flows_and_guidance.ipynb)                           |
| 5    | 7. Guidance and the Doob h-transform                | to come                                    | [Flows and guidance](code/flows_and_guidance.ipynb)                           |
| 5    | 8. Discrete diffusion models                        | to come                                    | ---                                                                          |

## Prerequisites

You should know linear algebra, probability, and basic stochastic calculus. Familiarity with convex optimisation or statistical learning theory is helpful.

Jack Daly’s [background slides](lectures/background_slides.pdf) review Brownian motion, Itô calculus, stochastic differential equations, Girsanov’s theorem, generators, and invariant measures.

## Assessment

The oral exam accounts for 100% of the course grade.

## Resources

### Books and notes

- S. Chewi. [*Log-Concave Sampling*](https://chewisinho.github.io/main.pdf). Book draft, 2024. Langevin dynamics and its convergence.
- C.-H. Lai, Y. Song, D. Kim, Y. Mitsufuji, S. Ermon. [*The Principles of Diffusion Models*](https://arxiv.org/abs/2510.21890). 2025. Diffusion models, flows and guidance.
- B. Øksendal. *Stochastic Differential Equations: An Introduction with Applications*. Springer, 6th ed., 2003. Stochastic calculus.
- G. A. Pavliotis. *Stochastic Processes and Applications: Diffusion Processes, the Fokker–Planck and Langevin Equations*. Springer, 2014.
- P. Holderrieth, E. Erives. [An introduction to flow matching and diffusion models](https://arxiv.org/abs/2506.02070). 2025. Notes for the [MIT course](https://diffusion.csail.mit.edu/).
- Y. Song. [Generative modeling by estimating gradients of the data distribution](https://yang-song.net/blog/2021/score/). Blog post, 2021. A gentle entry point.

### Papers

- Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, B. Poole. [Score-based generative modeling through stochastic differential equations](https://arxiv.org/abs/2011.13456). ICLR 2021.
- J. Ho, A. Jain, P. Abbeel. [Denoising diffusion probabilistic models](https://arxiv.org/abs/2006.11239). NeurIPS 2020.
- B. D. O. Anderson. Reverse-time diffusion equation models. *Stochastic Processes and their Applications*, 1982.
- A. Hyvärinen. [Estimation of non-normalized statistical models by score matching](https://jmlr.org/papers/volume6/hyvarinen05a/hyvarinen05a.pdf). *JMLR*, 2005.
- P. Vincent. A connection between score matching and denoising autoencoders. *Neural Computation*, 2011.
- S. Chen, S. Chewi, J. Li, Y. Li, A. Salim, A. R. Zhang. [Sampling is as easy as learning the score](https://arxiv.org/abs/2209.11215). ICLR 2023.
- Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, M. Le. [Flow matching for generative modeling](https://arxiv.org/abs/2210.02747). ICLR 2023.
- J. Ho, T. Salimans. [Classifier-free diffusion guidance](https://arxiv.org/abs/2207.12598). 2022.
- A. Lou, C. Meng, S. Ermon. [Discrete diffusion modeling by estimating the ratios of the data distribution](https://arxiv.org/abs/2310.16834). ICML 2024.

## Acknowledgements

This course draws on *Computational and Statistical Aspects of Diffusion Models*
(401-4634-24L) by [Yuansi Chen](https://people.math.ethz.ch/~chenyua/) at ETH Zürich.
I thank him for making his course material publicly available.
