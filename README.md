# Generative Modelling with Stochastic Differential Equations

MSc in Mathematical Finance, Imperial College London, 2026–27. Lectures by Cristopher Salvi.

## About the course

Suppose we want to draw samples from a probability distribution $\mu$ on $\mathbb R^n$, where $n$ is
large. Sometimes we know the density of $\mu$ up to a normalising constant; sometimes we only have a
large collection of samples, such as a dataset of images, and want to produce new ones. In this
course we will study the mathematics behind the methods used in both situations, and in particular
behind diffusion models.

We will begin with Langevin dynamics, which samples from $\mu$ by following its score $\nabla\log\mu$
with added noise. We will prove that it converges quickly when $\mu$ is strongly log-concave, or satisfies
a Poincaré or log-Sobolev inequality, and see why it can be exponentially slow when $\mu$ has
well-separated modes.

We will then turn to diffusion models. These add Gaussian noise to the data until it looks like a
standard Gaussian, and then run the noising process backwards. We will show that the reversed
process is again a diffusion, whose drift involves the score of the noisy data, and that this score
can be learned by training a network to remove the noise. We will then bound the error of the
resulting sampler in terms of the time horizon, the step size and the accuracy of the learned score,
keeping track of the dimension.

Finally, we will look at deterministic samplers and flow matching, at conditional generation, and at
diffusion on discrete data. Throughout, Gaussian examples, where everything can be computed
explicitly, will let us test how sharp the results are.

## Course material

The lecture notes will be made available at the end of the course, so please come to the lectures and
take notes. There is an exercise sheet for each chapter of the notes, with exercises numbered as in
the notes, released as the course progresses.

| Week | Chapter | Exercises | Notebook |
| ---- | ------- | --------- | -------- |
| 1 | 1. Sampling in high dimension | [Sheet 1](notes/exercises_chapter1.pdf) | [Sampling and the score](code/week1_sampling_and_the_score.ipynb) |
| 1 | 2. Langevin dynamics and the score | [Sheet 2](notes/exercises_chapter2.pdf) | |
| 2 | 3. Convergence of the Langevin diffusion and of ULA | to come | [Langevin dynamics](code/week2_langevin_dynamics.ipynb) |
| 3 | 4. Noising and time reversal | to come | [Time reversal](code/week3_time_reversal.ipynb) |
| 4 | 5. Convergence of diffusion models | to come | [Convergence of diffusion models](code/week4_convergence_of_diffusion_models.ipynb) |
| 5 | 6. ODE and flow-based generative models | to come | [Flows and guidance](code/week5_flows_and_guidance.ipynb) |
| 5 | 7. Guidance and the Doob h-transform | to come | |
| 5 | 8. Discrete diffusion models | to come | |

## Prerequisites

The course assumes working knowledge in linear algebra, probability, and basic stochastic calculus.
Some familiarity with convex optimisation or statistical learning theory will help.

## Assessment

The course is assessed 100% by a written exam.

## Resources

### Books and monographs

- S. Chewi. [*Log-Concave Sampling*](https://chewisinho.github.io/main.pdf). Book draft, 2024.
- C.-H. Lai, Y. Song, D. Kim, Y. Mitsufuji, S. Ermon. [*The Principles of Diffusion Models*](https://arxiv.org/abs/2510.21890). 2025. [Book website](https://the-principles-of-diffusion-models.github.io/).
- B. Øksendal. *Stochastic Differential Equations: An Introduction with Applications*. Springer, 6th ed., 2003.
- D. Revuz, M. Yor. *Continuous Martingales and Brownian Motion*. Springer, 3rd ed., 1999.
- I. Karatzas, S. Shreve. *Brownian Motion and Stochastic Calculus*. Springer, 2nd ed., 1991.
- G. A. Pavliotis. *Stochastic Processes and Applications: Diffusion Processes, the Fokker–Planck and Langevin Equations*. Springer, 2014.
- D. Bakry, I. Gentil, M. Ledoux. *Analysis and Geometry of Markov Diffusion Operators*. Springer, 2014.
- J. Jost. *Partial Differential Equations*. Springer, 2007. Chapter 7 covers the heat equation, semigroups and Brownian motion.
- A. B. Tsybakov. *Introduction to Nonparametric Estimation*. Springer, 2009.
- F. Santambrogio. *Optimal Transport for Applied Mathematicians*. Birkhäuser, 2015.

### Tutorials and lecture notes

- W. Tang, H. Zhao. [Score-based diffusion models via stochastic differential equations: a technical tutorial](https://arxiv.org/abs/2402.07487). 2024.
- P. Holderrieth, E. Erives. [An introduction to flow matching and diffusion models](https://arxiv.org/abs/2506.02070). 2025. Notes for the [MIT course](https://diffusion.csail.mit.edu/).
- Y. Lipman et al. [Flow matching guide and code](https://arxiv.org/abs/2412.06264). 2024.
- A. Montanari. [Sampling, diffusions, and stochastic localization](https://arxiv.org/abs/2305.10690). 2023.
- The Stanford course CS236, [Deep Generative Models](https://deepgenerativemodels.github.io/).
- The CVPR 2022 tutorial [Denoising diffusion-based generative modeling](https://cvpr2022-tutorial-diffusion-models.github.io/).
- Y. Song. [Generative modeling by estimating gradients of the data distribution](https://yang-song.net/blog/2021/score/). Blog post, 2021.
- L. Weng. [What are diffusion models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/) Blog post, 2021.
- S. Dieleman. The blog [sander.ai](https://sander.ai/).

### Papers by topic

**Foundations of diffusion models**

- J. Sohl-Dickstein, E. Weiss, N. Maheswaranathan, S. Ganguli. [Deep unsupervised learning using nonequilibrium thermodynamics](https://arxiv.org/abs/1503.03585). ICML 2015.
- Y. Song, S. Ermon. [Generative modeling by estimating gradients of the data distribution](https://arxiv.org/abs/1907.05600). NeurIPS 2019.
- J. Ho, A. Jain, P. Abbeel. [Denoising diffusion probabilistic models](https://arxiv.org/abs/2006.11239). NeurIPS 2020.
- Y. Song, J. Sohl-Dickstein, D. P. Kingma, A. Kumar, S. Ermon, B. Poole. [Score-based generative modeling through stochastic differential equations](https://arxiv.org/abs/2011.13456). ICLR 2021.
- T. Karras, M. Aittala, T. Aila, S. Laine. [Elucidating the design space of diffusion-based generative models](https://arxiv.org/abs/2206.00364). NeurIPS 2022.
- R. Rombach, A. Blattmann, D. Lorenz, P. Esser, B. Ommer. [High-resolution image synthesis with latent diffusion models](https://arxiv.org/abs/2112.10752). CVPR 2022.

**Time reversal and score matching**

- B. D. O. Anderson. Reverse-time diffusion equation models. *Stochastic Processes and their Applications*, 1982.
- U. G. Haussmann, É. Pardoux. [Time reversal of diffusions](https://projecteuclid.org/journals/annals-of-probability/volume-14/issue-4/Time-Reversal-of-Diffusions/10.1214/aop/1176992362.full). *Annals of Probability*, 1986.
- H. Föllmer. [An entropy approach to the time reversal of diffusion processes](https://link.springer.com/chapter/10.1007/BFb0005070). 1985.
- A. Hyvärinen. [Estimation of non-normalized statistical models by score matching](https://jmlr.org/papers/volume6/hyvarinen05a/hyvarinen05a.pdf). *JMLR*, 2005.
- P. Vincent. A connection between score matching and denoising autoencoders. *Neural Computation*, 2011.
- B. Efron. Tweedie's formula and selection bias. *JASA*, 2011.

**Langevin dynamics and log-concave sampling**

- G. O. Roberts, R. L. Tweedie. Exponential convergence of Langevin distributions and their discrete approximations. *Bernoulli*, 1996.
- R. Jordan, D. Kinderlehrer, F. Otto. The variational formulation of the Fokker–Planck equation. *SIAM J. Math. Anal.*, 1998.
- A. Dalalyan. [Theoretical guarantees for approximate sampling from smooth and log-concave densities](https://arxiv.org/abs/1412.7392). *JRSS-B*, 2017.
- A. Durmus, É. Moulines. [Non-asymptotic convergence analysis for the unadjusted Langevin algorithm](https://arxiv.org/abs/1507.05021). *Annals of Applied Probability*, 2017.
- S. Vempala, A. Wibisono. [Rapid convergence of the unadjusted Langevin algorithm: isoperimetry suffices](https://arxiv.org/abs/1903.08568). NeurIPS 2019.

**Convergence theory for diffusion models**

- V. De Bortoli. [Convergence of denoising diffusion models under the manifold hypothesis](https://arxiv.org/abs/2208.05314). *TMLR*, 2022.
- S. Chen, S. Chewi, J. Li, Y. Li, A. Salim, A. R. Zhang. [Sampling is as easy as learning the score](https://arxiv.org/abs/2209.11215). ICLR 2023.
- H. Lee, J. Lu, Y. Tan. [Convergence of score-based generative modeling for general data distributions](https://arxiv.org/abs/2209.12381). ALT 2023.
- H. Chen, H. Lee, J. Lu. [Improved analysis of score-based generative modeling: user-friendly bounds under minimal smoothness assumptions](https://arxiv.org/abs/2211.01916). ICML 2023.
- G. Li, Y. Wei, Y. Chen, Y. Chi. [Towards faster non-asymptotic convergence for diffusion-based generative models](https://arxiv.org/abs/2306.09251). ICLR 2024.
- J. Benton, V. De Bortoli, A. Doucet, G. Deligiannidis. [Nearly d-linear convergence bounds for diffusion models via stochastic localization](https://arxiv.org/abs/2308.03686). ICLR 2024.
- S. Chen, S. Chewi, H. Lee, Y. Li, J. Lu, A. Salim. [The probability flow ODE is provably fast](https://arxiv.org/abs/2305.11798). NeurIPS 2023.

**Statistical theory of score estimation**

- K. Oko, S. Akiyama, T. Suzuki. [Diffusion models are minimax optimal distribution estimators](https://arxiv.org/abs/2303.01861). ICML 2023.
- Z. Dou, S. Kotekal, Z. Xu, H. H. Zhou. [From optimal score matching to optimal sampling](https://arxiv.org/abs/2409.07032). 2024.
- A. Wibisono, Y. Wu, K. Y. Yang. [Optimal score estimation via empirical Bayes smoothing](https://arxiv.org/abs/2402.07747). COLT 2024.
- S. Chen, V. Kontonis, K. Shah. [Learning general Gaussian mixtures with efficient score matching](https://arxiv.org/abs/2404.18893). 2024.

**ODE and flow-based models**

- R. T. Q. Chen, Y. Rubanova, J. Bettencourt, D. Duvenaud. [Neural ordinary differential equations](https://arxiv.org/abs/1806.07366). NeurIPS 2018.
- J. Song, C. Meng, S. Ermon. [Denoising diffusion implicit models](https://arxiv.org/abs/2010.02502). ICLR 2021.
- Y. Lipman, R. T. Q. Chen, H. Ben-Hamu, M. Nickel, M. Le. [Flow matching for generative modeling](https://arxiv.org/abs/2210.02747). ICLR 2023.
- X. Liu, C. Gong, Q. Liu. [Flow straight and fast: learning to generate and transfer data with rectified flow](https://arxiv.org/abs/2209.03003). ICLR 2023.
- M. S. Albergo, N. M. Boffi, E. Vanden-Eijnden. [Stochastic interpolants: a unifying framework for flows and diffusions](https://arxiv.org/abs/2303.08797). 2023.

**Guidance and conditional generation**

- P. Dhariwal, A. Nichol. [Diffusion models beat GANs on image synthesis](https://arxiv.org/abs/2105.05233). NeurIPS 2021.
- J. Ho, T. Salimans. [Classifier-free diffusion guidance](https://arxiv.org/abs/2207.12598). 2022.
- H. Chung, J. Kim, M. T. McCann, M. L. Klasky, J. C. Ye. [Diffusion posterior sampling for general noisy inverse problems](https://arxiv.org/abs/2209.14687). ICLR 2023.
- Y. Ren, W. Gao, L. Ying, G. M. Rotskoff, J. Han. [DriftLite: lightweight drift control for inference-time scaling of diffusion models](https://arxiv.org/abs/2509.21655). ICLR 2026.

**Low-dimensional structure**

- G. Li, Y. Yan. [Adapting to unknown low-dimensional structures in score-based diffusion models](https://arxiv.org/abs/2405.14861). NeurIPS 2024.
- P. Potaptchik, I. Azangulov, G. Deligiannidis. [Linear convergence of diffusion models under the manifold hypothesis](https://arxiv.org/abs/2410.09046). 2024.

**Discrete diffusion models**

- J. Austin, D. D. Johnson, J. Ho, D. Tarlow, R. van den Berg. [Structured denoising diffusion models in discrete state-spaces](https://arxiv.org/abs/2107.03006). NeurIPS 2021.
- A. Campbell et al. [A continuous time framework for discrete denoising models](https://arxiv.org/abs/2205.14987). NeurIPS 2022.
- A. Lou, C. Meng, S. Ermon. [Discrete diffusion modeling by estimating the ratios of the data distribution](https://arxiv.org/abs/2310.16834). ICML 2024.
- H. Chen, L. Ying. [Convergence analysis of discrete diffusion model: exact implementation through uniformization](https://arxiv.org/abs/2402.08095). 2024.
- S. S. Sahoo et al. [Simple and effective masked diffusion language models](https://arxiv.org/abs/2406.07524). NeurIPS 2024.

### Software

- Hugging Face [`diffusers`](https://github.com/huggingface/diffusers) provides pretrained diffusion models and samplers.
- [`facebookresearch/flow_matching`](https://github.com/facebookresearch/flow_matching) is a PyTorch library for flow matching.
- [`yang-song/score_sde_pytorch`](https://github.com/yang-song/score_sde_pytorch) is the reference implementation of score-based SDE models.

## Acknowledgements

This course follows *Computational and Statistical Aspects of Diffusion Models*
(401-4634-24L) by [Yuansi Chen](https://people.math.ethz.ch/~chenyua/) at ETH
Zürich. I thank him for making his course material publicly available.
