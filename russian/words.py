from myproject.settings import BASE_DIR
from language.views_common import *
from russian.models import *
import requests

# @var words_step
# Amount of words per page in the database
words_step = 50


@login_required
def index(request):
    data_bases = {
        'user': User_Word
    }

    # check_time_step(request.user)

    study_object_number = get_level(data_bases, request.user)

    print("User level: " + str(study_object_number))

    scraping = get_scraping(study_object_number)

    current_box = get_current_box(
        data_bases, request.user, study_object_number)

    next_levels = get_next_levels(current_box)

    studyObject = getStudyObject(study_object_number)

    context = {
        'title': "Russian",
        'studyObject': studyObject,
        'soup': scraping,
        'current_box': current_box,
        'next_levels': next_levels
    }

    return render(request, 'russian/flipMedia.html', context)


def getStudyObject(study_object_number):
    studyObject = {
        'number': get_number(study_object_number),
        'media': get_media(study_object_number),
        'subtitles': get_subtitle(study_object_number)
    }

    return studyObject


def get_number(study_object_number):
    params_ctrl = get_params_ctrl(study_object_number)
    columns = params_ctrl['columns']
    sync = params_ctrl['sync']

    number = filter_cyrillic(columns[sync].text)

    return number


def get_media(study_object_number):
    media = {
        'type': 'audio',
        'source': get_source_path(study_object_number)
    }

    return media


def get_source_path(study_object_number):
    params_ctrl = get_params_ctrl(study_object_number)
    columns = params_ctrl['columns']
    sync = params_ctrl['sync']

    source_path = get_pronunciation_path(
        filter_cyrillic(columns[sync + 2].text))

    return source_path


def get_params_ctrl(study_object_number):
    columns = get_columns_(study_object_number)

    sync = get_sync(study_object_number)

    params_ctrl = {
        'columns': columns,
        'sync': sync
    }

    return params_ctrl


def get_subtitle(study_object_number):
    params_ctrl = get_params_ctrl(study_object_number)
    columns = params_ctrl['columns']
    sync = params_ctrl['sync']

    cyrillic = {
        'language': 'Cyrillic',
        'text': filter_cyrillic(columns[sync + 2].text)
    }

    english = {
        'language': 'English',
        'text': columns[sync + 3].text
    }

    function = {
        'language': 'Function',
        'text': columns[sync + 4].text
    }

    subtitles = []
    subtitles.append(cyrillic)
    subtitles.append(english)
    subtitles.append(function)

    return subtitles


def get_scraping(level):
    '''
    # Acquisition of data on the word of the current level
    # @param level Current user level
    # @return Number, audio, cyrillic, english and function
    # about this word
    '''
    if level <= max_amount:
        file_path = get_file_path(level)

        columns = get_columns(file_path, level)

        return get_scraping2(level, columns)

    return []

# Acquire the file path
# @param level Current user level
# @return The file path


def get_file_path(level):
    if level <= words_step:
        specific_path = ""

    elif level <= words_step * 5:
        specific_path = str(math.ceil(level / words_step))

    elif level <= words_step * 6:
        specific_path = str(math.ceil(level / (words_step * 2)) + 2)

    file_path = 'russian' + get_slash() + 'static' + get_slash() + 'html' + \
        get_slash() + 'Most Common Russian Words' + specific_path + '.html'

    file_path = os.path.join(	BASE_DIR, file_path)

    return file_path

# Characterization of data columns for the current level
# @param file_path The source file path
# @param level Current user level
# @return Matching columns


def get_columns(file_path, level):
    soup = BeautifulSoup(open(file_path, encoding='utf-8'), "html.parser")

    table = soup.find("table", attrs={'class': 'topwords'})

    columns = table.find_all("td")

    return columns


def get_columns_(study_object_number):
    if study_object_number <= max_amount:
        file_path = get_file_path(study_object_number)

        columns = get_columns(file_path, study_object_number)

        if study_object_number <= words_step:
            start = 5

        elif study_object_number <= words_step * 6:
            start = 4

        return columns[start:]


# Acquisition of data on the word of the current level
# and known columns
# @param level Current user level
# @param columns Matching columns
# @return Number, audio, cyrillic, english and function
# about this word


def get_scraping2(level, columns):
    if level <= words_step:
        factor = 5

    elif level <= words_step * 6:
        factor = 4

    return get_data(level, columns[factor:])

# Acquisition of data relating to a word
# @param level Current user level
# @param columns Matching columns
# @return Number, audio, cyrillic, english and function
# about this word


def get_data(level, columns):
    sync = get_sync(level)

    data = {
        'number': filter_cyrillic(columns[sync].text),
        'audio': get_pronunciation_path(filter_cyrillic(columns[sync + 2].text)),
        'cyrillic': filter_cyrillic(columns[sync + 2].text),
        'english': columns[sync + 3].text,
        'function': columns[sync + 4].text
    }

    return data

# Synchronization of columns for data acquisition
# @param level Current user level
# @return


def get_sync(level):
    if level <= words_step:
        sync = 5 * (level - 1)
    else:
        if level <= words_step * 5:
            weight = words_step
        else:
            weight = words_step * 2

        sync = 4 * (level - (weight * (math.ceil(level/weight) - 1) + 1))

        sync = sync - 1

    return sync


def get_soup(url, header):
    r = requests.get(url, headers=header, allow_redirects=True)
    return BeautifulSoup(r.content, 'html.parser')

# Acquiring the path of the pronunciation file
# @param word Word under analysis
# @return The path of the pronunciation file


def get_pronunciation_path(word):
    file_path = 'http://localhost:8000/static/audio/words/' + \
        word.replace(" ", "_")+'.mp3'
    return file_path

# Cyrillic characters for acceptable characters
# @param word Word under analysis
# @return Word with acceptable characters


def filter_cyrillic(word):
    return word.replace(u'\xa0', u'')

# Rule for the choice of low difficulty
# @brief It demands user login
# @param request Standard Django request
# @param number Current user level
# @param current_box	Current user context
# @return Next page with a new word


@login_required
def easy(request, number, current_box):
    data_bases = {
        'user': User_Word
    }

    user_data = {
        'user': request.user,
        'next_level': number,
        'current_box': current_box
    }

    print("")
    print("Easy")
    print("    next:        " + str(number))
    print("    current-bos: " + str(current_box))

    easy_common(data_bases, user_data)

    return redirect('words')

# Rule for the choice of medium difficulty
# @brief It demands user login
# @param request Standard Django request
# @param number Current user level
# @param current_box	Current user context
# @return Next page with a new word


@login_required
def ok(request, number, current_box):
    data_bases = {
        'user': User_Word
    }

    user_data = {
        'user': request.user,
        'next_level': number,
        'current_box': current_box
    }

    print("")
    print("Medium")
    print("    next:        " + str(number))
    print("    current-bos: " + str(current_box))

    medium_common(data_bases, user_data)

    return redirect('words')

# Rule for the choice of medium difficulty
# @brief It demands user login
# @param request Standard Django request
# @param number Current user level
# @param current_box	Current user context
# @return Next page with a new word


@login_required
def hard(request, number, current_box):
    data_bases = {
        'user': User_Word
    }

    user_data = {
        'user': request.user,
        'next_level': number,
        'current_box': current_box
    }

    print("")
    print("Hard")
    print("    next:        " + str(number))
    print("    current-box: " + str(current_box))

    hard_common(data_bases, user_data)

    return redirect('words')
