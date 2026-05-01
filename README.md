# Temporal analysis of the number of doctor appointments in Primary Care in Portugal using Python and interactive visualization

![Python](https://img.shields.io/badge/Python-3.13-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-Complete-brightgreen)

## Overview
This project was defined and implemented as an answer to the Honors Track feature of "Python for Everybody Specialization", from the University of Michigan, available at coursera.org.

In the fifth and final module of this course, it is encouraged to create a project (Capstone) that uses the concepts taught and learnt in the four preceding modules.

The project analyses the evolution of the number of doctor appointments in Primary care in Portugal from 2018 to 2025, fetching data from a dataset made available at https://www.dados.gov.pt. The data is then processed, divided by categories (year, region...) and then interpreted looking for plausible meaningful conclusions that might be drawn from the data.

---

## Clinical Context
Citing the World Health Organization, Primary Health Care "is the most inclusive, equitable, cost-effective and efficient approach to enhance people’s physical and mental health, as well as social well-being." (https://www.who.int/news-room/fact-sheets/detail/primary-health-care). 
Meanwhile, there has been an alarming increase in the number of people with no designated family doctor in Portugal throughout the last decade (https://www.lusa.pt/article/44176435/portugal-people-without-family-doctors-still-over-1-5m-in-2024-health-service). 
At the same time, there are several reports of a decrease in the number of GPs working full-time in the public sector (https://pmc.ncbi.nlm.nih.gov/articles/PMC11316367/).

Analysing the number of GP appointments throughout the years may shed a new light regarding how well (or ill) covered is the portuguese population regarding Primary Care. At the same it, it might provide an interesting opportunity to assess how the global Covid-19 pandemic changed General Practice in Portugal. 

---

## Dataset
- **Source:** To be filled later 
- **Size:** To be filled later 
- **Features used:** To be filled later
- Note: To be filled later

---

## Methodology
1. **Search for a source**: dados.gov.pt was found. Downloaded the CSV dataset at https://dados.gov.pt/pt/datasets/consultas-medicas-nos-cuidados-de-saude-primarios-2/.
---
1. **Data extraction** — To be filled later
2. **Feature engineering** — To be filled later
3. **Modelling** — To be filled later
4. **Evaluation** — To be filled later
5. **Explainability** — To be filled later

---

## Results

(Just an example. To be filled later.)

| Model               | AUC-ROC | Brier Score |
|---------------------|---------|-------------|
| Logistic Regression | 0.71    | 0.18        |
| Random Forest       | 0.78    | 0.15        |
| XGBoost             | 0.82    | 0.13        |

![SHAP Summary Plot](images/shap_summary.png)

---

## How to Run

To be filled later

$ git clone https://github.com/danieleloi/readmission-mimic
$ cd readmission-mimic
$ pip install -r requirements.txt
$ jupyter notebook notebooks/01_data_extraction.ipynb

---

## Repository Structure
├── data/               # Raw data not included (see Dataset section)
├── notebooks/
│   ├── 01_data_extraction.ipynb
│   ├── 02_feature_engineering.ipynb
│   └── 03_modelling_evaluation.ipynb
├── src/                # Python modules
├── images/             # Plots and figures
├── requirements.txt
└── README.md

---

## Limitations & Future Work
(To be filled later)

- Data from the Vitacare EHR system was not embedded into the database provided.  

- Model trained on US ICU data (MIMIC); generalisability to Portuguese SNS context requires validation
- Missing data handled with median imputation — more robust methods (MICE) could improve performance
- Future work: temporal validation (train 2008–2015, test 2016–2019) and integration with a Streamlit interface

---

## Author
**Daniel Eloi, MD** — Family Physician transitioning to Clinical Data Science  
📍 Aveiro, Portugal | [LinkedIn](https://www.linkedin.com/in/daniel-e-55b439b6/) | [GitHub](https://github.com/DanielEloi)

