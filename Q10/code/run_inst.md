# Benchmark App
To run this flask app, follow these steps :

You can also refer to documentation used during our [bootcamp series](https://dev-foundations.acmbpdc.org/Week%201%3A%20Flask%20%28Backend%29/#13-introduction-to-flask).

1. Install python 3.8+ with the following libraries : numpy, pandas, flask, flask session, rq and rq-dashboard.

2. Install Redis

!!! note "Mac Fork Issue"
    On MacOS, if you see a issue with fork processes you will need to `export OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES`
    for running the `rq` workers

    To manage long running processes such as upload, download, spacy labelling, PINES jobs etc.

    - You can install [redis](https://redis.io/docs/install/install-redis/) locally on your computer 
    - Run redis docker [image](https://hub.docker.com/_/redis)

3. Start the Redis server on your machine. You can look at the [docs](https://redis.io/docs/) to find out how to do this via the command line.

4. Start the worker with the line : "python worker.py"

5. Start the flask server with the line : "python app.py"