from jinja2 import Environment, FileSystemLoader, Template
import yaml
import json

ENV = Environment(loader=FileSystemLoader('./'))

with open("./Inputs/globalvals.yaml") as inputfile:
    devglobals =  yaml.load(inputfile)

with open('./Inputs/devices.yaml') as inputfile:
    devs = yaml.load(inputfile)

for dev in devs:
    print dev
    print '----------/////////////////////////////////------------------------'

# Print dictionary generated from yaml


# Render template and print generated config to console
#template = ENV.get_template("Comware5_Template.j2")
#print (template.render(network_global=network_global, device_values = device_values, site= site))
