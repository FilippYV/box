from datetime import datetime, time

import matplotlib.pyplot as plt
import csv
import json
import pandas as pd

# Наименование файла с дампом данных
JSON_FILENAME = '../new/data.json'


# Функция получения экземпляра класса для записи CSV
def get_csv_writer(filestream, fieldnames):
    return csv.DictWriter(
        filestream,  # Файловый поток
        fieldnames=fieldnames,  # Наименования полей словаря и заголовков CSV файла
        delimiter=',',  # Разделитель CSV файла
        quotechar='"',  # Кавычки для обрамления текстовых значений, содержащих символ-разделитель
        quoting=csv.QUOTE_MINIMAL  # Политика расстановки кавычек
    )


# Функция получения экземпляра класса для чтения CSV
def get_csv_reader(filestream, fieldnames):
    return csv.DictReader(
        filestream,
        fieldnames=fieldnames,
        delimiter=',',
        quotechar='"',
        quoting=csv.QUOTE_MINIMAL
    )


# Функция получения данных из json-файла
def get_data_from_json(filename):
    with open(filename, 'r') as file:
        data = file.read()
        return json.loads(data)


def create_plots(plots_data_lists):
    # Создание графиков для отрисовки данных
    fig, axs = plt.subplots(1, figsize=(15, 7))  # Получим окно с 1 колонкой и 2 столбцами графиков
    # fig - окно, в котором будут отрисовываться графики
    # axs содержит в себе список графиков для отрисовки на них значений
    # Задание набора точек для отрисовки
    # Первый аргумент - список значений по оси X, второй аргумент - по оси Y
    axs.plot(plots_data_lists['time'], plots_data_lists['temperature'])
    axs.set_xlabel('time')
    axs.set_ylabel('temperature')
    axs.set_title('temperature all time graph')


def create_plots2_bar(plots_data_lists):  # без отступов
    # Задание лейблов для осей и графика
    # axs2.set_xlabel('Time')
    df = pd.DataFrame({'time': plots_data_lists['time'], 'val': plots_data_lists['voltage']})
    axs2 = df.plot.bar(x='time', y='val', rot=0)
    # fig2, axs2 = plt.subplots(1, figsize=(16, 6))
    # Формирование гистограммы
    # axs2.hist(mass_voltage_count)
    # axs2.set_xlabel('voltage')
    axs2.set_ylabel('voltage')
    axs2.set_title('voltage all time graph')
    # axs2.grid()
    return df, axs2


def create_plots2_hist_V2(mass_voltage_data, mass_voltage_count):
    # Задание лейблов для осей и графика
    # axs2.set_xlabel('Time')
    df = pd.DataFrame({'voltage': mass_voltage_data, 'val': mass_voltage_count})
    axs2 = df.plot.bar(x='voltage', y='val', rot=0)
    # fig2, axs2 = plt.subplots(1, figsize=(16, 6))
    # Формирование гистограммы
    # axs2.hist(mass_voltage_count)
    # axs2.set_xlabel('voltage')
    axs2.set_ylabel('quantity')
    axs2.set_title('voltage gradient graph')
    # axs2.grid()
    return df, axs2


def create_plots3(mass_co2_data, mass_co2_count):
    fig3, axs3 = plt.subplots(1, figsize=(16, 9))
    axs3.pie(mass_co2_count, labels=mass_co2_data, startangle=90)
    axs3.set_title('concentrationCO2')
    return fig3, axs3


def main():
    json_dict = get_data_from_json(JSON_FILENAME)
    data_list = json_dict

    fieldnames = data_list[0].keys()

    # Создание списков для хранения данных для графиков
    plots_data_lists = {
        'temperature': [],
        'voltage': [],
        'time': [],
        'Current Motion': []
    }
    mass_voltage_data = []
    mass_voltage_count = []
    mass_temperature_data = []
    mass_temperature_count = []

    # Создание CSV-файла
    with open("data.csv", "w") as csv_file:
        # Получение объекта для работы с CSV
        csv_writer = get_csv_writer(csv_file, fieldnames)

        # Запись заголовков в CSV файл, переданных в поле fieldnames
        csv_writer.writeheader()

        # Запись данных в CSV файл
        for info_dict in data_list:
            csv_writer.writerow(info_dict)

    with open('data.csv', 'r') as csv_file:
        # Создание объекта для чтения CSV (параметры соответствуют DictWriter)
        csv_reader = get_csv_reader(csv_file, fieldnames)

        line_count = 0
        for row in csv_reader:
            # В нулевой строке всегда читается заголовок
            if line_count == 0:
                line_count += 1
                continue

            # Заполнение списков с данными, с преобразованием типов
            t = datetime.fromisoformat(row['time'][:-7])
            # time(t.hour, t.minute, t.second)
            plots_data_lists['time'].append(str(t))
            plots_data_lists['temperature'].append(float(row['temperature']))

            for i in range(len(mass_voltage_data)):
                if mass_voltage_data[i] == float(row['voltage']):
                    mass_voltage_count[i] += 1
            # если не находим элемент то добавляем его в mass_co2_data
            # и записываем его количество как 1 а mass_co2_count
            if float(row['voltage']) not in mass_voltage_data:
                mass_voltage_data.append(float(row['voltage']))
                mass_voltage_count.append(1)

            plots_data_lists['voltage'].append(float(row['voltage']))
            plots_data_lists['Current Motion'].append(float(row['Current Motion']))
            line_count += 1

            for i in range(len(mass_temperature_data)):
                if mass_temperature_data[i] == float(row['temperature']):
                    mass_temperature_count[i] += 1

            # если не находим элемент то добавляем его в mass_co2_data
            # и записываем его количество как 1 а mass_co2_count
            if float(row['temperature']) not in mass_temperature_data:
                mass_temperature_data.append(float(row['temperature']))
                mass_temperature_count.append(1)

    for i in range(len(mass_voltage_data) - 1):
        for j in range(len(mass_voltage_data) - 1 - i):
            if mass_voltage_data[j] > mass_voltage_data[j + 1]:
                mass_voltage_data[j], mass_voltage_data[j + 1] = mass_voltage_data[j + 1], mass_voltage_data[j]
                mass_voltage_count[j], mass_voltage_count[j + 1] = mass_voltage_count[j + 1], mass_voltage_count[j]

    for i in range(len(mass_temperature_data) - 1):
        for j in range(len(mass_temperature_data) - 1 - i):
            if mass_temperature_data[j] > mass_temperature_data[j + 1]:
                mass_temperature_data[j], mass_temperature_data[j + 1] = mass_temperature_data[j + 1], \
                                                                         mass_temperature_data[j]
                mass_temperature_count[j], mass_temperature_count[j + 1] = mass_temperature_count[j + 1], \
                                                                           mass_temperature_count[j]

    create_plots2_bar(plots_data_lists)
    create_plots2_hist_V2(mass_voltage_data, mass_voltage_count)
    create_plots(plots_data_lists)
    create_plots3(mass_temperature_data, mass_temperature_count)
    plt.show()


if __name__ == "__main__":
    main()
