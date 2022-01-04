from configparser import ConfigParser
from gurobipy import Env, GRB, Model
from math import ceil, inf, log
from pathlib import Path
from time import time
from sys import exit


class CrespOptimizer:

    def __init__(self) -> None:
        self.cresp_optimizer_config_file_path = Path("config/cresp_optimizer.cfg")
        self.betaZero = 0.0
        self.betaOne = 0.0
        self.betaTwo = 0.0
        self.betaThree = 0.0
        self.betaFour = 0.0
        self.betaFive = 0.0
        self.betaSix = 0.0
        self.betaSeven = 0.0
        self.M = 0
        self.Gamma = 0
        self.Upsilon = 0.0
        self.Phi = 0.0
        self.Tau = 0.0
        self.m = 0
        self.m_lower_bound = 0
        self.m_upper_bound = 0
        self.R = 0
        self.R_lower_bound = 0
        self.R_upper_bound = 0
        self.monetary_unit = None
        self.time_unit = None
        self.alfaZero = 0.0
        self.alfaOne = 0.0
        self.alfaTwo = 0.0
        self.alfaThree = 0.0
        self.alfaFour = 0.0
        self.alfaFive = 0.0
        self.optimization_problem = 0
        self.optimization_problem_description = None
        self.optimization_modes = None
        self.T3 = inf
        self.C = inf
        self.Nu = 0

    def get_beta_i(self,
                   config_parser: ConfigParser,
                   beta_i: str) -> float:
        exception_message = "{0}: '{1}' must be a float value equal or higher than zero!" \
            .format(self.cresp_optimizer_config_file_path, beta_i)
        try:
            beta_i_value = float(config_parser.get("beta parameters", beta_i))
            if beta_i_value < 0.0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return beta_i_value

    def load_beta_parameters(self,
                             config_parser: ConfigParser) -> None:
        self.betaZero = self.get_beta_i(config_parser, "β0")
        self.betaOne = self.get_beta_i(config_parser, "β1")
        self.betaTwo = self.get_beta_i(config_parser, "β2")
        self.betaThree = self.get_beta_i(config_parser, "β3")
        self.betaFour = self.get_beta_i(config_parser, "β4")
        self.betaFive = self.get_beta_i(config_parser, "β5")
        self.betaSix = self.get_beta_i(config_parser, "β6")
        self.betaSeven = self.get_beta_i(config_parser, "β7")

    def get_M(self,
              config_parser: ConfigParser) -> int:
        exception_message = "{0}: 'M' (number of Map tasks) must be a integer value higher than zero!" \
            .format(self.cresp_optimizer_config_file_path)
        try:
            M = int(config_parser.get("input parameters", "M"))
            if M <= 0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return M

    def get_gamma(self,
                  config_parser: ConfigParser) -> int:
        exception_message = "{0}: 'γ' (gamma: number of slots per node) must be a integer value higher than zero!" \
            .format(self.cresp_optimizer_config_file_path)
        try:
            gamma = int(config_parser.get("input parameters", "γ"))
            if gamma <= 0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return gamma

    def get_upsilon(self,
                    config_parser: ConfigParser) -> float:
        exception_message = "{0}: 'υ' (upsilon: monetary cost, per hour, of one node) " \
                            "must be a float value higher than zero!" \
            .format(self.cresp_optimizer_config_file_path)
        try:
            upsilon = float(config_parser.get("input parameters", "υ"))
            if upsilon <= 0.0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return upsilon

    def get_phi(self,
                config_parser: ConfigParser) -> float:
        exception_message = "{0}: 'φ' (phi: maximum monetary cost for finishing the job) " \
                            "must be a float value higher than zero!" \
            .format(self.cresp_optimizer_config_file_path)
        try:
            phi = float(config_parser.get("input parameters", "φ"))
            if phi <= 0.0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return phi

    def get_tau(self,
                config_parser: ConfigParser) -> float:
        exception_message = "{0}: 'τ' (tau: maximum amount of time, in hours, for finishing the job) " \
                            "must be a float value higher than zero!" \
            .format(self.cresp_optimizer_config_file_path)
        try:
            tau = float(config_parser.get("input parameters", "τ"))
            if tau <= 0.0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return tau

    def load_input_parameters(self,
                              config_parser: ConfigParser) -> None:
        self.M = self.get_M(config_parser)
        self.Gamma = self.get_gamma(config_parser)
        self.Upsilon = self.get_upsilon(config_parser)
        self.Phi = self.get_phi(config_parser)
        self.Tau = self.get_tau(config_parser)

    def get_m_bounds(self,
                     config_parser: ConfigParser) -> list:
        exception_message = "{0}: 'm' (number of Map slots) must have valid integer bounds!" \
            .format(self.cresp_optimizer_config_file_path)
        m_bounds = []
        try:
            m_bounds_list = config_parser.get("variables bounds", "m").split("...")
            m_lower = int(m_bounds_list[0])
            if m_lower <= 0:
                raise ValueError(exception_message)
            else:
                m_bounds.append(m_lower)
            m_higher = int(m_bounds_list[1])
            if m_higher <= 0 or m_higher <= m_lower:
                raise ValueError(exception_message)
            else:
                m_bounds.append(m_higher)
        except ValueError:
            raise ValueError(exception_message)
        return m_bounds

    def load_m_bounds(self,
                      config_parser: ConfigParser) -> None:
        m_bounds = self.get_m_bounds(config_parser)
        self.m_lower_bound = m_bounds[0]
        self.m_upper_bound = m_bounds[1]

    def get_R_bounds(self,
                     config_parser: ConfigParser) -> list:
        exception_message = "{0}: 'R' (number of Reduce tasks) must have valid integer bounds!" \
            .format(self.cresp_optimizer_config_file_path)
        R_bounds = []
        try:
            R_bounds_list = config_parser.get("variables bounds", "R").split("...")
            R_lower = int(R_bounds_list[0])
            if R_lower <= 0:
                raise ValueError(exception_message)
            else:
                R_bounds.append(R_lower)
            R_higher = int(R_bounds_list[1])
            if R_higher <= 0 or R_higher <= R_lower:
                raise ValueError(exception_message)
            else:
                R_bounds.append(R_higher)
        except ValueError:
            raise ValueError(exception_message)
        return R_bounds

    def load_R_bounds(self,
                      config_parser: ConfigParser) -> None:
        R_bounds = self.get_R_bounds(config_parser)
        self.R_lower_bound = R_bounds[0]
        self.R_upper_bound = R_bounds[1]

    def get_monetary_unit(self,
                          config_parser: ConfigParser) -> str:
        valid_monetary_unit_list = ["USD"]
        exception_message = "{0}: supported 'monetary_unit' values: {1}." \
            .format(self.cresp_optimizer_config_file_path, " | ".join(valid_monetary_unit_list))
        try:
            monetary_unit = str(config_parser.get("general", "monetary_unit"))
            if monetary_unit not in valid_monetary_unit_list:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return monetary_unit

    def load_monetary_unit(self,
                           config_parser: ConfigParser) -> None:
        self.monetary_unit = self.get_monetary_unit(config_parser)

    def get_time_unit(self,
                      config_parser: ConfigParser) -> str:
        valid_time_unit_list = ["second", "minute", "hour"]
        exception_message = "{0}: supported 'time_unit' values: {1}." \
            .format(self.cresp_optimizer_config_file_path, " | ".join(valid_time_unit_list))
        try:
            time_unit = str(config_parser.get("general", "time_unit"))
            if time_unit not in valid_time_unit_list:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return time_unit

    def load_time_unit(self,
                       config_parser: ConfigParser) -> None:
        self.time_unit = self.get_time_unit(config_parser)

    def convert_time_unit_dependent_variables(self) -> None:
        if self.time_unit == "minute":
            self.Upsilon = self.Upsilon / 60  # Price of renting one VM instance per minute
            self.Tau = self.Tau * 60  # Maximum amount of time τ, in minutes, for finishing the job (Time constraint)
        elif self.time_unit == "second":
            self.Upsilon = self.Upsilon / 3600  # Price of renting one VM instance per second
            self.Tau = self.Tau * 3600  # Maximum amount of time τ, in seconds, for finishing the job (Time constraint)

    def calculate_alfa_constants(self) -> None:
        self.alfaZero = self.betaZero + (self.betaSix * self.M)
        self.alfaOne = self.betaOne * self.M
        self.alfaTwo = self.betaTwo * self.M
        self.alfaThree = self.betaThree
        self.alfaFour = (self.betaFour * self.M * log(self.M)) + (self.betaFive * self.M)
        self.alfaFive = self.betaSeven

    def get_optimization_problem(self,
                                 config_parser: ConfigParser) -> int:
        valid_optimization_problem_list = ["1", "2", "3"]
        exception_message = "{0}: supported 'optimization_problem' values: {1}." \
            .format(self.cresp_optimizer_config_file_path, " | ".join(valid_optimization_problem_list))
        try:
            optimization_problem = int(config_parser.get("cresp", "optimization_problem"))
            if str(optimization_problem) not in valid_optimization_problem_list:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return optimization_problem

    def load_optimization_problem(self,
                                  config_parser: ConfigParser) -> None:
        self.optimization_problem = self.get_optimization_problem(config_parser)
        if self.optimization_problem == 1:
            self.optimization_problem_description = \
                "Minimize the job time, given a maximum monetary cost φ = " \
                + str(self.Phi) + " " + str(self.monetary_unit)
        elif self.optimization_problem == 2:
            self.optimization_problem_description = \
                "Minimize the monetary cost, given a maximum amount of time τ = " \
                + str(self.Tau) + " " + str(self.time_unit) + "(s)"
        elif self.optimization_problem == 3:
            self.optimization_problem_description = "Minimize the monetary cost (without time τ constraint)"

    def get_optimization_modes(self,
                               config_parser: ConfigParser) -> list:
        valid_optimization_mode_list = ["brute_force", "gurobi"]
        exception_message = "{0}: supported 'optimization_modes' values: {1}." \
            .format(self.cresp_optimizer_config_file_path, " | ".join(valid_optimization_mode_list))
        try:
            optimization_modes = str(config_parser.get("general", "optimization_modes")).split(", ")
            for optimization_mode in optimization_modes:
                if optimization_mode not in valid_optimization_mode_list:
                    raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return optimization_modes

    def load_optimization_modes(self,
                                config_parser: ConfigParser) -> None:
        self.optimization_modes = self.get_optimization_modes(config_parser)

    def calculate_T3(self,
                     m_candidate: int,
                     R_candidate: int) -> float:
        T3 = self.alfaZero + \
             self.alfaOne / m_candidate + \
             (self.alfaTwo * R_candidate) / m_candidate + \
             (self.alfaThree * m_candidate) / R_candidate + \
             self.alfaFour / R_candidate + \
             self.alfaFive * R_candidate
        if self.time_unit == "hour":
            T3 = T3 / 3600
        elif self.time_unit == "minute":
            T3 = T3 / 60
        return T3

    def calculate_C(self,
                    T3_candidate: float,
                    m_candidate: int,
                    R_candidate: int) -> float:
        return self.Upsilon * T3_candidate * (m_candidate + R_candidate) / self.Gamma

    def is_constraint_not_violated(self,
                                   C: float,
                                   T3: float) -> bool:
        if self.optimization_problem == 1:
            return C <= self.Phi
        if self.optimization_problem == 2:
            return T3 <= self.Tau

    def reset_model_results(self) -> None:
        self.m = 0
        self.R = 0
        self.T3 = inf
        self.C = inf
        self.Nu = 0

    def optimize_model_with_brute_force(self) -> None:
        if self.optimization_problem == 1:
            # MINIMIZE T3(m,R):
            # SUBJECT TO:
            # Upsilon * [T3(m,R)] * [(m+R) / Gamma] <= Phi
            for m_candidate in range(self.m_lower_bound, self.m_upper_bound + 1):
                for R_candidate in range(self.R_lower_bound, self.R_upper_bound + 1):
                    T3_candidate = self.calculate_T3(m_candidate, R_candidate)
                    C_candidate = self.calculate_C(T3_candidate, m_candidate, R_candidate)
                    if self.is_constraint_not_violated(C_candidate, T3_candidate):
                        if T3_candidate < self.T3:
                            self.m = m_candidate
                            self.R = R_candidate
                            self.T3 = T3_candidate
                            self.C = C_candidate
        elif self.optimization_problem == 2:
            # MINIMIZE Upsilon * [T3(m,R)] * [(m+R) / Gamma]
            # SUBJECT TO:
            # T3(m,R) <= τ
            for m_candidate in range(self.m_lower_bound, self.m_upper_bound + 1):
                for R_candidate in range(self.R_lower_bound, self.R_upper_bound + 1):
                    T3_candidate = self.calculate_T3(m_candidate, R_candidate)
                    C_candidate = self.calculate_C(T3_candidate, m_candidate, R_candidate)
                    if self.is_constraint_not_violated(C_candidate, T3_candidate):
                        if C_candidate < self.C:
                            self.m = m_candidate
                            self.R = R_candidate
                            self.T3 = T3_candidate
                            self.C = C_candidate
        elif self.optimization_problem == 3:
            # MINIMIZE Upsilon * [T3(m,R)] * [(m+R) / Gamma]
            for m_candidate in range(self.m_lower_bound, self.m_upper_bound + 1):
                for R_candidate in range(self.R_lower_bound, self.R_upper_bound + 1):
                    T3_candidate = self.calculate_T3(m_candidate, R_candidate)
                    C_candidate = self.calculate_C(T3_candidate, m_candidate, R_candidate)
                    if C_candidate < self.C:
                        self.m = m_candidate
                        self.R = R_candidate
                        self.T3 = T3_candidate
                        self.C = C_candidate

    def optimize_model_with_gurobi(self) -> None:
        with Env() as env, Model(name="CRESP Cost Model on Gurobi for Python", env=env) as model:
            # SET MODEL PARAMETERS
            model.setParam("NonConvex", 2)
            # SET MODEL DECISION VARIABLE
            m = model.addVar(name="m",
                             vtype=GRB.INTEGER,
                             lb=self.m_lower_bound,
                             ub=self.m_upper_bound)
            R = model.addVar(name="R",
                             vtype=GRB.INTEGER,
                             lb=self.R_lower_bound,
                             ub=self.R_upper_bound)
            z1 = model.addVar(name="z1",
                              vtype=GRB.CONTINUOUS,
                              lb=(1 / self.m_upper_bound),
                              ub=(1 / self.m_lower_bound))  # z1 = 1 / m -> m = 1 / z1
            z2 = model.addVar(name="z2",
                              vtype=GRB.CONTINUOUS,
                              lb=(1 / self.R_upper_bound),
                              ub=(1 / self.R_lower_bound))  # z2 = 1 / R -> R = 1 / z2
            z3 = model.addVar(name="z3",
                              vtype=GRB.CONTINUOUS,
                              lb=1,
                              ub=GRB.INFINITY)  # z3 = R * z1
            z4 = model.addVar(name="z4",
                              vtype=GRB.CONTINUOUS,
                              lb=1,
                              ub=GRB.INFINITY)  # z4 = m * z2
            # SET TIME COST FUNCTION: T3(m,R) = α0 + α1/m + α2R/m + α3m/R + α4/R + α5R
            T3 = self.alfaZero + \
                self.alfaOne * z1 + \
                self.alfaTwo * z3 + \
                self.alfaThree * z4 + \
                self.alfaFour * z2 + \
                self.alfaFive * R
            if self.time_unit == "hour":
                T3 = T3 / 3600
            elif self.time_unit == "minute":
                T3 = T3 / 60
            # SET MODEL OBJECTIVE AND CONSTRAINTS
            if self.optimization_problem == 1:
                # MINIMIZE T3(m,R):
                # SUBJECT TO:
                # Upsilon * [T3(m,R)] * [(m+R) / Gamma] <= Phi
                model.setObjective(T3, GRB.MINIMIZE)
                model.addConstr(self.Upsilon * T3 * ((m + R) / self.Gamma) <= self.Phi, "c0")
            elif self.optimization_problem == 2:
                # MINIMIZE Upsilon * [T3(m,R)] * [(m+R) / Gamma]
                # SUBJECT TO:
                # T3(m,R) <= τ
                model.setObjective(self.Upsilon * T3 * ((m + R) / self.Gamma), GRB.MINIMIZE)
                model.addConstr(T3 <= self.Tau, "c0")
            elif self.optimization_problem == 3:
                # MINIMIZE Upsilon * [T3(m,R)] * [(m+R) / Gamma]
                model.setObjective(self.Upsilon * T3 * ((m + R) / self.Gamma), GRB.MINIMIZE)
            model.addConstr(z1 * m == 1, "c1")  # z1 = 1 / m => m = 1 / z1
            model.addConstr(z2 * R == 1, "c2")  # z2 = 1 / R => R = 1 / z2
            model.addConstr(z3 == R * z1, "c3")  # z3 = R * z1
            model.addConstr(z4 == m * z2, "c4")  # z4 = m * z2
            # OPTIMIZE MODEL
            model.optimize()
            # IF MODEL IS FEASIBLE (FOUND OPTIMAL VALUE, GRB.OPTIMAL):
            if model.status == 2:
                for v in model.getVars():
                    if str(v.varName) == "z1":
                        self.m = ceil(1 / v.x)
                    if str(v.varName) == "z2":
                        self.R = ceil(1 / v.x)
                self.T3 = T3.getValue()
                self.C = self.calculate_C(self.T3, self.m, self.R)
            del env
            del model

    def calculate_optimal_number_of_vms(self) -> None:
        self.Nu = ceil((self.m + self.R) / self.Gamma)

    def print_optimization_results(self,
                                   optimization_mode: str,
                                   optimization_time_in_seconds: time) -> None:
        print("-------------------- {0} ({1} seconds) -------------------".format(optimization_mode.upper(),
                                                                                  optimization_time_in_seconds))
        if self.m > 0 and self.R > 0:
            print("Estimated Time Cost: {0} {1}(s)".format(self.T3, self.time_unit))
            print("Number of Map Slots (m): {0}".format(self.m))
            print("Number of Reduce Slots (R = r): {0}".format(self.R))
            print("Number of Nodes/VMs (ν): {0}".format(self.Nu))
            print("Estimated Monetary Cost: {0} {1}".format(self.C, self.monetary_unit))
        else:
            print("MODEL IS INFEASIBLE!")

    def optimize_model_with_available_optimization_modes(self) -> None:
        print("CRESP's Optimization Problem \"{0}\" - {1}:".format(self.optimization_problem,
                                                                   self.optimization_problem_description))
        for mode in self.optimization_modes:
            self.reset_model_results()
            optimization_start_time = time()
            if mode == "brute_force":
                self.optimize_model_with_brute_force()
            if mode == "gurobi":
                self.optimize_model_with_gurobi()
            optimization_end_time = time() - optimization_start_time
            self.calculate_optimal_number_of_vms()
            self.print_optimization_results(mode, optimization_end_time)


def main():
    # INIT CRESP OPTIMIZER OBJECT
    co = CrespOptimizer()

    # INIT CONFIGPARSER OBJECT
    cp = ConfigParser()

    # PRESERVE OPTIONS NAMES' CASE
    cp.optionxform = str

    # READ CONFIG FILE
    cp.read(co.cresp_optimizer_config_file_path, encoding="utf-8")

    # LOAD BETA PARAMETERS (β0, β1, β2, β3, β4, β5, β6, β7)
    co.load_beta_parameters(cp)

    # LOAD INPUT PARAMETERS (M, γ, υ, φ, τ)
    # M: Number of chunks of data (Map tasks); M = Input (GB) * 1024MB / HDFS Block Size (MB)
    # γ (Gamma): Fixed number of slots (vCPUs) per node for a specific cluster setup
    # υ (Upsilon): Price of renting one VM instance for an hour
    # φ (Phi): Maximum monetary cost φ for finishing the job (Monetary budget constraint)
    # τ (Tau): Maximum amount of time τ, in hours, for finishing the job (Time constraint)
    co.load_input_parameters(cp)

    # LOAD m BOUNDS (lower, upper)
    co.load_m_bounds(cp)

    # LOAD R BOUNDS (lower, upper)
    co.load_R_bounds(cp)

    # LOAD MONETARY UNIT [USD]
    co.load_monetary_unit(cp)

    # LOAD TIME UNIT [second | minute | hour]
    co.load_time_unit(cp)

    # CONVERT TIME UNIT DEPENDENT VARIABLES (υ, τ)
    co.convert_time_unit_dependent_variables()

    # CALCULATE ALFA CONSTANTS (α0, α1, α2, α3, α4, α5)
    co.calculate_alfa_constants()

    # LOAD OPTIMIZATION PROBLEM [1 | 2 | 3]
    # 1: Given a maximum monetary cost φ for finishing the job (Monetary budget constraint),
    #    find the best resource allocation to minimize the job time
    # 2: Given a maximum amount of time τ for finishing the job (Time constraint),
    #    find the best resource allocation to minimize the monetary cost
    # 3: Find the most economical solution for the job without the Time constraint τ
    co.load_optimization_problem(cp)

    # LOAD OPTIMIZATION MODES [brute_force | gurobi]
    co.load_optimization_modes(cp)

    # OPTIMIZE MODEL WITH AVAILABLE OPTIMIZATION MODES
    co.optimize_model_with_available_optimization_modes()

    # DELETE CONFIGPARSER OBJECT
    del cp

    # DELETE CRESP OPTIMIZER OBJECT
    del co

    # END
    exit(0)


if __name__ == "__main__":
    main()
