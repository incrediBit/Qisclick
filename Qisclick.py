 import os
import subprocess
import sys
import platform
import shutil # For cross-platform directory removal and finding executables

# Define the virtual environment directory
# Changed venv_dir to be relative to the script's location
script_dir = os.path.dirname(os.path.abspath(__file__))
venv_dir = os.path.join(script_dir, 'qisclick_env')

def run_command(command, cwd=None, shell=False, check=True, capture_output=True):
    """
    Helper function to run shell commands and handle errors.
    Args:
        command (list or str): The command to execute.
        cwd (str, optional): The current working directory. Defaults to None.
        shell (bool, optional): If True, the command will be executed through the shell. Defaults to False.
        check (bool, optional): If True, raise a CalledProcessError if the command returns a non-zero exit code. Defaults to True.
        capture_output (bool, optional): If True, stdout and stderr are captured. Defaults to True.
    Returns:
        bool: True if the command succeeded, False otherwise.
    """
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            shell=shell,
            check=check,
            stdout=subprocess.PIPE if capture_output else None,
            stderr=subprocess.PIPE if capture_output else None,
            text=True # Decode stdout/stderr as text
        )
        if capture_output:
            if result.stdout:
                print(result.stdout.strip())
            if result.stderr:
                print(result.stderr.strip())
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {' '.join(command) if isinstance(command, list) else command}")
        if e.stdout:
            print(f"Stdout: {e.stdout.strip()}")
        if e.stderr:
            print(f"Stderr: {e.stderr.strip()}")
        print(f"Error details: {e}")
        return False
    except FileNotFoundError:
        print(f"Command not found. Please ensure necessary executables (like python, pip) are in your PATH.")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

def main():
    """
    Main function for Qisclick to set up the Qiskit virtual environment.
    It handles removal of old environments, clearing pip cache,
    creating a new environment, installing latest Qiskit components,
    running a verification test, and finally launching an interactive Python interpreter.
    """
    # Branding display
    print("\n" + "="*50)
    print("        Qisclick".center(50))
    print("        by incredibit".center(50))
    print("="*50 + "\n")

    # Step 1: Remove any existing virtual environment at the target path
    if os.path.exists(venv_dir):
        print(f"Removing existing virtual environment at {venv_dir}...")
        try:
            # shutil.rmtree is a cross-platform way to remove directories
            shutil.rmtree(venv_dir)
            print("Old virtual environment removed successfully.")
        except OSError as e:
            print(f"Error removing old virtual environment: {e}")
            sys.exit(1)
    else:
        print(f"No existing virtual environment found at {venv_dir}, skipping removal.")

    # Step 2: Uninstall any Qiskit residues from global pip cache
    print("Attempting to clear pip cache for Qiskit residues...")
    # Find the system's pip executable
    system_pip = shutil.which('pip')
    if system_pip:
        # Use check=False because purge might fail if no cache exists, which is fine.
        # We also want to see the output, so not capturing output here.
        if not run_command([system_pip, 'cache', 'purge'], check=False, capture_output=False):
            print("Warning: Could not purge pip cache. This might be normal if no cache exists.")
        else:
            print("Pip cache purged successfully (or no cache to purge).")
    else:
        print("Warning: 'pip' command not found in system PATH. Cannot purge cache.")

    # Step 3: Create a new virtual environment
    print(f"Creating a new virtual environment named '{os.path.basename(venv_dir)}' at '{os.path.dirname(venv_dir)}'...")
    # sys.executable ensures we use the Python interpreter that's running the script
    if not run_command([sys.executable, '-m', 'venv', venv_dir]):
        print("Failed to create virtual environment. Exiting.")
        sys.exit(1)
    print("New virtual environment created successfully.")

    # Determine the path to pip and python within the new virtual environment
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_dir, 'Scripts', 'pip.exe')
        python_path = os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:
        pip_path = os.path.join(venv_dir, 'bin', 'pip')
        python_path = os.path.join(venv_dir, 'bin', 'python')

    # Step 4: Upgrade pip in the new virtual environment
    print("Upgrading pip in the new virtual environment...")
    if not run_command([pip_path, 'install', '--upgrade', 'pip']):
        print("Failed to upgrade pip. Exiting.")
        sys.exit(1)
    print("Pip upgraded successfully.")

    # Step 5: Install Qiskit and its compatible components (latest versions)
    print("Installing Qiskit and its components (latest compatible versions)...")
    # Removed version pins to install latest compatible versions as requested
    packages_to_install = [
        'qiskit',
        'qiskit-aer',
        'qiskit-ibm-runtime',
        'qiskit-terra'
    ]

    for package in packages_to_install:
        print(f"Installing {package}...")
        # Use a list for command arguments
        if not run_command([pip_path, 'install', package]):
            print(f"Error installing {package}. Please check your internet connection. Exiting.")
            sys.exit(1)
        print(f"{package} installed.")

    print("\nAll specified Qiskit components installed successfully!")

    # Step 6: Run a simple Qiskit test program
    print("\nRunning a simple Qiskit test to verify installation...")
    qiskit_test_script = """
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import sys

try:
    # Create a quantum circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)

    # Add a Hadamard gate to qubit 0, putting it in superposition
    qc.h(0)

    # Add a CNOT gate with qubit 0 as control and qubit 1 as target
    qc.cx(0, 1)

    # Measure both qubits and map them to classical bits
    qc.measure([0, 1], [0, 1])

    # Use the AerSimulator
    simulator = AerSimulator()

    # Transpile the circuit for the simulator
    compiled_circuit = transpile(qc, simulator)

    # Run the circuit on the simulator and get results
    job = simulator.run(compiled_circuit, shots=1024)
    result = job.result()
    counts = result.get_counts(qc)

    print("\\nQiskit test successful! Results:")
    print(f"Measurement counts: {counts}")
    print("Your Qiskit installation is working correctly.")

except ImportError as e:
    print(f"Qiskit test failed: Missing module. {e}")
    print("Please ensure all Qiskit components were installed correctly.")
    sys.exit(1)
except Exception as e:
    print(f"An unexpected error occurred during Qiskit test: {e}")
    sys.exit(1)
"""
    # Execute the Qiskit test script using the virtual environment's python
    # We pass the script as a string to the python interpreter's -c flag
    # We want to see the output of the test directly, so we don't capture output in run_command.
    if not run_command([python_path, '-c', qiskit_test_script], capture_output=False):
        print("Qiskit test failed. Please review the output above for errors.")
        sys.exit(1)
    else:
        print("\nQiskit test completed successfully!")


    print("\nInstallation and test complete! Your 'qisclick' virtual environment is ready.")
    print("Launching an interactive Python interpreter within 'qisclick' environment...")
    print("Type 'exit()' and press Enter to quit the interpreter.")

    # Step 7: Open an interactive Python interpreter
    try:
        # Use subprocess.run with no arguments for python_path to launch interactive interpreter
        # stdin, stdout, stderr are redirected to the parent process's streams
        subprocess.run(python_path, stdin=sys.stdin, stdout=sys.stdout, stderr=sys.stderr)
    except Exception as e:
        print(f"Error launching interactive Python interpreter: {e}")
        sys.exit(1)

    print("\nExited 'qisclick' interactive Python interpreter.")
    print("You can activate it again anytime by running:")
    if platform.system() == "Windows":
        print(f"{os.path.join(venv_dir, 'Scripts', 'activate.bat')}")
    else:
        print(f"source {os.path.join(venv_dir, 'bin', 'activate')}")

if __name__ == "__main__":
    main()

