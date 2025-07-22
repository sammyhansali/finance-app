import textwrap
from datetime import datetime, timedelta

# Importing the operators
from airflow.providers.standard.operators.bash import BashOperator

# Importing the DAG class from the airflow SDK
from airflow.sdk import DAG

# Setting default arguments for the DAG - can be overriden on a per-task basis if desired.
default_args = {
    "depends_on_past": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Instantiating the DAG
with DAG(
    "tutorial", # DAG name
    default_args = default_args,
    description = "A dead-simple tutorial dag... you good, mud ;)",
    schedule = timedelta(days=1),
    start_date = datetime(2021,1,1),
    catchup = False,
    tags = ["example-tag", "daddywuzhere;D"],
) as dag:

    t1 = BashOperator(
        task_id = "print_date",
        bash_command = "date",
    )

    t2 = BashOperator(
        task_id = "sleep",
        depends_on_past = False,
        bash_command = "sleep 5",
        retries = 3,
    )

    templated_command = textwrap.dedent(
        """
        {% for i in range(5) %}
            echo "{{ ds }}"
            echo "{{ macros.ds_add(ds, 7) }}"
        {% endfor %}
        """
    )

    t3 = BashOperator(
        task_id = "templated",
        depends_on_past = False,
        bash_command = templated_command,
    )

    t1.doc_md = textwrap.dedent(
        """
        #### Task Documentation
        You can document your task using the attributes `doc_md` (markdown),
        `doc` (plain text), `doc_rst`, `doc_json`, `doc_yaml` which gets
        rendered in the UI's Task Instance Details page.
        ![img](https://imgs.xkcd.com/comics/fixing_problems.png)
        **Image Credit:** Randall Munroe, [XKCD](https://xkcd.com/license.html)
        """
    )

    dag.doc_md = "Rando doc for a rando dag"

    t1 >> [t2, t3]
