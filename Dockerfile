FROM odoo:17.0

USER root

RUN pip3 install --no-cache-dir openpyxl

USER odoo