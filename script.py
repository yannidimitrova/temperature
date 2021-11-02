if __name__ == '__main__':
    import pytz
    from pytz import all_timezones
    from argparse import ArgumentParser

    import dateutil.parser
    from geopy.geocoders import Nominatim
    from timezonefinder import TimezoneFinder


    def get_timezone(city):
            local_timezone = ''
            for tz in all_timezones:
                if city in tz:
                    local_timezone = tz
                    break
            if not local_timezone:
                geolocator = Nominatim(user_agent="myname")
                location = geolocator.geocode(city)
                timezone_object = TimezoneFinder()
                local_timezone = timezone_object.timezone_at(lng=location.longitude, lat=location.latitude)
            local_timezone = pytz.timezone(local_timezone)
            return local_timezone


    def get_datetime(datetime_string, city):
        datetime_to_datetime_format = dateutil.parser.parse(datetime_string)
        dt_correct_timezone = datetime_to_datetime_format.astimezone(get_timezone(city))
        return str(dt_correct_timezone)


    def get_temperature_in_fahrenheit(temperature):
        if "C" in temperature:
            celsius_number = ''.join(element for element in temperature if element.isdigit())
            fahrenheit_number = str(int(float(celsius_number) * 1.8 + 32)) + "F\n"
            return fahrenheit_number
        return temperature


    def converter(input_file, output_file_name):
        input = open(f"input_files/{input_file}.csv", "rt")
        output = open(f"output_files/{output_file_name}.csv", "wt")

        for line in input:
            elements_in_line = line.split(",")

            """ Datetime """
            city = elements_in_line[0]
            datetime_string = elements_in_line[1].strip()
            elements_in_line[1] = get_datetime(datetime_string, city)

            """ Temperature in Fahrenheit """
            temperature = elements_in_line[2]
            elements_in_line[2] = get_temperature_in_fahrenheit(temperature)

            output.write(','.join(elements_in_line))
        input.close()
        output.close()


    parser = ArgumentParser()
    parser.add_argument("-input_file")
    parser.add_argument("-output_file_name")
    args = parser.parse_args()

    input_file = getattr(args, "input_file")
    output_file_name = getattr(args, "output_file_name")

    converter(input_file, output_file_name)