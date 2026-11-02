# Nexa --- Crowd Monitoring and Alert Generation Prototype

Nexa is an academic software prototype that combines
computer-vision-based person detection with a web-based monitoring
dashboard. It processes recorded video, estimates the number of people
visible in each frame, classifies the current crowd level using
configurable prototype thresholds, and sends monitoring updates and
alert events to a Spring Boot backend.

> **Important:** Nexa is a prototype. Its thresholds are demonstration
> rules, not validated public-safety limits. It does not claim to
> predict or prevent stampedes.

## Features

-   Person detection in recorded video using Python, OpenCV, and
    Ultralytics YOLO.
-   People counting and configurable `NORMAL`, `WARNING`, and `CRITICAL`
    classification.
-   Alert creation, resolution, and persisted alert history.
-   Monitoring source state and historical samples stored in PostgreSQL.
-   Web dashboard with source status, people-count history, risk
    information, and alerts.
-   JWT authentication and role-based authorization (`ADMIN`,
    `SECURITY`).
-   Dashboard controls for selecting a video and starting or stopping
    the Python monitoring process.

## Technology Stack

  Area              Technologies
  ----------------- -----------------------------------------------------
  Backend           Java, Spring Boot, Spring Security, Spring Data JPA
  Authentication    JWT, BCrypt
  Database          PostgreSQL
  Computer vision   Python, OpenCV, Ultralytics YOLO
  Frontend          HTML, CSS, JavaScript
  Build             Maven
  Server            Embedded Apache Tomcat

## Architecture

``` text
Recorded Video
     |
     v
Python Detection Pipeline (OpenCV + YOLO)
     |
     +--> Person detection and counting
     +--> Crowd-level evaluation
     +--> Alert lifecycle events
     |
     v
Spring Boot REST API
     |
     +--> JWT authentication and role checks
     +--> Monitoring state and history
     +--> Alert history
     |
     v
PostgreSQL Database
     |
     v
Web Dashboard
```

## Project Structure

``` text
nexa/
├── ai/
│   ├── detection/       # Detection, alert, and backend integration scripts
│   ├── video/           # Input videos for testing
│   └── .venv/           # Local Python environment (not committed)
├── launcher/
│   └── Start-Nexa.ps1   # Windows launcher
├── src/
│   └── main/
│       ├── java/        # Spring Boot source code
│       └── resources/
│           └── static/  # Dashboard and login frontend
├── mvnw
├── mvnw.cmd
└── pom.xml
```

## Requirements

-   Windows 10/11
-   Java Development Kit compatible with the project (development used
    Java 25)
-   PostgreSQL (development used PostgreSQL 18)
-   Python 3
-   Git

The repository includes the Maven Wrapper, so a separate Maven
installation is not required.

## Configuration

1.  Create a PostgreSQL database named `nexa`, unless your local
    configuration uses another name.
2.  Configure the database URL, username, and password in the
    application's local configuration.
3.  Configure the JWT signing secret using a secure local configuration
    method.
4.  Keep passwords, signing keys, tokens, and other credentials out of
    Git.

If a secret was already committed, deleting it from the latest version
is not enough. Rotate the exposed credential and clean the repository
history before publishing.

## Run the Backend

From the project root in PowerShell:

``` powershell
.\mvnw.cmd spring-boot:run
```

The current development setup uses port `8081`.

-   Login: http://localhost:8081/login.html
-   Dashboard: http://localhost:8081/dashboard.html

## Run the Video Monitoring Pipeline

Create a Python virtual environment if one does not already exist:

``` powershell
py -m venv .\ai\.venv
.\ai\.venv\Scripts\Activate.ps1
```

Install the Python dependencies required by the detection scripts. If
the repository contains a dependency file, install from that file;
otherwise install the packages specified by the project source.

Set credentials for the Nexa account in the current PowerShell session:

``` powershell
$env:NEXA_EMAIL="your-account-email"
$env:NEXA_PASSWORD="your-account-password"
```

Run the pipeline with a video file that exists in `ai\video`:

``` powershell
.\ai\.venv\Scripts\python.exe .\ai\detection\video_alert_test.py ".\ai\video\sample.mp4"
```

Press `q` in the OpenCV window to close the video display. If the
pipeline was started from the dashboard, use its Stop Monitoring control
as well.

Supported video extensions in the dashboard: `.mp4`, `.avi`, `.mov`, and
`.mkv`.

## Prototype Risk Rules

The current prototype configuration uses these count-based categories:

  Category     People count
  ---------- --------------
  NORMAL              0--19
  WARNING            20--39
  CRITICAL       40 or more

Persistence settings currently used:

-   Escalation: 15 consecutive frames
-   Recovery: 90 consecutive frames

These are implementation settings for testing. They are not
scientifically validated crowd-safety thresholds and must not be used
for real-world emergency decisions.

## Monitoring API

  -------------------------------------------------------------------------------------------------------
  Method                  Endpoint                                                Purpose
  ----------------------- ------------------------------------------------------- -----------------------
  POST                    `/api/security/monitoring/updates`                      Receive monitoring
                                                                                  updates

  GET                     `/api/security/monitoring/sources`                      List monitoring sources

  GET                     `/api/security/monitoring/sources/{sourceId}`           Get a source's latest
                                                                                  state

  GET                     `/api/security/monitoring/sources/{sourceId}/history`   Retrieve recent
                                                                                  monitoring samples

  GET                     `/api/security/video/videos`                            List available video
                                                                                  files

  POST                    `/api/security/video/start`                             Start video monitoring

  POST                    `/api/security/video/stop`                              Stop video monitoring

  GET                     `/api/security/video/status`                            Check video process
                                                                                  status
  -------------------------------------------------------------------------------------------------------

Protected endpoints require a valid JWT and the appropriate role.

## Build and Test

Compile:

``` powershell
.\mvnw.cmd clean compile
```

Package (this command skips tests):

``` powershell
.\mvnw.cmd clean package -DskipTests
```

Run automated tests separately:

``` powershell
.\mvnw.cmd test
```

## Current Limitations

-   Processes recorded video; it is not a complete live-CCTV deployment.
-   Uses count-based risk categories and configurable persistence rules.
-   Does not perform validated stampede prediction.
-   Does not provide crowd-flow analysis, evacuation guidance, or
    certified emergency notifications.
-   Video-process management is tied to the running backend instance;
    production-grade multi-instance process management is outside the
    current prototype scope.

## Future Scope

Possible extensions include live camera integration, improved
crowd-density estimation, movement and flow analysis, site-specific
policies, audit reporting, deployment monitoring, and evaluation against
labelled datasets. Safety-related capabilities would require
domain-expert review and validation before operational use.

## Contributors

Add the project contributors and their roles here.

## Academic Project Disclaimer

Nexa is an academic prototype demonstrating the integration of computer
vision, backend services, database persistence, authentication, and a
web dashboard. It is not a certified crowd-control or
emergency-management product.
