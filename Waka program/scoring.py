class Scoring:
    @staticmethod
    def return_scores(lif_teams, points_reference):
        regional_scores = {}
        for team in lif_teams:
            team_id, team_place, team_name, team_regional_association = team
            team_place = int(team_place)
            score = points_reference.get(str(team_place), points_reference[">"])
            if team_regional_association not in regional_scores:
                regional_scores[team_regional_association] = 0
            regional_scores[team_regional_association] += score
        return regional_scores

    @staticmethod
    def return_year_sum_score(files_regional_association_score_list):
        year_scores = {}
        for file_scores in files_regional_association_score_list:
            for region, score in file_scores.items():
                if region not in year_scores:
                    year_scores[region] = 0
                year_scores[region] += score
        return year_scores

    @staticmethod
    def sort_score(year_regional_association_scores):
        return dict(sorted(year_regional_association_scores.items(), key=lambda item: item[1], reverse=True))

scoring_c = Scoring()