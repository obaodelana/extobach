import { useState } from 'react';
import Suggestion from './Suggestion';
import Product from './Product';
import Loader from './Loader';
import Comments from './Comments';
import Graph from './Graph';

function Search() {
  const [suggestions, setSuggestions] = useState([])
  const [product, setProduct] = useState()
  const [details, setDetails] = useState();
  const [comments, setComments] = useState();
  const [sentimentData, setSentimentData] = useState();
  const [relevancyData, setRelevancyData] = useState();
  const [loaderVisibility, setLoaderVisibility] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  async function getProductDetails(event) {
    event.preventDefault();
    setLoaderVisibility(true);
    setIsSearching(true);
    setDetails(null);
    setComments(null);
    setSentimentData(null);
    setRelevancyData(null);
    
    const searchQuery = document.getElementById('searchbox').value;
    
    const product_url = "/sonar/product"
    const stat_url = "/stats"

    if (!searchQuery) {
      setLoaderVisibility(false);
      setIsSearching(false);
      return;
    }

    try {
      const response = await fetch(product_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productName: searchQuery })
      });
      const data = await response.json();
      
      // Set product details
      setDetails(data);

      const statResponse = await fetch(stat_url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ productName: data.name, releaseDate: data.releaseDate })
      })

      const statData = await statResponse.json();
      setComments(statData.comments);
      setRelevancyData(statData.relevancy);
      setSentimentData(statData.sentiment);
      console.log(statData)

      return data;
    } catch (error) {
      console.error('Error fetching product details:', error);
    } finally {
      setLoaderVisibility(false);
      setIsSearching(false);
    }
  }
  
  return (
    <main>
      <div className="jumbotron">
        <h1>GoodsLine</h1>
        <form 
          action="#" 
          method="get" 
          id="search-form" 
          onSubmit={async e => {
            const data = await getProductDetails(e);
          }}
        >
          <input 
            type="text" 
            name="search-input" 
            id="searchbox" 
            placeholder="Search for products..." 
            autoComplete="off"
          />
          <input type="submit" className="hidden-submit" />
        </form>
        <Suggestion suggestions={suggestions} />
      </div>
      
      {loaderVisibility && (
        <div className="loading-container">
          <Loader />
          <div className="loading-text">Searching for products...</div>
        </div>
      )}
      
      <div className="product-results">
        {details && <Product productDetails={details}/>}
        
        {/* Graphs Container */}
        {/* {(sentimentData || relevancyData) && ( */}
          <div className="graphs-container">
            {sentimentData && (
              <Graph 
                data={sentimentData} 
                title="Sentiment Analysis" 
                type="sentiment"
              />
            )}
            {relevancyData && (
              <Graph 
                data={relevancyData} 
                title="Relevancy Score" 
                type="relevancy"
              />
            )}
          </div>
        {/* )} */}
        
        {/* Comments Section */}
        {comments && <Comments comments={comments} />}
      </div>
    </main>
  )
}

export default Search