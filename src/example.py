MQT_PREDICTOR_LOCATION = r"..\..\training_env\mqt-predictor\src"

import sys

sys.path.insert(0, MQT_PREDICTOR_LOCATION)
import mqt.predictor
import mqt.bench
import qiskit.qasm3

QASM_2_HADAMARD = """
OPENQASM 2.0;
include "qelib1.inc";

// Declare a quantum register with 1 qubit
qreg q[1];

// Declare a classical register with 1 bit
creg c[1];

// Apply a Hadamard gate to the qubit
h q[0];

// Measure the qubit and store the result in the classical bit
measure q[0] -> c[0];
"""
QASM_2_BELL = """
OPENQASM 2.0;
include "qelib1.inc";

// Declare quantum and classical registers
qreg q[2];
creg c[2];

// Create superposition on q[0]
h q[0];

// Entangle q[0] and q[1]
cx q[0], q[1];

// Measure both qubits
measure q[0] -> c[0];
measure q[1] -> c[1];
"""

QASM_3_HADAMARD = """
OPENQASM 3.0;
include "stdgates.inc";

// Declare a quantum bit and a classical bit
qubit q;
bit c;

// Apply a Hadamard gate to the qubit
h q;

// Measure the qubit and store the result in the classical bit
c = measure q;
"""
QASM_3_BELL = """
OPENQASM 3.0;
include "stdgates.inc";

qubit q0;
qubit q1;
bit c0;
bit c1;

// Create superposition on q0
h q0;

// Entangle q0 and q1
cx q0, q1;

// Measure both qubits
c0 = measure q0;
c1 = measure q1;
"""
QASM_3_ARRAYS = """
OPENQASM 3.0;

array[int[8], 16] my_ints;
array[float[64], 8, 4] my_doubles;
array[uint[32], 4] my_defined_uints = {5, 6, 7, 8};
array[float[32], 4, 2] my_defined_floats = {
    {0.5, 0.5},
    {1.0, 2.0},
    {-0.4, 0.7},
    {1.3, -2.1e-2}
};
array[float[32], 2] my_defined_float_row = my_defined_floats[0];
const uint[8] DIM_SIZE = 2;
array[int[8], DIM_SIZE, DIM_SIZE] all_ones = {{2+3, 4-1}, {3+8, 12-4}};
uint[8] a = my_defined_uints[0];
float[32] b = my_defined_floats[2, 1];
my_defined_uints[1] = 5;
my_defined_floats[3, 0] = -0.45;
my_defined_uints[a - 1] = a + 1;
my_defined_floats[2] = my_defined_float_row;
my_defined_floats[0:1] = my_defined_floats[2:3];
const uint[32] first_dimension = sizeof(my_doubles, 0);
const uint[32] second_dimension = sizeof(my_doubles, 1);
const uint[32] first_dimension = sizeof(my_doubles);

def copy_3_bytes(readonly array[uint[8], 3] in_array, mutable array[uint[8], 3] out_array) {
}

def multi_dimensional_input(readonly array[int[32], #dim=3] my_array) {
    uint[32] dimension_0 = sizeof(my_array, 0);
    uint[32] dimension_1 = sizeof(my_array, 1);
    uint[32] dimension_2 = sizeof(my_array, 2);
}
"""

# get a benchmark circuit on algorithmic level representing the GHZ state with 5 qubits from [MQT Bench](https://github.com/cda-tum/mqt-bench)
# qc_uncompiled = mqt.bench.get_benchmark(benchmark_name="ghz", level="alg", circuit_size=5)

# DESIRED INPUT:
qc_uncompiled = qiskit.qasm2.loads(QASM_2_HADAMARD)
# qc_uncompiled = qiskit.qasm2.loads(QASM_2_BELL)
# qc_uncompiled = qiskit.qasm3.loads(QASM_3_HADAMARD)
# qc_uncompiled = qiskit.qasm3.loads(QASM_3_BELL)
# qc_uncompiled = qiskit.qasm3.loads(QASM_3_ARRAYS)

# compile it using the MQT Predictor
qc_compiled, compilation_information, quantum_device = mqt.predictor.qcompile(
    qc_uncompiled, figure_of_merit="expected_fidelity"
)

# print the selected device and the compilation information
print(quantum_device, compilation_information)

# DESIRED OUTPUT:
print(quantum_device.name)

# draw the compiled circuit
# print(qc_compiled.draw())
