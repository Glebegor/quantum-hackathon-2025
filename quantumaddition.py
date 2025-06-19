import time
from qiskit import ClassicalRegister, QuantumRegister, QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Determine the maximum input length
# Určení maximální délky vstupu
start = time.time()
firstBinaryNumber = "1011"
secondBinaryNumber = "1011"
maxInputLength = max(len(firstBinaryNumber), len(secondBinaryNumber))

'''
Initializing registers:
- Two quantum registers (regA, regB) for input numbers
- One quantum register (regC) for carry bits
- One classical register (regD) to store the final sum

Inicializace registrů:
- Dva kvantové registry (regA, regB) pro vstupní čísla
- Jeden kvantový registr (regC) pro přenosové bity
- Jeden klasický registr (regD) pro konečný součet
'''

# Quantum registers for input and calculations
# Kvantové registry pro vstup a výpočty
regA = QuantumRegister(maxInputLength, "regA")        # First number / První číslo
regB = QuantumRegister(maxInputLength + 1, "regB")    # Second number & sum / Druhé číslo a součet
regC = QuantumRegister(maxInputLength, "regC")        # Carry bits / Přenosové bity

# Classical register for measurement
# Klasický registr pro měření
regD = ClassicalRegister(maxInputLength + 1, "regD")  # Final output / Konečný výstup

# Create the quantum circuit
# Vytvoření kvantového obvodu
qc = QuantumCircuit(regA, regB, regC, regD)

# Setting up the quantum registers to store input values
# Nastavení kvantových registrů pro uložení vstupních hodnot
for idx, val in enumerate(firstBinaryNumber):
    if val == "1":
        qc.x(regA[len(firstBinaryNumber) - (idx + 1)])  # Apply X gate / Aplikace X brány

for idx, val in enumerate(secondBinaryNumber):
    if val == "1":
        qc.x(regB[len(secondBinaryNumber) - (idx + 1)])  # Apply X gate / Aplikace X brány

# Implementing carry gate logic for addition
# Implementace přenosové brány pro sčítání
for i in range(maxInputLength - 1):
    qc.ccx(regA[i], regB[i], regC[i + 1])  # Compute carry / Výpočet přenosu
    qc.cx(regA[i], regB[i])  # Partial sum / Částečný součet
    qc.ccx(regC[i], regB[i], regC[i + 1])  # Update carry / Aktualizace přenosu

# Final carry computation using regB[maxInputLength] instead of regC[maxInputLength]
# Konečný výpočet přenosu pomocí regB[maxInputLength] místo regC[maxInputLength]
qc.ccx(regA[maxInputLength - 1], regB[maxInputLength - 1], regB[maxInputLength])
qc.cx(regA[maxInputLength - 1], regB[maxInputLength - 1])
qc.ccx(regC[maxInputLength - 1], regB[maxInputLength - 1], regB[maxInputLength])

# Undo last carry operation to reset the state
# Vrácení poslední přenosové operace pro reset stavu
qc.cx(regC[maxInputLength - 1], regB[maxInputLength - 1])

# Reverse the carry operations to reset all carry bits to |0>
# Reverzní operace přenosu pro reset všech přenosových bitů na |0>
for i in range(maxInputLength - 1):
    qc.ccx(regC[(maxInputLength - 2) - i], regB[(maxInputLength - 2) - i], regC[(maxInputLength - 1) - i])
    qc.cx(regA[(maxInputLength - 2) - i], regB[(maxInputLength - 2) - i])
    qc.ccx(regA[(maxInputLength - 2) - i], regB[(maxInputLength - 2) - i], regC[(maxInputLength - 1) - i])

    # These operations act as a sum gate: flips regB if control is |1>
    # Tyto operace fungují jako součtová brána: přepínají regB, pokud je řídicí bit |1>
    qc.cx(regC[(maxInputLength - 2) - i], regB[(maxInputLength - 2) - i])
    qc.cx(regA[(maxInputLength - 2) - i], regB[(maxInputLength - 2) - i])

# Measure qubits and store results in the classical register
# Měření qubitů a uložení výsledků do klasického registru
for i in range(maxInputLength + 1):
    qc.measure(regB[i], regD[i])

# Transpile circuit for simulation
# Překlad obvodu pro simulaci
simulator = AerSimulator()
circ = transpile(qc, simulator)

# Run the circuit and retrieve results
# Spuštění obvodu a získání výsledků
result = simulator.run(circ).result()
counts = result.get_counts(circ)

print(*counts)
end = time.time() - start
print(end)
# Plot histogram of measurement results
# Vykreslení histogramu měření
#plot_histogram(counts, title='Quantum Addition')

# Draw the quantum circuit
# Vykreslení kvantového obvodu
qc.draw("mpl")

# Counts is a dictionary where keys represent measurement results (binary strings)
# Counts je slovník, kde klíče představují výsledky měření (binární řetězce)

# Extract the keys (measurement outcomes), using the extrating operator and print the first one
# Extrahuje klíče (výstupy měření), pomocí extračního operátoru a vypíše první výsledek
