import logging

import mqt.bench
import mqt.predictor

devices = ["ibm_washington", "ibm_montreal"]  # limit devices only for testing


def train_rl_model():
    for device in devices:
        rl_pred = mqt.predictor.rl.Predictor(
            figure_of_merit="expected_fidelity", device_name=device, logger_level=logging.DEBUG
        )  # show debug logs only for testing
        rl_pred.train_model(timesteps=2048)
        # timesteps=2048 only for testing


def train_ml_model():
    ml_pred = mqt.predictor.ml.Predictor(
        figure_of_merit="expected_fidelity", devices=devices, logger_level=logging.DEBUG
    )  # show debug logs only for testing
    ml_pred.generate_compiled_circuits(timeout=600)  # timeout in seconds
    training_data, name_list, scores_list = ml_pred.generate_trainingdata_from_qasm_files()
    ml_pred.save_training_data(
        training_data,
        name_list,
        scores_list,
    )
    ml_pred.train_random_forest_classifier()


if __name__ == '__main__':
    train_rl_model()
    train_ml_model()
