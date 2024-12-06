import simpy
import pandas as pd
import math
import random

# Simulation Parameters
LATENCY_LEVELS = [0, 10, 50, 100, 150, 200]
NUM_LAPTOPS = 3
RESULTS = []

def calculate_throughput(latency, packet_loss):
    """Realistic throughput formula considering latency and packet loss. At zero latency and packet loss, throughput should equal maximum bandwidth."""
    bandwidth = 100  # Max bandwidth in Mbps
    rtt_min = 10  # Minimum RTT in ms for the network
    # Convert packet loss from percentage to a part
    loss_rate = packet_loss / 100
    # Avoid division by zero
    if latency == 0:
        return bandwidth * (1 - loss_rate)
    # Calculate throughput dynamically for non-zero latency
    throughput = bandwidth * (1 - loss_rate) * (1 / (1 + (latency / rtt_min)))
    # Ensure throughput not fall below 1 Mbps
    return max(1, throughput)

def calculate_packet_loss(latency):
    """realistic packet loss. Packet loss grows non-linearly with latency to simulate real-world congestion effects."""
    a = 20  # Scaling factor
    b = 0.02  # Growth rate
    base_loss = a * (1 - math.exp(-b * latency))
    # Add random variability to simulate real-world
    variability = random.uniform(-1, 1)  # Random noise between -1% and +1%
    return max(0, base_loss + variability)  # Ensure no negative packet loss

def calculate_response_time(latency, packet_loss):
    """Realistic response time formula considering RTT, processing delay, queueing delay, and retransmissions."""
    # RTT: Round-trip time
    rtt = 2 * latency  # Latency affects both forward and return trips 
    # Processing Delay
    processing_delay = 1  #constant 1 ms processing delay
    # Queueing Delay (increases with packet loss)
    base_queueing_delay = 2  # Base queueing delay in ms
    queueing_delay = base_queueing_delay * (1 + packet_loss / 100)
    # Retransmission Delay (optional, based on loss rate)
    retransmission_delay = rtt * (packet_loss / 100)
    # Total Response Time
    return rtt + processing_delay + queueing_delay + retransmission_delay

def laptop_process(env, laptop_id, switch, latency):
    """Simulates a laptop sending data through a switch to a router. Each laptop introduces a latency level to the network."""
    yield env.timeout(10)  # Simulate sending data every 10 ms
    yield env.process(switch.forward(env, laptop_id, latency))

class Switch:
    """Simulates a network switch that forwards packets to a router."""
    def __init__(self, env, router):
        self.env = env
        self.router = router

    def forward(self, env, laptop_id, latency):
        switch_latency = latency / 2  # Switch contributes half the latency
        yield env.timeout(switch_latency)
        yield env.process(self.router.forward(env, laptop_id, latency))

class Router:
    """Simulates a router forwarding packets to the destination. Calculates throughput, packet loss, and response time."""
    def __init__(self, env):
        self.env = env

    def forward(self, env, laptop_id, latency):
        router_latency = latency / 2  # Router contributes half the latency
        yield env.timeout(router_latency)
        
        # Calculate metrics
        packet_loss = calculate_packet_loss(latency)
        throughput = calculate_throughput(latency, packet_loss)
        response_time = calculate_response_time(latency, packet_loss)  # Realistic response time
        
        # Log results
        RESULTS.append({
            'Laptop ID': laptop_id,
            'Latency (ms)': latency,
            'Response Time (ms)': response_time,
            'Throughput (Mbps)': throughput,
            'Packet Loss (%)': packet_loss
        })

def run_simulation(env):
    """Simulates network traffic for multiple laptops at different latency levels."""
    router = Router(env)
    switch = Switch(env, router)
    
    for latency in LATENCY_LEVELS:
        for laptop_id in range(NUM_LAPTOPS):
            env.process(laptop_process(env, laptop_id, switch, latency))
            yield env.timeout(1)  # Small delay between processes

# Initialize the simulation environment
env = simpy.Environment()
env.process(run_simulation(env))
env.run()

# Convert results to a DataFrame and calculate averages per latency level
results_df = pd.DataFrame(RESULTS)
average_results_df = results_df.groupby(['Latency (ms)']).mean().reset_index()

# Display the results
print(average_results_df)
