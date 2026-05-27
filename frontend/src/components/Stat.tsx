import React from "react";
import { motion } from "framer-motion";

interface StatProps {
  label: string;
  value: string | number;
  icon?: React.ReactNode;
  trend?: number;
}

const Stat: React.FC<StatProps> = ({ label, value, icon, trend }) => {
  return (
    <motion.div
      className="glass-dark p-4 rounded-lg"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-400 text-sm">{label}</p>
          <p className="text-2xl font-bold text-cyan-400 mt-2">{value}</p>
          {trend !== undefined && (
            <p className={trend > 0 ? "text-green-400" : "text-red-400"} >
              {trend > 0 ? "↑" : "↓"} {Math.abs(trend)}%
            </p>
          )}
        </div>
        {icon && <div className="text-3xl text-cyan-400">{icon}</div>}
      </div>
    </motion.div>
  );
};

export default Stat;
