import { useEffect, useState } from "react";
import "./App.css";

function App() {
  const [articles, setArticles] = useState([])
  const [selectedCategory, setSelectedCategory] = useState("Összes")
  const [selectedSource, setSelectedSource] = useState("Összes")
  const [search, setSearch] = useState("")
  const [debouncedSearch, setDebouncedSearch] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")
  const [darkMode, setDarkMode] = useState(() => {
  return localStorage.getItem("theme") === "dark"
  })
  const categories = [
    "Összes",
    "Elektromos autók",
    "Motorsport",
    "Autótesztek",
    "Új autók",
    "Tuning",
    "Közlekedés",
    "Egyéb"
  ];

  const sources = [
    "Összes",
    "Vezess",
    "Autónavigátor"
  ];  
  useEffect(() => {
    localStorage.setItem("theme", darkMode ? "dark" : "light")
  }, [darkMode])
  useEffect(() => {
    const params = new URLSearchParams()

    if (debouncedSearch) {
      params.append("search", debouncedSearch)
    }

    if (selectedCategory !== "Összes") {
      params.append("category", selectedCategory)
    }

    if (selectedSource !== "Összes") {
      params.append("source", selectedSource)
    }

    const queryString = params.toString()

    const url = queryString
      ? `/api/articles?${queryString}`
      : "/api/articles"

    
    setLoading(true)
    setError("")

    fetch(url)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Nem sikerült lekérni a híreket.")
        }

        return response.json()
      })
      .then((data) => {
        setArticles(data)
      })
      .catch((error) => {
        console.error("Hiba a hírek lekérésekor:", error)
        setError("Nem sikerült betölteni a híreket.")
      })
      .finally(() => {
        setLoading(false)
      })
  }, [debouncedSearch, selectedCategory, selectedSource])
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
      <header className="top-section">
       <div className="top-bar">
         <h1>Autós Hírek</h1>
          <button
            className="theme-toggle"
            onClick={() => setDarkMode(!darkMode)}
            aria-label={darkMode ? "Világos mód" : "Sötét mód"}
          >
            <img
              src={darkMode ? "/sun.svg" : "/moon.svg"}
              alt=""
            />
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
        {loading && (
          <p className="status-message">
            Hírek betöltése...
          </p>
        )}
      
        {error && (
          <p className="status-message error-message">
            {error}
          </p>
        )}
      
        {!loading && !error && articles.length === 0 && (
          <p className="status-message">
            Nincs találat.
          </p>
        )}
      
        {!loading && !error && articles.map((article) => (
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