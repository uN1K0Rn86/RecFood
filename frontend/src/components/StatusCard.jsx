import Card from "./Card.jsx";

const StatusCard = ({ apiError, dbError, recipesError }) => (
  <Card
    style={{
      backgroundColor: "#0f172a",
      color: "#f8fafc",
      textAlign: "center",
    }}
  >
    <div style={{ fontSize: "1.1rem", fontWeight: "600" }}>RecFood</div>
    {apiError ? (
      <div style={{ color: "#fca5a5", marginTop: "0.5rem" }}>
        API unavailable: {apiError}
      </div>
    ) : null}
    {dbError ? (
      <div style={{ color: "#fca5a5", marginTop: "0.5rem" }}>
        Database unavailable: {dbError}
      </div>
    ) : null}
    {recipesError ? (
      <div style={{ color: "#fca5a5", marginTop: "0.5rem" }}>
        Recipes unavailable: {recipesError}
      </div>
    ) : null}
  </Card>
);

export default StatusCard;
