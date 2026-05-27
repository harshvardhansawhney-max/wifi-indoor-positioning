import React from "react";
import { motion } from "framer-motion";

const Training: React.FC = () => {
  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="gradient-text text-4xl font-bold mb-8">Model Training</h1>
      
      <div className="space-y-6">
        <motion.div
          className="glass-dark p-6 rounded-lg"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <h2 className="text-xl font-bold text-cyan-400 mb-4">Training Status</h2>
          <p className="text-slate-300">No active training session</p>
          <button className="mt-4 px-6 py-2 bg-cyan-500 hover:bg-cyan-600 text-white rounded-lg">
            Start Training
          </button>
        </motion.div>
      </div>
    </motion.div>
  );
};

export default Training;
