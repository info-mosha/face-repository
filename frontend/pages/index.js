import { useState } from "react";
import axios from "axios";

export default function Home() {
  const [file, setFile] = useState(null);
  const [results, setResults] = useState([]);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("http://localhost:8000/search/", formData);
    setResults(res.data.matches);
  };

  return (
    <div style={{ padding: 40 }}>
      <h1>ابحث عن صورك</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>بحث</button>

      <div>
        {results.map((img, i) => (
          <img key={i} src={img} width="200" />
        ))}
      </div>
    </div>
  );
}
