import mqt.predictor

rl_pred = mqt.predictor.rl.Predictor(
    figure_of_merit="expected_fidelity", device_name="ibm_washington"
)
rl_pred.train_model(timesteps=100000, model_name="sample_model_rl")

ml_pred = mqt.predictor.ml.Predictor(figure_of_merit="expected_fidelity")
ml_pred.generate_compiled_circuits(timeout=600)  # timeout in seconds
training_data, name_list, scores_list = ml_pred.generate_trainingdata_from_qasm_files()
ml_pred.save_training_data(
    training_data,
    name_list,
    scores_list,
)

ml_pred.train_random_forest_model()
