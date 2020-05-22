

from operator import itemgetter

def isValidChampion(competitions, competition_name):

    if competitions[-1]['competition name'] != competition_name:
        # there is no competition entries for this competition name
        return True
    champion_id = competitions[-1]['competitor id']
    is_valid = True

    for competition_entry in competitions[-2::-1]:
        if competition_entry['competition name'] != competition_name:
            break
        elif competition_entry['competitor id'] == champion_id:
            is_valid = False
            competitions.remove(competition_entry)

    if not is_valid:
        del competitions[-1]
        return False

    return True


def clearInvalidChampions(competitions,competition_name):
    while not isValidChampion(competitions,competition_name):
        continue
    return


def deleteAllCompetitionEntries(competitions, competition_to_delete):
    if competitions or len(competitions) > 0:
        deleted = True
    else:
        deleted = False
    while deleted: #TODO fix bug here index error
        if competitions[-1]['competition name'] != competition_to_delete:
            deleted = False
            continue
        else:
            del competitions[-1]

    return


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

    print(f'Competitor {competitor_id} from {competitor_country} participated in {competition_name} ({competition_type}) and scored {result}')


def printCompetitionResults(competition_name, winning_gold_country, winning_silver_country, winning_bronze_country):
    '''
    Given a competition name and its champs countries, the function prints the winning countries 
        in that competition in a specific format.
    Arguments:
        competition_name: the competition name
        winning_gold_country, winning_silver_country, winning_bronze_country: the champs countries
    '''
    undef_country = 'undef_country'
    countries = [country for country in [winning_gold_country, winning_silver_country, winning_bronze_country] if country != undef_country]
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
    # TODO Part A, Task 3.4
    with open(file_name, 'r') as f:
        lines = f.readlines()
        competitor_lines = []
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
    timed_competitions = [dict for dict in competitors_in_competitions if dict['competition type'] == 'timed']
    knockout_competitions = [dict for dict in competitors_in_competitions if dict['competition type'] == 'knockout']

    sorted_timed_competitions = sorted(timed_competitions, key=key_sort_competitor, reverse=True)
    sorted_untimed_competitions = sorted(untimed_competitions, key=key_sort_competitor)
    sorted_knockout_competitions = sorted(knockout_competitions, key=key_sort_competitor, reverse=True)


    competitions_types =[
        sorted_untimed_competitions,
        sorted_timed_competitions,
        sorted_knockout_competitions
    ]

    for current_type in competitions_types:

        while current_type:
            current_competition = current_type[-1]['competition name']
            clearInvalidChampions(current_type, current_competition)

            if current_type[-1]['competition name'] != current_competition:
                continue
            else:
                current_result =[current_competition]
                for i in range(3):
                    if (not current_type) or (current_type[-1]['competition name'] != current_competition):
                        current_result.append('undef_country')
                    else:
                        champion_entry = current_type.pop(-1)
                        current_result.append(champion_entry['competitor country'])       # appending the champion to the score board
                competitions_champs.append(current_result)                                            # adding the competition result to the competitions_champs
                deleteAllCompetitionEntries(current_type, current_competition) #deleting all entries of that competition - don't need them.

    return competitions_champs


def partA(file_name = 'input.txt', allow_prints = True):
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


def partB(file_name = 'input.txt'):
    competitions_results = partA(file_name, allow_prints = False)
    # TODO Part B


if __name__ == "__main__":
    '''
    The main part of the script.
    __main__ is the name of the scope in which top-level code executes.
    
    To run only a single part, comment the line below which correspondes to the part you don't want to run.
    '''
    file_name = 'test2.txt'


    partA(file_name, True)
    # partB(file_name)
