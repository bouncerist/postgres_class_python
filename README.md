# Project Setup Guide

## Container Setup
### Open terminal/command prompt
### Navigate to the project directory:

cd path/to/repository

### Start the containers:  
   
docker-compose up -d

## Python Tasks Execution

### Navigate to python_tasks directory:  
   cd ./python_tasks

### Create and activate virtual environment:
### Windows
   python -m venv myenv <br />
   myenv\Scripts\activate

### MacOS/Linux:  
   python3 -m venv myenv <br />
   source myenv/bin/activate

### Install dependencies
   pip install -r requirements.txt <br />
   
## Run the main script
### Windows
   python main.py

### MacOS/Linux:  
   python3 main.py

## SQL Queries Execution

### Open DBeaver and configure connection to the database (containers must be running)
### Open SQL files from the queries directory
### Set database context at the beginning of each script
### Execute each query separately

## To stop working with the repository and clean up:  
docker-compose down -v
