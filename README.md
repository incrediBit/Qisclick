# Qisclick
# Qisclick: Automated Qiskit Environment Setup  Qisclick automates Qiskit setup: creates a clean virtual env in the script's directory, installs latest Qiskit components, verifies installation, and launches an interactive Python session. Cross-platform and single-click ready!  --- *by incredibit*
Qisclick: Automated Qiskit Environment Setup

Qisclick is a powerful and user-friendly Python script designed to simplify and automate the setup of a dedicated Qiskit development environment on your local machine. It handles the entire process, from creating a clean virtual environment to installing the latest Qiskit components and verifying the installation, all with a single execution.
Features:

    Automated Environment Management: Qisclick intelligently detects and removes any pre-existing qisclick_env virtual environment in the script's directory, ensuring a fresh and clean installation every time.

    Clean Installation: Before installing new packages, the script attempts to clear the global pip cache. This crucial step helps prevent conflicts and ensures that no outdated Qiskit "residues" interfere with the new, latest installations.

    Latest Qiskit Versions: It automatically installs the most recent compatible versions of essential Qiskit components, including qiskit, qiskit-aer, qiskit-ibm-runtime, and qiskit-terra, ensuring you're always working with up-to-date libraries.

    Installation Verification: After all components are installed, Qisclick runs a simple, built-in Qiskit quantum circuit test. This test verifies that your Qiskit installation is fully functional and ready for use, providing immediate feedback.

    Interactive Session: Upon successful installation and verification, the script automatically launches an interactive Python interpreter. This allows you to immediately begin experimenting and coding with Qiskit within your newly configured environment.

    Cross-Platform Compatibility: The script is meticulously designed to function seamlessly across various operating systems, including Windows, macOS, and Linux, handling OS-specific commands and path conventions.

How to Use:

    Save the Script: Download or copy the qisclick.py script and save it to your desired project directory.

    Open Your Terminal: Navigate to the directory where you saved the qisclick.py script using your terminal or command prompt.

    cd /path/to/your/script/directory

    Run the Script: Execute the script using your Python interpreter:

    python qisclick.py

    Follow the Prompts: The script will provide detailed status updates as it progresses through each step of the environment setup.

    Start Coding: Once the installation and the verification test are complete, an interactive Python interpreter will launch. You can now start writing and running your Qiskit code directly!

    Exit Interpreter: To exit the interactive Python session, type exit() and press Enter.

Virtual Environment Location:

The qisclick_env virtual environment will be created as a subfolder within the same directory where you place and run the qisclick.py script.
Activating the Environment (Manual Activation):

If you close the interactive interpreter and wish to reactivate the qisclick_env virtual environment later, you can do so from your terminal. Make sure you are in the directory containing qisclick_env.

    For macOS / Linux:

    source ./qisclick_env/bin/activate

    For Windows (Command Prompt):

    .\qisclick_env\Scripts\activate.bat

    For Windows (PowerShell):

    .\qisclick_env\Scripts\Activate.ps1

Developed by incredibit
