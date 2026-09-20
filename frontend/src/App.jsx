import { useEffect, useState } from "react";

function App() {
  const [articles, setArticles] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/articles")
      .then((response) => response.json())
      .then((data) => {
        setArticles(data);
      })
      .catch((error) => {
        console.error("Hiba a hírek lekérésekor:", error);
      });
  }, []);

  return (
    <div>
      <h1>Autós Híraggregátor</h1>

      {articles.map((article) => (
        <div key={article.id}>
          <h2>{article.title}</h2>

          <p>{article.summary}</p>

          <p>
            Forrás: {article.source}
          </p>

          <p>
            Kategória: {article.category}
          </p>

          <a
            href={article.link}
            target="_blank"
            rel="noreferrer"
          >
            Cikk megnyitása
          </a>

          <hr />
        </div>
      ))}
    </div>
  );
}

export default App;