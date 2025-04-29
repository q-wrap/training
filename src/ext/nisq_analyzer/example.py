import json

import requests
from requests import Response

API_URL = "http://localhost:5010/nisq-analyzer"


def format_json(json_str: str) -> str:
    return json.dumps(json.loads(json_str), indent=4)


class GetRequests:
    @staticmethod
    def get_links() -> str:
        return requests.get(f"{API_URL}/").text

    @staticmethod
    def get_compilers(provider="ibmq") -> str:  # other providers: ionq, rigetti
        return requests.get(f"{API_URL}/compilers?provider={provider}").text

    @staticmethod
    def get_analysis_jobs() -> str:
        return requests.get(f"{API_URL}/analysis-results/jobs").text

    @staticmethod
    def get_compiler_analysis_results() -> str:
        return requests.get(f"{API_URL}/compiler-results/").text

    @staticmethod
    def get_compiler_analysis_jobs() -> str:
        return requests.get(f"{API_URL}/compiler-results/jobs").text

    @staticmethod
    def get_sdks() -> str:
        return requests.get(f"{API_URL}/sdks/").text

    @staticmethod
    def get_prioritization_methods() -> str:
        return requests.get(f"{API_URL}/mcda-methods/").text

    @staticmethod
    def get_execution_results(impl_id: str = "") -> str:
        return requests.get(f"{API_URL}/execution-results/").text

    @staticmethod
    def get_implementations(algo_id: str = "") -> str:
        return requests.get(f"{API_URL}/implementations/").text

    @staticmethod
    def get_qpu_selections_results(user_id: str = ""):
        return requests.get(f"{API_URL}/qpu-selection-results/").text

    @staticmethod
    def get_qpu_selections_jobs(user_id: str = ""):
        return requests.get(f"{API_URL}/qpu-selection-results/jobs").text

    @classmethod
    def print_all_requests(cls):
        print(f"/ => {format_json(cls.get_links())}")
        print(f"/compilers?provider=ibmq => {format_json(cls.get_compilers())}")
        print(f"/analysis-results/jobs => {format_json(cls.get_analysis_jobs())}")
        print(f"/compiler-results/ => {format_json(cls.get_compiler_analysis_results())}")
        print(f"/compiler-results/jobs => {format_json(cls.get_compiler_analysis_jobs())}")
        print(f"/sdks/ => {format_json(cls.get_sdks())}")
        print(f"/mcda-methods/ => {format_json(cls.get_prioritization_methods())}")
        print(f"/execution-results/ => {format_json(cls.get_execution_results())}")
        print(f"/implementations/ => {format_json(cls.get_implementations())}")
        print(f"/qpu-selection-results/ => {format_json(cls.get_qpu_selections_results())}")
        print(f"/qpu-selection-results/jobs => {format_json(cls.get_qpu_selections_jobs())}")


class SelectionMethods:
    @staticmethod
    # done by ProvideQ Toolbox
    def select_algorithm(): return NotImplementedError

    @staticmethod
    # done by ProvideQ Toolbox, possible via {API_URL}/selection
    def post_select_implementation_for_algorithm(): return NotImplementedError

    @staticmethod
    # done by ProvideQ Toolbox, possible via {API_URL}/compiler-selection
    def post_select_compiler_for_implementation(): return NotImplementedError

    @staticmethod
    # done by ProvideQ Toolbox
    def compile_circuit(): return NotImplementedError

    @staticmethod
    # done by wrapper
    def post_select_qpu_for_circuit() -> Response:
        body = {
            "allowedProviders": [
                "ibmq", "ionq", "rigetti"
            ],
            "circuitLanguage": "qiskit",
            "circuitUrl": "https://raw.githubusercontent.com/UST-QuAntiL/nisq-analyzer-content/refs/heads/master/"
                          "example-implementations/Grover-SAT/grover-fix-sat-qiskit.py",
            # "qasmCode": """
            #             OPENQASM 3.0;
            #             qubit[2] q;
            #             h q[0];
            #             cx q[0], q[1];
            #             bit[2] c;
            #             measure q[0] -> c[0];
            #             measure q[1] -> c[1];
            #             """,
            # "tokens": {},
            # "refreshToken": "",
            "circuitName": "bell",
            "preciseResultsPreference": False,
            "shortWaitingTimesPreference": True,
            # "queueImportanceRatio": 0,
            "maxNumberOfCompiledCircuits": 3,
            # "predictionAlgorithm": "",
            # "metaOptimizer": "",
            "userId": "1",
            # "compilers": [
            #     ""
            # ]
        }

        return requests.post(f"{API_URL}/qpu-selection", json=body)


if __name__ == '__main__':
    # GetRequests.print_all_requests()

    response = SelectionMethods.post_select_qpu_for_circuit()
    print(response, response.text)
    if response.status_code == 200:
        print(format_json(response.text))
