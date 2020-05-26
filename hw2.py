from operator import itemgetter
from copy import deepcopy


def find_cheaters(competitions):
    if not competitions:
        return []
    cheaters_index_list = []

    for index, competition_candidate in enumerate(competitions):
        is_a_cheater = False
        competition_name = competition_candidate['competition name']
        competition_id = competition_candidate['competitor id']
        iteration_index = index + 1
        if iteration_index == len(competitions):
            break
        competitor = competitions[iteration_index]

        while competitor['competition name'] == competition_name:
            if competitor['competitor id'] == competition_id:
                cheaters_index_list.append(iteration_index)
                if is_a_cheater is False:
                    cheaters_index_list.append(index)
                    is_a_cheater = True
            iteration_index += 1
            if iteration_index == len(competitions):
                break
            competitor = competitions[iteration_index]

    return sorted(cheaters_index_list)


def remove_cheaters(cheaters_index_list, competitions):
    valid_competitors = []
    for index, entry in enumerate(competitions):
        if index not in cheaters_index_list:
            valid_competitors.append(entry)
    return valid_competitors


def get_country(entry):
    return entry['competitor country']


def calc_winners(candidates):
    competition_champs = []
    for entry in candidates:
        if candidates.index(entry) == 0:
            entry2 = entry
        if entry2 is None:
            break
        competition_name = candidates[candidates.index(entry)]['competition name']
        winning_list = [competition_name]
        count = 0
        ans = False # flag that helps to determine if we've still haven't reached the end
        if entry == entry2:
            last_index = candidates.index(entry)
            for iterator in candidates[last_index::]:
                if iterator['competition name'] != competition_name:
                    ans = True
                    break
                if count == 3:
                    break
                winning_list.append(get_country(iterator))
                count += 1

            if len(winning_list) < 4:
                while len(winning_list) < 4:
                    winning_list.append('undef_country')

            competition_champs.append(winning_list)
            if ans is True:
                next_index = candidates.index(iterator)

            else:
                next_index = candidates.index(iterator) + 1

            if next_index == len(candidates):
                entry2 = None

            else:
                entry2 = candidates[next_index]

    if not competition_champs:
        return []

    return competition_champs


def printCompetitor(competitor):
    '''
    Given the data of a competitor, the function prints it in a specific format.
    Arguments:
        competitor: {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    competition_type = competitor['competition type']
    competitor_id = competitor['competitor id']
    competitor_country = competitor['competitor country']
    result = competitor['result']

    print \
            (
            f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if
                 country != undef_country]
    print(f'The winning competitors in {competition_name} are from: {countries}')


def key_sort_competitor(competitor):
    '''
    A helper function that creates a special key for sorting competitors.
    Arguments:
        competitor: a dictionary contains the data of a competitor in the following format: 
                    {'competition name': competition_name, 'competition type': competition_type,
                        'competitor id': competitor_id, 'competitor country': competitor_country, 
                        'result': result}
    '''
    competition_name = competitor['competition name']
    result = competitor['result']
    return (competition_name, result)


def readParseData(file_name):
    '''
    Given a file name, the function returns a list of competitors.
    Arguments: 
        file_name: the input file name. Assume that the input file is in the directory of this script.
    Return value:
        A list of competitors, such that every record is a dictionary, in the following format:
            {'competition name': competition_name, 'competition type': competition_type,
                'competitor id': competitor_id, 'competitor country': competitor_country, 
                'result': result}
    '''
    competitors_in_competitions = []
    competitor_lines = []
    # TODO Part A, Task 3.4
    with open(file_name, 'r') as f:
        lines = f.readlines()
        for line in lines:
            line_parts = line.split()
            if line_parts[0] == 'competition':
                competitors_in_competitions.append({'competition name': line_parts[1],
                                                    'competition type': line_parts[3],
                                                    'competitor id': int(line_parts[2]),
                                                    'competitor country': 'none',
                                                    'result': int(line_parts[4])})
            else:
                competitor_lines.append(line_parts[1:])

        for line_parts in competitor_lines:
            for competition_entry in competitors_in_competitions:
                if int(line_parts[0]) == competition_entry['competitor id']:
                    competition_entry['competitor country'] = line_parts[1]

        return competitors_in_competitions


def calcCompetitionsResults(competitors_in_competitions):
    '''
    Given the data of the competitors, the function returns the champs countries for each competition.
    Arguments:
        competitors_in_competitions: A list that contains the data of the competitors
                                    (see readParseData return value for more info)
    Return value:
        A list of competitions and their champs (list of lists).
        Every record in the list contains the competition name and the champs, in the following format:
        [competition_name, winning_gold_country, winning_silver_country, winning_bronze_country]
    '''

    competitions_champs = []
    # TODO Part A, Task 3.5

    untimed_competitions = [dict for dict in competitors_in_competitions if dict['competition type'] == 'untimed']
    timed_competitions = [dict for dict in competitors_in_competitions if dict['competition type'] == 'timed'
                          or dict['competition type'] == 'knockout']

    sorted_timed_competitions = sorted(timed_competitions, key=key_sort_competitor)
    sorted_untimed_competitions = sorted(untimed_competitions, key=key_sort_competitor, reverse=True)

    cheaters_list_timed = find_cheaters(sorted_timed_competitions)
    cheaters_list_untimed = find_cheaters(sorted_untimed_competitions)

    clear_timed_list = remove_cheaters(cheaters_list_timed, sorted_timed_competitions)
    clear_untimed_list = remove_cheaters(cheaters_list_untimed, sorted_untimed_competitions)

    winners_timed = calc_winners(clear_timed_list)
    winners_untimed = calc_winners(clear_untimed_list)

    competitions_champs.extend(winners_untimed)
    competitions_champs.extend(winners_timed)
    return competitions_champs


def partA(file_name='input.txt', allow_prints=True):
    # read and parse the input file
    competitors_in_competitions = readParseData(file_name)
    if allow_prints:
        for competitor in sorted(competitors_in_competitions, key=key_sort_competitor):
            printCompetitor(competitor)

    # calculate competition results
    competitions_results = calcCompetitionsResults(competitors_in_competitions)
    if allow_prints:
        for competition_result_single in sorted(competitions_results):
            printCompetitionResults(*competition_result_single)

    return competitions_results


def partB(file_name='input.txt'):
    competitions_results = partA(file_name, allow_prints=False)
    import Olympics
    olympics = Olympics.OlympicsCreate()

    for competition in competitions_results:
        Olympics.OlympicsUpdateCompetitionResults(
            olympics, str(competition[1]), str(competition[2]), str(competition[3]))

    Olympics.OlympicsWinningCountry(olympics)
    Olympics.OlympicsDestroy(olympics)


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''
    file_name = 'tests/in/test1.txt'

    partA(file_name, True)
    partB(file_name)
