# Backend service

This is the frist time I use these technologies, I was exploring.



This uses fastapi to validate everything and autogenerate an openapi.

How to examine:

1. `main.py` is where the routes are defined
2. The processor for files is in `_process`.
   1. It depends on a implementation of an async Counter.
      1. A simple version is implemented with python collections (Counter), but
      2. it is abstracted to be able to implement easily anything that allows safe async communcation (not mongodb).
      3. I got it to work with redis,
         1. adding the metadata in a clean way to replicate the CSV gets out of hand, with trying to handle and encode/decode it... Just to simplify, I simply base64 encoded the pair... it seemed ugly
         2. It actually works with multiple processes processing different parts of the file all at once (redis is great)
      4. It assumes that the date is always on the same format, gargage-in, garbage-out
3. The task manager submits to the same asyncio loop, which isn't the best... we are just testing here, in the real world that would be a completely separate process. (and as an agreggator you would use something closer to Kafka and that family of gians... and you wouldn't use CSVs, you would use streams/events/etc)
4. The `__init__` files define a strict surface between modules. To discourage the use of internal functions outside of those modules


To run this and debug/develop appropriatly, use the vscode debugger as explained on [here](../README.md)
