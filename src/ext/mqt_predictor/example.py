from mqt.predictor import qcompile
from mqt.bench import get_benchmark

# get a benchmark circuit on algorithmic level representing the GHZ state with 5 qubits from [MQT Bench](https://github.com/cda-tum/mqt-bench)
qc_uncompiled = get_benchmark(benchmark_name="ghz", level="alg", circuit_size=5)

# compile it using the MQT Predictor
qc_compiled, compilation_information, quantum_device = qcompile(
    qc_uncompiled, figure_of_merit="expected_fidelity"
)

# print the selected device and the compilation information
print(quantum_device, compilation_information)

# draw the compiled circuit
print(qc_compiled.draw())
