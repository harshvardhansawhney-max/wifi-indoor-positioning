import axios from "axios";

const API_URL = process.env.REACT_APP_API_URL || "http://localhost:8000/api";
const WS_URL = process.env.REACT_APP_WS_URL || "ws://localhost:8001";

const api = axios.create({
  baseURL: API_URL,
  timeout: 10000,
});

export const signalAPI = {
  uploadSignal: (signal: any) => api.post("/signals/upload", signal),
  getLiveSignals: (limit?: number) =>
    api.get("/signals/live", { params: { limit } }),
  getSignalHistory: (apMac: string, limit?: number) =>
    api.get("/signals/history", { params: { ap_mac: apMac, limit } }),
};

export const locationAPI = {
  updateLocation: (location: any) => api.post("/location/update", location),
  getCurrentLocation: () => api.get("/location/current"),
  getLocationHistory: (limit?: number) =>
    api.get("/location/history", { params: { limit } }),
};

export const calibrationAPI = {
  startCalibration: (houseName: string) =>
    api.post("/calibration/start", { house_name: houseName }),
};

export const healthAPI = {
  check: () => api.get("/health"),
};

export class WebSocketService {
  private ws: WebSocket | null = null;

  connect(url: string = WS_URL) {
    return new Promise((resolve, reject) => {
      try {
        this.ws = new WebSocket(url);
        this.ws.onopen = () => resolve(this.ws);
        this.ws.onerror = (error) => reject(error);
      } catch (error) {
        reject(error);
      }
    });
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  on(event: string, callback: (data: any) => void) {
    if (this.ws) {
      this.ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        if (data.event === event) callback(data);
      };
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}
