from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from Doctor.models import DoctorSchedule, slot_availability

def add_minutes_to_time(t, m, date):
    return (datetime.combine(date, t) + timedelta(minutes=m)).time()

def generate_slots_for_schedule(schedule):  
    start_date = schedule.start_date
    end_date = schedule.end_date
    start_time = schedule.start_time
    end_time = schedule.end_time
    slot_duration = schedule.slot_duration

    if start_date > end_date:
        raise ValidationError("start_date must be <= end_date")
    if start_time >= end_time:
        raise ValidationError("start_time must be < end_time")

    slots = []
    current_date = start_date

    while current_date <= end_date:
        current_time = start_time

        while current_time < end_time:
            slot_end = add_minutes_to_time(current_time, slot_duration, current_date)
            if slot_end > end_time:
                break

            already_exists = slot_availability.objects.filter(
                schedule=schedule,
                date=current_date,
                start_time=current_time,
                end_time=slot_end
            ).exists()

            if not already_exists:
                slots.append(
                    slot_availability(
                        schedule=schedule,
                        date=current_date,
                        start_time=current_time,
                        end_time=slot_end,
                        is_booked=False
                    )
                )

            current_time = slot_end
        current_date += timedelta(days=1)

    slot_availability.objects.bulk_create(slots)
    return {"message": "Slots generated", "count": len(slots)}