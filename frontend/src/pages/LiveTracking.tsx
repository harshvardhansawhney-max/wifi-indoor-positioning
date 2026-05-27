import React from "react";
import { motion } from "framer-motion";

const LiveTracking: React.FC = () => {
  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="gradient-text text-4xl font-bold mb-8">Live Tracking</h1>
      
      <div className="glass-dark p-8 rounded-lg h-96 flex items-center justify-center">
        <div className="text-center text-slate-400">
          <p className="text-xl">🗺️ Live Movement Map</p>
          <p className="text-sm mt-2">Real-time position and movement tracking</p>
        </div>
      </div>
    </motion.div>
  );
};

export default LiveTracking;
