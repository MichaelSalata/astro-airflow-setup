"""
## Print the number of people currently in space

This DAG pulls the number of people currently in space. The number is pulled
from XCom and was pushed by the `get_astronauts` task in the `example_astronauts` DAG.
"""

from airflow.sdk import Asset, dag, task  # , chain

@dag(
    schedule=[Asset("current_astronauts")],
    doc_md=__doc__,
    default_args={"owner": "Astro", "retries": 3},
    tags=["My First DAG"],
)
def my_astronauts_dag() -> None:

    @task
    def print_num_people_in_space(**context):
        """
        This task pulls the number of people currently in space from XCom. The number is
        pushed by the `get_astronauts` task in the `example_astronauts` DAG.
        """
        num_people_in_space = context["ti"].xcom_pull(
            dag_id="example_astronauts",
            task_ids="get_astronauts",
            key="number_of_people_in_space",
            include_prior_dates=True,
        )

        print(f"There are currently {num_people_in_space} people in space.")

    @task.bash
    def print_reaction():
        # Return a bash command/script string for the bash task to execute
        return "echo 'This is awesome!'"

    # IMPORTANT: call the bash task to create a task instance before chaining
    print_num_people_in_space() >> print_reaction()

my_astronauts_dag()