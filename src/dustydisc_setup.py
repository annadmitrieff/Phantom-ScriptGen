#!/usr/bin/env python
import os
from sim_setup import SimulationSetup

class DustyDiscSetup(SimulationSetup):
    def modify_setup_file(self, setup_file):
        modifications = [
            self.modify_component(setup_file, 'np', 4, "number of gas particles"),
            self.modify_component(setup_file, 'np_dust', 5, "number of large dust particles"),
            self.modify_component(setup_file, 'dist_unit', 10, "distance unit"),
            self.modify_component(setup_file, 'mass_unit', 11, "mass unit"),
            self.modify_component(setup_file, 'icentral', 14, "use sink particles or external potential"),
            self.modify_component(setup_file, 'nsinks', 15, "number of sinks"),
            self.modify_component(setup_file, 'm1', 17, "star mass"),
            self.modify_component(setup_file, 'accr1', 18, "star accretion radius"),
            self.modify_component(setup_file, 'isetgas', 23, "how to set gas density profile"),
            self.modify_component(setup_file, 'itapergas', 24, "exponentially taper the outer disc profile"),
            self.modify_component(setup_file, 'ismoothgas', 26, "smooth inner disc"),
            self.modify_component(setup_file, 'iwarp', 27, "warp disc"),
            self.modify_component(setup_file, 'R_in', 28, "inner radius"),
            self.modify_component(setup_file, 'R_ref', 29, "reference radius"),
            self.modify_component(setup_file, 'R_out', 30, "outer radius"),
            self.modify_component(setup_file, 'disc_m', 32, "disc mass"),
            self.modify_component(setup_file, 'pindex', 33, "power law index of surface density"),
            self.modify_component(setup_file, 'qindex', 34, "power law index of sound speed"),
            self.modify_component(setup_file, 'H_R', 37, "H/R at R=R_ref"),
            self.modify_component(setup_file, 'alphaSS', 38, "desired alphaSS"),
            self.modify_component(setup_file, 'dust_method', 52, "dust method"),
            self.modify_component(setup_file, 'dust_to_gas', 53, "dust to gas ratio"),
            self.modify_component(setup_file, 'ndusttypesinp', 54, "number of grain sizes"),
            self.modify_component(setup_file, 'grainsizeinp', 55, "grain size (in cm)"),
            self.modify_component(setup_file, 'isetdust', 58, "how to set dust density profile"),
            self.modify_component(setup_file, 'nplanets', 41, "number of planets"),
            self.modify_component(setup_file, 'discstrat', 44, "stratify disc"),
            self.modify_component(setup_file, 'norbits', 47, "maximum number of orbits at outer disc"),
            self.modify_component(setup_file, 'deltat', 48, "output interval as fraction of orbital period")
        ]
        return "\n".join([mod for mod in modifications if mod])
