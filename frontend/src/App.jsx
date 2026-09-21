import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [articles, setArticles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("Összes");
  const [selectedSource, setSelectedSource] = useState("Összes");
  const [darkMode, setDarkMode] = useState(false);
  const [search, setSearch] = useState("")
  const [debouncedSearch, setDebouncedSearch] = useState("")

  useEffect(() => {
  const params = new URLSearchParams()

  if (search) {
    params.append("search", search)
  }

  if (selectedCategory) {
    params.append("category", selectedCategory)
  }

  if (selectedSource) {
    params.append("source", selectedSource)
  }

  const queryString = params.toString()

  const url = queryString
    ? `/api/articles?${queryString}`
    : "/api/articles"

  fetch(url)
    .then((response) => response.json())
    .then((data) => setArticles(data))
    .catch((error) => {
      console.error("Hiba a hírek lekérésekor:", error)
    })
  }, [search, selectedCategory, selectedSource])

  const categories = [
    "Összes",
    ...new Set(articles.map((article) => article.category))
  ];

  const sources = [
    "Összes",
    ...new Set(articles.map((article) => article.source))
  ];
  useEffect(() => {
    const timer = setTimeout(() => {
      setDebouncedSearch(search)
    }, 300)

    return () => {
      clearTimeout(timer)
    }
  }, [search])

  return (
    <div className={darkMode ? "app dark" : "app"}>
<     header className="top-section">
       <div className="top-bar">
         <h1>Autós Hírek</h1>

         <button
           className="theme-button"
           onClick={() => setDarkMode(!darkMode)}
         >
           {darkMode ? "Világos mód" : "Sötét mód"}
         </button>
       </div>

       <div className="filters">
         <input
           type="text"
           placeholder="Keresés a hírek között..."
           value={search}
           onChange={(event) => setSearch(event.target.value)}
         />

         <select
           value={selectedCategory}
           onChange={(event) => setSelectedCategory(event.target.value)}
         >
           {categories.map((category) => (
             <option key={category} value={category}>
               {category}
             </option>
           ))}
         </select>
         
         <select
           value={selectedSource}
           onChange={(event) => setSelectedSource(event.target.value)}
         >
           {sources.map((source) => (
             <option key={source} value={source}>
               {source}
             </option>
           ))}
         </select>
       </div>
      </header>

      <main className="article-list">
        {filteredArticles.map((article) => (
        <article
          className="article-card"
          key={article.id}
          onClick={() => window.open(article.link, "_blank")}
        >
          <div className="article-meta">
            <span>{article.source}</span>
            <span>{article.category}</span>
          </div>
                
          <h2>{article.title}</h2>
                
          <p>{article.summary}</p>
        </article>
        ))}
      </main>
    </div>
  );
}

export default App;