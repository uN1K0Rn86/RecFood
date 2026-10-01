import { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [message, setMessage] = useState("");
  const [dbHealth, setDbHealth] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadData = async () => {
      try {
        const [messageResponse, dbResponse] = await Promise.all([
          axios.get("http://127.0.0.1:8000/"),
          axios.get("http://127.0.0.1:8000/db-health"),
        ]);

        setMessage(messageResponse.data.message);
        setDbHealth(String(dbResponse.data.database));
      } catch (error) {
        console.error(error);
        setError(error.message);
      }
    };

    loadData();
  }, []);

  return (
    <div>
      {error ? <div>Request failed: {error}</div> : null}
      <div>{message || "Loading..."}</div>
      <div>Database status: {dbHealth || "Loading..."}</div>
    </div>
  );
};

export default App;
