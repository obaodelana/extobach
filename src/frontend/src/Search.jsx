function Search() {
  return (
    <main>
      <div class="jumbotron">
        <h1>Goodsline</h1>
        <form action="#" method="get" id="search-form">
          <input type="text" name="search-input" id="searchbox" placeholder="Search a product..." />
          <input type="submit" class="hidden-submit" hid-focus="true" />
        </form>
      </div>
    </main>
  )
}

export default Search