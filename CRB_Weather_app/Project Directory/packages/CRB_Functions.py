import requests
import os
from tqdm import tqdm
import json
import csv
import utm
import math
import subprocess

THREE_HOUR_SWITCH = 36
LATEST_HOUR = 84


def download_grib_request(url, file_name, default_folder='input_data'):

    with requests.get(url, stream=True) as r:
        chunkSize = 1024
        with open(get_path_dir(default_folder, file_name), 'wb') as raw_file:
            for chunk in tqdm(iterable=r.iter_content(chunk_size=chunkSize), unit='KB', desc="Downloading %s" %file_name):
                raw_file.write(chunk)


def get_path_dir(directory, file_name, create=True):
    # Gets the path of the working directory (i.e. AgAuto's working directory).
    cwd = os.getcwd()
    # Add directory to the working directory path.
    file_base_dir = os.path.join(cwd, directory)
    # Add file_name to the new path created above.
    file_path = os.path.join(file_base_dir, file_name)

    # If the directory doesn't exist then raise an Exception.
    if not os.path.exists(file_base_dir):
        raise Exception('Directory %s does not exist within working directory.' % directory)
    # Raise an exception only if the user specifies create = False. Otherwise, assume they will create after.
    if not create:
        if not os.path.exists(file_path):
            raise Exception('File %s does not exist within %s.' % (file_name, directory))

    return file_path


def grib_grab(file_name, date):

    url_test = "https://nomads.ncep.noaa.gov/cgi-bin/filter_nam.pl?file=FILENAME&var_HGT=on&var_" \
               "HPBL=on&var_UGRD=on&var_VGRD=on&var_VRATE=on&subregion=&leftlon=-101.7&rightlon=-95.1&toplat=" \
               "52.9&bottomlat=48.9&dir=%2Fnam.YYYYMMDD"

    url_test = url_test.replace('FILENAME', file_name)
    url_test = url_test.replace('YYYYMMDD', date)

    download_grib_request(url_test, 'grib_test.grib2')
    subprocess.call(r'C:\Users\CAmao\Documents\CRB_Weather_app\CRB_Weather_app\Project Directory\1_download_data.bat')


def get_municipalities():

    file_name = 'municipalities.json'
    muni_set = []
    with open(file_name) as json_file:
        contents = json.load(json_file)
        for each in contents:
            if each['muni_name'] not in muni_set:
                muni_set.append(each['muni_name'])

    with open(get_path_dir('input_data', 'input_muni.csv'), 'wb') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(['Municipality', 'Longitude', 'Latitude'])
        for each in muni_set:
            writer.writerow([each, '', ''])


def create_lat_long_csv():
    input_muni = 'input_muni.csv'
    centroid_table = 'RM_Centroid_Table.csv'
    output_muni = 'muni_lat_lon.csv'
    muni_array = []
    muni_dict = {}
    with open(get_path_dir('input_data', input_muni)) as muni_list:
        reader = csv.reader(muni_list, delimiter=',')
        for each in reader:
            muni_array.append(each[0])

    with open(get_path_dir('input_data',centroid_table)) as centroid_csv:
        reader = csv.reader(centroid_csv, delimiter='\t')
        for each in reader:
            x_utm = int(each[-2])
            y_utm = int(each[-1])
            lat_lon = utm.to_latlon(x_utm, y_utm, 14, 'U')
            if each[2] in muni_array:
                muni_dict[each[2]] = '%f|%f' % (lat_lon[0], lat_lon[1])

    with open(get_path_dir('input_data', output_muni), 'wb') as output_csv:
        writer = csv.writer(output_csv, delimiter=',')
        writer.writerow(['Municipality', 'Latitude', 'Longitude'])
        for each in muni_array:
            value_array = muni_dict[each].split('|')
            lat = value_array[0]
            lon = value_array[1]
            writer.writerow([each, lat, lon])


def isclose(a, b, rel_tol=0.0625, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)


def init_muni_dict():
    muni_dict = {}
    muni_file_name = 'muni_lat_lon.csv'
    muni_array = []

    with open(get_path_dir('input_data', muni_file_name)) as muni_csv:
        reader = csv.reader(muni_csv, delimiter=',')
        for each in reader:
            if each[0] != 'Municipality':
                muni_dict[each[0]] = [float(each[1]), float(each[2])]
                muni_array.append(each[0])

    return muni_dict, muni_array


def get_muni_data(filename, default_folder='input_data'):
    data_list = []
    with open(get_path_dir(default_folder, filename)) as test_csv:
        reader = csv.reader(test_csv, delimiter=',')
        for each in reader:
            if each[0].strip() != 'X':
                data_list.append(each)

    return data_list


def calc_d_haversine(lat1, lon1, lat2, lon2):

    EARTH_RADIUS = 6371  # KM
    a = math.sin(math.radians((lat2-lat1)/2))**2 + math.cos(math.radians(lat1)) *\
        math.cos(math.radians(lat2))*math.sin(math.radians((lon2-lon1)/2))**2

    c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

    return EARTH_RADIUS*c


def initialize_data_indices():
    muni_dict, muni_array = init_muni_dict()
    muni_indices = {}
    data_list = get_muni_data('1_HGT_reserved.csv')
    for each in muni_array:
        muni_lat = muni_dict[each][0]
        muni_lon = muni_dict[each][1]
        total_abs_diff = 6371
        previous_diff = total_abs_diff
        index = 0
        for each_data in data_list:
            lat = float(each_data[-3])
            lon = float(each_data[-2])
            total_abs_diff = calc_d_haversine(muni_lat, muni_lon, lat, lon)
            if total_abs_diff < previous_diff:
                muni_indices[each] = index
                previous_diff = total_abs_diff
            index += 1

    return muni_indices


def get_delta_distance():
    muni_dict, muni_array = CRB.init_muni_dict()
    muni_indices = {}
    results = []
    data_list = CRB.get_muni_data('1_HGT_reserved.csv')
    for each in muni_array:
        muni_lat = muni_dict[each][0]
        muni_lon = muni_dict[each][1]
        total_abs_diff = 6371
        previous_diff = total_abs_diff
        index = 0
        data_entry = ""
        for each_data in data_list:
            lat = float(each_data[-3])
            lon = float(each_data[-2])
            total_abs_diff = CRB.calc_d_haversine(muni_lat, muni_lon, lat, lon)
            if total_abs_diff < previous_diff:
                data_entry = 'Muni: %s | Muni_lat: %s | Muni_long: %s | data_lat: %s | data_long  %s | dist: %.2f' % (
                    each, muni_lat, muni_lon, lat, lon, total_abs_diff)
                muni_indices[each] = index
                previous_diff = total_abs_diff
            index += 1
        results.append(data_entry)

    for each in results:
        print each


def update_json_data(date, hour_hh):
    iterables = get_iterable_hours()
    file_name = 'nam.tHOUR_HHz.awphysXX.tm00.grib2'.replace('HOUR_HH', hour_hh)
    file_name_new = file_name.replace('XX', str(iterables[0]).zfill(2))
    progress_size = len(iterables)

    for hour_iter in tqdm(iterables, total=progress_size, desc="Parsing %s" % file_name_new):
        file_name_new = file_name.replace('XX', str(hour_iter).zfill(2))
        grib_grab(file_name_new, date)
        # build nested dictionary.
        # build json file.
        # overwrite old json file.


def get_iterable_hours():
    hour = 0
    iterables = []
    while hour <= LATEST_HOUR:
        iterables.append(hour)
        if hour < THREE_HOUR_SWITCH:
            hour += 1
        else:
            hour += 3
    return iterables


def build_variable(file_name, default_folder='input_data'):
    return ""
