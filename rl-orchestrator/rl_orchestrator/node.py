import uuid
from subprocess import run, check_output

class Node:
    def __init__(self, image_name, cpu, ram):
        self.node_name = str(uuid.uuid4()) # what do we do here
        self.cpu = cpu
        self.ram = ram
        self.cost = (1 + cpu[0]) + 2*(ram[0] + 1)
        start_cmd = ["docker", "run", "--rm", "-d", "--name", self.node_name, "--net", "rl-test", "--network-alias", "apps", "--memory", f"{ram[1]}m", "--cpus", str(cpu[1]), "-p", "5000:5000", image_name]
        print(start_cmd)
        run(start_cmd)

    def query(self):
        query_cmd = ["docker", "stats", self.node_name, "--no-stream"]
        output = check_output(query_cmd).decode('utf-8') 
        data_vals = output.split("\n")[1].split()
        mem = float(data_vals[6].rstrip("%"))/100
        cpu = float(data_vals[2].rstrip("%"))/100/self.cpu[1]
        return (cpu, mem, self.cost)

    def destroy(self):
        destroy_cmd = ["docker", "stop", self.node_name]
        run(destroy_cmd)

