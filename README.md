# Temporal analysis of the number of doctor appointments in Primary Care in Portugal using Python and interactive visualization

![Python](https://img.shields.io/badge/Python-3.13-blue)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Status](https://img.shields.io/badge/Status-WIP-yellow)

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
- **Source:** https://dados.gov.pt/pt/datasets/consultas-medicas-nos-cuidados-de-saude-primarios-2/
- **Format:** JSON; each record is a dict with a fields dict containing the variables
- **Size:** 7092 entries for Subregion + Date pairs, each with data for face-to-face doctor appointments, house visits and other types of appointments 
- **Features used:** JSON module (Python), SQLite3 module (Python), SQLite3 browser for checking and debugging the database file, git BASH for version control

---

## Methodology
1. **Search for a source**: dados.gov.pt was found. Downloaded the JSON dataset at https://dados.gov.pt/pt/datasets/consultas-medicas-nos-cuidados-de-saude-primarios-2/.
2. **Understand the source file data and format**: the source file holds the Python equivalent to a list of dictionaries. Each entry of the list holds a dictionary with only one key-value pair that is relevant to us: "fields" : [dictionary]. The dictionary that represents the value for "fields", on the other hand, holds all the values we will be needing for this project.
3. **Design the data model for the SQL database**:

**Relational schema:**

`Region`

| Column   | Type    | Description           |
|----------|---------|-----------------------|
| id       | INTEGER | Primary key           |
| region   | TEXT    | Region name (e.g. Norte) |

`SubRegion`

| Column       | Type    | Description                    |
|--------------|---------|--------------------------------|
| id           | INTEGER | Primary key                    |
| subRegion    | TEXT    | Subregion name                 |
| region_id    | INTEGER | Foreign key → `Region.id`      |

`SubRegDate`

| Column           | Type    | Description                                      |
|------------------|---------|--------------------------------------------------|
| faceToFaceAppts  | INTEGER | Number of face‑to‑face appointments             |
| houseVisits      | INTEGER | Number of home visits                           |
| otherAppts       | INTEGER | Other appointments                              |
| PRIMARY KEY      | (subRegion_id, date) | Composite key                       |

4. **Implement the import script**: Implement the Python script file that imports the data from the source file and writes it on a SQL database file.
5. **Plan the information to be analyzed and shown in results**: It is easier and more productive to plan the information we intend do show at the end of the queries, and then write the queries accordingly.
Planned analyses include:
- Yearly totals per appointment type and share with unspecified area.
- Yearly activity relative to that appointment type’s peak across 2018–2025.
- Seasonal distribution of activity (winter/spring/summer/autumn).
- For each region (Norte, Centro, LVT, Alentejo, Algarve), the percentage of national total per appointment type.

Example of table:

| Year | F2F appoints | % with unspecified area | House visits | % with unspecified area | Other appts | % with unspecified area |
|------|--------------|-------------------------|--------------|-------------------------|-------------|-------------------------|
| 2018 |                                                                                                        
| 2019 |
| ...  |
| 2025 |

---

## Results

Preliminary results suggest a marked drop in face‑to‑face visits in 2020 with a compensatory rise in other appointment types.

---

## How to Run

```bash
git clone https://github.com/DanielEloi/GP_Data_PT.git
cd GP_Data_PT
python DataMiner.py
python DataQuery.py
```

---

## Repository Structure
(To be filled later)
```text
.
├── DataMiner.py
├── DataMiner_log.txt
├── DataQuery.py
├── GPappointsdata.db
├── GPappointsData.json
├── ReadFirst.txt
└── README.md
```

---

## Limitations & Future Work
- Data from the Vitacare EHR system was not embedded into the database provided.
- Some data is missing - many entries have no data regarding house visits or other types of appointments.
- The analysis in this project is straightforward; it does not use more advanced statistical concepts. It also does not relate the data with the number of GPs working in the public health system at each given time. In future work, it would be interesting to implement statistical analysis and relate appointment trends to the number of GPs working in the public system over time.


---

## Author
**Daniel M. Eloi, MD** — Family Physician transitioning to Clinical Data Science  
📍 Aveiro, Portugal | [LinkedIn](https://www.linkedin.com/in/daniel-e-55b439b6/) | [GitHub](https://github.com/DanielEloi)

