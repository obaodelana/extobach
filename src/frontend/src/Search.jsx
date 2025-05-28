import { useState } from 'react';
import Suggestion from './Suggestion';
import Product from './Product';
import Loader from './Loader';



function Search() {
  const [suggestions, setSuggestions] = useState([])
  const [product, setProduct] = useState()
  const [details, setDetails] = useState();
  const [loaderVisibility, setLoaderVisibility] = useState(false);

  async function getProductDetails(event) {
    event.preventDefault();
    setLoaderVisibility(true);
    setDetails(null);
    const searchQuery = document.getElementById('searchbox').value;
    // document.getElementById('searchbox').value = '';
    
    // get search query from input field
    const product_url = "/sonar/product"
    // const suggestion_url = "/sonar/suggestions"
    if (!searchQuery) return;

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
    }

    // ask server to give suggestions

    // store sugesstions in a list

    // pass list as props to suggestion
  }
  
  return (
    <main>
      <div className="jumbotron">
        <h1>Goodsline</h1>
        <form action="#" method="get" id="search-form" onSubmit={async e => {
          const data = await getProductDetails(e);
          const loader = document.querySelector(".loader");
          loader.setAttribute("display", "block")
          setDetails(data)
        } }>
          <input type="text" name="search-input" id="searchbox" placeholder="Search a product..." />
          <input type="submit" className="hidden-submit" hid-focus="true" />
        </form>
        <Suggestion suggestions={suggestions} />
      </div>
      {loaderVisibility && <Loader />}
      {details && <Product productDetails={details}/>}
    </main>
  )
}
/*
{
    availability: "In stock",
    brand: "Sony",
    category: "Technology",
    currency: "USD",
    description: "A high-quality product that meets all your needs.",
    image: [
      "https://example.com/image1.jpg",
      "https://example.com/image2.jpg",
      "https://example.com/image3.jpg",
      "https://example.com/image4.jpg",
      "https://example.com/image5.jpg"
    ],
    name: "Sample Product",
    price: {
      high: 100,
      low: 50
    },
    rating: 4.5,
    releaseDate: 2024
  }
*/

export default Search