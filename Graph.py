import matplotlib.pyplot as plt
import pandas as pd

# Data from your simulation results
data = {
    "Latency (ms)": [0, 10, 50, 100, 150, 200],
    "Response Time (ms)": [3, 24, 115, 237, 360, 480],
    "Throughput (Mbps)": [100, 48, 15, 8, 5, 4],
    "Packet Loss (%)": [0, 4, 12, 17, 19, 20]
}

# Create DataFrame
df = pd.DataFrame(data)

# Use a non-GUI backend to avoid Tcl/Tk issues
import matplotlib
matplotlib.use('Agg')  # Use a backend that does not require a display environment

# Plot 1: Response Time vs. Latency
plt.figure(figsize=(8, 6))
plt.plot(df["Latency (ms)"], df["Response Time (ms)"], marker='o', label="Response Time (ms)")
plt.title("Response Time vs. Latency")
plt.xlabel("Latency (ms)")
plt.ylabel("Response Time (ms)")
plt.grid(True)
plt.legend()
plt.savefig("Response_Time_vs_Latency.png")

# Plot 2: Throughput vs. Latency
plt.figure(figsize=(8, 6))
plt.plot(df["Latency (ms)"], df["Throughput (Mbps)"], marker='o', color='orange', label="Throughput (Mbps)")
plt.title("Throughput vs. Latency")
plt.xlabel("Latency (ms)")
plt.ylabel("Throughput (Mbps)")
plt.grid(True)
plt.legend()
plt.savefig("Throughput_vs_Latency.png")

# Plot 3: Packet Loss vs. Latency
plt.figure(figsize=(8, 6))
plt.plot(df["Latency (ms)"], df["Packet Loss (%)"], marker='o', color='red', label="Packet Loss (%)")
plt.title("Packet Loss vs. Latency")
plt.xlabel("Latency (ms)")
plt.ylabel("Packet Loss (%)")
plt.grid(True)
plt.legend()
plt.savefig("Packet_Loss_vs_Latency.png")
