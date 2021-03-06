from enum import Enum

class DoseEntryType(Enum):
    Bolus = 1
    Suspend = 2
    Resume = 3
    TempBasal = 4

class DoseUnit(Enum):
    UnitsPerHour = "U/hour"
    Units = "U"

class DoseEntry:
    def __init__(self, dose_entry_type, start_date, end_date = None, value = None, unit = None, description = None):
        self.dose_entry_type = dose_entry_type
        self.start_date = start_date
        self.end_date = end_date or start_date
        self.value = value
        self.unit = unit
        self.description = description

    def __repr__(self):
        return "%s %s : %f %s for %d minutes" % (self.dose_entry_type.name, self.start_date.isoformat(), self.value, self.unit.name, (self.end_date - self.start_date).total_seconds() / 60)

    def units(self):
        if self.unit == DoseUnit.UnitsPerHour:
            return self.value * ((self.end_date - self.start_date).total_seconds() / 3600)
        else:
            return self.value

    def units_delivered_during_daterange(self, start_date, end_date):
        if self.unit == DoseUnit.Units:
            # Bolus
            if self.start_date >= start_date and self.end_date < end_date:
                return self.value
            else:
                return 0
        elif self.start_date > end_date or self.end_date < start_date:
            # Delivery falls outside of date range entirely
            return 0
        elif self.start_date >= start_date and self.end_date <= end_date:
            # Delivery completely within date range
            return self.units()
        else:
            # Delivery overlaps date range partially
            duration = min(end_date, self.end_date) - max(start_date, self.start_date)
            if duration.total_seconds() < 0:
                return 0
            else:
                return self.value * duration.total_seconds() / 3600
        return

    def as_dict(self):
        return dict(
            dose_entry_type=self.dose_entry_type,
            start_date=self.start_date.isoformat(),
            end_date=self.end_date.isoformat(),
            value=self.value,
            unit=self.unit,
            description=self.description,
            )
