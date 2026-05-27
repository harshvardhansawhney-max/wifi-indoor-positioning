import { useEffect, useState } from "react";
import { locationAPI } from "@services/api";

export const useLocation = () => {
  const [location, setLocation] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const fetchLocation = async () => {
    setLoading(true);
    try {
      const response = await locationAPI.getCurrentLocation();
      setLocation(response.data);
    } catch (error) {
      console.error("Failed to fetch location", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLocation();
    const interval = setInterval(fetchLocation, 1000);
    return () => clearInterval(interval);
  }, []);

  return { location, loading, refetch: fetchLocation };
};
