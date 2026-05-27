import { create } from "zustand";

interface LocationState {
  room: string;
  x: number;
  y: number;
  confidence: number;
  movementState: string;
  timestamp: Date;
  setLocation: (location: Partial<LocationState>) => void;
}

export const useLocationStore = create<LocationState>((set) => ({
  room: "Unknown",
  x: 0,
  y: 0,
  confidence: 0,
  movementState: "stationary",
  timestamp: new Date(),
  setLocation: (location) => set((state) => ({ ...state, ...location })),
}));
