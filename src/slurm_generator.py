#!/usr/bin/env python
import os
from sim_setup import SimulationSetup
from disc_setup import DiscSetup
from dustydisc_setup import DustyDiscSetup
from dustysgdisc_setup import DustySGDiscSetup

class SLURMScriptGenerator:
    def __init__(self, job_name, partition, ntasks, cpus_per_task, mem, time, output_file, email, mail_type, sim_type, setup_params):
        self.job_name = job_name
        self.partition = partition
        self.ntasks = ntasks
        self.cpus_per_task = cpus_per_task
        self.mem = mem
        self.time = time
        self.output_file = output_file
        self.email = email
        self.mail_type = mail_type
        self.sim_type = sim_type
        self.setup_params = setup_params
        self.user_home = os.getenv('HOME')  # Get the home directory from environment variables

    def generate_script(self, directory):
        setup_class = self.get_setup_class()
        setup = setup_class(self.setup_params)

        script_content = f"""#!/bin/bash

#SBATCH --job-name={self.job_name}		                        # Job name
#SBATCH --partition={self.partition}                            # Partition name (batch, highmem_p, or gpu_p)
#SBATCH --ntasks={self.ntasks}                                  # Number of tasks
#SBATCH --cpus-per-task={self.cpus_per_task}                    # CPU core count per task
#SBATCH --mem={self.mem}                                        # Memory per node
#SBATCH --time={self.time}                                      # Time limit
#SBATCH --output={self.output_file}_%j.out                      # Standard output log
#SBATCH --mail-user={self.email}                                # Where to send mail
#SBATCH --mail-type={self.mail_type}                            # Mail events (BEGIN, END, FAIL, ALL)

source ~/.bashrc                                # Ensures ~/.bashrc file is sourced
ml SPLASH/3.10.3-foss-2022a                     # Loads `splash` module

#===========================================
# STEPS FOR INITIATING PHANTOM SIMULATION |
#===========================================

cd {self.user_home}/runs/

# Create subdirectory for the simulation
NUMBERATM=$(find ./ -type f -name "{self.sim_type}_*" | wc -l)
NUMBERATM=$((NUMBERATM+1))
if [ $NUMBERATM -lt "10" ]; then
    var=0$NUMBERATM
else
    var=$NUMBERATM
fi
mkdir {self.sim_type}_$var
cd {self.sim_type}_$var

# Writing a local Makefile
~/phantom/scripts/writemake.sh {self.sim_type} > Makefile

# Compiling phantom and phantomsetup
make
make setup

# Running phantomsetup with automatic inputs
echo "1\n1\n0\nno\nno\n0\n0.100\n100" | ./phantomsetup {self.sim_type}

# Modify the .setup file
{setup.modify_setup_file(f'{self.sim_type}.setup')}

# Final phantomsetup command with maximum particles (maxp set to arbitrarily high val)
./phantomsetup {self.sim_type} --maxp=100000000

# Running phantom
./phantom {self.sim_type}.in
"""
        file_path = os.path.join(directory, f"{self.job_name}.sh")
        with open(file_path, 'w') as script_file:
            script_file.write(script_content)

        print(f"SLURM script {self.job_name}.sh generated successfully in {directory}.")

    def get_setup_class(self):
        if self.sim_type == 'disc':
            return DiscSetup
        elif self.sim_type == 'dustydisc':
            return DustyDiscSetup
        elif self.sim_type == 'dustysgdisc':
            return DustySGDiscSetup
        else:
            raise ValueError(f"Unknown simulation type: {self.sim_type}")


# Example usage: Main Workflow
if __name__ == "__main__":
    # User inputs
    directory = input("Enter the directory to save the SLURM script: ")
    job_name = input("Enter the job name: ")
    partition = input("Enter the partition (e.g., highmem_p): ")
    ntasks = input("Enter the number of tasks: ")
    cpus_per_task = input("Enter the number of CPUs per task: ")
    mem = input("Enter the memory required (e.g., 600G): ")
    time = input("Enter the time limit (e.g., 6-23:59:59): ")
    output_file = job_name
    email = input("Enter your email: ")
    mail_type = input("Enter mail type (incl. BEGIN,END,FAIL,ALL): ")
    sim_type = input("Enter the simulation type (e.g., disc, dustydisc, dustysgdisc): ")
    
    # Default parameters for .setup file
    default_setup_params = {
        "np": "1000000",
        "np_dust": "200000",
        "dist_unit": "au",
        "mass_unit": "solarm",
        "icentral": "1",
        "nsinks": "1",
        "m1": "1.000",
        "accr1": "1.000",
        "isetgas": "0",
        "itapergas": "F",
        "ismoothgas": "T",
        "iwarp": "F",
        "R_in": "1.000",
        "R_ref": "10.000",
        "R_out": "150.000",
        "disc_m": "0.050",
        "pindex": "1.000",
        "qindex": "0.250",
        "H_R": "0.050",
        "alphaSS": "0.005",
        "dust_method": "2",
        "dust_to_gas": "0.010",
        "ndusttypesinp": "1",
        "grainsizeinp": "1.000",
        "isetdust": "0",
        "discstrat": "0",
        "norbits": "100",
        "deltat": "0.100"
    }
    
    # Prompt for .setup file parameters with option to skip and use defaults
    setup_params = {}
    for param, default in default_setup_params.items():
        user_input = input(f"Enter value for {param} (default: {default}): ")
        setup_params[param] = user_input if user_input else default
    
    # Generate the SLURM script
    script_generator = SLURMScriptGenerator(job_name, partition, ntasks, cpus_per_task, mem, time, output_file, email, mail_type, sim_type, setup_params)
    script_generator.generate_script(directory)
