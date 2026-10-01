import { useState, useEffect } from "react";
import axios from "axios";

const App = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const getMessage = async () => {
      try {
        const response = await axios.get("http://localhost:8000/");
        setMessage(response.data.message);
      } catch (error) {
        console.error("Request failed:", error);
      }
    };

    getMessage();
  }, []);

  return (
    <div>
      <div>{message || "Loading..."}</div>
    </div>
  );
};

export default App;
