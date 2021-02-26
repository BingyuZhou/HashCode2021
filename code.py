from utils import (
    Intersection,
    Street,
    Car,
    readIn,
    writeOut,
)
from typing import List
import numpy as np
import os


def sortCar(sim_time: int, car_list: List):
    """
    based on path. shorter path, better reward
    considering sim_time
    """
    for car in car_list:
        car.path_time = car.getLength()

    cars_sorted = sorted(car_list)
    cars_sorted = [c for c in cars_sorted if c.path_time <= sim_time]

    return cars_sorted


def simOneCar(car: Car) -> List:
    """
    sim the car along the path.
    assume you can turn on one TL.

    return:
    [(time, intersection_id, street_id)]
    """
    car_path_info = []
    time_accumulated = 0
    for i in range(car.num_path):
        street_name = car.path[i].name
        intersection_id = car.path[i].int_to
        car_path_info.append((time_accumulated, intersection_id, street_name))
        time_accumulated += car.path[i].time
    return car_path_info


def solve(sim_time, bonus, street_list, car_list):

    cars = sortCar(sim_time, car_list)

    schedule = simOneCar(cars[0])

    result = {}
    for s in schedule:
        interaction = Intersection(s[1])
        interaction.TL[s[2]] = [s[0], sim_time]
        result[s[1]] = interaction

    for car in cars[1:]:
        new_schedule = simOneCar(car)

        for schedule_i in new_schedule:
            timestamp, intersection_id, street_id = schedule_i
            if intersection_id in result:
                # update traffic to solve conflicts
                intersection = result[intersection_id]
                if street_id in intersection.TL:
                    # same street
                    old_time = intersection.TL[street_id]
                    new_time = [
                        min(timestamp, old_time[0]),
                        max(timestamp, old_time[1]),
                    ]

                    if not intersection.isConflict(
                        new_time[0]
                    ) and not intersection.isConflict(new_time[1]):
                        intersection.TL[street_id] = new_time
                else:
                    if not intersection.isConflict(timestamp):
                        intersection.TL[street_id] = [timestamp, timestamp + 1]
            else:
                intersection = Intersection(intersection_id)
                intersection.TL[street_id] = [timestamp, timestamp + 1]
                result[intersection_id] = intersection

    return result


if __name__ == "__main__":
    directory = "quali/"
    for file in os.listdir(directory):
        basic_info, street_list, car_list = readIn(directory + file)
        sim_time = basic_info[0]
        bonus = basic_info[-1]

        result = solve(sim_time, bonus, street_list, car_list)
        writeOut("output/" + file[0], result)
