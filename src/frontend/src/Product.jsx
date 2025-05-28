import './Product.css';
import { useState } from 'react';

function Product({productDetails}) {
  const [imageIndex, setImageIndex] = useState(0);
  console.log(productDetails)

  return(
    <div className="product-container">
      <div>
        <div className="product-image">
          <img src={productDetails.images[imageIndex]} alt="Product" onClick={() => {setImageIndex(prevIndex => (prevIndex+1)%5)}} />
        </div>
        <div className="product-details">
          <h2>{productDetails.name}</h2>
          <p>{productDetails.description}</p>
          <span className="price">From {productDetails.currency} {productDetails.price.low} - {productDetails.price.high}</span>
        </div>
      </div>
      <div className="product-stats">
        <div className="product-rating">
          <span>Rating: {productDetails.rating}</span>
        </div>
        <div className="product-availability">
          <span>Availability: {productDetails.availability}</span>
        </div>
        <div className="product-brand">
          <span>Brand: {productDetails.brand}</span>
        </div>
        <div className="product-category">
          <span>Category: {productDetails.category}</span>
        </div>
        <div className="product-release-date">
          <span>Release Date: {productDetails.releaseDate}</span>
        </div>
      </div>
    </div>
  )
}

export default Product