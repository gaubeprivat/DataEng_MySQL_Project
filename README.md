# Beispielprojekt zu Bewerbungszwecken

## Kurzbeschreibung
Dieses Projekt zeigt an einem Beispiel Grundlegende Programmierpraxis und Verstaendnis von Softwareentwicklung im Kontext der Datenverarbeitung.
Es wurde fuer eine MySQL Datenbank ein Schema desigend, das speziell auf die Daten von Amin et al. (2022) abgestimmt ist, welche ueber physionet.org frei zugaenglich sind.
Entsprechend meiner Vorerfahrungen aus der Masterarbeit handelt es sich bei diesen Beispieldatensatz um physiologische Signale und Eventserien. Speziell wird die Herzratenvariabilitaet (HRV) verarbeitet, welche fuer Studierende waehrend drei verschiedener Pruefungen erhoben wurden.
Neben der Datenverarbeitung und Datenbankerstellung wird testdriven developement und der Umgang mit git an diesem Beispielprojekt demonstriert.

## Datengrundlage
Die Daten sind ueber https://www.physionet.org/content/wearable-exam-stress/1.0.0/ frei zugaenglich. Die gedownloadete zip-Date darf fuer die Nutzung des Codes nicht umbenannt und nicht entpackt werden. 
Die zip-Datei ist entweder unter 'C:\tests' abzulegen oder der Pfad zur zip-Datei hard zu coden (siehe TODO).

## Datenbankanbindung
Fuer die Nutzung des Codes wird eine laufende MySQL Datenbank auf dem localhost vorausgesetzt. XAMPP stellt eine einfache Moeglichkeit zum hosten eines passenden Servers (MariaDB) bereit: https://www.apachefriends.org/de/index.html

Das Ergebnis kann mit einem beliebigien Datenbank Verwaltungstool eingesehen werden. Beispielsweise kann die OpenSource Software HeidiSQL genutzt werden(https://www.heidisql.com/download.php). Das hard gecodete Schema ist 'application_project_gaube'.


## Literaturnachweis
Amin, M. R., Wickramasuriya, D., & Faghih, R. T. (2022). A Wearable Exam Stress Dataset for Predicting Cognitive Performance in Real-World Settings (version 1.0.0). PhysioNet. https://doi.org/10.13026/kvkb-aj90