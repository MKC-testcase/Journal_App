import configparser
from pathlib import Path

# Refer to: https://www.geeksforgeeks.org/how-to-write-a-configuration-file-in-python/

def write_database_config():
    """Writes a config file based on the key value pairs provided"""
    # if len(keys) != len(values):
    #     return
    config = configparser.ConfigParser()
    # creating the config content
    # Below are fake config parameters
    config['Database'] = {'server': 'ServerName', 'database': "PizzaShop",
                          'username': "Joe", 'password': "secure_password"}

    # writing the config file
    destination_path = Path(__file__).parents[1]
    destination_path = str(destination_path) + '/controller/Journal/config.ini'
    with open(destination_path, 'w') as configfile:
        config.write(configfile)


def read_database_config():
    """Reads the config file for the database and returns the dictionary"""
    config = configparser.ConfigParser()

    # navigate to the area with the config file
    destination_path = Path(__file__).parents[1]
    destination_path = str(destination_path) + '/controller/Journal/config.ini'
    config.read(destination_path)

    server_name = config.get('Database', 'server')
    database_name = config.get('Database', 'database')
    username = config.get('Database', 'username')
    password = config.get('Database', 'password')

    config_dict = {
        'server_name': server_name,
        'database_name': database_name,
        'username': username,
        'password': password
    }
    return config_dict


if __name__ == "__main__":
    # write_database_config()
    temp = read_database_config()
    print(temp)