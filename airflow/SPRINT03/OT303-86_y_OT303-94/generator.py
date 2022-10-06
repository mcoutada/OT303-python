from fileinput import filename
from re import template
from jinja2 import Environment, FileSystemLoader
import yaml
import os

file_dir = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(file_dir))
template = env.get_template("template_dag.jinja2")


for file_name in os.listdir(file_dir):
    if file_name.endswith("yaml"):
        with open(os.path.join(file_dir, file_name), "r") as configfile:
            config = yaml.safe_load(configfile)
            with open(os.path.join(f"dag_{config['dag_id']}.py"), "w") as f:
                f.write(template.render(config))
