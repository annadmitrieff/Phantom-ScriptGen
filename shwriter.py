import os

# Function to generate SLURM script
def generate_slurm_script(directory, job_name, partition, ntasks, cpus_per_task, mem, time, output_file, email, mail_type, sim_type, setup_params):
    script_content = f"""#!/bin/bash

#SBATCH --job-name={job_name}		                        # Job name
#SBATCH --partition={partition}                            # Partition name (batch, highmem_p, or gpu_p)
#SBATCH --ntasks={ntasks}                                  # Number of tasks
#SBATCH --cpus-per-task={cpus_per_task}                    # CPU core count per task
#SBATCH --mem={mem}                                        # Memory per node
#SBATCH --time={time}                                      # Time limit
#SBATCH --output={output_file}_%j.out                      # Standard output log
#SBATCH --mail-user={email}                                # Where to send mail
#SBATCH --mail-type={mail_type}                            # Mail events (BEGIN, END, FAIL, ALL)

source ~/.bashrc                                # Ensures ~/.bashrc file is sourced
ml SPLASH/3.10.3-foss-2022a                     # Loads `splash` module

#===========================================
# STEPS FOR INITIATING PHANTOM SIMULATION |
#===========================================

cd /home/{os.getlogin()}/runs/

# Create subdirectory for the simulation
NUMBERATM=$(find ./ -type f -name "{sim_type}_*" | wc -l)
NUMBERATM=$((NUMBERATM+1))
if [ $NUMBERATM -lt "10" ]; then
    var=0$NUMBERATM
else
    var=$NUMBERATM
fi
mkdir {sim_type}_$var
cd {sim_type}_$var

# Writing a local Makefile
~/phantom/scripts/writemake.sh {sim_type} > Makefile

# Compiling phantom and phantomsetup
make
make setup

# Running phantomsetup with automatic inputs
echo "1\n1\n0\nno\nno\n0\n0.100\n100" | ./phantomsetup {sim_type}

# Modify the .setup file
{modify_setup_file(sim_type, setup_params)}

# Final phantomsetup command with maximum particles
./phantomsetup {sim_type} --maxp={setup_params['np']}

# Running phantom
./phantom {sim_type}.in
"""
    file_path = os.path.join(directory, f"{job_name}.sh")
    with open(file_path, 'w') as script_file:
        script_file.write(script_content)

    print(f"SLURM script {job_name}.sh generated successfully in {directory}.")

# Function to modify the .setup file based on the simulation type and parameters
def modify_setup_file(sim_type, setup_params):
    modifications = []
    
    if sim_type == 'disc':
        modifications.append(f"sed -i '4s/.*/                  np = {setup_params['np']}    ! number of gas particles/' disc.setup")
        modifications.append(f"sed -i '10s/.*/           dist_unit = {setup_params['dist_unit']}    ! distance unit/' disc.setup")
        modifications.append(f"sed -i '11s/.*/           mass_unit = {setup_params['mass_unit']}    ! mass unit/' disc.setup")
        modifications.append(f"sed -i '14s/.*/            icentral = {setup_params['icentral']}    ! use sink particles or external potential/' disc.setup")
        modifications.append(f"sed -i '15s/.*/          ipotential = {setup_params['ipotential']}    ! potential/' disc.setup")
        modifications.append(f"sed -i '16s/.*/          einst_prec = {setup_params['einst_prec']}    ! include Einstein precession/' disc.setup")
        modifications.append(f"sed -i '17s/.*/                  m1 = {setup_params['m1']}    ! black hole mass/' disc.setup")
        modifications.append(f"sed -i '18s/.*/               accr1 = {setup_params['accr1']}    ! black hole accretion radius/' disc.setup")
        modifications.append(f"sed -i '19s/.*/              bhspin = {setup_params['bhspin']}    ! black hole spin/' disc.setup")
        modifications.append(f"sed -i '20s/.*/         bhspinangle = {setup_params['bhspinangle']}    ! black hole spin angle/' disc.setup")
        modifications.append(f"sed -i '23s/.*/             isetgas = {setup_params['isetgas']}    ! how to set gas density profile/' disc.setup")
        modifications.append(f"sed -i '24s/.*/           itapergas = {setup_params['itapergas']}    ! exponentially taper the outer disc profile/' disc.setup")
        modifications.append(f"sed -i '25s/.*/        itapersetgas = {setup_params['itapersetgas']}    ! how to set taper/' disc.setup")
        modifications.append(f"sed -i '26s/.*/          ismoothgas = {setup_params['ismoothgas']}    ! smooth inner disc/' disc.setup")
        modifications.append(f"sed -i '27s/.*/               iwarp = {setup_params['iwarp']}    ! warp disc/' disc.setup")
        modifications.append(f"sed -i '28s/.*/                R_in = {setup_params['R_in']}    ! inner radius/' disc.setup")
        modifications.append(f"sed -i '29s/.*/               R_ref = {setup_params['R_ref']}    ! reference radius/' disc.setup")
        modifications.append(f"sed -i '30s/.*/               R_out = {setup_params['R_out']}    ! outer radius/' disc.setup")
        modifications.append(f"sed -i '31s/.*/                 R_c = {setup_params['R_c']}    ! characteristic radius of the exponential taper/' disc.setup")
        modifications.append(f"sed -i '32s/.*/              disc_m = {setup_params['disc_m']}    ! disc mass/' disc.setup")
        modifications.append(f"sed -i '33s/.*/              pindex = {setup_params['pindex']}    ! power law index of surface density/' disc.setup")
        modifications.append(f"sed -i '34s/.*/              qindex = {setup_params['qindex']}    ! power law index of sound speed/' disc.setup")
        modifications.append(f"sed -i '35s/.*/             posangl = {setup_params['posangl']}    ! position angle/' disc.setup")
        modifications.append(f"sed -i '36s/.*/                incl = {setup_params['incl']}    ! inclination/' disc.setup")
        modifications.append(f"sed -i '37s/.*/                 H_R = {setup_params['H_R']}    ! H/R at R=R_ref/' disc.setup")
        modifications.append(f"sed -i '38s/.*/             alphaSS = {setup_params['alphaSS']}    ! desired alphaSS/' disc.setup")
        modifications.append(f"sed -i '41s/.*/            nplanets = {setup_params['nplanets']}    ! number of planets/' disc.setup")
        modifications.append(f"sed -i '44s/.*/           discstrat = {setup_params['discstrat']}    ! stratify disc?/' disc.setup")
        modifications.append(f"sed -i '47s/.*/             norbits = {setup_params['norbits']}    ! maximum number of orbits/' disc.setup")
        modifications.append(f"sed -i '48s/.*/              deltat = {setup_params['deltat']}    ! output interval/' disc.setup")

    # Add more conditions here for other simulation types like 'grdisc', 'growingdisc', etc.
    
    return "\n".join(modifications)

# Example usage
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
    sim_type = input("Enter the simulation type (e.g., disc, grdisc): ")
    
    # Default parameters for .setup file
    default_setup_params = {
        "np": "1000000",
        "dist_unit": "au",
        "mass_unit": "solarm",
        "icentral": "0",
        "ipotential": "3",
        "einst_prec": "T",
        "m1": "1.000",
        "accr1": "30.",
        "bhspin": "1.000",
        "bhspinangle": "0.000",
        "isetgas": "0",
        "itapergas": "T",
        "itapersetgas": "0",
        "ismoothgas": "T",
        "iwarp": "F",
        "R_in": "30.",
        "R_ref": "150.",
        "R_out": "150.",
        "R_c": "150.",
        "disc_m": "0.050",
        "pindex": "1.000",
        "qindex": "0.250",
        "posangl": "0.000",
        "incl": "0.000",
        "H_R": "0.050",
        "alphaSS": "0.005",
        "nplanets": "0",
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
    generate_slurm_script(directory, job_name, partition, ntasks, cpus_per_task, mem, time, output_file, email, mail_type, sim_type, setup_params)
