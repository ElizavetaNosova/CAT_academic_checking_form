import requests
from nltk import sent_tokenize
from copy import copy

class ParagraphLengthException(Exception):
    def __init__(self, paragraph_length_limit):
        self.text = 'Too long paragraph is detected'
        self.paragraph_length_limit = paragraph_length_limit


class SpellChecker:
    def __init__(self, api_href='https://speller.yandex.net/services/spellservice.json/checkTexts', CHECKER_LIMIT=10000):
        self.__checker_limit = CHECKER_LIMIT
        self.__api_href = api_href
		
    def _check_text_parts(self, texts):
        response = requests.post(self.__api_href, {'text': texts})
        sucsess = response.status_code == 200
        problems = []
        if sucsess:
            problems = response.json()
            print('получены результаты запроса')
        return problems, sucsess

    def check_spelling(self, text):
        if len(text) <= self.__checker_limit:
            paragraphs = [text]
            problems, sucsess = self._check_text_parts(paragraphs)
            print('требовался один запрос, выполнен')
        else:
            paragraphs = text.split('\n')
            if all([len(paragraph <= self.__checker_limit) for paragraph in paragraphs]):
                problems = self._split_and_check(paragraphs)
            else:
                raise ParagraphLengthException(self.__checker_limit)
            print('все запросы выполнены')
        problems_with_context_and_fixed_ids = self.__add_context_and_fix_ids(problems, paragraphs)
        print('все данные отформатированы')
        text_problems = []
        for paragraph_problems in problems_with_context_and_fixed_ids:
            text_problems += paragraph_problems
        return {'problems': text_problems, 'sucsess': sucsess}

    def _split_and_check(self, paragraphs):
        spelling_problems = []
        current_texts = []
        no_server_problems = True
        current_len = 0
        for i, text in enumerate(paragraphs):
            if current_len + len(text) > self.__checker_limit:
                current_text_problems, current_text_problems_status_is_200 = self.__checker_query(current_texts)
                spelling_problems += current_text_problems
                no_server_problems *= current_text_problems_status_is_200
                current_len = len(text)
                current_texts = []
                current_texts.append(text)
            else:
                current_texts.append(text)
                current_len += len(text)
        current_text_problems, current_text_problems_status_is_200 = self.__checker_query(current_texts)
        spelling_problems += current_text_problems
        no_server_problems *= current_text_problems_status_is_200 
        return spelling_problems, no_server_problems     

    def __add_context_and_fix_ids(self, paragraph_problems, paragraphs):
        current_beginning_id = 0
        for problems, paragraph in zip(paragraph_problems, paragraphs):
            if problems:
                sentences_with_id = self._get_sentences_with_id(paragraph)
                print('получены айди предложений')
                current_sent_id = 0
                for problem in problems:
                    current_sent_data = sentences_with_id[current_sent_id]
                    while problem['pos'] > current_sent_data['end']:
                        current_sent_id += 1
                        current_sent_data = sentences_with_id[current_sent_id]
                        current_sent = current_sent_data['sent']
                    problem['context'] = current_sent
                    problem['bos'] += current_beginning_id
                    problem['end'] += current_beginning_id
                    print('отформатирован абзац')
            current_beginning_id = current_beginning_id + len(paragraph) + 1

    def _get_sentences_with_id(self, text, SPLITTINT_THRESHOLD=70, lang='russian'):
        '''
        Splits text into shorter fragments
        '''
        if len(text) <= SPLITTINT_THRESHOLD:
            sents_with_ids = [{'sent': text, 'pos':0, 'end': len(text)-1}]
        else:
            sents = sent_tokenize(text, 'russian')
            sents_with_ids = []
            prev_text_len=0
            text_copy = copy(text)
            for sent in sents:
                sent_position_data = {'sent': sent}
                position = text_copy.find(sent)
                print(position)
                sent_position_data['pos'] = prev_text_len + position
                sent_position_data['end'] = prev_text_len + position + len(sent)
                sents_with_ids.append(sent_position_data)
                text_copy = text_copy[sent_position_data['end']:]
                prev_text_len = sent_position_data['end']
        return sents_with_ids


def make_changes(text, corrections, ignore_options=['не исправлять']):
    text = copy(text)
    corrections = sorted(corrections, reverse=True)
    for correction in corrections:
        if correction['chosen_value'] not in ignore_options:
                text = text[:correction['pos']] + correction['chosen_value'] + text[correction['end']:]
    return 

spellchecker = SpellChecker()
text = """Торговля людьми, прежде всего женщинами и детьми, была громко осуждена международным сообществом как вопиющее нарушение прав человека, форма современного рабства и насилия над женщинами.
Из Протокола о предупреждении и пресечении торговли людьми, особенно женщинами и детьми, и наказании за нее, дополняющего Конвенцию Организации Объединенных Наций против транснациональной организованной преступности. 
Узнайте об инициативе в области борьбы против торговли людьми. Международной группы юристов-правозащитников.
Этот термин используется в контексте обсуждения прав человека, теневой экономики, политики, иммиграции, рабства. 
Россия является частью Европы потому-что Россияни одеваются обычно по моде, так-же как другие страны Европы, и так-же многие считают что они более подобны белой Европе чем Азии.  Политика в России отличается от Китая и например Индии. У нас нет систем касты. Даже если Россия чуть опаздывает от Европы по моде или например восточныя услугам, у нас все равно есть просвещение в отлицие от предедущих времён. Язык у нас так-же полнастью не похож на те-же Азиатские эроглифы. К мнению что основная часть России в Азии все равно не повод не считать Россиян Европейцами.  
Причины революции 1905 года были: либерализация страны, расширение гражданских свобод, улучшение условий труда, и т.д. Сначало  совершилась забастовка на заводе, затем мирная домонстрация 9-го января, и только потом известное "Кровавое воскресенье". Участвовал в этом тоже кризис 1903 года. Было ввостание рабочих и крестьян, недовольных зарплатой. В октябре месяце в Москве началась забастовка железнодорожников, которая переросла во Всероссийскую Октябрьскую политическую революцию.
Октябрьская революция 1917 года имело много причин, так-же как Первая руссская революция. Факторы экономические, политические, и социальные все имели к ней отношение. Крестьяни хотели помощичью землю, рабочие - восмичасовой день, а люди - люди хотели свободу. Первая мировая волна не решила проблем в России; в городах были очереди, психический надлом и маленькая зарплата при росте цен. Глава Временного правительства Керенский приказал о закрытии большевистских газет, и это было именно то, чего ждал Ленин для начала военных действий.Разнорабочий получал в дореволюционной России 14 руб. в месяц по  10 часов в день. Царский закон о штрафах  предусматривал возможность взыскания до 1/3 зарплаты без права обжалования не только за прогул, но и за "непослушание", за "нарушение тишины". "Но мало того, что мужик ест самый худший хлеб, он ещё надоедает. Если довольно хлеба в деревнях - едят по три раза; стало в хлебе умаление, хлебы коротки - едят по два раза, налегают больше на яровину, картофель, конопляную жмаку в хлеб прибавляют. Конечно - желудок набит, но от плохой пищи народ худеет, болеет, ребята растут туже - совершенно подобно тому, как бываетс дурносодержимым скотом..."
Автор приволит цены еды, зарплату, современные зарплаты, международную информацию.
Детей отправляют на работу с 12-летнего возраста, и часто работали по 10 часов в день. Многие работники исполняли физический труд, а только маленькая часть общества имела высококвалифицированные работы. Дети питались скудно, многим не хватало еды. Пример: "Статья "Голод в России": "В 1872 г. разразился первый самарский голод, поразивший именно ту губернию, которая до того времени считалась богатейшей житницей Росси.". В основном рабочии были неграмотными. ведь обязательное начальное образование было введено в 1908 году.
Из-за упрощения коммуникаций, как например интернета, люди снизили барьеры для торговли и услуг, и ускорили процесс глобализации. Эксплуатация стран третьего мира от лиц с высоким ВВП тоже стала причиной этого прогресса.

Глобальные проблема человечества включают эпидемию СПИДа, голод и бедность в странах третьего мира, и эксплуатацию этих же стран. Люди которые живут в "восточных" странах не знают стихию бедствий обрушевщих на неразвитые в плане экономики страны; которые не могут привыкнуть к такому новому, быстрому миру. У них просто нет (восновном) денежной возможности к конкуренции.

Я против процесса глобализации. При нём люди которые уже имеют капитал или приимущества из-за места жительства будут продолжать богатеть. А те которые уже бедные - беднеть. Люди теряють свою культуру и многие даже национальные диалекты или языки. Например, племена Индейцев в Америке. Несколько больших предприятий будут контролировать всю экономию - у стран не будет независимости. Открытие границ значит что можно спрятать украденные деньги и эксплуатировать страны третьего мира. 

«Священная война» это гимн страны во время Великой Отечественной Войны. Эта песня вызывает чувство патриотизма и гордости за свою Отчизну.  Также, песня вдохновляет советский  народ встать в бой, и призывает бросить все силы на защиту Родины. В песни говорится о ярости, которая должна вскипать при битве за свет и мир - против фашизма. Одна из главных идей гимна это борьба против «царства тьмы», и эта фраза имеет эмоциональную нагрузку. Цель этой песни - это отпор мучителям людей, «фашистской нечисти».
Песня «Здесь птицы не поют» очень грустная, в отличие от гимна, при ней сжимается сердце.  Эти музыкальные произведения были созданы, чтобы поднять силу духа как нашей армии так и работников тыла. Обе песни придавали уверенность в  победы. 
Советский Союз заплатил дорого за эту войну. Свыше 20 миллионов человек, многие из которых ушли на фронт добровольно, пали на полях сражений и скончались от ран. В итоге, эти песни приближали победу над вероломным врагом.
ермин "холодная война" был использован Черчилем в его речи в Фултоне (США) в 1946г. Именно  тогда его выступление явилось символом начала "холодной войны". "Холодная война" была конфронтацией  между США и СССР, которая  не дошла до военных действий. В конце второй мировой войны СССР расширяла "социалистический лагерь", а США во главе западных стран пытались его разрушть. Так как обе страны имели интересы в развитии индустриального общества, поиски ресурсов для увеличения промышленного роста в экономике были на первом месте. К счастью, обладание ядерными бомбами предотвращало настоящую войну, но "железный занавес" уже в полной силе работал против Советского Союза.
"""

print(spellchecker.check_spelling(text))
