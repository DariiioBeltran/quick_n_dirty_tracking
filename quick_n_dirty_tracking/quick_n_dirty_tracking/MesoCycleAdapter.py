import yaml
import os
import fire
from utils import get_sheet, calculate_col_letter_from_idx, create_sheet, load_workout_from_yaml_file
from models import WorkoutSchema
from dotenv import load_dotenv


class MesoCycleAdapter:
    def __init__(
        self, 
        mesocycle_name: str, # The Yaml File
        sheet_id: str | None = None # Sheet Id For Analysis
    ):
        self.sheet_id = sheet_id
        assert mesocycle_name, f"You must name your mesocycle"
        assert mesocycle_name != "mesocycle_template", f"This is the template provided, please choose another name"
        self.mesocycle_name = mesocycle_name
        # load mesocycle data from yaml file
        self.meso = load_workout_from_yaml_file(mesocycle_name)
        if not sheet_id:
            dotenv_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', '.env'))
            load_dotenv(dotenv_path)
            GMAIL = os.environ.get("GMAIL")
            self.full_sheet = create_sheet(self.meso.mesocycle_name)
            self.full_sheet.share(
                email_address=GMAIL,
                perm_type="user",
                role="writer",
                notify=True,
                email_message=None,
                with_link=True
            )
            print(f"\n\nCreated new sheet for mesocylce here: {self.full_sheet.url}")
            print(f"You can expect an email granting you access once the command finished running.\n\n")
        else:
            self.full_sheet = get_sheet(sheet_id)
            print(f"Successfully fetched the sheet from Google.")

    def _create_workout_sheet(self, workout: WorkoutSchema) -> None:
        total_cols = 2*sum([exercise.sets for exercise in workout.exercises]) + 1
        self.full_sheet.add_worksheet(title=workout.workout_name, rows=100, cols=total_cols)
        workout_sheet = self.full_sheet.worksheet(workout.workout_name)

        start_col = "A"
        end_col = calculate_col_letter_from_idx(total_cols)

        # Merge all cells and set "title" in first row
        title_range = f"{start_col}1:{end_col}1"
        workout_sheet.merge_cells(title_range)
        workout_sheet.update_cell(1,1,workout.workout_name)
        workout_sheet.format(title_range, {
            "horizontalAlignment": "CENTER",
        }) # TODO: add more formatting to make the generated sheets pretty out the box

        # Populate the weight/reps/exercise columns for tracking
        values = ["Date"]
        for exercise in workout.exercises:
            for s in range(exercise.sets):
                values += [
                    f"{exercise.exercise_name}, Weight",
                    f"{exercise.exercise_name}, Reps",
                ]

        workout_sheet.update(
            values=[values],
            range_name=f"A2:{end_col}2",
        )

    def _delete_default_sheet1(self, workouts: list[WorkoutSchema]) -> None:
        current_ws = set([ws.title for ws in self.full_sheet.worksheets()])
        workout_names = set([workout.workout_name for workout in workouts])
        if (
            "Sheet1" in current_ws
            and "Sheet1" not in workout_names
        ):
            sheet1 = self.full_sheet.worksheet("Sheet1")
            self.full_sheet.del_worksheet(sheet1)

    def setup_mesocycle_sheets(self) -> None:
        assert not self.sheet_id, f"To avoid conflicts during mesocycle setup don't pass in an existing sheet's id, we'll create a new sheet"
        for workout in self.meso.workouts:
            self._create_workout_sheet(workout)

        # Delete the default "Sheet1" that gets created by default by Google
        self._delete_default_sheet1(self.meso.workouts)


if __name__ == '__main__':
    fire.Fire(MesoCycleAdapter)
