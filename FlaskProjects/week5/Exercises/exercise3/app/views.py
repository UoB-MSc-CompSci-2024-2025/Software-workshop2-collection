from flask import render_template, flash, url_for, redirect, request, send_file
from app import app
from app.forms import ChooseFrom, OptionForm, DownloadForm, RadioForm

import os
import csv
import io


def get_menu():
    menu_info, menu_sorted = [], []
    if not menu_sorted:
        try:
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'menu.csv')
            with open(filepath, newline='') as f_csv:
                reader = csv.reader(f_csv)
                error_count = 0
                header_row = next(reader)
                if header_row != ['Course', 'Dish', 'Price']:
                    flash(
                        f"Error header row doesn't meet expected format.",
                        'danger'
                    )
                    raise ValueError('Header format error.')

                menu_info.append(header_row)
                for idx, row in enumerate(reader):
                    row_num = idx + 1
                    if error_count > 10:
                        flash(
                            'Too many errors in file, fix file and reduce errors before continuing.',
                            'danger'
                        )
                        raise ValueError('Too many errors in file.')
                    if len(row) != 3:
                        flash(
                            f"Error row {row_num} must contain 3 values: 'Course', 'Dish', 'Price'.",
                            'danger'
                        )
                        error_count += 1
                        continue
                    if error_count == 0:
                        menu_info.append(row)
            if error_count > 0:
                flash(
                    f"{error_count} errors encountered in file.",
                    'danger'
                )
                raise ValueError(f"Errors encountered in file.")

            headers, data = menu_info[0], menu_info[1:]

            data_sorted = sorted(data, key=lambda x: x[0], reverse=True)
            menu_sorted = [headers] + data_sorted
            return menu_sorted

        except Exception as e:
            app.logger.error(f"Error in reading file: Error={e}")
            flash('File upload failed.', 'danger')


def get_starters():
    menu_info = get_menu()
    starters, price = [(1, 'None')], ['None']
    value = 2
    for info in menu_info:
        if info[0] == 'Starter':
            starters.append((value, info[1]))
            price.append(info[2])
            value += 1

    return starters, price


def get_mains():
    menu_info = get_menu()
    main, price = [(1, 'None')], ['None']
    value = 2
    for info in menu_info:
        if info[0] == 'Main':
            main.append((value, info[1]))
            price.append(info[2])
            value += 1

    return main, price


def get_desserts():
    menu_info = get_menu()
    dessert, price = [(1, 'None')], ['None']
    value = 2
    for info in menu_info:
        if info[0] == 'Dessert':
            dessert.append((value, info[1]))
            price.append(info[2])
            value += 1

    return dessert, price


def toggle_service(value):
    if value == 'True':
        value = 'False'
    elif value == 'False':
        value = 'True'

    return value


@app.route('/')
def home():
    app.logger.debug("Debug")
    app.logger.info("Info")
    app.logger.warning("Warning")
    app.logger.error("Error")
    app.logger.critical("Critical")
    return render_template('index.html', title='MC Restaurant')


@app.route('/menu', methods=['POST', 'GET'])
def menu():
    menu_info = get_menu()
    form_menu = ChooseFrom()

    starters = get_starters()[0]
    form_menu.starter.choices = starters

    main = get_mains()[0]
    form_menu.main.choices = main

    dessert = get_desserts()[0]
    form_menu.dessert.choices = dessert

    if form_menu.validate_on_submit():
        starter = form_menu.starter.data
        main = form_menu.main.data
        dessert = form_menu.dessert.data

        return redirect(url_for('receipt', starter=starter, main=main, dessert=dessert))

    return render_template('menu.html', title='Menu Select', menu=menu_info, form_menu=form_menu)


@app.route('/menu_radio', methods=['POST', 'GET'])
def menu_radio():
    menu_info = get_menu()
    form_menu = RadioForm()

    starters = get_starters()[0]
    form_menu.starter.choices = starters

    main = get_mains()[0]
    form_menu.main.choices = main

    dessert = get_desserts()[0]
    form_menu.dessert.choices = dessert

    if form_menu.validate_on_submit():
        starter = form_menu.starter.data
        main = form_menu.main.data
        dessert = form_menu.dessert.data

        return redirect(url_for('receipt', starter=starter, main=main, dessert=dessert))

    return render_template('menu_radio.html', title='Menu Select', menu=menu_info, form_menu=form_menu)


@app.route('/download_menu', methods=['POST', 'GET'])
def download_menu():
    form = DownloadForm()

    menu_info = get_menu()
    starters, mains, desserts = [], [], []
    for info in menu_info:
        if info[0] == 'Starter':
            starters.append(info)
        if info[0] == 'Main':
            mains.append(info)
        if info[0] == 'Dessert':
            desserts.append(info)

    if form.validate_on_submit():
        starters_sorted = sorted(starters, key=lambda x: float(x[-1]))
        mains_sorted = sorted(mains, key=lambda x: float(x[-1]))
        desserts_sorted = sorted(desserts, key=lambda x: float(x[-1]))
        sorted_menu = [menu_info[0]] + starters_sorted + mains_sorted + desserts_sorted

        mem = io.BytesIO()
        wrapper = io.TextIOWrapper(mem, encoding='utf-8', newline='')
        writer = csv.writer(wrapper)

        for row in sorted_menu:
            writer.writerow(row)
        wrapper.flush()
        mem = wrapper.detach()
        mem.seek(0)
        return send_file(mem, as_attachment=True, download_name='sorted_menu.csv', mimetype='text/csv')



    return render_template(
        'download_menu.html',
        title='Download Menu',
        form=form
    )


@app.route('/receipt', methods=['POST', 'GET'])
def receipt():
    form_service = OptionForm()
    form_download = DownloadForm()
    form_service.amount.choices = [(1, '0%'), (2, '15%'), (3, '20%'), (4, '25%'), (5, 'Other')]
    service_charge = 10

    if request.method == 'GET':
        form_service.toggle_view.data = 'False'

    starter, starter_price = '', 0
    main, main_price = '', 0
    dessert, dessert_price = '', 0

    try:
        starter_ind = int(request.args.get('starter', '')) - 1
        main_ind = int(request.args.get('main', '')) - 1
        dessert_ind = int(request.args.get('dessert', '')) - 1

        starter = get_starters()[0][starter_ind][1]
        starter_price = get_starters()[1][starter_ind]

        main = get_mains()[0][main_ind][1]
        main_price = get_mains()[1][main_ind]

        dessert = get_desserts()[0][dessert_ind][1]
        dessert_price = get_desserts()[1][dessert_ind]
    except Exception as e:
        app.logger.error(f"Error: {e}")

    if form_service.validate_on_submit():
        starter = request.args.get('starter', '')
        main = request.args.get('main', '')
        dessert = request.args.get('dessert', '')

        for info in get_menu():
            if info[1] == starter:
                starter_price = info[-1]
            if info[1] == main:
                main_price = info[-1]
            if info[1] == dessert:
                dessert_price = info[-1]

        if form_service.choose.data.startswith('-'):
            form_service.choose.data = '10%'
            flash('Service charge cannot be a negative.', 'warning')

        form_service.toggle_view.data = toggle_service(form_service.toggle_view.data)
        if form_service.amount.data != '5':
            amount_choices = dict(form_service.amount.choices)
            select_label = amount_choices.get(int(form_service.amount.data))
            if select_label and '%' in select_label:
                service_charge = int(select_label.replace('%', ''))
        else:
            try:
                service_charge = int(form_service.choose.data.split('%')[0])
            except Exception as e:
                service_charge = form_service.choose.data
                app.logger.error(f"Error: {e}")

    return render_template(
        'receipt.html',
        title='Receipt',
        starter=starter, starter_price=starter_price,
        main=main, main_price=main_price,
        dessert=dessert, dessert_price=dessert_price,
        form_service=form_service,
        toggle_view=form_service.toggle_view.data,
        service_charge=service_charge,
        form_download=form_download
    )


@app.route('/download_receipt', methods=['POST', 'GET'])
def download_receipt():
    form_download = DownloadForm()

    starter = request.args.get('starter', '')
    starter_price = request.args.get('starter_price', '')

    main = request.args.get('main', '')
    main_price = request.args.get('main_price', '')

    dessert = request.args.get('dessert', '')
    dessert_price = request.args.get('dessert_price', '')

    service_charge = request.args.get('service_charge', '')

    total_price = [starter_price, main_price, dessert_price]
    for i in range(len(total_price)):
        if total_price[i] == 'None':
            total_price[i] = '0'

    total_price = sum(list(map(float, total_price)))

    if form_download.validate_on_submit():
        receipt_info = [
            ['Dish', 'Price'],
            [],
            ['Starter'],
            [starter, starter_price],
            [],
            ['Main'],
            [main, main_price],
            [],
            ['Dessert'],
            [dessert, dessert_price],
            [],
            ['Total Price', f"({service_charge}% service charge included) "
                            f"£{total_price * (1 + float(service_charge) / 100):.2f}"]
        ]

        # mem = io.BytesIO()
        # for row in receipt_info:
        #     row_str = ' | '.join(str(info) for info in row) + "\n"
        #     mem.write(row_str.encode('utf-8'))
        # mem.seek(0)
        # return send_file(mem, as_attachment=True, download_name='receipt.txt', mimetype='text/plain')

        with io.StringIO() as mem:
            for row in receipt_info:
                row_str = ' | '.join(str(info) for info in row) + "\n"
                mem.write(row_str.encode('utf-8'))
            mem.seek(0)
            return send_file(io.BytesIO(mem.getvalue().encode(encoding='utf-8')), as_attachment=True,
                                   download_name="MyFruitFile.csv", mimetype="text/csv")
