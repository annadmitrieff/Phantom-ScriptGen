# PhantomParamSetup
Work-in-progress (unmaintained) code for setting up `slurm` scripts initializing `phantom` simulations. Current script works specifically for writing SLURM submission scripts for UGA's Sapelo2.

This project has since been abandoned in favor of `PhantomBulk`, where I plan to implement parameter sweeps in addition to the current probabilistic sampling feature.

Supported pre-baked setups:

```bash
disc
dustydisc
dustysgdisc
```

To run code:

```bash
python3 ~/PhantomParamSetup/src/slurm_generator.py
```

