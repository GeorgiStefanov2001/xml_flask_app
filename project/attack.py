import os
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import ParseError as ParseError

from flask import Blueprint, flash, redirect, url_for
from flask_login import login_required

attack = Blueprint("attack", __name__)

file_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "static", "attack.xml"
)


def generate_xml():
    base_xml_doc = '<?xml version="1.0"?><!DOCTYPE lolz [<!ENTITY lol "lol"><!ELEMENT lolz (#PCDATA)>%s]><lolz>&lol9;</lolz>'

    def generate_line(start):
        sub = f"&lol{start-1};" if start > 1 else "&lol;"
        return f'<!ENTITY lol{start} "{sub*10}">'

    with open(file_dir, "w") as f:
        f.write((base_xml_doc % "".join([generate_line(i) for i in range(1, 10)])))


@attack.route("/lol")
@login_required
def billion_laughs():
    generate_xml()
    try:
        ET.parse(file_dir)
    except ParseError:
        flash(
            "Billion laughs attack detected :) XML you are trying to parse is corrupted."
        )

    return redirect(url_for("main.index"))
