from datetime import datetime

import db_utils
import file_utils
import network_utils

url_model = 'https://part4.info/model/'
url_detail = 'https://part4.info/detail/'
url_supplies = 'https://part4.info/cartridge/'


def gen_model():
    models_id = db_utils.get_id('models')
    list_of_urls = []
    for i in models_id:
        if db_utils.check_options(i[0]):
            list_of_urls.append(f'{url_model}{i[0]}?tab=options')
            print(f'\r', i[0], 'options', end='')
        if db_utils.check_parts(i[0]):
            list_of_urls.append(f'{url_model}{i[0]}?tab=parts')
            print(f'\r', i[0], 'parts', end='')
        if db_utils.check_errors(i[0]):
            list_of_urls.append(f'{url_model}{i[0]}?tab=errors')
            print(f'\r', i[0], 'errors', end='')
        if db_utils.check_supplies(i[0]):
            list_of_urls.append(f'{url_model}{i[0]}?tab=supplies')
            print(f'\r', i[0], 'supplies', end='')

    file_utils.save_sitemap('models', list_of_urls)


def gen_details():
    list_of_urls = []
    results = list(set(db_utils.get_id('details')) - set(db_utils.get_model_id_from_details()))
    for res in results:
        print(f'\r', res[0], end='')
        list_of_urls.append(f'{url_detail}{res[0]}')
    file_utils.save_sitemap('details', list_of_urls)


def gen_supplies():
    supplies_id = db_utils.get_id('all_cartridge')
    list_of_urls = []
    for i in supplies_id:
        print(f'\r', i[0], end='')
        if network_utils.check_url(f'{url_supplies}{i[0]}'):
            list_of_urls.append(f'{url_supplies}{i[0]}')
    file_utils.save_sitemap('supplies', list_of_urls)


def check_list(xid, models_list):
    for i in models_list:
        if i == xid:
            return False
    return True


if __name__ == '__main__':
    start_time = datetime.now()  # start
    print(start_time)

    MATERIALIZED_LIST = ['REFRESH MATERIALIZED VIEW "all_brand_models";',
                         'REFRESH MATERIALIZED VIEW "all_cartridge";',
                         'REFRESH MATERIALIZED VIEW "all_details";',
                         'REFRESH MATERIALIZED VIEW "all_errors";',
                         'REFRESH MATERIALIZED VIEW "all_models";',
                         'REFRESH MATERIALIZED VIEW "all_options_for_cartridges";',
                         'REFRESH MATERIALIZED VIEW "all_options_for_details";',
                         'REFRESH MATERIALIZED VIEW "all_options_model";',
                         'REFRESH MATERIALIZED VIEW "all_partcatalog";',
                         'REFRESH MATERIALIZED VIEW "model_for_filter";',
                         'REFRESH MATERIALIZED VIEW "search_cartridge";',
                         'REFRESH MATERIALIZED VIEW "search_detail_index";',
                         'REFRESH MATERIALIZED VIEW "search_error";',
                         'REFRESH MATERIALIZED VIEW "search_index";']

    n_time = datetime.now()
    print('models', n_time)
    try:
        gen_model()
    except:
        pass
    print(datetime.now() - n_time)

    n_time = datetime.now()
    print('supplies', n_time)
    try:
        gen_supplies()
    except:
        pass
    print(datetime.now() - n_time)

    n_time = datetime.now()
    print('details', n_time)
    try:
        gen_details()
    except:
        pass
    print(datetime.now() - n_time)

    file_utils.save_main_sitemap()

    for i in MATERIALIZED_LIST:
        print(i)
        db_utils.update_material_view(i)

    print(datetime.now() - start_time)  # end
