from PIL import ImageFile
from ImageDetails import ImageDetails
from PIL.ExifTags import TAGS, GPSTAGS
from functools import partial

def _get_from_dict(property_name, dict):
    return str(dict[property_name]) if property_name in dict else ''

def _convert_to_decimal(degrees, minutes, seconds, direction):
    decimal = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if direction in ['S', 'W']:
        decimal = -decimal
    return decimal

def _get_exif_data(img: ImageFile) -> dict:
    exif_data = img._getexif()
    if not exif_data:
        return {}
    exif_dict = {}
    for tag, value in exif_data.items():
        tag_name = TAGS.get(tag, tag)
        exif_dict[tag_name] = value
    return exif_dict

def _get_gps_info(exif_dict):
    gps_info = exif_dict.get('GPSInfo', {})
    if not gps_info:
        return None
    gps_data = {}
    for key, value in gps_info.items():
        key_name = GPSTAGS.get(key, key)
        gps_data[key_name] = value
    return gps_data

def _get_coordinates(exif_dict):
    gps_info = _get_gps_info(exif_dict)
    if gps_info and all(k in gps_info for k in ['GPSLatitude','GPSLongitude','GPSLatitudeRef','GPSLongitudeRef']):
        lat_deg, lat_min, lat_sec = gps_info['GPSLatitude']
        lon_deg, lon_min, lon_sec = gps_info['GPSLongitude']
        lat = _convert_to_decimal(lat_deg, lat_min, lat_sec, gps_info['GPSLatitudeRef'])
        lon = _convert_to_decimal(lon_deg, lon_min, lon_sec, gps_info['GPSLongitudeRef'])
        return f"{lat}, {lon}"
    return ''

def _get_exposure_time(exif_dict) -> str:
    if 'ExposureTime' in exif_dict:
        val = exif_dict['ExposureTime']
        return f"{val.numerator}/{val.denominator}"
    return ''

def _get_datetime(exif_dict) -> str:
    if 'DateTime' in exif_dict:
        return exif_dict['DateTime']
    elif 'DateTimeOriginal' in exif_dict:
        return exif_dict['DateTimeOriginal']
    return ''

def create(file_name, img, detected_objects, description, generated_with) -> ImageDetails:
    exif_dict = _get_exif_data(img)
    _get_prop = partial(_get_from_dict, dict=exif_dict)
    make = _get_prop('Make')
    model = _get_prop('Model')
    aperture_value = _get_prop('ApertureValue')
    focal_length = _get_prop('FocalLength')
    f_stops = _get_prop('FNumber')
    iso = _get_prop('ISOSpeedRatings')
    exposure_time = _get_exposure_time(exif_dict)
    dt = _get_datetime(exif_dict)
    gps = _get_coordinates(exif_dict)

    return ImageDetails(
        file_name,
        make,
        model,
        dt,
        aperture_value,
        focal_length,
        exposure_time,
        f_stops,
        iso,
        gps,
        detected_objects,
        description,
        generated_with
    )