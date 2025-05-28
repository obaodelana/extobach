import './Comments.css';

function Comments({ comments }) {
  if (!comments || comments.length === 0) {
    return (
      <div className="comments-container">
        <h3 className="comments-title">Customer Reviews</h3>
        <div className="no-comments">
          <p>No reviews available for this product yet.</p>
        </div>
      </div>
    );
  }

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  const renderStars = (rating) => {
    if (!rating) return null;
    const stars = [];
    const fullStars = Math.floor(rating);
    const hasHalfStar = rating % 1 !== 0;
    
    for (let i = 0; i < fullStars; i++) {
      stars.push(<span key={i} className="star filled">★</span>);
    }
    
    if (hasHalfStar) {
      stars.push(<span key="half" className="star half">★</span>);
    }
    
    const emptyStars = 5 - Math.ceil(rating);
    for (let i = 0; i < emptyStars; i++) {
      stars.push(<span key={`empty-${i}`} className="star empty">☆</span>);
    }
    
    return <div className="star-rating">{stars}</div>;
  };

  return (
    <div className="comments-container">
      <h3 className="comments-title">Customer Reviews ({comments.length})</h3>
      <div className="comments-list">
        {comments.map((comment, index) => (
          <div key={index} className="comment-item">
            <div className="comment-header">
              <div className="comment-author">
                <span className="author-name">{comment.author || 'Anonymous'}</span>
                {comment.verified && (
                  <span className="verified-badge">✓ Verified Purchase</span>
                )}
              </div>
              <div className="comment-meta">
                {comment.rating && renderStars(comment.rating)}
                {comment.date && (
                  <span className="comment-date">{formatDate(comment.date)}</span>
                )}
              </div>
            </div>
            
            {comment.title && (
              <h4 className="comment-title">{comment.title}</h4>
            )}
            
            <div className="comment-content">
              <p>{comment.content || comment.text || comment.review}</p>
            </div>
            
            {comment.helpful && (
              <div className="comment-footer">
                <span className="helpful-count">
                  👍 {comment.helpful} people found this helpful
                </span>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default Comments;