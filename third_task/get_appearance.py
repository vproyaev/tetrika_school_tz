from dataclasses import dataclass

data = {
    'lesson': [2800, 6400],
    'pupil': [
        2789, 4500, 2807, 4542, 4512, 4513,
        4564, 5150, 4581, 4582, 4734, 5009,
        5095, 5096, 5106, 6480, 5158, 5773,
        5849, 6480, 6500, 6875, 6502, 6503,
        6524, 6524, 6579, 6641
    ],
    'tutor': [
        35, 364, 2749, 5148, 5149, 6463
    ]
}


@dataclass
class Interval:
    START: int
    END: int


@dataclass
class Lesson:
    START: int
    END: int


@dataclass
class LessonMember:
    LESSON: Lesson
    INPUT_INTERVALS: list[int]

    def __post_init__(self) -> None:
        self.INTERVALS = []
        for interval in range(0, len(self.INPUT_INTERVALS), 2):
            interval_start = self.INPUT_INTERVALS[interval]
            interval_end = self.INPUT_INTERVALS[interval + 1]

            if (
                interval_start > self.LESSON.END
                or interval_end < self.LESSON.START
            ):
                continue

            if interval_start < self.LESSON.START:
                interval_start = self.LESSON.START

            if interval_end > self.LESSON.END:
                interval_end = self.LESSON.END

            if self.INTERVALS:
                previous_interval = self.INTERVALS[-1]
                if (
                    previous_interval.START
                    < interval_start
                    < previous_interval.END
                    and previous_interval.START
                    < interval_end
                    < previous_interval.END
                ):
                    continue

                if previous_interval.END > interval_start:
                    previous_interval.END = interval_end
                    continue

            self.INTERVALS.append(Interval(interval_start, interval_end))


def get_intersections(pupil: LessonMember, tutor: LessonMember) -> int:
    intersections_time = 0

    for tutor_interval in tutor.INTERVALS:
        for pupil_interval in pupil.INTERVALS:
            if (
                tutor_interval.END < pupil_interval.START
                or pupil_interval.END < tutor_interval.START
            ):
                continue

            pupil_time_interval = pupil_interval.END - pupil_interval.START

            if pupil_interval.START > tutor_interval.START:
                possible_intersections = (
                    tutor_interval.END - pupil_interval.START
                )
            else:
                possible_intersections = (
                    pupil_interval.END - tutor_interval.START
                )

            if possible_intersections > pupil_time_interval:
                intersections_time += pupil_time_interval
            else:
                intersections_time += possible_intersections

    return intersections_time


def appearance(lesson_data: dict[str, list[int]]) -> int:
    lesson = Lesson(*lesson_data.get('lesson'))
    pupil = LessonMember(lesson, lesson_data.get('pupil'))
    tutor = LessonMember(lesson, lesson_data.get('tutor'))

    intersections = get_intersections(pupil, tutor)

    return intersections
