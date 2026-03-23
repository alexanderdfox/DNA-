import os
import time
import random
import signal

class DNATeslaValve:
	bases = ['A', 'T', 'C', 'G']
	complement = {'A': 'T', 'T': 'A', 'C': 'G', 'G': 'C'}

	def __init__(self, sequence=None):
		if sequence:
			self.sequence = sequence
		else:
			self.sequence = [random.choice(self.bases) for _ in range(6)]
		self.forward_resistance_map = {'A': 1, 'T': 2, 'C': 3, 'G': 4}
		self.backward_resistance_map = {'A': 4, 'T': 3, 'C': 2, 'G': 1}

	def flow(self, input_flow, index, direction):
		base = self.sequence[index % len(self.sequence)]
		if direction == 'left':
			resistance = self.forward_resistance_map[base]
		elif direction == 'right':
			resistance = self.backward_resistance_map[base]
		else:
			raise ValueError("Direction must be 'left' or 'right'")
		effective_flow = input_flow / resistance
		return effective_flow, base

	def replicate_sequence(self):
		self.sequence = [self.complement[b] for b in self.sequence]

def simulate_node(valve, input_flow, index, timestep):
	left_flow, base_left = valve.flow(input_flow, index, 'left')
	right_flow, base_right = valve.flow(input_flow, index, 'right')

	left_bar = "=" * min(int(left_flow), 50)
	right_bar = "=" * min(int(right_flow), 50)

	print(f"[PID {os.getpid()}] Time {timestep+1} | Base: {base_left}/{base_right}")
	print(f"  Left  [{left_bar}] {left_flow:.2f}")
	print(f"  Right [{right_bar}] {right_flow:.2f}")
	time.sleep(0.5)

def main():
	input_flow = 100
	valve = DNATeslaValve()
	timestep = 0

	print("Forked DNA Tesla Valve with Left/Right Flow (Looping Forever)\n")

	while True:
		child_pids = []

		# Fork a process for each base/node
		for i in range(len(valve.sequence)):
			pid = os.fork()
			if pid == 0:
				simulate_node(valve, input_flow, i, timestep)
				os._exit(0)
			else:
				child_pids.append(pid)

		# Parent waits for all children
		for pid in child_pids:
			os.waitpid(pid, 0)

		timestep += 1

		# Replicate sequence every full cycle
		if timestep % len(valve.sequence) == 0:
			valve.replicate_sequence()
			print("\nSequence replicated!\n")

if __name__ == "__main__":
	main()
