from retrieval.yt import YTRetriever


class Relevancy:
    def __init__(self,
                 product_name: str,
                 release_date: int) -> None:
        self.product_name = product_name
        self.release_date = release_date
        # Cache to avoid repeated API calls
        self._yt_data: dict | None = None

    def _load_data(self) -> dict:
        if self._yt_data is None:
            retriever = YTRetriever(self.product_name, self.release_date)
            self._yt_data = retriever.retrieve()

        return self._yt_data

    def _get_stats(self, stat_name: str) -> dict[int, int]:
        video_data = self._load_data()

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

        video_data = self._load_data()
        for year, _ in video_data.items():
            year = int(year)

            score[year] = views[year] / likes[year]
            score[year] += comments[year] * 3

        return score
