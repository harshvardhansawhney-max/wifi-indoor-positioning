import React from "react";
import { useLocation } from "react-router-dom";
import { motion } from "framer-motion";

const Sidebar: React.FC = () => {
  const location = useLocation();
  const isActive = (path: string) => location.pathname === path;

  const menuItems = [
    { path: "/", label: "Dashboard", icon: "📊" },
    { path: "/tracking", label: "Live Tracking", icon: "📍" },
    { path: "/analytics", label: "Analytics", icon: "📈" },
    { path: "/training", label: "Training", icon: "🤖" },
    { path: "/calibration", label: "Calibration", icon: "⚙️" },
    { path: "/settings", label: "Settings", icon: "⚙️" },
  ];

  return (
    <motion.aside
      className="w-64 glass-dark p-6 border-r border-slate-700/50 flex flex-col"
      initial={{ x: -100 }}
      animate={{ x: 0 }}
      transition={{ duration: 0.3 }}
    >
      <h1 className="gradient-text text-2xl font-bold mb-8">WiFi Localization</h1>
      <nav className="flex-1">
        {menuItems.map((item) => (
          <a
            key={item.path}
            href={item.path}
            className={`block px-4 py-3 rounded-lg mb-2 transition-all ${
              isActive(item.path)
                ? "bg-cyan-500/20 text-cyan-400 border border-cyan-500/50"
                : "text-slate-300 hover:bg-slate-800/50"
            }`}
          >
            {item.icon} {item.label}
          </a>
        ))}
      </nav>
      <div className="text-xs text-slate-500 text-center">v0.1.0</div>
    </motion.aside>
  );
};

export default Sidebar;
