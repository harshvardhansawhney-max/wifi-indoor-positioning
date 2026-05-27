import React from "react";
import { motion } from "framer-motion";

const SignalAnalytics: React.FC = () => {
  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="gradient-text text-4xl font-bold mb-8">Signal Analytics</h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {["RSSI Over Time", "Signal Quality", "Channel Utilization", "AP Performance"].map(
          (title, i) => (
            <motion.div
              key={i}
              className="glass-dark p-6 rounded-lg h-80 flex items-center justify-center"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: i * 0.1 }}
            >
              <div className="text-center text-slate-400">
                <p className="text-lg">{title}</p>
                <p className="text-sm mt-2">Chart placeholder</p>
              </div>
            </motion.div>
          )
        )}
      </div>
    </motion.div>
  );
};

export default SignalAnalytics;
