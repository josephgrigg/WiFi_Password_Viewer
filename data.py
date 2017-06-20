import subprocess
import pickle
import sys
import os
import cmd_prompt_method as cpm


program_directory = sys.path[0]
os.chdir(program_directory)


class Data:
    data_collection_method = 'xml'

    def __init__(self):
        self.network_info = self.collect_network_info()

    def collect_network_info(self):
        if Data.data_collection_method == 'cmd':
            data = cpm.get_networks_and_pwds()

        elif Data.data_collection_method == 'xml':
            # Decrypt the XML wifi passwords under System context.
            subprocess.call('psexec.exe -i -s cmd.exe /c \"cd \"%s\" & python xml_decryption_method.py\"' % program_directory)
            # Load the pickled network data that was just saved.
            with open('data_pickle.p', 'rb') as pfile:
                data = pickle.load(pfile)
            # Delete the pickle file after it has been loaded.
            os.remove('data_pickle.p')

        else:
            data = []

        return data
