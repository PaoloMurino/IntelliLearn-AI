# <p align="center"> SmartCargo </p>

<p align="center">
<img width="350" alt="SmartCargo" src="https://github.com/vincenzo-esposit0/AvatarMarket/assets/72707004/2eadba50-4282-424c-858c-f8ac079a436e">
</p>

## Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Resources](#resources)
4. [Objective](#objective)
5. [Presentation](#presentation)
6. [Contributors](#contributors)

## General Info
***
This project was developed for the Fundamentals of Artificial Intelligence exam and is an integration for the Software Engineering exam at the University of Salerno. For more information, please refer to the complete project repository: https://github.com/vincenzo-esposit0/C07_SmartCargo
### Authors
A list of the authors of the project:
* Team Member - [Mariapia Sorrentino](https://github.com/Marypi02)
* Team Member - [Andreea C. C. Oprisecu](https://github.com/andreea3111)
* Team Member - [Roksana Duda](https://github.com/Roksid2002)
* Team Member - [Paolo Murino](https://github.com/PaoloMurino)


## Technologies
***
A list of technologies used within the project:
* [Python](https://www.python.org/)

## Resources
***
A list of resources used within the project:
* [MyMaps](https://www.google.com/intl/it/maps/about/mymaps/)
* [Dataset](https://github.com/PaoloMurino/IntelliLearn-AI/blob/master/src/algoritmoFia/coordinate.csv)

## Objective

**Q: What is the main objective of integrating artificial intelligence into the SmartCargo project in the Port of Valencia?** <br>
A: The main goal of the project is to enhance the existing system by integrating artificial intelligence, aiming to strengthen port infrastructure, improve the safety and efficiency of cargo handling operations, and optimize transit routes to reduce CO2 emissions.

To achieve these objectives, the development of an advanced search algorithm is proposed, particularly the well-known A* algorithm, aimed at calculating the shortest routes that truck drivers will need to follow to access the port and reach the destination point for cargo loading/unloading operations.

The integration of this algorithm will optimize transit routes, taking into account various factors such as traffic congestion, road safety, and CO2 emissions minimization. This will contribute to improving the overall efficiency of the port system, reducing transit times, and optimizing the use of available resources.

## How to replicate the work done?

**1. Map creation:** Through the use of MyMaps, trace the possible routes, each of which will be represented by a set of coordinates, composed of latitude and longitude. <br>
**2. Data formatting:** Using the library offered by Python, pandas, format the set of MyMaps coordinates in a csv file composed of two columns: latitude, longitude. <br>
**3. Construction of the graph:** Build the graph by defining the nodes close to each node by setting a maximum distance for which they can be considered such. <br>
**4. Definition of heuristics:** Choice of metric to use that represents additional information about the problem. In our case the Haversine distance was identified. <br>
**5. Implementation and execution of the algorithm:** Identify the search algorithm to implement based on the objectives to be satisfied, in our case the A* informed search algorithm was chosen; having done this, run the algorithm on the constructed graph and with the chosen heuristic and observe the results obtained.

## Presentation
* [Team Member's Presentation](https://www.canva.com/design/DAF6oBN4d58/_bE7eIt4P1xdDIiTGEIbTA/view?utm_content=DAF6oBN4d58&utm_campaign=designshare&utm_medium=link&utm_source=editor)

## Contributors
<a href="https://github.com/PaoloMurino/IntelliLearn-AI/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=PaoloMurino/IntelliLearn-AI" />
</a>
