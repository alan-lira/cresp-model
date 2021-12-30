from configparser import ConfigParser
from math import log
from numpy import array
from pathlib import Path
from scipy.optimize import nnls


class BetaParametersLearner:

    def __init__(self) -> None:
        self.cresp_optimizer_config_file_path = Path("cresp_optimizer_config")
        self.experiments_file_path = Path("experiments")
        self.A_matrix = []
        self.b_vector = []
        self.betaZero = 0.0
        self.betaOne = 0.0
        self.betaTwo = 0.0
        self.betaThree = 0.0
        self.betaFour = 0.0
        self.betaFive = 0.0
        self.betaSix = 0.0
        self.betaSeven = 0.0

    @staticmethod
    def calculate_x0() -> float:
        return 1

    @staticmethod
    def calculate_x1(m: int,
                     M: int) -> float:
        return M / m

    @staticmethod
    def calculate_x2(m: int,
                     r: int,
                     M: int) -> float:
        return (M * r) / m

    @staticmethod
    def calculate_x3(m: int,
                     r: int) -> float:
        return m / r

    @staticmethod
    def calculate_x4(r: int,
                     M: int) -> float:
        return (M * log(M)) / r

    @staticmethod
    def calculate_x5(r: int,
                     M: int) -> float:
        return M / r

    @staticmethod
    def calculate_x6(M: int) -> float:
        return M

    @staticmethod
    def calculate_x7(r: int) -> float:
        return r

    def load_A_matrix(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        cp.read(self.experiments_file_path)
        for section in cp.sections():
            m = int(cp.get(section, "m"))
            r = int(cp.get(section, "r"))
            M = int(cp.get(section, "M"))
            self.A_matrix.append([self.calculate_x0(),
                                  self.calculate_x1(m, M),
                                  self.calculate_x2(m, r, M),
                                  self.calculate_x3(m, r),
                                  self.calculate_x4(r, M),
                                  self.calculate_x5(r, M),
                                  self.calculate_x6(M),
                                  self.calculate_x7(r)])
        del cp  # DELETE CONFIGPARSER OBJECT

    def load_b_vector(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE)
        cp.read(self.experiments_file_path)
        for section in cp.sections():
            execution_time_in_seconds = float(cp.get(section, "execution_time_in_seconds"))
            self.b_vector.append(execution_time_in_seconds)
        del cp  # DELETE CONFIGPARSER OBJECT

    def solve_non_negative_least_squares_problem(self) -> None:
        solution_array = nnls(array(self.A_matrix), array(self.b_vector))[0]
        # SET THE BETA PARAMETERS LEARNED
        self.betaZero = solution_array[0]
        self.betaOne = solution_array[1]
        self.betaTwo = solution_array[2]
        self.betaThree = solution_array[3]
        self.betaFour = solution_array[4]
        self.betaFive = solution_array[5]
        self.betaSix = solution_array[6]
        self.betaSeven = solution_array[7]

    def update_beta_parameters_on_config_file(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE)
        cp.read(self.cresp_optimizer_config_file_path)
        section_name = "beta parameters"
        cp.set(section_name, "β0", str(self.betaZero))
        cp.set(section_name, "β1", str(self.betaOne))
        cp.set(section_name, "β2", str(self.betaTwo))
        cp.set(section_name, "β3", str(self.betaThree))
        cp.set(section_name, "β4", str(self.betaFour))
        cp.set(section_name, "β5", str(self.betaFive))
        cp.set(section_name, "β6", str(self.betaSix))
        cp.set(section_name, "β7", str(self.betaSeven))
        with open(self.cresp_optimizer_config_file_path, "w") as config_file:
            cp.write(config_file)
        del cp  # DELETE CONFIGPARSER OBJECT
        print("Updated '{0}' file with the Beta parameters learned from '{1}' file."
              .format(self.cresp_optimizer_config_file_path,
                      self.experiments_file_path))


def main():
    # INIT BETA PARAMETERS LEARNER OBJECT
    bpl = BetaParametersLearner()

    # LOAD "A" MATRIX
    bpl.load_A_matrix()

    # LOAD "b" VECTOR
    bpl.load_b_vector()

    # SOLVE THE NON-NEGATIVE LEAST SQUARES (NNLS) PROBLEM
    bpl.solve_non_negative_least_squares_problem()

    # UPDATE THE BETA PARAMETERS ON "cresp_optimizer_config" FILE
    bpl.update_beta_parameters_on_config_file()

    # DELETE BETA PARAMETERS LEARNER OBJECT
    del bpl


if __name__ == "__main__":
    main()
