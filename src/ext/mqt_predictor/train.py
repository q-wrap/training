from datetime import datetime

import mqt.bench
import mqt.predictor

devices = mqt.bench.devices.get_available_device_names()[:4]  # limit devices only for testing


def train_rl_model():
    print("--- (step 1/3) training reinforcement learning model ---")
    print_timestamp()

    for index, device in enumerate(devices):
        print(f"--- (device {index + 1}/{len(devices)}) training {device} ---")
        print_timestamp()

        rl_pred = mqt.predictor.rl.Predictor(figure_of_merit="expected_fidelity", device_name=device)
        rl_pred.train_model(timesteps=5 * 2048)  # timesteps=100_000 for full training


def train_ml_model():
    print("--- (step 2/3) generating training data for supervised machine learning ---")
    print_timestamp()

    ml_pred = mqt.predictor.ml.Predictor(figure_of_merit="expected_fidelity", devices=devices)
    ml_pred.generate_compiled_circuits(timeout=600)  # timeout in seconds
    training_data, name_list, scores_list = ml_pred.generate_trainingdata_from_qasm_files()
    ml_pred.save_training_data(
        training_data,
        name_list,
        scores_list,
    )

    print("--- (step 3/3) training supervised machine learning model ---")
    print_timestamp()

    ml_pred.train_random_forest_classifier()


def print_timestamp():
    print(f"--- time now: {datetime.now().ctime()} / time elapsed: {str(datetime.now() - start_time)} ---")


if __name__ == '__main__':
    start_time = datetime.now()
    print("--- training started ---")
    print_timestamp()

    train_rl_model()
    train_ml_model()

    print("--- training ended ---")
    print_timestamp()
