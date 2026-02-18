# Generative Models in Finance

MSc in Mathematical Finance, Imperial College London — Spring 2026.

**Lecturer:** Cristopher Salvi

A 5-week course (3h lecture per week) covering the mathematics of LLMs, RL training, financial applications, and theoretical foundations of diffusion models. 

## Course structure

| Week | Topic | Reference |
|------|-------|-----------|
| 1 | The Mathematics of Large Language Models | `llm_math.pdf` |
| 2 | Reinforcement Learning Training of LLMs | `llm_training.pdf` |
| 3 | Large Language Models for Finance | `llm_finance.pdf` |
| 4 | Introduction to Diffusion Models (Part 1) | `diffusion_models.pdf` |
| 5 | Introduction to Diffusion Models (Part 2) | `diffusion_models.pdf` |

## Code

Each week has an accompanying Jupyter notebook with worked examples and implementations.

### Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r code/requirements.txt
```

### Running notebooks

```bash
source .venv/bin/activate
jupyter notebook
```

Then navigate to the relevant `code/weekN/` folder and open the notebook.


## Assessment

Assessment is via a single final coursework which counts for 100% of grade. Details to be released in due course.