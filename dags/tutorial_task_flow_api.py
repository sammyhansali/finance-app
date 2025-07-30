import json
import pendulum
from airflow.sdk import dag, task

@dag(
    schedule = None,
    start_date = pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup = False,
    tags = ["example tag gang lord!!!", "daddywuzhere;D", "new tag gng"],
)
def taskflow_tutorial():
    """
    ### TaskFlow API Tutorial Documentation
    This is a simple data pipeline example which demonstrates the use of
    the TaskFlow API using three simple tasks for Extract, Transform, and Load.
    Documentation that goes along with the Airflow TaskFlow API tutorial is
    located
    [here](https://airflow.apache.org/docs/apache-airflow/stable/tutorial_taskflow_api.html)
    """

    @task()
    def extract():
        """
        #### Extract task
        A simple Extract task to get data ready for the rest of the data
        pipeline. In this case, getting data is simulated by reading from a
        hardcoded JSON string.
        """
        data = '{"1001": 301.27, "1002": 433.21, "1003": 502.22}'
        data_dict = json.loads(data)
        return data_dict

    @task(multiple_outputs=True)
    def transform(order_data_dict: dict):
        """
        #### Transform task
        A simple Transform task which takes in the collection of order data and
        computes the total order value.
        """
        total_order_value = 0

        for value in order_data_dict.values():
            total_order_value += value

        return {"total_order_value": total_order_value}
    
    @task()
    def load(total_order_value: float):
        """
        #### Load task
        A simple Load task which takes in the result of the Transform task and
        instead of saving it to end user review, just prints it out.
        """

        print(f"Total order value is: {total_order_value:.2f}")

    # Dependency chain
    e = extract()
    t = transform(e)
    load(t["total_order_value"])

taskflow_tutorial()