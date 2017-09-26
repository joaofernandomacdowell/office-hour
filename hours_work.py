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
    'input_error': 'ERROR. Departure time must be greater than arrival time',
    'invalid_working_hours': 'ERROR. You worked for less than 1 minute',
    'output_warning': 'WARNING. Your worked for only:',
    'output_success': 'SUCCESS. You worked for:'
}

FMT = '%H:%M'
LUNCH_TIME = datetime.timedelta(0, 5400) # Lunch = 1:30h (5400seg)
WORKING_HOURS = 8

def get_hours_of_work():
    arrival_time, departure_time = _assign_inputs()

    # Check if arrival_time and departure_time is not empty
    if arrival_time and departure_time:
        arrival_time = _string_to_datetime(arrival_time)
        departure_time = _string_to_datetime(departure_time)

        # Check if arrival_time and departure_time are valid
        if _arrival_and_departure_are_valid(arrival_time.hour, departure_time.hour):
            office_hour_td = _calculate_office_hour_td(arrival_time, departure_time)

            # Check if office_hour is valid
            if _office_hour_is_valid(office_hour_td):
                hour_and_minute_tuple = _timedelta_to_hour_minute_tuple(office_hour_td)
                output = _convert_tuple_to_formatted_string(hour_and_minute_tuple)

                if _office_hour_is_completed(hour_and_minute_tuple):
                    _log_msg(COLORS['SUCCESS'], MSGS['output_success'], output)
                else:
                    _log_msg(COLORS['WARNING'], MSGS['output_warning'], output)
            else:
                _log_msg(COLORS['FAIL'], MSGS['invalid_working_hours'])
        else:
            _log_msg(COLORS['FAIL'], MSGS['input_error'])
    else:
        _log_msg(COLORS['FAIL'], MSGS['insufficient_data'])

def _arrival_time_after_lunch(arrival_time):
    if arrival_time == '13:00' or arrival_time == '13:30':
        return True

    return False

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
    if _arrival_time_after_lunch:
        return departure_time - arrival_time
    else:
        return (departure_time - arrival_time) - LUNCH_TIME

def _log_msg(color, msg, value=''):
    text = '{} {} {} {}\n'.format(color, msg, value, COLORS['CLOSE_TAG'])
    sys.stdout.write(text)

def _timedelta_to_hour_minute_tuple(office_hour_timedelta):
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
    formatted_output = datetime_obj.strftime(FMT)

    return '{}h'.format(formatted_output)

def _arrival_and_departure_are_valid(arrival_hour, departure_hour):
    return True if arrival_hour < departure_hour else False

def _office_hour_is_valid(office_hour_timedelta):
    return True if office_hour_timedelta.days != -1 else False

if __name__ == '__main__':
    get_hours_of_work()
