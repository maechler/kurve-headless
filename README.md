# Kurve headless

This is an experimental project with the goal to introduce AI bots to [achtungkurve.com](https://achtungkurve.com).

## Installation

### Prerequisites

You need to have the Headless Chrome binaries installed on your system.

### Setup virtualenv

```
pip install virtualenv
python -m virtualenv env
source env/bin/activate
```

### Install requirements

```
pip install -r requirements.txt
```

## Run demo

```
python demo.py --binary_location="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
```
