import language_tool_python
import Levenshtein as lev

import json
import re
import string
import typing as tp
from typing import Type


CRITERIA_PATH = "criteria.json"
QUARTER = " квартал"
NOT_VALID_TEXT_LENGTH = "Поле текст пустое"
NOT_VALID_CLASS = "Не подходит ни один из классов"
NOT_VALID_TWO_CLASSES = "Возможно несколько вариантов"
NOT_VERIFIED = {
    "name": None,
    "code": 0,
    "path": ["Не верифицированные документы", None, None, None, None],
    "criteria_list": [],
    "compute_date": 0
}

MONTH_NUMBER = {
    "январь": 1, "февраль": 2, "март": 3,
    "апрель": 4, "май": 5, "июнь": 6,
    "июль": 7, "август": 8, "сентябрь": 9,
    "октябрь": 10, "ноябрь": 11, "декабрь": 12
}

MONTH_NUMBER_P = {
    "января": 1, "февраля": 2, "марта": 3,
    "апреля": 4, "мая": 5, "июня": 6,
    "июля": 7, "августа": 8, "сентября": 9,
    "октября": 10, "ноября": 11, "декабря": 12
}

DATE_WORD = "дата"

SIMPLE_DATE_REG = r"\d\d \w\w \d\d\d\d"


def correct_text(txt: str) -> str:
#     tool = language_tool_python.LanguageTool('ru-RU')
#     txt = tool.correct(txt)
#     txt = txt.lower().encode('ascii', 'ignore').decode()
    txt = txt.lower()
    filt = re.compile("[^а-яa-z0-9 ]+")
    txt = re.sub(filt, "", txt)
#     txt = re.sub('[%s]' % re.escape(string.punctuation), ' ', txt)
    return txt


class CriteriaClassifier:
    def __init__(self, classes_json_path: str = CRITERIA_PATH, not_verified = NOT_VERIFIED,
                 not_verified_simple_threshold: float = 1.0, not_verified_lev_threshold: float = 0.8) -> None:
        self.classes = self._load_class_criteria_from_json(classes_json_path) # Список классов, принадлежность к которым проверяем
        assert len(self.classes) > 0
        self.not_verified = not_verified # Уровни для неверифицированных документов
        self.not_verified_lev_threshold = not_verified_lev_threshold # Порог, при достижении которого документ не считается принадлежащим классу
        self.not_verified_simple_threshold = not_verified_simple_threshold
        self.stats = dict()
        
    def __call__(self, text: str) -> tp.Any:
        text = correct_text(text)
        if len(text) == 0:
            self.not_verified["name"] = NOT_VALID_TEXT_LENGTH
            return self.not_verified
        words = text.split()
            
        simple_distances = [self._compute_simple_criteria_dist(cl, text) for cl in self.classes]
        lev_distances = [self._compute_lev_criteria_dist(cl, words) for cl in self.classes]
        time_distances = [self._compute_time_dist(cl, text) for cl in self.classes]
        self.stats["simple_distances"] = [(self.classes["code"], simple_distances[i]) for i in range(len(self.classes))]
        self.stats["lev_distances"] = [(self.classes["code"], lev_distances[i]) for i in range(len(self.classes))]
        self.stats["time_distances"] = [(self.classes["code"], time_distances[i]) for i in range(len(self.classes))]
        
        simple_min = self._find_min_inds(simple_distances, self.not_verified_simple_threshold)
        if len(simple_min) == 1:
            return self._return_class(text, simple_min[0])
        
        lev_min = self._find_min_inds(lev_distances, self.not_verified_lev_threshold,
                                      ignore={i for i in range(len(lev_distances)) if i not in simple_min})
        if len(lev_min) == 1:
            return self._return_class(text, lev_min[0])
        
        time_min = self._find_min_inds(time_distances, 10,
                                       ignore={i for i in range(len(time_distances)) if i not in lev_min})
        
        if len(time_min) == 1:
            return self._return_class(text, time_min[0])
        if len(time_min) > 1:
            self.not_verified["name"] = NOT_VALID_TWO_CLASSES
            return self.not_verified
        self.not_verified["name"] = NOT_VALID_CLASS
        return self.not_verified
    
    def get_stats(self):
        return self.stats
    
    def _return_class(self, text, ind: int) -> tp.Any:
        if self.classes[ind]["compute_date"] > 0:
            year, month, day = self._compute_date(text)
            self.classes[ind]["path"][2] = str(year)
            self.classes[ind]["path"][3] = str((month + 3) // 4) + QUARTER
        return self.classes[ind]
    
    def _find_min_inds(self, dst: tp.List[float], threshold: float, ignore: tp.Set[int] = {}) -> tp.List[int]:
        min_ind = None
        for i in range(len(dst)):
            if (min_ind is None or dst[i] < dst[min_ind]) and i not in ignore:
                min_ind = i
        if min_ind is None:
            return []
        return [i for i in range(len(dst)) if dst[i] == dst[min_ind] and dst[i] <= threshold and i not in ignore]
        
    def _compute_date(self, text: str) -> tp.Tuple[str]:
        try:
            match_dates = [(m.start(0), m.end(0), tuple(map(int, text[m.start(0):m.end(0)].split())))
               for m in re.finditer(SIMPLE_DATE_REG, text)]
            match_dates += [(m.start(0), m.end(0), text[m.start(0):m.end(0)].split())
                            for m in re.finditer(r"\d\d\s(?:" + "|".join(MONTH_NUMBER_P.keys()) + ")\s\d{4}", text)]
            match_dates += [(m.start(0), m.end(0), text[m.start(0):m.end(0)].split())
                            for m in re.finditer(r"\d\s(?:" + "|".join(MONTH_NUMBER_P.keys()) + ")\s\d{4}", text)]
            match_dates += [(m.start(0), m.end(0), text[m.start(0):m.end(0)].split())
                            for m in re.finditer(r"\d\d\s(?:" + "|".join(MONTH_NUMBER.keys()) + ")\s\d{4}", text)]
            match_dates += [(m.start(0), m.end(0), text[m.start(0):m.end(0)].split())
                            for m in re.finditer(r"\d\s(?:" + "|".join(MONTH_NUMBER.keys()) + ")\s\d{4}", text)]
            match_dates += [(m.start(0), m.end(0), text[m.start(0):m.end(0)].split())
                            for m in re.finditer(r"\s(?:" + "|".join(MONTH_NUMBER_P.keys()) + ")\s\d{4}", text)]
            match_dates += [(m.start(0), m.end(0), text[m.start(0):m.end(0)].split())
                            for m in re.finditer(r"\s(?:" + "|".join(MONTH_NUMBER.keys()) + ")\s\d{4}", text)]
            match_dates = sorted(match_dates, reverse=True)
            date = match_dates[-1][-1]
            if type(date[0]) == str:
                if len(date) == 2 and date[0] in MONTH_NUMBER:
                    return int(date[1]), MONTH_NUMBER[date[0]], 0
                if len(date) == 2 and date[0] in MONTH_NUMBER_P:
                    return int(date[1]), MONTH_NUMBER_P[date[0]], 0
                if date[1] in MONTH_NUMBER:
                    return int(date[2]), MONTH_NUMBER[date[1]], int(date[0])
                return int(date[2]), MONTH_NUMBER_P[date[1]], int(date[0])
            return date[2], date[1], date[0]
        except:
            return 0, 0, 0
    
    def _compute_time_dist(self, cl, text: str) -> float:
        year, month, day = self._compute_date(text)
        if cl["compute_date"] == month:
            return 0
        if cl["compute_date"] < 12 and cl["compute_date"] > 0 and month > 0 and month < 12:
            return 0
        return 1
    
    def _compute_simple_criteria_dist(self, class_criteria: tp.Dict[str, tp.Any], text: str) -> float:
        distance_sum = 0.0
        for crit in class_criteria["criteria_list"]:
            if crit in text:
                distance_sum += 1
        return 1.0 - distance_sum / len(class_criteria["criteria_list"]) # Процент не вошедших в документ критериев 
    
    def _compute_lev_criteria_dist(self, class_criteria: tp.Dict[str, tp.Any], words: tp.List['str']) -> float:
        distance_sum = 0.0
        for crit in class_criteria["criteria_list"]:
            min_dist = len(crit) + 0.0
            n_words = len(crit.split())
            for i in range(len(words)):
                substr = " ".join(words[i:min(i + n_words, len(words))])
                min_dist = min(min_dist, lev.distance(substr, crit))
            distance_sum += min_dist / max(len(crit), len(substr))
        return distance_sum / len(class_criteria["criteria_list"]) # Среднее минимальное расстояние между критериями и текстом. Принадлежит отрезку [0, 1]

    def _load_class_criteria_from_json(self, path):
        with open(path) as json_file:
            class_criteria = json.load(json_file)
            for cl in class_criteria:
                for i in range(len(cl["criteria_list"])):
                    cl["criteria_list"][i] = correct_text(cl["criteria_list"][i])
        return class_criteria
