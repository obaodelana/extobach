from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class Sentiment:
    def __init__(self,
                 product_name: str,
                 release_date: int, yt_data: dict) -> None:
        self.product_name = product_name
        self.release_date = release_date
        self.yt_data = yt_data
    
    def _get_stats(self):
        
        stats = {}

        for year, videos in self.yt_data:
            for video in videos:
                comment = video['topComments']['text']
                stats[int(year)] = comment
        
        return stats


    def get_score(self):
        
        sid_obj = SentimentIntensityAnalyzer()
        
        score = {}

        for year, comments in self._get_stats():
            #Get list of compound scores for each comment
            compound_scores = [sid_obj.polarity_scores(comment)['compound'] for comment in comments]

            if len(self._get_stats[int(year)]) > 0:
                #Get the average compound score for all comments in each year
                score[int(year)] = sum(compound_scores) / len(self._get_stats[int(year)])
            
        return score

