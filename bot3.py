from datetime import datetime, timedelta
from collections import UserDict

class Field:
    def __init__(self, value=None):
        self.value = value

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if self.is_valid_phone(new_value):
            self.__value = new_value

    def is_valid_phone(self, phone):
        if phone.isdigit():
            return True

class Birthday(Field):
    def __init__(self, birthday):
        self.value = None
        self.set_birthday(birthday)
        
    def set_birthday(self, birthday):
        # Додайте перевірку на коректність дня народження
        if self.is_valid_birthday(birthday):
            self.value = birthday
        else:
            raise ValueError("Invalid birthday")

    def is_valid_birthday(self, birthday):
        return True 

class Record:
    def __init__(self, name, phone, birthday=None):
        self.name = Name(name)
        self.phone = Phone(phone)
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        self.phone.set_phone(phone)

    def remove_phone(self, phone):
        if self.phone.value == phone:
            self.phone.value = None

    def edit_phone(self, old_phone, new_phone):
        if self.phone.value == old_phone:
            self.phone.set_phone(new_phone)

    def days_to_birthday(self):
        if self.birthday.value:
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            next_birthday = datetime.strptime(self.birthday.value, "%Y-%m-%d").replace(year=today.year)
            if today > next_birthday:
                next_birthday = next_birthday.replace(year=today.year + 1)
            days_left = (next_birthday - today).days
            return days_left
        else:
            return None

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def remove_record(self, record_name):
        if record_name in self.data:
            del self.data[record_name]

    def get_record(self, record_name):
        return self.data.get(record_name)

    def __getitem__(self, record_name):
        return self.get_record(record_name)

    def __iter__(self):
        self._iter_index = 0
        self._items = list(self.data.values())
        return self

    def __next__(self):
        if self._iter_index < len(self._items):
            result = self._items[self._iter_index]
            self._iter_index += 1
            return result
        else:
            raise StopIteration

# Test code
if __name__ == "__main__":
    ab = AddressBook()
    rec1 = Record('Bill', '1234567890', '1990-08-15')
    rec2 = Record('Alice', '9876543210', '1995-10-20')
    ab.add_record(rec1)
    ab.add_record(rec2)
    
    for record in ab:
        print(record.name.value, record.phone.value, record.days_to_birthday())
