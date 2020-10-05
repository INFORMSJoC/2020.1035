"""Example Python script for frvcpy.

This example follows the "Example Usage" seciton (5.2) from the original research
article describing frvcpy (_link coming soon_).

The script translates an instance from the VRP-REP format, solves an FRVCP on the
instance, and writes the solution to file.
"""

from frvcpy.translator import translate
from frvcpy.solver import Solver

if __name__ == "__main__":

    # Translate the VRP-REP instance.
    frvcp_instance = translate("../data/vrprep-instance.xml")
    
    route = [0,40,12,33,38,16,0]      # route to make energy feasible
    q_init = frvcp_instance["max_q"]  # EV begins with max battery capacity
    
    # Initialize solver with the instance, route, and initial charge.
    frvcp_solver = Solver(frvcp_instance, route, q_init)
    
    # Run the algorithm.
    duration, feas_route = frvcp_solver.solve()
    
    # Write a VRP-REP compliant solution file.
    frvcp_solver.write_solution("../results/my-solution.xml", instance_name="frvcpy-instance")

    print(f"Duration: {duration:.4}")
    # Duration: 7.339
    
    print(f"Energy-feasible route:\n{feas_route}")
    # Energy-feasible route:
    # [(0, None), (40, None), (12, None), (33, None), (48, 6673.379615520617), (38, None),(16, None), (0, None)]
