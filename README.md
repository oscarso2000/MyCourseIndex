# MyCourseIndex
MyCourseIndex is a project for CS/INFO 4300: Language and Information that acts as an essential search engine for Cornell students and their courses with the initial goal to improve the Piazza search user experience. This search gathers all information from Piazza posts to Textbook and Notes Resources and returns valid results for the student to utilize.  

[![Build Status](https://travis-ci.org/oscarso2000/MyCourseIndex.svg?branch=master)](https://travis-ci.org/oscarso2000/MyCourseIndex)

## Links
Note: You must have a Cornell Email to utilize this website due to security reasons.

* [Website Link: www.mycourseindex.com](https://www.mycourseindex.com)
* [Prototype 2: v2.mycourseindex.com](https://v2.mycourseindex.com)
* [Prototype 1: v1.mycourseindex.com](https://v1.mycourseindex.com)
* [Documentation: docs.mycourseindex.com](https://docs.mycourseindex.com)

## Preview 
![Login Sequence](demo/Login.gif)

![Class Search](demo/1998.gif)

![Concept Matching](demo/4300.gif)

![Sorting](demo/Sorts.gif)

![Boolean Search](demo/Boolean.gif)

![Link](demo/Link.gif)

![Abouts Page](demo/About.gif)

## TOC
1. [Getting Started](#getting-started)
    1. [Accessing the source code](#accessing-the-source-code)
    1. [Prerequisites](#prerequisites)
    1. [Project Structure](#project-structure)
    1. [Backend](#backend)
    1. [Frontend](#frontend)
1. [System Design](#system-design)
1. [Deployment](#deployment)
    1. [Kubernetes](#kubernetes)
1. [Contributing](#contributing)
1. [Author](#author)
1. [License](#license)


## Getting Started

### Accessing the Source Code

```bash
git clone
```

### Prerequisites

- Python v3.7.6
- AWS Cloud account
- Poetry

### Project Structure

Describe structure of project in terms of generic folders and poetry (and other python tools) usage

### Backend
```
poetry install
poetry run python app.py
```
Website should be on browser @ localhost:5000

### Frontend
```
cd client
yarn install
yarn build
cd ..
```

## System Design

## Deployment
Using GitOps (explain more)

### Kubernetes
`Piazza Search` leverages [Kubernetes](https://kubernetes.io) to automate deployment, scaling,
and management of containerized microservices.

**TODO**: Image of the Kubernetes structure

## Author
1. [Magd Bayoumi (mb2363)](https://github.com/bayoumi17m)
1. [Jenna Kressin (jek343)](https://github.com/jek343)
1. [Souleiman Benhida (sb2342)](https://github.com/soule)
1. [Sheetal Athrey (spa42)](https://github.com/sheetal-athrey)
1. [Oscar So (ons4)](https://github.com/oscarso2000)
