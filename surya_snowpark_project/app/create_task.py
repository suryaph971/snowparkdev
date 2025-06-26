from snowflake.core import Root
import snowflake.connector
from datetime import timedelta
from snowflake.core.task import Task
from snowflake.snowpark import Session
import os
from snowflake.core.task.dagv1 import DAG,DAGTask,DAGOperation,CreateMode,DAGTaskBranch

#conn = snowflake.connector.connect()
conn =snowflake.connector.connect(
    user=os.environ.get('SNOWFLAKE_USER'),
    password=os.environ.get('SNOWFLAKE_PASSWORD'),
    account=os.environ.get("SNOWFLAKE_ACCOUNT"),
    warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
    database=os.environ.get('SNOWFLAKE_DATABASE'),
    schema=os.environ.get('SNOWFLAKE_SCHEMA'),
    role=os.environ.get('SNOWFLAKE_ROLE'))

print("Connection established")
print(conn)

root = Root(conn)


my_task = Task("Root_task",
              definition="Select current_timestamp() as timestamp",
              schedule=timedelta(minutes=30),
              warehouse="COMPUTE_WH")

tasks = root.databases["Practice_db"].schemas["Public"].tasks

#tasks.create(my_task)
print("Task created successfully")

with DAG("my_dag",schedule=timedelta(days=1)) as dag:
    dag_task1 = DAGTask("dag_task1",
                        definition="Select current_timestamp() as timestamp",
                        warehouse="COMPUTE_WH")
    dag_task2 = DAGTask("dag_task2",
                        definition="Select current_timestamp() as timestamp",
                        warehouse="COMPUTE_WH")

    dag_task3 = DAGTask("dag_task3",
                        definition="Select current_timestamp() as timestamp",
                        warehouse="COMPUTE_WH")

    dag_task4 = DAGTask("dag_task4",
                        definition="Select current_timestamp() as timestamp",
                        warehouse="COMPUTE_WH")


    dag_task1 >> dag_task2 >>[dag_task3, dag_task4]

    schema = root.databases["Practice_db"].schemas["Public"]
    dag_op = DAGOperation(schema)
    dag_op.deploy(dag, mode=CreateMode.or_replace)
    print("DAG Created Successfully")