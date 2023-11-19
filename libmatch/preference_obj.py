from __future__ import annotations
# allows use of type hint syntax intoduced in Python 3.9 for earlier Python versions

class PreferenceHaver:
    """
    An entity (student or course) participating in the Match.
    """

    def __init__(self, name: str, weights: dict[PreferenceHaver, float]):
        """
        Present this entity's wishes as a list of weights.
        """
        self.name = name
        self.weights = weights
        self.preferences = list(map(lambda x: x[0], sorted(weights.items(), key=lambda x:-x[1])))

    def get_name(self) -> str:
        """
        Some unique, human-readable name of this entity.
        """
        return self.name


class Student(PreferenceHaver):
    """
    An object to represent students in the match. 

    Attributes:
    - name: string
    - weights: dictionary of courses to weights
    - num_electives: int
    - class_year: int 
    """
    def __init__(self, name: str, weights: dict[Course, float], num_required_courses: int, num_elective_courses: int, class_year : int):
        super().__init__(name, weights)
        self.num_required_courses = num_required_courses
        self.num_elective_courses = num_elective_courses
        self.class_year = class_year

    def __repr__(self) -> str:
        return "'" + self.name + "'"
    
    def get_iterable(self) -> list:
        my_repr_list = [self.name, self.weights, self.num_required_courses, self.num_elective_courses, self.class_year]
        return my_repr_list

class Course(PreferenceHaver):
    """
    An object to represent courses in the match. 

    Attributes:
    - name: string
    - weights: dictionary of students to weights
    - is_elective: bool
    - capacity: int 
    """
    def __init__(self, name: str, weights: dict[Student, float], is_elective: bool, capacity: int):
        super().__init__(name, weights)
        self.is_elective = is_elective
        self.capacity = capacity
    
    def __repr__(self) -> str:
        return "'" + self.name + "'"
    
    def get_iterable(self) -> list:
        my_repr_list = [self.name, self.weights, self.is_elective, self.capacity]
        return my_repr_list