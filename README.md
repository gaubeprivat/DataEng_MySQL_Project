# Using open Soucre Data and Tools to demonstrate SQL and Data Engineering Skills

## Summary
This project is not solely about "problem-solving" but aims to demonstrate fundamental programming practices and concepts, as well as an understanding of software development in the context of data processing, using an example. Therefore, the zip file is treated as if data in this exact format will repeatedly be provided, which will be transferred to a database using the Python script.

A schema was designed for a MySQL database, specifically tailored to the data from Amin et al. (2022), which is freely accessible via physionet.org. Based on my prior experience from my master's thesis, this sample dataset consists of physiological signals and event series. Specifically, heart rate variability (HRV) data collected from students during three different exams is processed.

In addition to data processing and database creation, test-driven development and the use of Git are demonstrated through this example project. A brief data query and processing are conducted in the accompanying Jupyter Notebook for demonstration purposes.


## Data
The data is freely accessible via https://www.physionet.org/content/wearable-exam-stress/1.0.0/. he downloaded zip file must not be renamed or unpacked for the use of the code. The zip file should either be placed under 'C:\tests' or the path to the zip file should be hardcoded (see TODO).

## Database
For using the code, a running MySQL database on the localhost is required. XAMPP provides an easy way to host a suitable server (MariaDB): https://www.apachefriends.org/de/index.html

DSure, here is the translation:

The result can be viewed with any database management tool. For example, the open-source software HeidiSQL can be used  (https://www.heidisql.com/download.php). The hard-coded schema is 'application_project_gaube'.


## References
Amin, M. R., Wickramasuriya, D., & Faghih, R. T. (2022). A Wearable Exam Stress Dataset for Predicting Cognitive Performance in Real-World Settings (version 1.0.0). PhysioNet. https://doi.org/10.13026/kvkb-aj90