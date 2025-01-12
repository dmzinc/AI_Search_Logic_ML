from pyDatalog import pyDatalog

pyDatalog.clear()

# Define predicates
pyDatalog.create_terms('can_schedule, has_time_slot, assigned, schedule, Lecturer, Class, Time')

# Define facts (example data)
+has_time_slot('Matthew', '9AM-10AM')
+has_time_slot('Matthew', '10AM-11AM')
+has_time_slot('Sophia', '9AM-10AM')
+has_time_slot('Sophia', '11AM-12PM')

+schedule('Intro to Ai', 'Matthew', '9AM-10AM')
+schedule('Applied AI', 'Sophia', '11AM-12PM')

# Define rules
can_schedule(Lecturer, Class, Time) <= has_time_slot(Lecturer, Time) & schedule(Class, Lecturer, Time)

# Function to get a schedule
def get_schedule():
    result = can_schedule(Lecturer, Class, Time)
    print("Query Result:", result)  # Debug print
    return result
