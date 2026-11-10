# Generative Modelling with Stochastic Differential Equations

MSc in Mathematical Finance, Imperial College London, 2026–27. Lectures by Cristopher Salvi.

## About the course

Diffusion models are the technology behind today's image, video and audio generation. The course uses  tools from stochastic analysis to provide a mathematical description of how modern generative approaches are used to model a probability distribution.
We will begin by analysing Langevin dynamics and score matching, and then develop diffusion models, flow matching and guidance as a mathematical theory.

## Course material

The lecture notes will be made available at the end of the course, so please come to the lectures and
take notes. There is an exercise sheet for each chapter of the notes, with exercises numbered as in
the notes, released as the course progresses.

| Week | Chapter                                             | Exercises                                  | Notebook                                                                     |
| ---- | --------------------------------------------------- | ------------------------------------------ | ---------------------------------------------------------------------------- |
| 1    | 1. Sampling in high dimension                       | [Sheet 1](exercises/exercises_chapter1.pdf) | [Sampling and the score](code/sampling_and_the_score.ipynb)                   |
| 1    | 2. Langevin dynamics and the score                  | to come                                    | [Sampling and the score](code/sampling_and_the_score.ipynb)                   |
| 2    | 3. Convergence of the Langevin diffusion and of ULA | to come                                    | [Langevin dynamics](code/langevin_dynamics.ipynb) |
| 3    | 4. Noising and time reversal                        | to come                                    | [Time reversal](code/time_reversal.ipynb) |
| 4    | 5. Convergence of diffusion models                  | to come                                    | [Convergence of diffusion models](code/convergence_of_diffusion_models.ipynb) |
| 5    | 6. ODE and flow-based generative models             | to come                                    | [Flows and guidance](code/flows_and_guidance.ipynb) |
| 5    | 7. Guidance and the Doob h-transform                | to come                                    | [Flows and guidance](code/flows_and_guidance.ipynb) |
| 5    | 8. Discrete diffusion models                        | to come                                    |                                                                              |

## Prerequisites

The course assumes working knowledge in linear algebra, probability, and basic stochastic calculus.
Some familiarity with convex optimisation or statistical learning theory will help.

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

This course follows *Computational and Statistical Aspects of Diffusion Models*
(401-4634-24L) by [Yuansi Chen](https://people.math.ethz.ch/~chenyua/) at ETH
Zürich. I thank him for making his course material publicly available.
