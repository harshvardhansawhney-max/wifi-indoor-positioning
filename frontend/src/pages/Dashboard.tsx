import React from "react";
import { motion } from "framer-motion";

const Dashboard: React.FC = () => {
  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="gradient-text text-4xl font-bold mb-8">Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        {[
          { label: "Current Room", value: "Living Room", icon: "🏠" },
          { label: "Confidence", value: "92%", icon: "✓" },
          { label: "Movement", value: "Stationary", icon: "⏸" },
          { label: "Last Update", value: "2s ago", icon: "🕐" },
        ].map((stat, i) => (
          <motion.div
            key={i}
            className="glass-dark p-6 rounded-lg"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <p className="text-slate-400 text-sm">{stat.label}</p>
            <p className="text-2xl font-bold text-cyan-400 mt-2">{stat.value}</p>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Map placeholder */}
        <motion.div
          className="lg:col-span-2 glass-dark p-6 rounded-lg h-96 flex items-center justify-center"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="text-center text-slate-400">
            <p className="text-xl">📍 Floor Plan</p>
            <p className="text-sm mt-2">Interactive floor plan will be rendered here</p>
          </div>
        </motion.div>

        {/* Recent signals */}
        <motion.div
          className="glass-dark p-6 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <h2 className="text-lg font-bold text-cyan-400 mb-4">Recent Signals</h2>
          <div className="space-y-2">
            {["Router 1: -45 dBm", "Router 2: -62 dBm", "Router 3: -78 dBm"].map(
              (signal, i) => (
                <div key={i} className="text-sm text-slate-300 py-2 border-b border-slate-700">
                  {signal}
                </div>
              )
            )}
          </div>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Dashboard;
