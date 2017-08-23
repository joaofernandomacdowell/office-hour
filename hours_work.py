# coding: utf-8

import sys
import datetime

COLORS = {
    'COMMON': '\x1b[0;37;40m',
    'FAIL': '\x1b[1;31;40m',
    'WARNING': '\x1b[6;30;43m',
    'SUCCESS': '\x1b[5;30;42m'
}

MSGS = {
    'input_arrival_time': 'Enter with your arrival time. (Ex: 09:00)',
    'input_departure_time': 'Enter with your departure time. (Ex: 18:30)',
    'insufficient_data': 'ERROR. Specify your arrival time and departure time.',
    'output_fail': 'Incorrect data format, should be HH:MM. Ex: 09:30',
    'output_warning': 'WARNING. Your worked for only:',
    'output_success': 'SUCCESS. You worked for:'
}

lunch_time = datetime.timedelta(0, 5400) # Lunch = 1:30h (5400seg)

def hours_of_work():
    arrival_time, departure_time = assign_inputs()

    if arrival_time and departure_time:
        arrival_time = string_to_datetime(arrival_time)
        departure_time = string_to_datetime(departure_time)

        office_hour = calculate_office_hour(arrival_time, departure_time)

        if office_hour_is_valid(office_hour):
            log_msg(COLORS['SUCCESS'], MSGS['output_success'], office_hour)
        else:
            log_msg(COLORS['WARNING'], MSGS['output_warning'], office_hour)
    else:
        log_msg(COLORS['FAIL'], MSGS['insufficient_data'])

def assign_inputs():
    log_msg(COLORS['COMMON'], MSGS['input_arrival_time'])
    arrival_time = raw_input()
    print('---------------------------------------------------')

    log_msg(COLORS['COMMON'], MSGS['input_departure_time'])
    departure_time = raw_input()
    print('---------------------------------------------------')

    return arrival_time, departure_time

def string_to_datetime(time_string):
    try:
        datetime_obj = datetime.datetime.strptime(time_string, '%H:%M')
    except ValueError:
        raise ValueError(COLORS['FAIL'] + MSGS['output_fail'])

    return datetime_obj

def calculate_office_hour(arrival_time, departure_time):
    work_seconds = (departure_time - arrival_time) - lunch_time
    return str(work_seconds)[0:4] + 'h'

def log_msg(color, msg, value=''):
    text = '{} {} {} {}\n'.format(color, msg, value, '\x1b[0m')
    sys.stdout.write(text)

def office_hour_is_valid(office_hour):
    return office_hour[0] >= '6'

if __name__ == '__main__':
    hours_of_work()
