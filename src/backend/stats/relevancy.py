class Relevancy:
    def __init__(self,
                 yt_data: dict) -> None:
        self._yt_data: dict = yt_data

    def _get_stats(self, stat_name: str) -> dict[int, int]:
        video_data = self._yt_data

        stats = {}
        # Extract all view count for all videos in each year
        for year, videos in video_data.items():
            total = 0
            for video in videos:
                count = video['statistics'].get(stat_name, 'N/A')
                if count != 'N/A':
                    total += int(count)
            stats[int(year)] = total

        return stats

    def get_score(self) -> dict[int, float]:
        views = self._get_stats("views")
        likes = self._get_stats("likes")
        comments = self._get_stats("comments")

        score = {}

        video_data = self._yt_data
        for year, _ in video_data.items():
            year = int(year)

            score[year] = views[year] / likes[year]
            score[year] += comments[year] * 3

        return score
