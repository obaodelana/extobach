import './Product.css';
import { useState } from 'react';

function Product({productDetails}) {
  const [imageIndex, setImageIndex] = useState(0);
  console.log(productDetails)

  if (!productDetails) {
    return null;
  }

  const images = productDetails.images || productDetails.image || [];
  const totalImages = images.length;

  const handleImageClick = () => {
    if (totalImages > 1) {
      setImageIndex(prevIndex => (prevIndex + 1) % totalImages);
    }
  };

  const formatPrice = (price) => {
    if (typeof price === 'object' && price.low && price.high) {
      return `${productDetails.currency || 'USD'} ${price.low} - ${price.high}`;
    }
    return `${productDetails.currency || 'USD'} ${price}`;
  };

  const getAvailabilityClass = (availability) => {
    if (availability && availability.toLowerCase().includes('in stock')) {
      return 'availability-in-stock';
    }
    return 'availability-out-of-stock';
  };

  return(
    <div className="product-container">
      <div className="product-image-section">
        <div className="product-image">
          {images.length > 0 ? (
            <>
              <img 
                src={images[imageIndex]} 
                alt={`${productDetails.name} - Image ${imageIndex + 1}`}
                onClick={handleImageClick}
              />
              {totalImages > 1 && (
                <div className="image-indicator">
                  {imageIndex + 1} / {totalImages}
                </div>
              )}
            </>
          ) : (
            <div style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              color: 'var(--text-secondary)',
              fontSize: '1.1rem'
            }}>
              No Image Available
            </div>
          )}
        </div>
      </div>
      
      <div className="product-details">
        <h2 className="product-name">{productDetails.name}</h2>
        
        {productDetails.description && (
          <p className="product-description">{productDetails.description}</p>
        )}
        
        {productDetails.price && (
          <div className="price-section">
            <span className="price">
              {formatPrice(productDetails.price)}
            </span>
          </div>
        )}
        
        <div className="product-stats">
          {productDetails.rating && (
            <div className="stat-item">
              <span className="stat-label">Rating</span>
              <span className="stat-value rating-value">
                ⭐ {productDetails.rating}/5
              </span>
            </div>
          )}
          
          {productDetails.availability && (
            <div className="stat-item">
              <span className="stat-label">Availability</span>
              <span className={`stat-value ${getAvailabilityClass(productDetails.availability)}`}>
                {productDetails.availability}
              </span>
            </div>
          )}
          
          {productDetails.brand && (
            <div className="stat-item">
              <span className="stat-label">Brand</span>
              <span className="stat-value">{productDetails.brand}</span>
            </div>
          )}
          
          {productDetails.category && (
            <div className="stat-item">
              <span className="stat-label">Category</span>
              <span className="stat-value">{productDetails.category}</span>
            </div>
          )}
          
          {productDetails.releaseDate && (
            <div className="stat-item">
              <span className="stat-label">Release Date</span>
              <span className="stat-value">{productDetails.releaseDate}</span>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default Product