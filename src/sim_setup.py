#!/usr/bin/env python
import os

class SimulationSetup:
    def __init__(self, setup_params):
        self.setup_params = setup_params

    def modify_component(self, setup_file, param_name, line_number, description=""):
        """
        General method to modify a specific component in the setup file.
        This method takes in the parameter name, the line number in the setup file, 
        and an optional description.
        """
        param_value = self.setup_params.get(param_name)
        if param_value is not None:
            return f"sed -i '{line_number}s/.*/                  {param_name} = {param_value}    ! {description}/' {setup_file}"
        return ""

    def modify_setup_file(self, setup_file):
        """
        Base method to be overridden by subclasses for specific setup types.
        """
        raise NotImplementedError("Subclasses should implement this!")

