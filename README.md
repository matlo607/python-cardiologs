# Holter Record Summary

A normal heart beat produces three entities on the ECG — a P wave, a QRS complex, a T wave.
See [\[Wikipedia\] Electrocardiography](https://en.wikipedia.org/wiki/Electrocardiography#Theory) for more details.

Identifying those entities in a signal is called delineation. Here are CSV of an algorithm output for a 24h ECG: [record.csv](https://cardiologs-public.s3.amazonaws.com/python-interview/record.csv)

Rows have the following fields:
- Wave type: P, QRS, T or INV (invalid)
- Wave onset: Start of the wave in ms
- Wave offset: End of the wave in ms
- Optionally, a list of wave tags


Using Python 3, write a simple console program that provides the following measurements to a physician:
- The number of P waves tagged "premature", as well as the number of QRS complexes tagged "premature"
- The mean heart rate of the recording (Frequency at which QRS complexes appear).
- The minimum and maximum heart rate, each with the time at which they happened. As the date and the time of the recording are not included in the file, the user of the program should be able to set them.

Cardiologs should be able to easily recover your work, understand it, trust it, maintain it, make changes to it, etc.

_Bonus question: We want to efficiently host delineations online, and be able to quickly download a range of it (e.g. the record between 2 and 3pm on the third day). How would you achieve that ?_

## Test it !

### Run analyse.py in a container

A Dockerfile is provided with a python3 environment.
Run this docker directly will execute analyse.py on record.csv (`pipenv run ./analyse.py -f record.csv`)
```
docker build . -t cardiologs:latest
docker run -it cardiologs:latest
```

Run analyse.py on record.csv and display graphs.
```
xhost +local:root
docker run -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix -it cardiologs:latest \
           pipenv run ./analyse.py -f record.csv --plot-graph
```

Run unit tests.
```
docker run -it cardiologs:latest pipenv run ./test.py
```

### Coverage
```
pipenv shell
coverage run ./test.py
coverage report
```
