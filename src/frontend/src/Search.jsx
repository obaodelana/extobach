import { useState } from 'react';
import Suggestion from './Suggestion';
import Product from './Product';
import Loader from './Loader';

function Search() {
  const [suggestions, setSuggestions] = useState([])
  const [product, setProduct] = useState()
  const [details, setDetails] = useState();
  const [loaderVisibility, setLoaderVisibility] = useState(false);
  const [isSearching, setIsSearching] = useState(false);

  async function getProductDetails(event) {
    event.preventDefault();
    setLoaderVisibility(true);
    setIsSearching(true);
    setDetails(null);
    const searchQuery = document.getElementById('searchbox').value;
    
    const product_url = "/sonar/product"
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
      return await response.json();
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
            setDetails(data)
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
      </div>
    </main>
  )
}

export default Search