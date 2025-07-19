# Training for q-wrap

This repository contains the code for training the machine learning models of the
[MQT Predictor](https://github.com/munich-quantum-toolkit/predictor) which is necessary to use the q-wrap API.
See the [q-wrap repository](https://github.com/q-wrap/q-wrap) for more information.

## Environment

The training environment used by the MQT Predictor is quite selective regarding the hardware environment. Our
observations indicate that it is incompatible with NVIDIA GPUs, resulting in error messages related to NVIDIA CUDA.
However, the training works well on an Apple Silicon MacBook.

You also have to adapt the MQT Predictor slightly which is described in the section
[Adaptions of the MQT Predictor](#adaptions-of-the-mqt-predictor) below.

## Installation

Install Python 3.12 on your system. You can download it from the
[official Python website](https://www.python.org/downloads/release/python-31210/).

Clone this repository, where `<path>` is the URL of this repository and `--depth 1` is optional:

```bash
git clone --depth 1 <path>
```

Before you install the required packages, you should create and activate a virtual environment. However, this is
optional, and you are free to use another package manager like `uv` as well.

```bash
python -m venv venv  # Python 3.12

# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

Install the required packages:

```bash
pip install -r requirements.txt
```

If you want to get an overview of the packages used by this application, see the `requirements_direct.txt` file,
instead, which only contains directly installed or imported packages without their dependencies.

## Adaptions of the MQT Predictor

After installing the required packages, the MQT Predictor must be slightly adapted. Specifically, you need to 
deactivate the compilation passes by the Berkeley Quantum Synthesis Toolkit (BQSKit) which can be achieved by
commenting out the following blocks of code in the file `mqt/predictor/rl/helper.py`:

```Python
...
def get_actions_opt() -> list[dict[str, Any]]:
    ...
    return [
        ...,
        # {
        #     "name": "BQSKitO2",
        #     "transpile_pass": ...,
        #     "origin": "bqskit",
        # },
    ]
...
def get_actions_mapping() -> list[dict[str, Any]]:
    ...
    return [
        ...,
        # {
        #     "name": "BQSKitMapping",
        #     "transpile_pass": ...,
        #     "origin": "bqskit",
        # },
    ]
...
def get_actions_synthesis() -> list[dict[str, Any]]:
    ...
    return [
        ...,
        # {
        #     "name": "BQSKitSynthesis",
        #     "transpile_pass": ...,
        #     "origin": "bqskit",
        # },
    ]   
...
```

## Usage

Make sure that your virtual environment is activated if you created one. The training can then be started by
executing the script at `src/train.py`. This may take about one day, depending on your hardware and the number of
iterations and quantum computers you want to train on. The training for the OQC Lucy and the IQM Adonis quantum
computer is deactivated by default since it failed in our setup.

## Documentation

The file `docs/train_simple.py` contains a simplified version of the training code which might help in understanding
the process. The training code in `src/train.py` mainly adds logging and the ability to skip the training for 
already trained quantum computers.
