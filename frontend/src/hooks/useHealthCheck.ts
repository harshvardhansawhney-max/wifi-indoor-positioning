import { useEffect, useState } from "react";
import { healthAPI } from "@services/api";

export const useHealthCheck = () => {
  const [isHealthy, setIsHealthy] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const check = async () => {
      try {
        await healthAPI.check();
        setIsHealthy(true);
      } catch (error) {
        setIsHealthy(false);
      } finally {
        setLoading(false);
      }
    };

    check();
    const interval = setInterval(check, 5000);
    return () => clearInterval(interval);
  }, []);

  return { isHealthy, loading };
};
