from pymongo import MongoClient

class DatabaseHandler:
    def __init__(self):
        self.client = MongoClient("mongodb+srv://red:blxgre369@cluster0-oaiys.mongodb.net/test?retryWrites=true")
        self.form_db = self.client.formula
        self.pit_col = self.form_db.pitstop

    def calculate_and_store(self, tire_params=None, race_params=None):
        if (tire_params or race_params) is None:
            return None

        tire_cond = tire_params.get("tire_cond")
        tire_type = tire_params.get("tire_type")

        current_lap = race_params.get("current_lap")
        total_laps = race_params.get("total_laps")

        pit_message = ""
        race_control = ""
        next_tire_sel = ""

        if 0.75*total_laps <= current_lap < total_laps:
            if tire_type is "SOFT":
                race_control = "CRITICAL"
                next_tire_sel = "SOFT"
            elif tire_type is "MEDIUM":
                race_control = "CRITICAL"
                next_tire_sel = "SOFT"
            elif tire_type is "HARD":
                race_control = "CONSERVE"
                next_tire_sel = "SOFT"
        elif 0.5*total_laps <= current_lap < 0.75*total_laps:
            if tire_type is "SOFT":
                race_control = "CONSERVE"
                next_tire_sel = "MEDIUM"
            elif tire_type is "MEDIUM":
                race_control = "CONSERVE"
                next_tire_sel = "SOFT"
            elif tire_type is "HARD":
                race_control = "PUSH"
                next_tire_sel = "SOFT"
        else:
            if tire_type is "SOFT":
                race_control = "PUSH"
                next_tire_sel = "MEDIUM"
            elif tire_type is "MEDIUM":
                race_control = "PUSH"
                next_tire_sel = "HARD"
            elif tire_type is "HARD":
                race_control = "PUSH"
                next_tire_sel = "SOFT"


        if tire_cond is "SMOOTH":
            pit_message = "OK"
        if tire_cond is "GRAINY":
            pit_message = "CONSERVE"
        if tire_cond is "CHIPPING":
            pit_message = "BOX NEXT LAP"

        full_message = {
            "msg": pit_message,
            "race_ctrl": race_control,
            "next_tire": next_tire_sel
        }

        self.pit_col.insert(full_message)

        return full_message

    def get_all_messages(self):
        return self.pit_col.find({})

        