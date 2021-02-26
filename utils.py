from typing import Dict, List


class Street:
    def __init__(
        self, id: int, name: str, int_from: int, int_to: int, time: int
    ) -> None:
        self.id = id
        self.name = name
        self.int_from = int_from
        self.int_to = int_to
        self.time = time

    def __lt__(self, other):
        return self.id < other.id

    def __repr__(self):
        return f"Street {self.id} - {self.name} from {self.int_from} to {self.int_to} with time {self.time}"

    def setTLDuration(self):
        return


class Car:
    def __init__(self, id: int, num_path: int, path: List[Street]) -> None:
        self.id = id
        self.num_path = num_path
        self.path = path
        self.path_time = 0

    def __repr__(self):
        return f"Car {self.id} drives through {self.num_path} streets"

    def getLength(self):
        length = 0
        for i, street in enumerate(self.path):
            if i > 0:
                length += street.time
        return length

    def __lt__(self, other):
        return self.path_time < other.path_time


class Intersection:
    def __init__(self, id) -> None:
        self.id = id
        self.different_incoming_streets = None
        self.TL = dict()  # street: [start time, end time]

    def print(self) -> str:
        output = ""
        output += str(self.id) + "\n"
        output += str(len(self.TL)) + "\n"
        for street, time_range in self.TL.items():
            output += street + " " + str(time_range[1] - time_range[0])
            output += "\n"
        return output

    def isConflict(self, time_range: List[int]):
        for _, time in self.TL.items():
            if time_range[0] >= time[0] and time_range[0] < time[1]:
                return True
            if time[0] >= time_range[0] and time[0] < time_range[1]:
                return True
        return False


def readIn(filename):
    """
    returns:
        basic_info: List[int]: D, I, S, V, F
        street_list: List[Street]
        vehicle_list: List[Vehicle]
    """
    infile = open(filename, "r")

    lines = infile.readlines()

    basic_info = lines[0].split()
    basic_info = list(map(int, basic_info))

    num_streets = basic_info[2]
    num_vehicles = basic_info[3]

    street_list = []
    vehicle_list = []

    for i in range(1, num_streets + 1):
        st_info = lines[i].split()
        st = Street(
            id=i - 1,
            int_from=int(st_info[0]),
            int_to=int(st_info[1]),
            name=st_info[2],
            time=int(st_info[3]),
        )
        street_list.append(st)

    street_names = [getattr(street, "name") for street in street_list]

    for i in range(num_streets + 1, num_streets + num_vehicles + 1):
        car_info = lines[i].split()
        path_names = car_info[1:]
        path = [street_list[street_names.index(name)] for name in path_names]
        car = Car(id=i - num_streets, num_path=int(car_info[0]), path=path)
        vehicle_list.append(car)

    return basic_info, street_list, vehicle_list


def writeOut(out_file: str, result):
    print("result of ", out_file, "\n")
    with open(f"{out_file}_output", "w") as f:
        f.write(str(len(result)) + "\n")
        for _, intersection in result.items():
            f.write(intersection.print())

