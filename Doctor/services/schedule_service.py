from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from Doctor.models import DoctorSchedule, slot_avaibility


def add_minutes_to_time(t, m, date):
    return (datetime.combine(date, t) + timedelta(minutes=m)).time()


def generate_slots_for_schedule(doctor_instance):
    schedules = DoctorSchedule.objects.filter(doctor=doctor_instance)

    if not schedules.exists():
        raise ValidationError("No schedule found for this doctor")

    slots = []

    for schedule in schedules:
        start_date = schedule.start_date
        end_date = schedule.end_date
        start_time = schedule.start_time
        end_time = schedule.end_time
        slot_duration = schedule.slot_duration
        doctor = schedule.doctor

     
        if start_date > end_date:
            raise ValidationError("start_date must be <= end_date")

        if start_time >= end_time:
            raise ValidationError("start_time must be < end_time")

        current_date = start_date
        while current_date <= end_date:
            current_time = start_time
            while current_time < end_time:
                slot_end = add_minutes_to_time(current_time, slot_duration, current_date)
                if slot_end > end_time:
                    break
                slots.append(
                    slot_avaibility(
                        doctor=doctor,
                        date=current_date,
                        start_time=current_time,
                        end_time=slot_end,
                        is_booked=False
                    )
                )
                current_time = slot_end
            current_date += timedelta(days=1)

    slot_avaibility.objects.bulk_create(slots)
    return {"message": "Slots generated", "count": len(slots)}