# coding: utf-8

import sys
import datetime

COLORS = {
    'COMMON': '\x1b[0;37;40m',
    'FAIL': '\x1b[1;31;40m',
    'WARNING': '\x1b[6;30;43m',
    'SUCCESS': '\x1b[5;30;42m',
    'CLOSE_TAG': '\x1b[0m'
}

MSGS = {
    'input_arrival_time': 'Enter with your arrival time. (Ex: 09:00)',
    'input_departure_time': 'Enter with your departure time. (Ex: 18:30)',
    'insufficient_data': 'ERROR. Specify your arrival time and departure time.',
    'output_fail': 'Incorrect data format, should be HH:MM. Ex: 09:30',
    'output_warning': 'WARNING. Your worked for only:',
    'output_success': 'SUCCESS. You worked for:'
}

FMT = '%H:%M'
LUNCH_TIME = datetime.timedelta(0, 5400) # Lunch = 1:30h (5400seg)
WORKING_HOURS = 8

def hours_of_work():
    arrival_time, departure_time = _assign_inputs()

    if arrival_time and departure_time:
        arrival_time = _string_to_datetime(arrival_time)
        departure_time = _string_to_datetime(departure_time)

        office_hour_td = _calculate_office_hour_td(arrival_time, departure_time)
        hour_and_minute_tuple = _timedelta_to_tuple(office_hour_td)
        output = _convert_tuple_to_formatted_string(hour_and_minute_tuple)

        if _office_hour_is_completed(hour_and_minute_tuple):
            _log_msg(COLORS['SUCCESS'], MSGS['output_success'], output)
        else:
            _log_msg(COLORS['WARNING'], MSGS['output_warning'], output)
    else:
        _log_msg(COLORS['FAIL'], MSGS['insufficient_data'])

def _assign_inputs():
    _log_msg(COLORS['COMMON'], MSGS['input_arrival_time'])
    arrival_time = input()
    print('---------------------------------------------------')

    _log_msg(COLORS['COMMON'], MSGS['input_departure_time'])
    departure_time = input()
    print('---------------------------------------------------')

    return arrival_time, departure_time

def _string_to_datetime(time_string):
    try:
        datetime_obj = datetime.datetime.strptime(time_string, FMT)
    except ValueError:
        _log_msg(COLORS['FAIL'], MSGS['output_fail'])
        sys.exit(1)

    return datetime_obj

def _calculate_office_hour_td(arrival_time, departure_time):
    return (departure_time - arrival_time) - LUNCH_TIME

def _log_msg(color, msg, value=''):
    text = '{} {} {} {}\n'.format(color, msg, value, COLORS['CLOSE_TAG'])
    sys.stdout.write(text)

def _timedelta_to_tuple(office_hour_timedelta):
    hours = office_hour_timedelta.seconds // 3600
    minutes = (office_hour_timedelta.seconds // 60) % 60

    return hours, minutes

def _office_hour_is_completed(office_hour_tuple):
    return office_hour_tuple[0] >= WORKING_HOURS

def _tuple_to_string(office_hour_tuple):
    hour_str = str(office_hour_tuple[0])
    minute_str = str(office_hour_tuple[1])

    return '{}:{}'.format(hour_str, minute_str)

def _convert_tuple_to_formatted_string(hour_and_minute_tuple):
    office_hour_str = _tuple_to_string(hour_and_minute_tuple)
    datetime_obj = _string_to_datetime(office_hour_str)
    hour_minute = datetime_obj.strftime(FMT)

    return '{}h'.format(hour_minute)

if __name__ == '__main__':
    hours_of_work()
