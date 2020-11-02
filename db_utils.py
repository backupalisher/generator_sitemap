import db


def get_id(table_name):
    q = db.i_request(f'SELECT id FROM {table_name}')
    if q:
        return q


def get_model_id_from_details():
    q = db.i_request(f'SELECT id FROM details WHERE "partcode_id" IS NULL AND "module_id" IS NULL ORDER BY "id"')
    if q:
        return q


def get_detail_id():
    q = db.i_request(f'SELECT id, model_id FROM details')
    if q:
        return q


def check_options(model_id):
    q = db.i_request(f'SELECT * FROM all_options_model WHERE '
                     f'detail_id = (SELECT id FROM details WHERE model_id = {model_id} and partcode_id '
                     f'is null ORDER BY id LIMIT 1)')
    if q:
        return True
    else:
        return False


def check_parts(model_id):
    q = db.i_request(f'SELECT * FROM all_partcatalog WHERE model_id = {model_id} and partcode is not null')
    if q:
        return True
    else:
        return False


def check_errors(model_id):
    q = db.i_request(f'SELECT * FROM all_errors WHERE mid = {model_id} and code is not null')
    if q:
        return True
    else:
        return False


def check_supplies(model_id):
    q = db.i_request(f'SELECT * FROM all_cartridge WHERE {model_id} = ANY(model_id)')
    if q:
        return True
    else:
        return False
