# Example

- NGINX for uploading files faster
- A backend with fastapi that doesn't touch the files to use all the validation magic of fastapi
- Debugging magic to allow easy development using VScode tasks and docker compose

# Backend Engineer - Assignment

1. The test should not take longer than a few hours or up to a day.
2. The simpler the better.
3. The test consists of two logical parts:
    - CSV processing module;
    - API and task execution system which uses this module to process the uploaded files.

## Large CSV Processing

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


## API and Asynchronous Task Processing

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
