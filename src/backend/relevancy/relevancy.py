from retrieval.yt import YTRetriever
from retrieval.retriever import Retriever


class Relevancy(Retriever):
    def __init__(self,
                product_name: str,
                release_date: int) -> None:
        super().__init__(product_name, release_date)

        #Cache to avoid repeated API calls
        self._yt_data = None
    
    def load_data(self):
        if self._yt_data is None:
            retriever = YTRetriever(self.product_name, self.release_date)
            self._yt_data = retriever.retrieve()
            
        return self._yt_data()
    
    def all_views(self) -> int:        
        video_data = self.load_data()

        total_views = 0

        # Extract all view count for all videos in each year
        for _ , videos in video_data.items():
            for video in videos:
                view_count = video['statistics'].get('views', 'N/A')

                if view_count != 'N/A':
                    total_views += int(view_count)

        return total_views
    

    def all_likes(self) -> int:        
        video_data = self.load_data()

        total_likes = 0

        # Extract all view count for all videos in each year
        for _ , videos in video_data.items():
            #Retrieve view count for each video
            for video in videos:
                like_count = video['statistics'].get('likes', 'N/A')

                if like_count != 'N/A':
                    total_likes += int(like_count)

        return total_likes



    #Return relevancy score across all videos in the last 5 years
    def get_score(self) -> int:
       views = self.all_views()
       likes = self.all_likes()

       if likes == 0:
           return float('inf')

       return f"Relevancy score for {self.product_name} is: {views / likes}" 

    

