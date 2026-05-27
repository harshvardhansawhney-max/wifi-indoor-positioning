import { create } from "zustand";

interface Signal {
  ap_mac: string;
  rssi: number;
  timestamp: Date;
}

interface SignalsState {
  signals: Signal[];
  addSignal: (signal: Signal) => void;
  clearSignals: () => void;
}

export const useSignalsStore = create<SignalsState>((set) => ({
  signals: [],
  addSignal: (signal) =>
    set((state) => ({
      signals: [signal, ...state.signals].slice(0, 100),
    })),
  clearSignals: () => set({ signals: [] }),
}));
