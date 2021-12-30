from configparser import ConfigParser
from math import ceil
from pathlib import Path
from random import sample


class ExperimentsMaker:

    def __init__(self) -> None:
        self.experiments_maker_config_file_path = Path("config/experiments_maker_config")
        self.experiments_output_file_path = None
        self.number_of_experiments = 0
        self.data_block_size_in_megabytes = 0
        self.gamma = 0
        self.m_range = []
        self.r_range = []
        self.M_range = []
        self.m_list = []
        self.r_list = []
        self.M_list = []
        self.input_size_list = []
        self.number_of_vms_list = []

    def load_general_settings(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        cp.read(self.experiments_maker_config_file_path)
        self.number_of_experiments = int(cp.get("general settings", "number_of_experiments"))
        self.data_block_size_in_megabytes = float(cp.get("general settings", "data_block_size_in_megabytes"))
        self.gamma = int(cp.get("general settings", "γ"))
        self.experiments_output_file_path = Path(cp.get("general settings", "experiments_output_file"))
        del cp  # DELETE CONFIGPARSER OBJECT

    def load_samples_ranges(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        cp.read(self.experiments_maker_config_file_path)
        m_range = cp.get("samples range settings", "m").split("...")
        self.m_range.append(m_range[0])
        self.m_range.append(m_range[1])
        r_range = cp.get("samples range settings", "r").split("...")
        self.r_range.append(r_range[0])
        self.r_range.append(r_range[1])
        M_range = cp.get("samples range settings", "M").split("...")
        self.M_range.append(M_range[0])
        self.M_range.append(M_range[1])
        del cp  # DELETE CONFIGPARSER OBJECT

    def get_m_range(self) -> range:
        return range(int(self.m_range[0]), int(self.m_range[1]))

    def pseudo_randomly_populate_m_list(self) -> None:
        for _ in range(self.number_of_experiments):
            random_m = sample(self.get_m_range(), 1)[0]
            self.m_list.append(random_m)

    def get_r_range(self,
                    current_m: int) -> range:
        if "m" in self.r_range[0]:
            m_extracted = str(self.r_range[0]).replace("m", "")
            if len(m_extracted) > 0:
                r_lower = int(m_extracted) * current_m
            else:
                r_lower = current_m
        else:
            r_lower = int(self.r_range[0])
        if "m" in self.r_range[1]:
            m_extracted = str(self.r_range[1]).replace("m", "")
            if len(m_extracted) > 0:
                r_higher = int(m_extracted) * current_m
            else:
                r_higher = current_m
        else:
            r_higher = int(self.r_range[1])
        return range(r_lower, r_higher)

    def pseudo_randomly_populate_r_list(self) -> None:
        for i in range(self.number_of_experiments):
            current_m = self.m_list[i]
            if current_m == 1:
                self.r_list.append(1)
            else:
                random_r = sample(self.get_r_range(current_m), 1)[0]
                self.r_list.append(random_r)

    def get_M_range(self,
                    current_m: int) -> range:
        if "m" in self.M_range[0]:
            m_extracted = str(self.M_range[0]).replace("m", "")
            if len(m_extracted) > 0:
                M_lower = int(m_extracted) * current_m
            else:
                M_lower = current_m
        else:
            M_lower = int(self.M_range[0])
        if "m" in self.M_range[1]:
            m_extracted = str(self.M_range[1]).replace("m", "")
            if len(m_extracted) > 0:
                M_higher = int(m_extracted) * current_m
            else:
                M_higher = current_m
        else:
            M_higher = int(self.M_range[1])
        return range(M_lower, M_higher)

    def pseudo_randomly_populate_M_list(self) -> None:
        for i in range(self.number_of_experiments):
            current_m = self.m_list[i]
            random_M = sample(self.get_M_range(current_m), 1)[0]
            self.M_list.append(random_M)

    def calculate_input_size_list(self) -> None:
        for M in self.M_list:
            input_size_in_gb = M * (self.data_block_size_in_megabytes / 1024)
            self.input_size_list.append(int(ceil(input_size_in_gb)))

    def calculate_number_of_vms_list(self) -> None:
        for i in range(self.number_of_experiments):
            nu = int(ceil((self.m_list[i] + self.r_list[i]) / self.gamma))
            self.number_of_vms_list.append(nu)

    def generate_experiments_file(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        for i in range(self.number_of_experiments):
            with open(self.experiments_output_file_path, "w") as file_object:
                cp["Experiment " + str(i+1)] = {
                    "m": str(self.m_list[i]),
                    "r": str(self.r_list[i]),
                    "M": str(self.M_list[i]),
                    "input_size_in_gb": str(self.input_size_list[i]),
                    "number_of_vms": str(self.number_of_vms_list[i]),
                    "number_of_vcpus_per_vm": str(self.gamma),
                    "total_number_of_vcpus": str(self.number_of_vms_list[i] * self.gamma),
                    "execution_time_in_seconds": ""
                }
                cp.write(file_object)
        del cp  # DELETE CONFIGPARSER OBJECT
        print("Generated '{0}' file with the settings read from '{1}' file."
              .format(self.experiments_output_file_path,
                      self.experiments_maker_config_file_path))


def main():
    # INIT EXPERIMENTS MAKER OBJECT
    em = ExperimentsMaker()

    # LOAD GENERAL SETTINGS (number of experiments, data block size in MB, gamma, output file path)
    em.load_general_settings()

    # LOAD SAMPLES RANGES FOR "m", "r" AND "M"
    em.load_samples_ranges()

    # PSEUDO RANDOMLY POPULATE "m" LIST
    em.pseudo_randomly_populate_m_list()

    # PSEUDO RANDOMLY POPULATE "r" LIST
    em.pseudo_randomly_populate_r_list()

    # PSEUDO RANDOMLY POPULATE "M" LIST
    em.pseudo_randomly_populate_M_list()

    # CALCULATE INPUT SIZE LIST (IN GIGABYTES)
    em.calculate_input_size_list()

    # CALCULATE NUMBER OF VIRTUAL MACHINES LIST
    em.calculate_number_of_vms_list()

    # GENERATE 'experiments' FILE
    em.generate_experiments_file()

    # DELETE EXPERIMENTS MAKER OBJECT
    del em


if __name__ == "__main__":
    main()
