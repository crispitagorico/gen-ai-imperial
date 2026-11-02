# Generative Modelling with Stochastic Differential Equations

MSc in Mathematical Finance, Imperial College London, 2026–27. Lectures by Cristopher Salvi.

## About the course

Suppose we are given a large number of samples from an unknown probability distribution $q$ on
$\mathbb R^n$, with $n$ large, and we would like to generate new samples from $q$. Diffusion models,
which are now widely used to generate images and audio, approach this problem as follows.

One first destroys the data by running the Ornstein–Uhlenbeck process

$$dX_\tau=-X_\tau\,d\tau+\sqrt2\,dB_\tau,\qquad X_0\sim q .$$

The law $q_\tau$ of $X_\tau$ converges to the standard Gaussian, exponentially fast as soon as $q$
has a finite second moment. One then tries to run this process backwards. It is a classical, and not entirely obvious, fact that
the time reversal of a diffusion is again a diffusion. Here it solves

$$dY_t=\bigl[Y_t+2\nabla\log q_{T-t}(Y_t)\bigr]dt+\sqrt2\,dB_t ,$$

so if $Y_0$ is drawn from $q_T$, which for large $T$ is very nearly Gaussian, then $Y_T$ has law $q$.
The only unknown in this equation is the score $\nabla\log q_\tau$ of the noised distributions. If we
write $X_\tau=e^{-\tau}X_0+\sigma_\tau Z$, with $\sigma_\tau^2=1-e^{-2\tau}$ and $Z$ standard
Gaussian, then Tweedie's formula gives

$$\nabla\log q_\tau(x)=-\sigma_\tau^{-1}\,\mathbb E[Z\mid X_\tau=x],$$

so the score is, up to a factor, the best prediction of the noise given the noisy point. Estimating
it is a regression problem, and in practice one solves it by training a neural network to denoise.

Generating samples has thus been reduced to regression, and this course is about making that
reduction quantitative. How large must $T$ be, how finely must we discretise the reverse equation,
and how accurately must we learn the score? How do the answers depend on the dimension? And why does
the method work for distributions with several well-separated modes, where Langevin dynamics can be
exponentially slow?

It helps to keep one example in mind throughout. If $q=N(m,\Sigma)$ is Gaussian then so is
$q_\tau=N\bigl(e^{-\tau}m,\,e^{-2\tau}\Sigma+\sigma_\tau^2I_n\bigr)$, the score is affine in $x$, and
the reverse equation is a linear SDE that can be solved explicitly. We will use this case to test the
general results and to see how sharp they are. It already shows the main technical difficulty. If
$\Sigma$ is singular, so that the data lie on a proper subspace, the score has Lipschitz constant of
order $1/\tau$ as $\tau\to0$, and a good part of the convergence theory is about coping with this.

## Outline

The course consists of five three-hour lectures, given on the board. The outline below is
provisional, and the pace will adapt to the class. Material marked ⋆ is optional and will not be
examined.

### Week 1. Sampling in high dimension (Chapters 1–2)

Why sampling in high dimension is hard, seen through rejection sampling and kernel density
estimation. Langevin dynamics, which needs only the score of the target, and the estimation of the
score from samples by score matching, denoising and Tweedie's formula.

### Week 2. Convergence of Langevin dynamics (Chapter 3)

How fast Langevin dynamics and its discretisation approach the target, under strong convexity and
under Poincaré and log-Sobolev inequalities, and why they become very slow when the target has
several well-separated modes.

### Week 3. Time reversal (Chapter 4, and Chapter 5⋆)

Simulated annealing, the Ornstein–Uhlenbeck process and the time reversal of diffusions, which
together lead to score-based diffusion models. The proof of the time-reversal formula is optional.

### Week 4. Convergence of diffusion models (Chapter 6)

Error bounds for diffusion models obtained from Girsanov's theorem, with and without smoothness
assumptions on the score, and the statistical cost of learning the score.

### Week 5. Flows and guidance (Chapters 7–8, and Chapter 9⋆)

The probability flow ODE and flow matching. Conditional generation, and guidance seen through Doob's
$h$-transform. Discrete diffusion models are optional.

An appendix of the notes collects the background we need from stochastic calculus and on divergences
between probability measures.

## Course material

The lecture notes will be made available at the end of the course, so please come to the lectures and
take notes. There is an exercise sheet for each week, with exercises numbered according to the
chapters of the notes, and exercises marked ⋆ are on optional material. A separate background sheet
revises the stochastic calculus used in the course.

| Week | Chapters | Exercises | Notebook |
|------|----------|-----------|----------|
| 1 | 1–2 | [Sheet 1](notes/exercises_week1.pdf) | [Sampling and the score](code/week1_sampling_and_the_score.ipynb) |
| 2 | 3 | [Sheet 2](notes/exercises_week2.pdf) | [Langevin dynamics](code/week2_langevin_dynamics.ipynb) |
| 3 | 4, 5⋆ | [Sheet 3](notes/exercises_week3.pdf) | [Time reversal](code/week3_time_reversal.ipynb) |
| 4 | 6 | [Sheet 4](notes/exercises_week4.pdf) | [Convergence of diffusion models](code/week4_convergence_of_diffusion_models.ipynb) |
| 5 | 7–8, 9⋆ | [Sheet 5](notes/exercises_week5.pdf) | [Flows and guidance](code/week5_flows_and_guidance.ipynb) |
| | Appendix | [Background sheet](notes/exercises_background.pdf) | |

The notebooks are not exercises. They illustrate the results of the lectures numerically, and they
are stored with their outputs, so they can be read on GitHub without running them. Weeks 4 and 5
train small diffusion models on MNIST. More details are in the [notebooks' README](code/README.md).

## Prerequisites

The course assumes linear algebra, probability, and stochastic calculus at the level of Brownian
motion, Itô's formula and stochastic differential equations. The background exercise sheet revises
what we use. Some familiarity with convex optimisation or statistical learning theory will help.

## Assessment

The course is assessed by an oral exam. Details will be announced during the term.

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
