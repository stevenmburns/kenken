# kenken
[![CircleCI](https://circleci.com/gh/stevenmburns/kenken.svg?style=svg)](https://circleci.com/gh/stevenmburns/kenken)

KenKen solver using SAT

Requires the "tally" Python package from "ALIGN-analoglayout/ALIGN-public/Pysat

Or use docker (to build and run the unit tests):
```bash
docker build -t kenken_image .
docker run kenken_image bash -c "source general/bin/activate && cd kenken && python setup.py test"
```
