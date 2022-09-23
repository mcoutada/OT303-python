from airflow import DAG
from airflow.operators.dummy import DummyOperator
from datetime import timedelta, datetime

print(datetime.today)

with DAG    (
            "DAG_universidades_D",
            description = "DAG_universidades_D",
            schedule_interval = timedelta(hours=1),
            start_date = datetime.today()
                ) as dag:

             run_this_first = DummyOperator (
            task_id = 'branching',
             dag = dag,
             )

     options = ['DAG_universidades_D'] ,

        branching = BranchPythonOperator(
            task_id = 'branching',
            python_callable = lambda: random.choice(DAG_universidades_D),
            dag = dag,
            )

            run_this_first >> branching

                            join = DummyOperator(
                task_id = 'enable_system',
                trigger_rule = 'one_success',
                dag = dag,
            )

                     for option in options:
                 t = DummyOperator(
                task_id = option,
                dag = dag,
             )

                dummy_follow = DummyOperator (
                task_id = 'follow_' + option,
                dag = dag ,
            )


branching >> t >> dummy_follow >> join

u_tecnologica_nacional_extract = DummyOperator(task_id="u_tecnologica_nacional_extract") ,
u_tecnologica_nacional_transform = DummyOperator(task_id="u_tecnologica_nacional_transform"),
u_tecnologica_nacional_load = DummyOperator(task_id="u_tecnologica_nacional_load"),

[u_tecnologica_nacional_extract >> u_tecnologica_nacional_transform >> u_tecnologica_nacional_load]

u_tres_de_febrero_extract = DummyOperator(task_id=" u_tres_de_febrero_extract")
u_tres_de_febrero_transform = DummyOperator(task_id=" u_tres_de_febrero_transform")
u_tres_de_febrero_load = DummyOperator(task_id=" u_tres_de_febrero_load")

[u_tres_de_febrero_extract >>  u_tres_de_febrero_transform >> u_tres_de_febrero_load]