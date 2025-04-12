```
  _   _  _____     ____  __ ____ _____ ____  
 | \ | |/ _ \ \   / /  \/  | __ )___ /|  _ \ 
 |  \| | | | \ \ / /| |\/| |  _ \ |_ \| |_) |
 | |\  | |_| |\ V / | |  | | |_) |__) |  _ < 
 |_| \_|\___/  \_/  |_|  |_|____/____/|_| \_\
```

# Novmber: Academic Ransomware - Information Security Research Project

This repository contains an academic ransomware developed for **research purposes** in the field of **Information Security**. The goal is to study **ransomware behavior**, encryption techniques, and countermeasures in a controlled and ethical environment. It is essential that this tool is used only in **isolated environments**, such as virtual machines (VMs), where its effects can be safely studied.

# ⚠️ Disclaimer

**Warning**: This project is **intended only for academic and educational purposes**. **Misuse** of this code may result in **legal action**. The authors and contributors **do not take any responsibility** for the misuse or illegal activities performed with this software. Always use it **responsibly** and **ethically**, and **only in isolated**, **authorized environments**.

# 📚 About the Project

The ransomware simulation is designed to replicate the behavior of real-world ransomware, including:

- File encryption using advanced cryptographic techniques

- Multithreading for efficient processing

- File renaming to indicate encryption

- Key transmission to a remote server for retrieval (in a simulated context)

This tool is meant to help researchers understand the lifecycle of ransomware attacks and test **defensive measures** in an isolated and safe environment.

# 🔧 How to Use

1. Clone the repository:

```bash
git clone https://github.com/limadaniel70/Novmber.git
cd Novmber
```

2. Install dependencies: Ensure that Python 3.12+ is installed, then install the required libraries:

```bash
pip install -r requirements.txt
```

3. Run the ransomware simulation:

- The application will encrypt files located in the specified target directory.

- It will send the encryption key to a server (for testing purposes).

- A warning text will be created, instructing the user about the encryption process.

Example:

```bash
python3 src/novmber.py
```

Make sure to test it in a **controlled environment** such as a virtual machine or isolated network.

# 🚨 Important Notes

- **Test in Virtual Machines (VMs)**: Always run the simulation in a VM or other isolated environment to avoid any unintentional consequences.

- **No real harm intended**: This project is meant solely for learning and research. It does not cause permanent damage to files or systems but simulates encryption behavior.

- **Ethical Use Only**: Never run this tool on unauthorized systems or data. It should only be used where you have explicit permission to conduct such testing.

# 📄 License

This repository is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.

# ⚖️ Ethical Considerations

This project is designed to promote **ethical research** and **responsible use of security tools**. Please respect the guidelines and use the tool **only in legal, controlled environments**.

# Additional Notes

- Key Management: Since this project involves cryptography, it's essential to properly handle encryption keys. Always ensure that keys are securely stored and never exposed without encryption.
- Data Integrity: Ensure that any encrypted files are properly backed up and the data integrity is preserved, especially in academic experiments.

# 🛑 Final Reminder

Do **not** deploy or run this code **on live environments, production systems**, or any system that you do not have explicit permission to test.

This project should only be used in controlled, isolated environments designed for **ethical hacking** and **cybersecurity research**.
