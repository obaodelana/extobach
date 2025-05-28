from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Sentiment:
    def __init__(self, yt_data: dict) -> None:
        self.yt_data = yt_data

    def _get_stats(self) -> dict:
        stats = {}

        for year, videos in self.yt_data.items():
            stats[int(year)] = []
            for video in videos:
                comments = video['topComments']
                for comment in comments:
                    stats[int(year)].append(comment["text"])

        return stats

    def get_score(self):
        sid_obj = SentimentIntensityAnalyzer()

        score = {}
        stats = self._get_stats()
        for year, comments in stats.items():
            if len(comments) > 0:
                # Get list of compound scores for each comment
                compound_scores = [sid_obj.polarity_scores(comment)['compound']
                                   for comment in comments]
                # Get the average compound score for all comments in each year
                score[year] = sum(compound_scores) / len(comments)

        return score
