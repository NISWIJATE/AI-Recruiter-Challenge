\# AI Recruiter Challenge



\## Overview



This project builds an AI-powered candidate ranking system that matches candidates to a job description using semantic understanding, role relevance, career history, skills, and behavioral signals instead of simple keyword matching.



\## Problem Statement



Traditional ATS systems rely heavily on keyword matching, often missing highly relevant candidates. This solution uses a hybrid ranking approach to identify candidates who genuinely fit the role.



\## Approach



\### 1. Job Description Understanding



\* Extract requirements from the job description.

\* Identify required skills, experience, and role expectations.



\### 2. Candidate Representation



\* Combine:



&#x20; \* Profile information

&#x20; \* Career history

&#x20; \* Skills

&#x20; \* Certifications

&#x20; \* Behavioral signals



\### 3. Retrieval Layer



\* TF-IDF semantic retrieval used to find relevant candidates.

\* Candidate profiles converted into searchable text.



\### 4. Hybrid Ranking



Additional scoring factors:



\* Role Fit Score

\* Career History Score

\* AI Skill Score

\* Assessment Score

\* Behavioral Signal Score

\* Founding/Product Builder Indicators



\### 5. Tier-Based Ranking



\#### Tier A



Direct AI/ML/Search/Recommendation roles.



\#### Tier B



Strong career transition candidates.



\#### Tier C



AI enthusiasts with partial evidence.



\#### Tier D



Low relevance candidates.



\## Tech Stack



\* Python

\* Pandas

\* Scikit-Learn

\* Jupyter Notebook



\## Repository Structure



AI-Recruiter-Challenge/



├── data/



├── notebooks/



│ └── EDA.ipynb



├── output/



├── src/



└── README.md



\## How to Run



1\. Install dependencies



pip install pandas numpy scikit-learn python-docx



2\. Open notebook



jupyter notebook



3\. Run EDA.ipynb



4\. Generate ranked candidates



5\. Export final submission CSV



\## Author



Tejaswini Mane



