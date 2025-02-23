from typing import Optional

class ImageDetails():
    file_name:str=''
    make:str=''
    model:str=''
    dt:str=''
    aperture_value:str=''
    focal_length:str=''
    exposure_time:str=''
    f_stops:str=''
    iso:str=''
    gps:Optional[str]
    detected_objects:list[dict]
    description:str=''
    generated_with:str=''

    def __init__(self, file_name, make, model, dt, aperture_value, focal_length, exposure_time, f_stops, iso, gps, detected_objects, description, generated_with):
        self.file_name = file_name
        self.make = make
        self.model = model
        self.dt = dt
        self.aperture_value = aperture_value
        self.focal_length = focal_length
        self.exposure_time = exposure_time
        self.f_stops = f_stops
        self.iso = iso
        self.gps = gps
        self.detected_objects = detected_objects
        self.description = description
        self.generated_with = generated_with

    def to_dict(self):
        return {
            'file_name': self.file_name,
            'make': self.make,
            'model': self.model,
            'dt': self.dt,
            'aperture_value': self.aperture_value,
            'focal_length': self.focal_length,
            'exposure_time': self.exposure_time,
            'f_stops': self.f_stops,
            'iso': self.iso,
            'gps': self.gps,
            'detected_objects': self.get_detected_objects_text(),
            'description': self.description,
            'generated_with': self.generated_with
        }

    def get_page_content(self):
        retval = f"{self.get_detected_objects_text()}\n\n{self.description}"
        return retval

    def get_detected_objects_text(self) -> str:
         retval = '\n'.join([f"{item['name']} - {item['description']}" for item in self.detected_objects])
         return retval

    def __str__(self):
        retval = ''
        retval += f'EXIF DATA:\n'
        retval += f"MAKE    : {self.make}\n"
        retval += f"MODEL   : {self.model}\n"
        retval += f"DATE    : {self.dt}\n"
        retval += f"AV      : {self.aperture_value}\n"
        retval += f"TV      : {self.exposure_time}\n"
        retval += f"F/STOPs : {self.f_stops}\n"
        retval += f"ISO     : {self.iso}\n"
        retval += f"GPS     : {self.gps}\n"
        retval += '\n'
        retval += f'DETECTED OBJECTS:\n'
        retval += self.get_detected_objects_text()
        retval += '\n\n'
        retval += f'IMAGE DESCRIPTION:\n'
        retval += self.description
        return retval
