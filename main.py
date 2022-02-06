# -*- coding: utf-8 -*-

import random, string, json, secrets
from flask import Flask, request, jsonify, redirect, make_response
from werkzeug.exceptions import HTTPException
import requests

app = Flask(
	__name__,
	template_folder='public',
	static_folder='static'
)

ok_chars = string.ascii_letters + string.digits

def remove_non_ascii(s):
  return "".join(c for c in s if ord(c) < 128)

def load_templates():
  with open("Database.json", "r") as file:
    return json.loads(file.read())

@app.route('/templates/')
def templates():
  templates = load_templates()
  
  return jsonify(templates)

@app.route('/templates/<key>/')
def template(key):
  templates = load_templates()
    
  for template in templates:
    if (template["key"] == key):
      return jsonify(template)

@app.route('/templates/<key>/delete', methods=["POST"])
def delete(key):
  templates = load_templates()
    
  for template in templates:
    if (template["key"] == key):
      templates.remove(template)
  
  with open(f"Database.json","w") as f:
    json.dump(templates, f, indent=2)

  return jsonify(templates)

@app.route('/templates/create/', methods=["POST"])
def create():
  data = request.get_json()
  templates = load_templates()
  """request.args.getlist("tiles")"""
  for template in templates:
    if (template["name"] == data["name"]):
      return jsonify({"Error": "000 Name is already used in another template", "Code": 000})

  template = {"key": secrets.token_hex(16), "name": data["name"], "tiles": data["tiles"], "positions": data["positions"], "rotations": data["rotations"]}
  templates.append(template)
  
  with open(f"Database.json","w") as f:
    json.dump(templates, f, indent=2)

  return jsonify(template)

@app.errorhandler(Exception)
def error(e):
	code = 500
	if isinstance(e, HTTPException):
		code = e.code
	return jsonify({"Error": str(e), "Code": code})

if __name__ == "__main__":
	app.run(
		host='0.0.0.0',
		port=random.randint(2000, 9000)
)