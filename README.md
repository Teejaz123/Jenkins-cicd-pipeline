# Jenkins CI/CD Pipeline

This project demonstrates a simple **CI/CD pipeline using Jenkins**.

## Overview
- A small Flask app (Python)
- Dockerized for portability
- Jenkins pipeline automates:
  1. Code checkout
  2. Docker build
  3. Unit tests (pytest)
  4. Run container

## Prerequisites
- Docker installed
- Jenkins with Docker & Pipeline plugins

## Pipeline Stages
1. **Checkout** – Pulls code from GitHub  
2. **Build** – Creates Docker image  
3. **Test** – Runs pytest on the app  
4. **Run** – Deploys the container locally  

## Run locally
```bash
docker build -t jenkins-cicd-app ./docker
docker run -d -p 5000:5000 jenkins-cicd-app
