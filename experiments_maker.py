from configparser import ConfigParser
from math import ceil
from pathlib import Path
from random import sample
from sys import exit


class ExperimentsMaker:

    def __init__(self) -> None:
        self.experiments_maker_config_file_path = Path("config/experiments_maker.cfg")
        self.experiments_output_file_path = None
        self.number_of_experiments = 0
        self.data_block_size_in_megabytes = 0
        self.gamma = 0
        self.m_range = None
        self.r_range = None
        self.M_range = []
        self.m_list = []
        self.r_list = []
        self.M_list = []
        self.input_size_list = []
        self.number_of_nodes_list = []

    def get_number_of_experiments(self,
                                  config_parser: ConfigParser) -> int:
        exception_message = "{0}: 'number_of_experiments' must be a integer value higher than zero!" \
            .format(self.experiments_maker_config_file_path)
        try:
            number_of_experiments = int(config_parser.get("general", "number_of_experiments"))
            if number_of_experiments <= 0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return number_of_experiments

    def get_data_block_size_in_megabytes(self,
                                         config_parser: ConfigParser) -> int:
        exception_message = "{0}: 'data_block_size_in_megabytes' must be a integer value higher than zero!" \
            .format(self.experiments_maker_config_file_path)
        try:
            data_block_size_in_megabytes = int(config_parser.get("general", "data_block_size_in_megabytes"))
            if data_block_size_in_megabytes <= 0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return data_block_size_in_megabytes

    def get_gamma(self,
                  config_parser: ConfigParser) -> int:
        exception_message = "{0}: 'γ' (gamma: number of slots per node) must be a integer value higher than zero!" \
            .format(self.experiments_maker_config_file_path)
        try:
            gamma = int(config_parser.get("general", "γ"))
            if gamma <= 0:
                raise ValueError(exception_message)
        except ValueError:
            raise ValueError(exception_message)
        return gamma

    def get_experiments_output_file_path(self,
                                         config_parser: ConfigParser) -> Path:
        exception_message = "{0}: 'experiments_output_file' must be a valid path file!" \
            .format(self.experiments_maker_config_file_path)
        try:
            experiments_output_file_path = Path(config_parser.get("general", "experiments_output_file"))
        except ValueError:
            raise ValueError(exception_message)
        return experiments_output_file_path

    def load_general_settings(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        cp.read(self.experiments_maker_config_file_path, encoding="utf-8")
        self.number_of_experiments = self.get_number_of_experiments(cp)
        self.data_block_size_in_megabytes = self.get_data_block_size_in_megabytes(cp)
        self.gamma = self.get_gamma(cp)
        self.experiments_output_file_path = self.get_experiments_output_file_path(cp)
        del cp  # DELETE CONFIGPARSER OBJECT

    def get_m_range(self,
                    config_parser: ConfigParser) -> range:
        exception_message = "{0}: 'm' (number of Map slots) must be a valid integer range!" \
            .format(self.experiments_maker_config_file_path)
        try:
            m_range_list = config_parser.get("samples ranges", "m").split("...")
            if int(m_range_list[0]) <= 0 or int(m_range_list[1]) <= 0 or int(m_range_list[1]) <= int(m_range_list[0]):
                raise ValueError(exception_message)
            m_range = range(int(m_range_list[0]), int(m_range_list[1]) + 1)
        except ValueError:
            raise ValueError(exception_message)
        return m_range

    def get_r_range(self,
                    config_parser: ConfigParser) -> list:
        exception_message = "{0}: 'r' (number of Reduce slots) must be a valid integer (or multiple of 'm') range!" \
            .format(self.experiments_maker_config_file_path)
        r_range = []
        try:
            r_range_list = config_parser.get("samples ranges", "r").split("...")
            r_lower = str(r_range_list[0])
            if "m" in r_lower:
                m_extracted_lower = r_lower.replace("m", "")
                if len(m_extracted_lower) > 0:
                    if int(m_extracted_lower) <= 0:
                        raise ValueError(exception_message)
                    else:
                        r_range.append(r_lower)
                else:
                    r_range.append(r_lower)
            else:
                if int(r_lower) <= 0:
                    raise ValueError(exception_message)
                else:
                    r_range.append(int(r_lower))
            r_higher = str(r_range_list[1])
            if "m" in r_higher:
                m_extracted_lower = r_lower.replace("m", "")
                m_extracted_higher = r_higher.replace("m", "")
                if len(m_extracted_higher) > 0:
                    if int(m_extracted_higher) <= 0 or int(m_extracted_higher) <= int(m_extracted_lower):
                        raise ValueError(exception_message)
                    else:
                        r_range.append(r_higher)
                else:
                    r_range.append(r_higher)
            else:
                if int(r_higher) <= 0 or int(r_higher) <= int(r_lower):
                    raise ValueError(exception_message)
                else:
                    r_range.append(int(r_higher))
        except ValueError:
            raise ValueError(exception_message)
        return r_range

    def get_M_range(self,
                    config_parser: ConfigParser) -> list:
        exception_message = "{0}: 'M' (number of Map tasks) must be a valid integer (or multiple of 'm') range!" \
            .format(self.experiments_maker_config_file_path)
        M_range = []
        try:
            M_range_list = config_parser.get("samples ranges", "M").split("...")
            M_lower = str(M_range_list[0])
            if "m" in M_lower:
                m_extracted_lower = M_lower.replace("m", "")
                if len(m_extracted_lower) > 0:
                    if int(m_extracted_lower) <= 0:
                        raise ValueError(exception_message)
                    else:
                        M_range.append(M_lower)
                else:
                    M_range.append(M_lower)
            else:
                if int(M_lower) <= 0:
                    raise ValueError(exception_message)
                else:
                    M_range.append(int(M_lower))
            M_higher = str(M_range_list[1])
            if "m" in M_higher:
                m_extracted_lower = M_lower.replace("m", "")
                m_extracted_higher = M_higher.replace("m", "")
                if len(m_extracted_higher) > 0:
                    if int(m_extracted_higher) <= 0 or int(m_extracted_higher) <= int(m_extracted_lower):
                        raise ValueError(exception_message)
                    else:
                        M_range.append(M_higher)
                else:
                    M_range.append(M_higher)
            else:
                if int(M_higher) <= 0 or int(M_higher) <= int(M_lower):
                    raise ValueError(exception_message)
                else:
                    M_range.append(int(M_higher))
        except ValueError:
            raise ValueError(exception_message)
        return M_range

    def load_samples_ranges(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        cp.read(self.experiments_maker_config_file_path, encoding="utf-8")
        self.m_range = self.get_m_range(cp)
        self.r_range = self.get_r_range(cp)
        self.M_range = self.get_M_range(cp)
        del cp  # DELETE CONFIGPARSER OBJECT

    def pseudo_randomly_populate_m_list(self) -> None:
        for _ in range(self.number_of_experiments):
            random_m = sample(self.m_range, 1)[0]
            self.m_list.append(random_m)

    def get_numeric_r_range(self,
                            current_m: int) -> range:
        if isinstance(self.r_range[0], str):
            m_extracted = str(self.r_range[0]).replace("m", "")
            if len(m_extracted) > 0:
                r_lower = int(m_extracted) * current_m
            else:
                r_lower = current_m
        else:
            r_lower = self.r_range[0]
        if isinstance(self.r_range[1], str):
            m_extracted = str(self.r_range[1]).replace("m", "")
            if len(m_extracted) > 0:
                r_higher = int(m_extracted) * current_m
            else:
                r_higher = current_m
        else:
            r_higher = self.r_range[1]
        return range(r_lower, r_higher + 1)

    def pseudo_randomly_populate_r_list(self) -> None:
        for i in range(self.number_of_experiments):
            current_m = self.m_list[i]
            if current_m == 1:
                self.r_list.append(1)
            else:
                random_r = sample(self.get_numeric_r_range(current_m), 1)[0]
                self.r_list.append(random_r)

    def get_numeric_M_range(self,
                            current_m: int) -> range:
        if isinstance(self.M_range[0], str):
            m_extracted = str(self.M_range[0]).replace("m", "")
            if len(m_extracted) > 0:
                M_lower = int(m_extracted) * current_m
            else:
                M_lower = current_m
        else:
            M_lower = self.M_range[0]
        if isinstance(self.M_range[1], str):
            m_extracted = str(self.M_range[1]).replace("m", "")
            if len(m_extracted) > 0:
                M_higher = int(m_extracted) * current_m
            else:
                M_higher = current_m
        else:
            M_higher = self.M_range[1]
        return range(M_lower, M_higher + 1)

    def pseudo_randomly_populate_M_list(self) -> None:
        for i in range(self.number_of_experiments):
            current_m = self.m_list[i]
            random_M = sample(self.get_numeric_M_range(current_m), 1)[0]
            self.M_list.append(random_M)

    def calculate_input_size_list(self) -> None:
        for M in self.M_list:
            input_size_in_gb = M * (self.data_block_size_in_megabytes / 1024)
            self.input_size_list.append(int(ceil(input_size_in_gb)))

    def calculate_number_of_nodes_list(self) -> None:
        for i in range(self.number_of_experiments):
            nu = int(ceil((self.m_list[i] + self.r_list[i]) / self.gamma))
            self.number_of_nodes_list.append(nu)

    def generate_experiments_file(self) -> None:
        cp = ConfigParser()  # INIT CONFIGPARSER OBJECT
        cp.optionxform = str  # PRESERVE OPTIONS NAMES' CASE
        for i in range(self.number_of_experiments):
            with open(self.experiments_output_file_path, "w", encoding="utf-8") as file_object:
                cp["Experiment " + str(i+1)] = {
                    "m": str(self.m_list[i]),
                    "r": str(self.r_list[i]),
                    "M": str(self.M_list[i]),
                    "input_size_in_gb": str(self.input_size_list[i]),
                    "number_of_nodes": str(self.number_of_nodes_list[i]),
                    "number_of_slots_per_node": str(self.gamma),
                    "total_number_of_slots": str(self.number_of_nodes_list[i] * self.gamma),
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

    # LOAD GENERAL SETTINGS (number of experiments, data block size in MB, gamma, experiments output file path)
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

    # CALCULATE NUMBER OF NODES LIST
    em.calculate_number_of_nodes_list()

    # GENERATE 'experiments' FILE
    em.generate_experiments_file()

    # DELETE EXPERIMENTS MAKER OBJECT
    del em

    # END
    exit(0)


if __name__ == "__main__":
    main()
