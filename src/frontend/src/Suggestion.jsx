function Suggestion({ suggestions }) {
  if (!suggestions || suggestions.length === 0) {
    return null;
  }

  const suggestionItems = suggestions.map((suggestion, index) => (
    <li key={index} className="suggestion-item">
      <span>{suggestion}</span>
    </li>
  ));

  return (
    <div className="suggestion-container">
      <ul className="suggestion-list">
        {suggestionItems}
      </ul>
    </div>
  )
}

export default Suggestion