import React from "react";
import { motion } from "framer-motion";

const Settings: React.FC = () => {
  return (
    <motion.div
      className="p-8"
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.5 }}
    >
      <h1 className="gradient-text text-4xl font-bold mb-8">Settings</h1>
      
      <div className="max-w-2xl space-y-6">
        {[
          { title: "Privacy", icon: "🔒" },
          { title: "WiFi Configuration", icon: "📶" },
          { title: "Advanced Options", icon: "⚙️" },
        ].map((setting, i) => (
          <motion.div
            key={i}
            className="glass-dark p-6 rounded-lg"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: i * 0.1 }}
          >
            <h2 className="text-lg font-bold text-cyan-400 mb-4">{setting.icon} {setting.title}</h2>
            <p className="text-slate-400 text-sm">Settings options will be displayed here</p>
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
};

export default Settings;
