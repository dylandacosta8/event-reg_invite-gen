### <h1 align=center>IS601 Final Project</h1>
### <h2 align=center>Feature: QR Code Generation User Invites with MinIO </h2> 
<div align=center>

This repository includes:
<b>1 new Feature
5+ QA Issues
10+ new Test Cases
</b>

</div>

---
<div align=>

### The submission meets the following goals:

1. <b>Implements a NEW feature</b> into the existing codebase.
2. <b>Fixed 5+ QA Issues/Bugs</b> across the codebase.
3. <b>Wrote 10+ NEW Tests</b> for the new feature implemented.
4. Includes a <b>Reflection Document</b> for the course.
5. Includes <b>Extensive Documentation</b> of the feature, bugs and test cases implemented.

</div>

---
### Course Reflection Document - <a href="https://docs.google.com/document/d/1ouE42CfAX-04u_KONLJEpqo6GNTmMJ4f-0BwwHU069M/edit?usp=sharing">here</a>

---
### QR Code Generation User Invites with MinIO - <a href="documentation/feature.md">here</a>

---
### QA Issues/Bugs - <a href="documentation/bugs.md">here</a>

---
### Test Cases - <a href="documentation/test.md">here</a>

---
### Getting the Project Setup:
<br>

* <b>Clone the repository to your local machine</b>

```
git clone https://github.com/dylandacosta8/is601_final.git
```

* <b>Change directory to the project</b>

```
cd is601_final
```

* <b>Install and Setup Docker [Mandatory]</b>
    <br>
    1. <u>For Linux users</u> - Make sure Docker is installed using your choice of installer for your distribution. <b> > <a href="https://docs.docker.com/engine/install/"> Official Documentation </a> < </b>
    2. <u>For Mac/Windows users</u> - Make sure Docker Desktop is installed and running. <b> > <a href="https://docs.docker.com/desktop/"> Official Documentation </a> < </b>
    <br>

* <b>Start your containerized environment</b>

```
docker compose up --build
```

* <b>Running tests using pytest</b>

```
docker compose exec fastapi pytest
```

* <b>Access various components</b>
    <br>
    1. <b>PgAdmin</b>
    ```
    http://localhost:5050
    ```
    2. <b>FastAPI Swagger UI</b>
    ```
    http://localhost/docs
    ```
    3. <b>MinIO UI</b>
    ```
    http://localhost:9001
    ```

<b>Note:</b>In case you receive an error stating tables do not exist while running tests please run the following command

```
docker compose exec fastapi alembic upgrade head
```
