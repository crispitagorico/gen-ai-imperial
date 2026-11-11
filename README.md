# Generative Modelling with Stochastic Differential Equations

MSc in Mathematical Finance, Imperial College London, 2026–27. Lectures by Cristopher Salvi.

## About the course

Diffusion models are the technology behind today's image, video and audio generation. The course uses  tools from stochastic analysis to provide a mathematical description of how modern generative approaches are used to model a probability distribution.
We will begin by analysing Langevin dynamics and score matching, and then develop diffusion models, flow matching and guidance as a mathematical theory.

### 1. Sampling in high dimension

We begin with the problem of the course, which is to draw samples from a probability distribution $\mu$ on $\mathbb{R}^n$ when $n$ is large, knowing either its density up to a normalising constant or only a collection of samples. We will see that the classical methods stop working in high dimension, because they explore the space without knowing where $\mu$ puts its mass, and their cost grows exponentially with $n$. This will lead us to the score $\nabla\log\mu$, which at every point gives the direction in which the density increases fastest. The score does not depend on the normalising constant and can be estimated from samples, so it is available in both settings.

### 2. Langevin dynamics and the score

We will then use the score to build a first sampling algorithm. Following the score alone would only take us to a maximum of the density, so we will add random noise to the motion, which gives the Langevin diffusion. We will show that the score and the noise balance each other, so that a point distributed according to $\mu$ remains distributed according to $\mu$ at all later times. Discretising time will give an algorithm that only needs evaluations of the score. We will also see how to learn the score by regression when we only have samples from $\mu$.

### 3. Convergence of the Langevin diffusion and of ULA

Next we will study how long the Langevin diffusion has to run before its law is close to $\mu$, when it is started from an arbitrary distribution. When $\mu$ has a single mode, or more precisely when it is strongly log-concave, we will find that the convergence is exponentially fast and that the number of steps of the algorithm is polynomial in $n$, so the curse of dimensionality is gone. When $\mu$ has several separated modes, we will find that the process needs an exponentially long time to move from one mode to another.

### 4. Noising and time reversal

The distributions of generative modelling have many modes, so we will need a different idea. We will add Gaussian noise to the data progressively, until only a Gaussian is left, and then learn to run this process backwards, from noise to data. We will show that the backward process only requires the scores of the noised data, which we can learn as in Chapter 2. This is the diffusion model, the central object of the course. The modes appear gradually as the noise is removed, so the sample never has to travel from one mode to another.

### 5. Convergence of diffusion models

We will then prove that diffusion models work. The algorithm used in practice starts from a Gaussian, which is only close to the law of the fully noised data, uses a learned score, and moves in discrete time steps. We will bound the error that each of these three approximations introduces. If the score is learned accurately, the number of steps will turn out to be polynomial in $n$, this time with no assumption on the number of modes.

### 6. ODE and flow-based generative models

We will see that the passage from noise to data can also be made by a deterministic motion, given by an ordinary differential equation, in which the only randomness is the starting point. This will lead us to flow matching, where we learn directly by regression a velocity field that transports noise to data. Diffusion models will appear as a particular case.

### 7. Guidance and the Doob h-transform

Up to this point the models return an arbitrary sample from the data distribution. We will learn how to steer them towards a sample with a prescribed label, such as an image that matches a text prompt. This is called guidance. It adds to the score a term that pushes the sample towards the data with this label, and we will show that the result is exactly a sample from the data conditioned on the label. In practice this term is amplified, and we will see that the sampling is then no longer exact.

### 8. Discrete diffusion models

Finally, we will adapt the construction to discrete data such as text, where there is neither Gaussian noise nor a gradient. The noise will change the symbols of a sequence at random times, and we will see that ratios of probabilities between sequences that differ in one symbol take the place of the score.

## Course material

The lecture notes will be made available at the end of the course, so please come to the lectures and take notes. There is an exercise sheet for each chapter of the notes, with exercises numbered as in the notes, released as the course progresses.

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

The course assumes working knowledge in linear algebra, probability, and basic stochastic calculus. Some familiarity with convex optimisation or statistical learning theory will help.

The stochastic calculus used in the course (Brownian motion, the Itô integral, Itô's formula, stochastic differential equations, Girsanov's theorem, generators and invariant measures) is reviewed in the [background slides](lectures/background_slides.pdf) by Jack Daly.

## Assessment

The course is assessed 100% by an oral exam.

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
