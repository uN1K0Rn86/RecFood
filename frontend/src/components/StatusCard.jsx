import Card from "./Card.jsx";

const StatusCard = ({ error, message, dbHealth }) => (
  <Card
    style={{
      backgroundColor: "#0f172a",
      color: "#f8fafc",
      textAlign: "center",
    }}
  >
    {error ? (
      <div style={{ color: "#fca5a5" }}>Request failed: {error}</div>
    ) : null}
    <div style={{ fontSize: "1.1rem", fontWeight: "600" }}>
      {message || "Loading..."}
    </div>
    <div style={{ color: "#cbd5e1", marginTop: "0.5rem" }}>
      Database status: {dbHealth || "Loading..."}
    </div>
  </Card>
);

export default StatusCard;
