# Generative Modelling with Stochastic Differential Equations

MSc in Mathematical Finance, Imperial College London, 2026–27. Lectures by Cristopher Salvi.

## About the course

Diffusion models are the technology behind today's image, video and audio generation. The course uses  tools from stochastic analysis to provide a mathematical description of how modern generative approaches are used to model a probability distribution.
We will begin by analysing Langevin dynamics and score matching, and then develop diffusion models, flow matching and guidance as a mathematical theory.

### 1. Sampling in high dimension

We want to sample from a probability distribution $\mu$ on $\mathbb{R}^n$, where $n$ is large. Either we know the density of $\mu$ up to a normalising constant, or we only have samples from $\mu$. In this chapter we review the classical methods for both settings, such as inverse-CDF sampling, rejection sampling and density estimation. We show that their cost grows at least exponentially with $n$, because they need samples or proposals to fall in a region whose probability decays exponentially with the dimension. This is the curse of dimensionality. These methods fail because they make no use of the structure of $\mu$. The score $\nabla\log\mu$ gives such information. It points in the direction in which the density increases fastest, it does not depend on the normalising constant, and it can be estimated from samples.

So far we have no sampling method that uses the score. We build one in Chapter 2.

### 2. Langevin dynamics and the score

If we simply follow the score, we get the gradient flow of $\log\mu$, which converges to a local maximum of the density and does not sample from $\mu$. In this chapter we add Brownian noise to the gradient flow. This gives the Langevin diffusion, and we show that $\mu$ is invariant for it. Discretising in time gives the unadjusted Langevin algorithm (ULA), which only needs evaluations of the score. If we only have samples from $\mu$, we do not know the score, and we show that we can estimate it from the samples by solving a regression problem.

We only showed that the Langevin diffusion keeps the law $\mu$ if it is started from $\mu$ itself. So far we have no guarantee on what happens if it is started from a different distribution. Also, ULA introduces a bias, because its invariant law is not $\mu$. We treat both points in Chapter 3.

### 3. Convergence of the Langevin diffusion and of ULA

In this chapter we show that the Langevin diffusion started from any initial law converges to $\mu$ exponentially fast. We prove this in Wasserstein distance when the potential is strongly convex, and in $\chi^2$-divergence or relative entropy when $\mu$ satisfies a Poincaré or a log-Sobolev inequality, which does not require convexity. For ULA with a strongly convex and smooth potential, we show convergence up to a bias that vanishes with the step size. The number of iterations needed for a given accuracy is then polynomial in $n$, so for these targets there is no curse of dimensionality.

These guarantees become useless when $\mu$ has several well-separated modes, because the process moves from one mode to another only exponentially rarely. The distributions of interest in generative modelling are of this type. We construct a different method in Chapter 4.

### 4. Noising and time reversal

Langevin dynamics is slow when the target has several modes. In this chapter we sample the data distribution $q$ in a different way. We first add Gaussian noise to the data progressively, until its law is close to a standard Gaussian. We then show that this noising process can be reversed in time. The reverse process is again a diffusion, and its drift only requires the scores of the noised data, which we can learn by the regression of Chapter 2. Starting from a Gaussian sample and simulating the reverse process gives a sample from $q$. This is the score-based diffusion model. The process never has to move between separated modes, because the modes appear gradually as the noise is removed.

This holds only with the exact scores and in continuous time. In Chapter 5 we bound the error of the sampler used in practice.

### 5. Convergence of diffusion models

In practice we start the reverse process from a standard Gaussian, we use a learned score, and we discretise time. In this chapter we bound the relative entropy between $q$ and the law of the output, with one error term for each of these three approximations. The main tool is Girsanov's theorem, which compares two diffusions with the same noise through the difference of their drifts. If the scores are Lipschitz and the learned score is accurate, the number of steps needed for a given accuracy is polynomial in $n$. We do not assume convexity or a functional inequality on $q$, so the result covers the multimodal distributions for which Langevin dynamics fails.

### 6. ODE and flow-based generative models

In this chapter we replace the reverse SDE by an ordinary differential equation started from a random initial point. We first derive the probability flow ODE, whose solution has the same law as the reverse SDE at every time. We then go in the other direction. We choose an interpolation between noise and data, and we learn by regression a velocity field whose flow has the same marginal laws as the interpolation. This is flow matching. For Gaussian interpolations the velocity field is an affine function of the score, and one particular choice gives back the probability flow ODE. So diffusion models and flow matching are two cases of the same construction.

All the models so far sample from the data distribution $q$ itself. We cannot yet ask for a sample with a prescribed property. We treat this in Chapter 7.

### 7. Guidance and the Doob h-transform

Suppose that each data point comes with a label, such as a class or a text prompt, and that we want samples with a given label. In this chapter we show how to modify a diffusion model to do this. In classifier guidance, we train a classifier that predicts the label from a noised data point, and at each step of the reverse process we add a term that moves the sample in the direction in which the classifier finds the label more likely. We show that the modified process samples exactly from the data with the given label. In classifier-free guidance, no classifier is needed. We train a single score model, both with and without the label, and the difference between its two outputs gives the same term. We explain why these methods are exact through the Doob h-transform, which describes a diffusion conditioned on an event at its final time.

In practice the additional term is multiplied by a scale larger than one, because this is found to give samples that are more typical of the label, at the expense of diversity. This is useful, but it is no longer exact conditional sampling. We show on a Gaussian example that the output is then more concentrated than the distribution one would expect to obtain.

Everything in Chapters 4 to 7 is on $\mathbb{R}^n$ and does not apply to discrete data such as text. We treat this case in Chapter 8, if time allows.

### 8. Discrete diffusion models

On a finite state space we have neither Gaussian noise nor the gradient of the log-density. In this chapter we build their analogues on the Boolean cube $\lbrace 0,1\rbrace^n$. We add noise by flipping each coordinate at random times, until the law is close to uniform. The reversed process is again a Markov chain, and its jump rates are ratios of probabilities between neighbouring states. These ratios take the place of the score, and we learn them with a denoising loss. A discrete analogue of Girsanov's theorem bounds the error of the sampler by this loss, as in Chapter 5. Unlike in the continuous case, we can simulate the learned chain exactly. The last section treats masked diffusion, the variant used for sequences of tokens.

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

## Assessment

The course is assessed 100% by a written exam.

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
