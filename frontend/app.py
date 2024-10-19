import reflex as rx
import requests

# Define the URL for the FastAPI backend
API_URL = (
    "http://backend:3000/workouts/"  # Make sure this matches your docker-compose setup
)


class WorkoutApp(rx.App):
    def __init__(self):
        super().__init__()

        # Initialize states
        self.workout_type = rx.State("pushups")  # Default workout type
        self.date = rx.State("")  # Store the date as a string
        self.series = rx.State(0)  # Store the number of series as an integer
        self.repetitions = rx.State(0)  # Store the total repetitions as an integer
        self.max_series = rx.State(0)  # Store the maximum series as an integer
        self.duration = rx.State(0)  # Store the duration as an integer
        self.peak_speed = rx.State(0.0)  # Store the peak speed as a float
        self.peak_heartbeat = rx.State(0)  # Store the peak heartbeat as an integer
        self.distance = rx.State(0.0)  # Store the distance as a float
        self.message = rx.State("")  # Store response messages

    def submit_workout(self):
        # Prepare the data based on the selected workout type
        if self.workout_type.get() in ["pushups", "pullups"]:
            workout_data = {
                "date": self.date.get(),
                "type": self.workout_type.get(),
                "series": self.series.get(),
                "repetitions": self.repetitions.get(),
                "max_series": self.max_series.get(),
            }
        else:  # For exercise bike
            workout_data = {
                "date": self.date.get(),
                "type": "exercise bike",
                "duration": self.duration.get(),
                "peak_speed": self.peak_speed.get(),
                "peak_heartbeat": self.peak_heartbeat.get(),
                "distance": self.distance.get(),
            }

        # Send data to the backend
        response = requests.post(API_URL, json=workout_data)

        if response.status_code == 200:
            self.message.set(response.json()["message"])
            self.reset_fields()
        else:
            self.message.set("Failed to add workout.")

    def reset_fields(self):
        self.date.set("")
        self.series.set(0)
        self.repetitions.set(0)
        self.max_series.set(0)
        self.duration.set(0)
        self.peak_speed.set(0.0)
        self.peak_heartbeat.set(0)
        self.distance.set(0.0)

    @rx.route("/")  # Define the main route
    def index(self):
        return rx.vstack(
            rx.h1("Workout Tracker"),
            rx.select(
                options=["pushups", "pullups", "exercise bike"],
                value=self.workout_type,
                on_change=lambda value: self.workout_type.set(value),
                placeholder="Select workout type",
            ),
            rx.input(
                placeholder="Date (YYYY-MM-DD)",
                value=self.date,
                on_change=lambda value: self.date.set(value),
            ),
            rx.if_cond(
                lambda: self.workout_type.get() in ["pushups", "pullups"],
                rx.vstack(
                    rx.input(
                        placeholder="Number of Series",
                        type="number",
                        value=self.series,
                        on_change=lambda value: self.series.set(
                            int(value) if value else 0
                        ),
                    ),
                    rx.input(
                        placeholder="Total Repetitions",
                        type="number",
                        value=self.repetitions,
                        on_change=lambda value: self.repetitions.set(
                            int(value) if value else 0
                        ),
                    ),
                    rx.input(
                        placeholder="Max Series of the Day",
                        type="number",
                        value=self.max_series,
                        on_change=lambda value: self.max_series.set(
                            int(value) if value else 0
                        ),
                    ),
                ),
            ),
            rx.if_cond(
                lambda: self.workout_type.get() == "exercise bike",
                rx.vstack(
                    rx.input(
                        placeholder="Duration (minutes)",
                        type="number",
                        value=self.duration,
                        on_change=lambda value: self.duration.set(
                            int(value) if value else 0
                        ),
                    ),
                    rx.input(
                        placeholder="Peak Speed (km/h)",
                        type="number",
                        value=self.peak_speed,
                        on_change=lambda value: self.peak_speed.set(
                            float(value) if value else 0.0
                        ),
                    ),
                    rx.input(
                        placeholder="Peak Heartbeat",
                        type="number",
                        value=self.peak_heartbeat,
                        on_change=lambda value: self.peak_heartbeat.set(
                            int(value) if value else 0
                        ),
                    ),
                    rx.input(
                        placeholder="Distance (km)",
                        type="number",
                        value=self.distance,
                        on_change=lambda value: self.distance.set(
                            float(value) if value else 0.0
                        ),
                    ),
                ),
            ),
            rx.button("Submit Workout", on_click=self.submit_workout),
            rx.p(self.message),
        )
