function Suggestion({ suggestions }) {
  const suggestionItems = suggestions.map(suggestion => (
    <li className="suggestion-item">
      <span>{suggestion}</span>
    </li>
  ))

  return (
    <div className="suggestion-container">
      {suggestionItems}
    </div>
  )
}

export default Suggestion