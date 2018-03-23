from ConfigParser import ConfigParser
from jinja2 import Environment, FileSystemLoader
from jirahelper import get_issues

config = ConfigParser()
config.read("./config.ini")
project_name = config.get('instance', 'project_name')
version = config.get('instance', 'version')
image_host = config.get('instance', 'image_host')
results_url = config.get('instance', 'results_url')
header_text = config.get('instance', 'header_text')

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('release_notes.html')


issues = get_issues()

if issues:

    output_from_parsed_template = template.render(
        issues=issues,
        version=version,
        project_name=project_name,
        header_text=header_text,
        image_host=image_host,
        results_url=results_url
    )

    with open("update.html", "wb") as fh:
        fh.write(output_from_parsed_template.encode('utf-8').strip())
