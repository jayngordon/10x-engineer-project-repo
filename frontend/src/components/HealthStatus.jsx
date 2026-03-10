import { useEffect, useState } from "react";
import { getHealth } from "../api/health";

const HealthStatus = () => {
  const [healthy, setHealthy] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    let ignore = false;
    const loadHealth = async () => {
      setLoading(true);
      try {
        const data = await getHealth();
        if (!ignore) {
          setHealthy(data?.status === "healthy");
        }
      } catch (err) {
        if (!ignore) {
          setHealthy(false);
        }
      } finally {
        if (!ignore) {
          setLoading(false);
        }
      }
    };
    loadHealth();
    return () => {
      ignore = true;
    };
  }, []);

  const badgeText = loading
    ? "Checking backend…"
    : healthy === null
    ? "Pending"
    : healthy
    ? "Backend healthy"
    : "Backend unavailable";

  const badgeClasses = healthy ? "bg-emerald-500/20 text-emerald-300" : "bg-rose-500/10 text-rose-300";

  return (
    <div className={`rounded-full border border-slate-800 px-4 py-2 text-sm font-semibold ${badgeClasses}`}>
      {badgeText}
    </div>
  );
};

export default HealthStatus;
