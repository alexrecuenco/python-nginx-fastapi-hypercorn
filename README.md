# Example

- NGINX for uploading files faster
- A backend with fastapi that doesn't touch the files to use all the validation magic of fastapi
- Debugging magic to allow easy development using VScode tasks and docker compose

# Requirements

Docker, and docker compose.

Tested with

```txt
❯ docker --version
Docker version 24.0.6, build ed223bc
❯ docker compose version
Docker Compose version v2.22.0-desktop.2
```

# How to use

1. After running (See How to Run), go to `localhost:8080`
2. Upload your CSV, it will POST to `uploads/` and return a task-id
3. Check your task-id in `uploads/{task-id}`
4. If your task is done, it will automatically redirect you to a download
5. If there was an error, it will give you the error code, you could "report" this to the server manager, and he will find in the logs how it happened searching for your task ID, if they have logs enabled to the correct level.


# How to run

## For developers

In debug mode, if you are using vscode, simply go to "Run and Debug" and click run.

It might take some time, since it is building all the docker images and running everything first, but you get a full debug context attached once it runs


- It exposes port 8000 (backend), 8080 (frontend), 5678 (backend debugger), 6379 (redis)
- It activates DEBUG logging
- It has auto-reload, so just modify a file in the backend section and explore that it autoreloads correctly (It should say "listening..." again when it does so)
- NGINX is a mess to work with

## Without debugging

Simply run

```bash
docker compose up -d
```

# Large files

Large files are memory constrained, as long as the number of songs and days is bounded below the available memory

I was planning to fix that using the redis backend, but I ran out of the self-allocated time, I couldn't come up with a "clean" way to allocate multi-column counts (because simply uploading to a SQL-server, creating an index and executing COUNT seems like cheating)

# NGINX

NGINX here is simulating a upload server with a shared file-service that you can stream over the internet to our server (Like S3, a ntfs server, etc). It proxy's the backend server, saves the file in a network volume, and provides to the backend the necessary information to know where to find that file. If you are feeding a large blob to python directly, you are looking for trouble.

Also, this NGINX module used here can do resumable downloads! (Even though it is disabled here)

# Backend

Extra information on the backend implementation and how to read it [here](./backend/README.md)

# Frontend

The frontend is as ugly as it gets... I did want to try React Aria, but, again, time

# Tests

Linting and tests run automatically with github actions.

# Assignment

## Backend Engineer - Assignment

1. The test should not take longer than a few hours or up to a day.
2. The simpler the better.
3. The test consists of two logical parts:
    - CSV processing module;
    - API and task execution system which uses this module to process the uploaded files.

### Large CSV Processing

1. Create a module/function which takes a CSV file of the following format as its input, processes it and generates the output CSV file.
2. Explain how your code works. Explain O(…) computational complexity of this processing.

*Input CSV file*: `“Song”, “Date”, “Number of Plays”`.

There will be many records for each song within each day. Input is not sorted.

*Output CSV file*: `“Song”, “Date, “Total Number of Plays for Date”`


**Important notes**:
- Both input and output CSV files can be larger than available memory.
- You can use Python built-ins or any available third-party libraries/frameworks/software.
- If you are using a third-party library which solves the problem - please explain how it works internally and why it is suitable for this task. Give a brief explanation of the computational complexity of the algorithms used in the library.

```csv
Input example:
Song,Date,Number of Plays
Umbrella,2020-01-02,200
Umbrella,2020-01-01,100
In The End,2020-01-01,500
Umbrella,2020-01-01,50
In The End,2020-01-01,1000
Umbrella,2020-01-02,50
In The End,2020-01-02,500

Output example for this input file:
Song,Date, Total Number of Plays for Date
Umbrella,2020-01-01,150
Umbrella,2020-01-02,250
In The End,2020-01-01,1500
In The End,2020-01-02,500
```


### API and Asynchronous Task Processing

1. API Endpoint 1: Schedule file to processing
    - Input: CSV file upload (remember – they can be larger than memory)
    - Output: ID of the processing task.
   - process the uploaded large CSV file in background with the code implemented above;
   - return ID of the processing task to retrieve the results later.

2. API Endpoint 2: Download the result.
- Input: ID of the processing task.
- Output: The resulting CSV if processing is done.

**Important Notes**
- **Both input and output files can be larger than memory and processing can take much time**. Implement it in a way for the API server to be able to receive further requests while the previous file is still being processed.
- You can use any Python API and task execution frameworks you prefer or not use them at all.
- This is not a production-ready system but a test to demonstrate your understanding of the API and asynchronous task processing concepts.
- Please provide all the configuration and instructions needed to start your project by a person who did not see it previously and examples on how to upload a file and download the results.


---
Thank you for your time!


## TODO

- Create `pyproject.toml` (See https://github.com/pgjones/hypercorn/blob/main/pyproject.toml)
  - Add `tox`  to it (See https://stackoverflow.com/a/72258987/7346915 to get started)
  - Add poetry for version mnagement
