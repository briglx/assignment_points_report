#!/usr/bin/python
"""Filter grades"""
import csv

from bs4 import BeautifulSoup
from bs4 import Tag as bs4Tag


def main():

    # full_file_name = os.path.join(folder_name, file_name)
    with open("grades.html", "r", encoding="utf8") as html_file:

        with open("grades_filtered.csv", "w", encoding="utf8") as filtered_file:
            writer = csv.writer(filtered_file)

            header = (
                "assignment_date",
                "course_name",
                "assignment_name",
                "points_earned",
                "points_possible",
                "assignment_percent",
            )
            writer.writerow(header)

            soup = BeautifulSoup(html_file, "html.parser")

            assignments = soup.find_all(attrs={"class": "assignment__row"})

            for assignment in assignments:

                assignment_date = ""
                assignment_class = ""
                assignment_name = ""
                assignment_points_earned = ""
                assignment_points_possible = ""
                assignment_percent = ""

                parent = assignment.find_parent("app-assignment")
                prev_sibs = parent.previous_siblings
                for prev_sibs in parent.previous_siblings:
                    if type(prev_sibs) is bs4Tag:
                        assignment_date = prev_sibs.text.strip()
                        assignment_date = assignment_date.replace("Today", "")
                        break

                assignment_name = assignment.find(
                    attrs={"class": "assignment__largeScreen--cell-assignmentName"}
                ).text.strip()
                assignment_class = assignment.find(
                    attrs={"class": "assignment__largeScreen--cell-courseDueDate"}
                ).text.strip()
                assignment_scores_el = assignment.find_all(
                    attrs={"class": "assignment-score__score"}
                )

                for assignment_score_el in assignment_scores_el:
                    assignment_scores_text = assignment_score_el.text.strip()

                    if "/" in assignment_scores_text:
                        assignment_points = assignment_scores_text.split("/")
                        assignment_points_earned = assignment_points[0]
                        assignment_points_possible = assignment_points[1]

                    if "(" in assignment_scores_text:
                        assignment_percent = assignment_scores_text[1:-1]

                # assignment_points  = assignment_scores[0].text.strip()
                # if len(assignment_points) > 0:
                #     assignment_points = assignment_scores[0].text.strip().split('/')
                #     assignment_points_earned =  assignment_points[0]
                #     assignment_points_possible = assignment_points[1]

                #     assignment_percent = assignment_scores[1].text.strip()
                #     assignment_percent = assignment_percent[1:-1]

                # else:
                #     assignment_points_earned = ""
                #     assignment_points_possible = ""
                #     assignment_percent = ""

                row = (
                    assignment_date,
                    assignment_class,
                    assignment_name,
                    assignment_points_earned,
                    assignment_points_possible,
                    assignment_percent,
                )
                writer.writerow(row)


if __name__ == "__main__":

    main()
