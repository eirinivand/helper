from flask import render_template, request, Blueprint
import csv
import os
import re

from werkzeug.utils import secure_filename

bp = Blueprint('csvvalidator', __name__, url_prefix='/csvvalidator')


@bp.route('/validate', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        result = {}
        f = request.files['file']
        if not f:
            return render_template("result.html",
                                   result={'file': '', 'result': {'File Error': ['Not file selected.']},
                                           'patterns': []})
        f.save('files/' + secure_filename(f.filename))
        patterns = {}
        if not f.filename.endswith('.csv'):
            os.remove('files/' + secure_filename(f.filename))
            return render_template("result.html",
                                   result={'file': f.filename, 'result': {'File Error': ['Not a .csv file']},
                                           'patterns': patterns})
        for k, v in validate_file(f.filename, patterns).items():
            if v:
                result['Line ' + k] = v
        for k, v in patterns.items():
            v = str(v)

        os.remove('files/' + secure_filename(f.filename))
    return render_template("result.html", result={'file': f.filename, 'result': result, 'patterns': patterns})


def validate_file(file, patterns):
    f = open('files/' + file.replace(' ', '_'), "r", newline='', encoding="utf8")
    reader = csv.reader(f, delimiter=',', quotechar='"')
    line_number = 0
    result = {}
    parameter_count = 0
    price_parameters_indexes = {}
    for line in reader:
        line_number = line_number + 1
        print(str(line_number) + ':')
        if line_number == 1:
            parameter_count = len(line)
            for w in line:
                if w == 'offer_initial_price' or w == 'offer_price':
                    price_parameters_indexes[line.index(w)] = w
        validation_result = validate_line(line, parameter_count, line_number, patterns, price_parameters_indexes)
        if validation_result:
            result[str(line_number)] = validation_result
            result[str(line_number)] = list(filter(bool, result[str(line_number)]))

    f.close()
    if not result:
        result[0] = 'File validated Successfully'

    return result


def validate_line(l, count, line_number, patterns, price_parameters_indexes):
    result = []
    # Validate no patter of type '//+' exists
    if count != len(l):
        result.append('Failed Validations: Wrong number of attributes has ' + str(len(l)) + ' should be ' + str(
            count) + ' this means that some of the following parameter positions might be wrong')
    for w in l:
        result.append(validation_vertical_slash(w, l.index(w) + 1))
        if l.index(w) == 0:
            result.append(validation_pattern(w, l.index(w) + 1, line_number, patterns))
        elif line_number != 1 and l.index(w) in price_parameters_indexes.keys():
            result.append(
                validation_price_formatting(w, l.index(w), price_parameters_indexes[l.index(w)]))
        result.append(validation_tag_formatting(w, l.index(w) + 1))

    return result


def validation_pattern(w, index_of_w, line_number, patterns):
    validation_1 = re.search('(.*[/])(.*[/])(.*[+])(.*)', w)
    patterns[line_number] = re.findall('[^\\[a-zA-Z0-9]*', w)
    patterns[line_number] = ''.join(str(x) for x in list(filter(None, patterns[line_number])))
    if validation_1 is not None:
        return 'Failed Validation: found pattern //+ at ' + str(index_of_w) + ' th parameter '
    return ''


def validation_vertical_slash(w, index_of_w):
    validation_1 = re.search('[|]', w)
    if validation_1 is not None:
        return 'Failed Validation: found vertical slash | at ' + str(index_of_w) + ' th parameter '
    return ''


def validation_tag_formatting(w, index_of_w):
    close_tags = re.findall('(</(?P<tag>[a-zA-Z0-9]*)>)', w)
    open_tags = re.findall('(<(?P<tag>[a-zA-Z0-9]*)>)', w)
    if len(close_tags) != len(open_tags):  # (t != '<br>' and t != '</br>')and
        i = 0
        missing_tags = ''
        for ot in open_tags:
            if ot[1] == 'br':
                open_tags.remove(ot)
        while i < len(close_tags):
            for ot in open_tags:
                if close_tags[i][1] == ot[1]:
                    open_tags.remove(ot)
                    break
            i += 1
        for ot in open_tags:
            missing_tags += ot[1] + ' '
        # if len(close_tags)- len(open_tags) == len([s for s in ot if "br" in s]):
        if missing_tags:
            return 'Failed Validation : tag formatting for tag:' + missing_tags + ' at: ' + \
                   str(index_of_w) + ' th parameter '
    return ''


def validation_price_formatting(w, index_of_w, parameter_name):
    matched = re.findall('[0-9]+[\'&comma;\'][0-9]+[\'&euro;\']', w)
    if not matched:
        return 'Failed Validation : price formatting for ' + parameter_name + ' :' + w + ' at: ' + \
               str(index_of_w) + ' th parameter '
    return ''
